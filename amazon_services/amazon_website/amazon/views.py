from django.shortcuts import render, redirect, get_object_or_404
#from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from random import choice
from .models import *
import socket, json, time
#import protobuf_pb2

# Create your views here.

print("Trying to connect to amazon server")
# Try to connect to amazon server until success
amazon_socket = None

#HOST = '152.3.54.140'  # The server's hostname or IP address
#HOST = '152.3.53.130'  # The server's hostname or IP address james
HOST = '0.0.0.0'
PORT = 55555        # The port used by the server
address = (HOST, PORT)


def home(request):
    products = Commodity.objects.all().order_by("commodity_id")
    warehouses = Warehouse.objects.all().order_by("warehouse_id")
    context = {"products": products, "warehouses": warehouses}
    return render(request, "frontend/home.html",context)

def register(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id') # assuming 'user_id' is the name of the input field in the registration form
        request.session['user_id'] = user_id
        return redirect('home')
    else:
        #return redirect('home')
        return render(request, "frontend/register.html")

def search_products(request):
    query = request.GET.get('search_input')
    if query:
        products = Commodity.objects.filter(description=query)
    else:
        products = Commodity.objects.all()
    return render(request, "frontend/search.html", {'products': products, 'query': query})

def clear_cart(request):
    cart = request.session.get('cart', {})
    user_id = request.session.get('user_id', None)
    new_cart = {}
    for key, items in cart.items():
        new_cart[key] = [item for item in items if item.get('user_id') != user_id]
    request.session['cart'] = new_cart
    return render(request, 'frontend/clear_cart.html')

def Buy(request):
    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            products = Commodity.objects.all()
            warehouses = Warehouse.objects.all()
            error_message = add_to_cart(request)
            return render(request, "frontend/buy.html", {'products':products,'warehouses':warehouses, 'error_message':error_message})
        else:
            user_id = request.session.get('user_id', None)
            # Get the form data from the POST request
            description = request.POST.get('description')
            quantity = request.POST.get('quantity')
            destination_x = request.POST.get('destination_x')
            destination_y = request.POST.get('destination_y')
            
            product = Commodity.objects.get(description=description)
            product_id = product.commodity_id
            # Check if the requested quantity is valid
            if int(quantity) <= 0 or int(quantity) > product.count:
                error_message = f"Only {product.count} units of {description} are available. Failed to buy!"
                print("product.count is: ", product.count)
                products = Commodity.objects.all()
                return render(request, 'frontend/buy.html', {'error_message':error_message,'products': products})
            
            # Send data over socket
            orders = {}
            key = f"{destination_x},{destination_y}"
            orders[key] = []
            orders[key].append({'destination_x': destination_x})
            orders[key].append({'destination_y': destination_y})
            orders[key].append({'user_id': user_id})
            # add the product
            orders[key].append({ 
                'product_id': product_id,
                'description': product.description,
                'quantity': quantity,
            })
            
            orders_data = json.dumps(orders[key])
            product.count -= int(quantity)
            product.save()
            
            connected = False
            while not connected:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect(address)
                    client_socket.sendall(orders_data.encode())
                    client_socket.close()
                    connected = True
                except:
                    print("waiting for the world to be ready")
            # Redirect to a confirmation page
            return render(request, 'frontend/buy_confirmed.html')
            #return redirect('home')
    else:
        # Render the buy form with a list of available products
        products = Commodity.objects.all()
        return render(request, 'frontend/buy.html', {'products': products})
    
def Cartbuy(request):
    user_id = request.session.get('user_id', None)
    cart = request.session.get('cart', {})
    request.session['purchase_fail'] = {}
    print("purchase_fail is:",request.session.get('purchase_fail', {}))
    purchase_fail = {}
    orders = {}
    # manipulate the data with user_id
    filtered_cart = {}
    for key, items in cart.items():
        filtered_items = [item for item in items if item['user_id'] == user_id]
        if filtered_items:
            filtered_cart[key] = filtered_items
    
    for key, products in filtered_cart.items():
        destination_x, destination_y = key.split(',')
        orders[key] = []
        orders[key].append({'destination_x': destination_x})
        orders[key].append({'destination_y': destination_y})
        orders[key].append({'user_id': user_id})
        purchase_fail[key] = []
        for product in products:
            flag = 0
            commodity = Commodity.objects.get(description=product['description'])
            if product['quantity'] > commodity.count:
                purchase_fail[key].append({'destination_x': destination_x})
                purchase_fail[key].append({'destination_y': destination_y})
                purchase_fail[key].append({'user_id': user_id})
                purchase_fail[key].append({
                    'product_id': product['product_id'],
                    'description': product['description'],
                    'quantity': product['quantity'],
                })
                print("Quantity exceed the maximum value of the product. Try again!")
                continue
            else:
                commodity.count -= product['quantity']
                commodity.save()
                
                orders[key].append({ # add the order to the list of orders for this key
                'product_id': product['product_id'],
                'description': product['description'],
                'quantity': product['quantity'],
                })
                
        if len(orders[key]) == 3:
            continue
        request.session['purchase_fail'] = purchase_fail
        #print("orders[key] value: ")
        #print(orders[key])
        # serialize the orders data to JSON format
        orders_data = json.dumps(orders[key])
        connected = False
        while not connected:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(address)
                client_socket.sendall(orders_data.encode())
                client_socket.close()
                connected = True
            except:
                print("waiting for the world to be ready")
    # clear the cart and redirect to the confirmation page
    for key, items in cart.items():
        cart[key] = [item for item in items if item['user_id'] != user_id]
    
    #request.session['cart'] = {}
    purchase_fail = request.session.get('purchase_fail')
    # Remove the items from the cart
    for key, item in list(purchase_fail.items()):
        if len(item) == 0:
            del purchase_fail[key]
    request.session['purchase_fail'] = purchase_fail
    print("purchase_fail is 2:",request.session.get('purchase_fail', {}))
    #print(purchase_fail)
    return render(request, 'frontend/cart_confirmed.html', {'purchase_fail': purchase_fail})
    #return redirect('home')

def add_to_cart(request):
    #request.session.clear()
    description = request.POST.get('description')
    quantity = int(request.POST.get('quantity'))
    destination_x = request.POST.get('destination_x')
    destination_y = request.POST.get('destination_y')
    product = Commodity.objects.get(description=description)
    user_id = request.session.get('user_id', None)
    # Get the product from the database
    available_quantity = product.count
    
    # Check if the requested quantity is available
    if quantity <= 0:
        # Show an error message to the user
        error_message = "Quantity need to be larger than 0."
        return error_message
    
    if quantity > available_quantity:
        # Show an error message to the user
        error_message = f"Only {available_quantity} units of {description} are available. Failed to add to cart!"
        return error_message
    # Add product to cart
    product_id = product.commodity_id
    cart = request.session.get('cart', {})
    
    key = f"{destination_x},{destination_y}"
    if key in cart:
        flag = 0
        for item in cart[key]:
            if item['description'] == description and item['user_id'] == user_id:
                total = item['quantity'] + quantity
                if total > available_quantity:
                    # Show an error message to the user
                    error_message = f"Exceed the maximum number of {description}.\nFail to add the {description} to the cart."
                    return error_message
                item['quantity'] += quantity
                flag = 1
                break   
        if flag == 0:
            cart[key].append({
            'product_id': product_id,
            'description': description,
            'quantity': quantity,
            'destination_x':destination_x,
            'destination_y':destination_y,
            'user_id':user_id,
        })
    else:
        cart[key] = [{
            'product_id': product_id,
            'description': description,
            'quantity': quantity,
            'destination_x':destination_x,
            'destination_y':destination_y,
            'user_id':user_id,
        }]

    request.session['cart'] = cart
    #request.session.clear()

def cart_items(request):
    user_id = request.session.get('user_id', None)
    cart = request.session.get('cart', {})
    filtered_cart = {}
    
    for key, items in cart.items():
        filtered_items = [item for item in items if item['user_id'] == user_id]
        if filtered_items:
            filtered_cart[key] = filtered_items

    items = []
    for key, product_items in filtered_cart.items():
        destination_x, destination_y = key.split(',')
        #print("item_key:", key)
        #print("item_value:", product_items)
        for item in product_items:
            items.append({
                #'product': product,
                'product_id':item['product_id'],
                'description': item['description'],
                'quantity': item['quantity'],
                'destination_x': destination_x,
                'destination_y': destination_y,
            })
    context = {'items': items}
    return render(request, 'frontend/cart_items.html', context)

# not use
def status_search(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        package = Package.objects.filter(package_id)
        if package is not None:
            status = package.status
            return render(request, 'frontend/package_status.html', {'package': package})
        else:
            status = f"No package found for package_id '{package_id}'"
            return render(request, 'frontend/package_status.html', {'status': status})
    else:
        return render(request, 'frontend/status_search.html')

# not use
def package_detail(request):
    # Get the package_id parameter from the request.GET dictionary
    package_id = request.GET.get('package_id')

    # Get the user ID from the session
    user = request.session.get('user_id')
    # Get the order that matches the given package_id
    orders = Order.objects.filter(package_id=package_id, package__user_id=user)

    if not orders.exists():
        # If no order is found, render a message indicating so
        error_message = f"No order found for package ID {package_id}."
        return render(request, 'frontend/package_status.html', {'error_message':error_message})

    # If an order is found, render the package status information
    return render(request, 'frontend/package_status.html', {'orders': orders})

def order_status(request):
    user_id = request.session.get('user_id', None)
    packages = Package.objects.filter(user_id=user_id)
    orders = []
    for package in packages:
        package_orders = Order.objects.filter(package=package)
        orders += list(package_orders)
    return render(request, 'frontend/order_status.html', {'orders': orders})


def modify_form(request, product_id, description, quantity, destination_x, destination_y):
    products = Commodity.objects.all().order_by("commodity_id")
    context = {
        'product_id': product_id,
        'description': description,
        'quantity': quantity,
        'destination_x': destination_x,
        'destination_y': destination_y,
        'products': products,
    }
    return render(request, 'frontend/modify_form.html', context)

def cancel_form(request, product_id, description, quantity, destination_x, destination_y):
    # Retrieve the cart items from the session
    user_id = request.session.get('user_id')
    cart = request.session.get('cart', {})
    items_to_remove = []
     # Find the item in the cart that matches the given product ID and user ID
    for key, items in cart.items(): 
        for item in items:
            if (item['user_id'] == user_id and
                item['product_id'] == product_id and
                item['description'] == description and
                int(item['quantity']) == int(quantity) and
                int(item['destination_x']) == int(destination_x) and
                int(item['destination_y']) == int(destination_y)):
                #print("match!!!")
                # Remove the item from the cart
                items_to_remove.append((key, item))
                
    # Remove the items from the cart
    for key, item in items_to_remove:
        cart[key].remove(item)
        if len(cart[key]) == 0:
            del cart[key]

    # Save the updated cart items back to the session
    request.session['cart'] = cart

    # Redirect the user back to the cart page
    return redirect('cart')

def modify_order(request, product_id, description, quantity, destination_x, destination_y):
    # Retrieve the cart items from the session
    user_id = request.session.get('user_id')
    cart = request.session.get('cart', {})
    items_to_remove = []
     # Find the item in the cart that matches the given product ID and user ID
    for key, items in cart.items(): 
        for item in items:
            if (item['user_id'] == user_id and
                item['product_id'] == product_id and
                item['description'] == description and
                int(item['quantity']) == int(quantity) and
                int(item['destination_x']) == int(destination_x) and
                int(item['destination_y']) == int(destination_y)):
                #print("match!!!")
                # Remove the item from the cart
                items_to_remove.append((key, item))
                
    # Remove the items from the cart
    for key, item in items_to_remove:
        cart[key].remove(item)
        if len(cart[key]) == 0:
            del cart[key]

    # Add an item with key (destination_x, destination_y)
    new_description = request.POST.get('description')
    new_quantity = int(request.POST.get('quantity'))
    new_desx = int(request.POST.get('destination_x'))
    new_desy = int(request.POST.get('destination_y'))
    product = Product.objects.get(description=new_description)
    new_product_id = product.product_id
    # Append the new item to the list of items under the given key
    newkey = f"{new_desx},{new_desy}"
    if newkey not in cart:
        cart[newkey] = []
    cart[newkey].append({
        'product_id': new_product_id,
        'description': new_description,
        'quantity': new_quantity,
        'destination_x': new_desx,
        'destination_y': new_desy,
        'user_id': user_id,
    })
    # Save the updated cart items back to the session
    request.session['cart'] = cart

    # Redirect the user back to the cart page
    return redirect('cart')