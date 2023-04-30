from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tables import *
import random, socket, json

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

def getOrdersWithPackageid(package_id):
    session = Session()

    # query all orders with package_id = 1
    orders = session.query(Order).filter(Order.package_id == package_id).all()

    # print the description of the products in the orders
    session.close()
    return orders

def getOpenRequest():
    session = Session()
    open_requests = session.query(Request).filter_by(status='open').all()
    # Print the results
    for request in open_requests:
        print(request.request_id, request.type, request.status, request.package.package_id)
    session.close()

    return open_requests

def getProductWithProductid(product_id):
    session = Session()
    product = session.query(Product).filter_by(product_id=product_id).first()
    session.close()
    return product

def get_Package(package_id):
    session = Session()
    package = session.query(Package).filter_by(package_id=package_id).first()
    session.close()
    return package

def update_request_status_to_ack(request_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Request).filter_by(request_id=request_id).first()
    request.status = 'ACK'
    session.commit()
    session.close()

def update_request_status_to_open(request_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Request).filter_by(request_id=request_id).first()
    request.status = 'open'
    session.commit()
    session.close()

def get_request_with_ack(request_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Request).filter_by(request_id=request_id).first()
    session.close()
    return request

def add_open_request(package_id, type):
    session = Session()
    new_request = Request(type=type, status="open", pk_id=package_id)
    session.add(new_request)
    session.commit()
    session.close()

def delete_request(request_id):
    session = Session()
    request = session.query(Request).filter_by(request_id=request_id).first()
    session.delete(request)
    session.commit()
    session.close()

def update_package_status(package_id, status):
    session = Session()
    package = session.query(Package).filter_by(package_id=package_id).first()
    package.status = status
    session.commit()
    session.close()

def init_warehouse(x, y):
    session = Session()
    new_warehouse = Warehouse(location_x=x, location_y=y)
    session.add(new_warehouse)
    session.commit()
    session.close()

def get_sizeof_request():
    session = Session()
    size = session.query(Request).count()
    session.close()
    return size
    


if __name__ == "__main__":
    # update_request_status_to_ack(1)
    #add_pack_request(1)
    #delete_request(12)
    update_request_status_to_open(1)
    # update_request_status_to_open(1)
    #add_open_request(1, "purchase")
    pass

