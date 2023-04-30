from django.urls import path
from . import views


urlpatterns = [
    # home page
    path('', views.register, name='register'),
    path('home', views.home, name='home'),
    # search page
    path('search_result', views.search_products, name='search_result'),
    path('buy', views.Buy, name='buy'),
    #path('add_product', views.add_product, name='add_product'),
    #path('add_warehouse', views.add_warehouse, name='add_warehouse'),
    path('cart', views.cart_items, name='cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    #path('buy_confirmed', views.buy_confirm, name='buy_confirmed'),
    path('Cartbuy', views.Cartbuy, name='Cartbuy'),
    path('Search_product', views.status_search, name='Search_product'),
    #path('Order_Status', views.package_detail, name='Order_Status'),
    path('order_status', views.order_status, name='order_status'),
    path('modify_order/<int:product_id>/<str:description>/<int:quantity>/<int:destination_x>/<int:destination_y>/', views.modify_order, name='modify_order'),
    path('modify-form/<int:product_id>/<str:description>/<int:quantity>/<int:destination_x>/<int:destination_y>/', views.modify_form, name='modify_form'),
    path('cancel-form/<int:product_id>/<str:description>/<int:quantity>/<int:destination_x>/<int:destination_y>/', views.cancel_form, name='cancel_form'),
    #path('Product_status', views.package_status, name='Product_status'),
    
    #path('home/search_results/order', views.assign_order, name='order'),
]
