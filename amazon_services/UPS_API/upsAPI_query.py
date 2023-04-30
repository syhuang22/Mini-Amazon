from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tables import *
import random, socket, json

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

def give_package_truckid(package_id, truck_id):
    print("get_Package\n")
    session = Session()
    package = session.query(Package).filter_by(package_id=package_id).first()
    package.truck_id = truck_id
    session.commit()
    print("Package id: ", package.package_id)
    print("Destination x: ", package.destination_x)
    print("Destination y: ", package.destination_y)
    print("User id: ", package.user_id)
    print("truckid: ", package.truck_id)
    print("====================================")
    session.close()

def update_package_status(package_id, status):
    session = Session()
    package = session.query(Package).filter_by(package_id=package_id).first()
    package.status = status
    session.commit()
    session.close()

def add_open_request(package_id, type):
    session = Session()
    new_request = Request(type=type, status="open", pk_id=package_id)
    session.add(new_request)
    session.commit()
    session.close()
    
if __name__ == "__main__":
    #give_package_truckid(1)
    pass
