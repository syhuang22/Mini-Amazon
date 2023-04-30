# This is a client api to get the data from the frontend and store them in the database 
 
# Create the SQLAlchemy engine and session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tables import *
from query_func import *
import random, socket, json
import time

def frontend_connection():
    # create a TCP/IP socket
    frontend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()
    # set the port for UPS to connect to
    port = 55555
    frontend_socket.bind((host, port))
    return frontend_socket

def internal_connection():
    # create a TCP/IP socket
    internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = '152.3.53.130'
    #host = '152.3.54.140'
    # set the port for UPS to connect to
    port = 7777
    internal_socket.bind((host, port))
    return internal_socket


LOCAL_HOST = '152.3.53.130'
#LOCAL_HOST = '152.3.54.140'
LOCAL_PORT = 7777

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
        
    while True:
        try:
            # create a TCP/IP socket
            internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            internal_socket.bind((LOCAL_HOST, LOCAL_PORT))
            #internal_socket = internal_connection()
            internal_socket.listen()
            print('listening to internal requests...')
            connection, address = internal_socket.accept()
            print(f"Connected to {address}")
            message = connection.recv(4096).decode()
            print(f"Received message: {message}")
            break
        except Exception as e:
            print(e)
            time.sleep(2)
            # Receive the message from the connection
        
    while True:
        add_commodity()
        add_product()
        #add_warehouse()
        frontend_socket = frontend_connection()
        frontend_socket.listen()
        print('Waiting for frontend request...')
        while True:
            connection, client_address = frontend_socket.accept()
            print('Connected by', client_address)

            while True:
                # Check if the connection is receiving any messages
                data = connection.recv(4096)
                if not data:
                    print('Connection closed by', client_address)
                    break
                frontend_request = json.loads(data.decode())
                print(frontend_request)
                # Process the received message here
                #warehouse_id = random.randint(1, 100)
                warehouse_id = random.randint(1, 3)
                destination_x = int(frontend_request[0]['destination_x'])
                destination_y = int(frontend_request[1]['destination_y'])
                user_id = int(frontend_request[2]['user_id'])
                
                #add_package(destination_x, destination_y, user_id)
                pk_id = add_package(destination_x, destination_y, user_id)
                print("pk_id:", pk_id)
                # Extract product and quantity data from the remaining dictionaries
                order_data = [(d['product_id'], d['quantity']) for d in frontend_request[3:]]

                # Loop through the order data and create new Order instances for each item
                for product_id, quantity in order_data:
                    # Create a new Order instance with the retrieved Product, quantity, and Warehouse, as well as the new Package
                    add_order(product_id, quantity, pk_id, warehouse_id)
                add_request(pk_id)
                
            connection.close()


'''
if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    add_commodity()
    add_product()
    add_warehouse()
    frontend_socket = frontend_connection()
    frontend_socket.listen()
    print('Waiting for frontend request...')
    while True:
        connection, client_address = frontend_socket.accept()
        print('Connected by', client_address)

        while True:
            # Check if the connection is receiving any messages
            data = connection.recv(1024)
            if not data:
                print('Connection closed by', client_address)
                break
            frontend_request = json.loads(data.decode())
            print(frontend_request)
            # Process the received message here
            #warehouse_id = random.randint(1, 100)
            warehouse_id = random.randint(1, 3)
            destination_x = int(frontend_request[0]['destination_x'])
            destination_y = int(frontend_request[1]['destination_y'])
            user_id = int(frontend_request[2]['user_id'])
            
            #add_package(destination_x, destination_y, user_id)
            pk_id = add_package(destination_x, destination_y, user_id)
            print("pk_id:", pk_id)
            # Extract product and quantity data from the remaining dictionaries
            order_data = [(d['product_id'], d['quantity']) for d in frontend_request[3:]]

            # Loop through the order data and create new Order instances for each item
            for product_id, quantity in order_data:
                # Create a new Order instance with the retrieved Product, quantity, and Warehouse, as well as the new Package
                add_order(product_id, quantity, pk_id, warehouse_id)
            add_request(pk_id)
            
        connection.close()
'''

    # # need the below parameter part from frontend via socket
    # frontend_request = [
    #     {'id': 1, 'description': 'product1', 'count': 10},
    #     {'id': 2, 'description': 'product2', 'count': 5},
    # ]
    # user_id = 67890  # optional user id
    # x = 1  # Replace with the actual x coordinate
    # y = 2  # Replace with the actual y coordinate