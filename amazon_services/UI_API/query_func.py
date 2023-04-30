from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random, socket, json
from tables import *

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


def add_commodity():
    session = Session()

    # create commodities
    commodities = [
        ('apple', 70),
        ('book', 50),
        ('cat', 30),
        ('dog', 30),
        ('banana', 60),
        ('clothes', 70),
        ('shoes', 50),
        ('kimchi', 100),
        ('TV', 60),
        ('coach', 50),
        ('ball', 100),
        ('beef noodle', 10),
    ]

    for description, count in commodities:
        commodity = session.query(Commodity).filter_by(description=description).first()
        if not commodity:
            commodity = Commodity(description=description, count=count)
            session.add(commodity)

    session.commit()
    session.close()
    
def add_product():
    session = Session()

    # create commodities
    products = [
        ('apple'),
        ('book'),
        ('cat'),
        ('dog'),
        ('banana'),
        ('clothes'),
        ('shoes'),
        ('kimchi'),
        ('TV'),
        ('coach'),
        ('ball'),
        ('beef noodle'),
    ]

    for description in products:
        product = session.query(Product).filter_by(description=description).first()
        if not product:
            product = Product(description=description)
            session.add(product)

    session.commit()
    session.close()
    
def add_warehouse():
    session = Session()

    # create commodities
    warehouses = [
        (1, 1),
        (2, 2),
        (3, 3),
    ]

    for location_x, location_y in warehouses:
        warehouse = Warehouse(location_x=location_x, location_y=location_y)
        session.add(warehouse)

    session.commit()
    session.close()

def add_package(destination_x, destination_y, user_id):
    session = Session()
    new_package = Package(destination_x=destination_x, destination_y=destination_y, user_id = user_id)
    session.add(new_package)
    session.commit()
    new_package_id = new_package.package_id
    session.close()
    return new_package_id

def add_order(product_id, count, pk_id, warehouse_id):
    session = Session()

    # Retrieve the product, warehouse, and package objects based on the provided IDs
    product = session.query(Product).get(product_id)
    warehouse = session.query(Warehouse).get(warehouse_id)
    package = session.query(Package).get(pk_id)

    # Create a new order with the retrieved product, quantity, warehouse, and package objects
    new_order = Order(product=product, quantity=count, warehouse=warehouse, package=package)

    # Add the new order to the session and commit the transaction
    session.add(new_order)
    session.commit()
    session.close()

def add_request(pk_id):
    session = Session()
    package = session.query(Package).get(pk_id)
    new_request = Request(type = "purchase", status = "open", package=package)
    session.add(new_request)
    session.commit()
    session.close()
    
def change_status(sequence_number, new_type, new_status):
    session = Session()
    request = session.query(Request).get(sequence_number)
    request.type = new_type
    request.status = new_status
    session.commit()
    session.close()
    
if __name__ == "__main__":
    #give_package_truckid(1)
    pass