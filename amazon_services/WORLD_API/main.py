# this is a client api that is used to communicate with the world server and the UPS server
import socket
import time
import select
import threading
from construct_msg import *
from worldAPI_query import *
from transmit_msg import *

data_lock = threading.Lock()


#LOCAL_HOST = '152.3.53.130'
#LOCAL_HOST = '152.3.54.140'
LOCAL_HOST = '0.0.0.0'
EXTERNAL_HOST = '172.28.184.254'
CAROLINE_HOST = '152.3.54.6'
JERRY_HOST = '152.3.54.140' 

# world server socket
WORLD_HOST = LOCAL_HOST  
WORLD_PORT = 23456
world_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set the IP address and port number of the UPS server
AMAZON_UPS_HOST = CAROLINE_HOST  # IP address of the UPS server
AMAZON_UPS_PORT = 54321 # UPS server port
# ups_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# while True:
#     try:
#         ups_socket.connect((AMAZON_UPS_HOST, AMAZON_UPS_PORT))
#         break
#     except:
#         print("UPS server not ready yet")
#         time.sleep(2)

# Internal UI Socket
UI_HOST = LOCAL_HOST 
UI_PORT = 7777

# Internal World Socket
INTERNAL_WORLD_SERVICE_HOST = LOCAL_HOST 
INTERNAL_WORLD_SERVICE_PORT = 9487


def getWorldId():
    # Internal UPS Socket
    internal_ups = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the IP address and port number of the world server
    internal_ups.bind((INTERNAL_WORLD_SERVICE_HOST, INTERNAL_WORLD_SERVICE_PORT))
    internal_ups.listen(5)
    print("waiting for world id...", flush=True)
    conn, addr = internal_ups.accept()
    worldid = int(conn.recv(1024).decode())
    print("world id received: ", worldid)
    return worldid

def initialize_world():
    ups_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            ups_socket.connect((AMAZON_UPS_HOST, AMAZON_UPS_PORT))
            break
        except:
            print("UPS server not ready yet", flush=True)
            time.sleep(2)
    
    worldid = getWorldId()
    while True:
        try:
            world_socket.connect((WORLD_HOST, WORLD_PORT))
            break
        except:
            print("World server not ready yet")
            time.sleep(2)
    # add 100 AInitWarehouse messages to the AConnect message
    ###### DB
    init_warehouse_list = []
    # for i in range(10):
    #     for j in range(10):
    wh = construct_AInitWarehouse(1,1,1)
    init_warehouse_list.append(wh)
    init_warehouse(1, 1)

    connect_msg = construct_AConnect(worldid, init_warehouse_list, True)
    send_command(connect_msg, world_socket)
    world_connect_response = receive_AConnected(world_socket)

    if(world_connect_response.result == "connected!"):
        print("Connection to world server successful!")
        conneted_msg = construct_AzConnected(world_connect_response.worldid, "success")
        send_command(conneted_msg, ups_socket)
    else:
        print("Connection to world server failed.")
        conneted_msg = construct_AzConnected(world_connect_response.worldid, "failed")
        send_command(conneted_msg, ups_socket)
        raise ConnectionError("Failed to connect to world server")
    return ups_socket

def inform_ui():
    connected = False
    internal_ui = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        time.sleep(2)
        try:
            internal_ui.connect((UI_HOST, UI_PORT))
            print("Conneted to internal UI API")
            break
        except:
            print("Connection to internal UI failed. Retrying...")
    internal_ui.send("world is ready".encode())

def handle_request(request, shared_data):
    if request.type == "purchase":
        # ... (your purchase code)
        seqnum = request.request_id
        package_id = request.pk_id
        orders = getOrdersWithPackageid(package_id)
        whnum = 1
        products = []
        for order in orders:
            product = getProductWithProductid(order.product_id)
            product_id = product.product_id
            description = product.description
            count = order.quantity
            Aproduct = construct_AProcuct(product_id, description, count)
            products.append(Aproduct)
        purchase_more = construct_APurchaseMore(whnum, products, seqnum)
        with data_lock:
            shared_data['buy'].append(purchase_more)
    elif request.type == "pack":
        # ... (your pack code)
        seqnum = request.request_id
        package_id = request.pk_id
        orders = getOrdersWithPackageid(package_id)
        whnum = 1
        products = []
        for order in orders:
            product = getProductWithProductid(order.product_id)
            product_id = product.product_id
            description = product.description
            count = order.quantity
            Aproduct = construct_AProcuct(product_id, description, count)
            products.append(Aproduct)
        pack = construct_APack(whnum, products, package_id, seqnum)
        with data_lock:
            shared_data['topack'].append(pack)
    elif request.type == "load":
        # ... (your load code)
        seqnum = request.request_id
        package_id = request.pk_id
        package = get_Package(package_id)
        truck_id = package.truck_id
        orders = getOrdersWithPackageid(package_id)
        whnum = 1
        # for order in orders:
        #     whnum = order.warehouse_id
        APutOnTruck = construct_APutOnTruck(whnum, truck_id, package_id, seqnum)
        with data_lock:
            shared_data['load'].append(APutOnTruck)

if __name__ == '__main__':
    ups_socket = initialize_world()
    inform_ui()

    while True:
        # get open requests from the DB
        requests = getOpenRequest()
        shared_data = {'buy': [], 'topack': [], 'load': [], 'queries': [], 'acks': None}

        # buy = []
        # topack = []
        # load = [] 
        # queries =[] 
        # #simspeed = None 
        # #disconnect = None 
        # acks = None

        # Create threads for each request
        threads = []
        for request in requests:
            thread = threading.Thread(target=handle_request, args=(request, shared_data))
            threads.append(thread)
            thread.start()
        
         # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Extract the results from shared_data
        buy = shared_data['buy']
        topack = shared_data['topack']
        load = shared_data['load']
        queries = shared_data['queries']
        acks = shared_data['acks']

        # only construct and send ACommands if there exist buy, topack, load, queries, or acks
        if buy or topack or load or queries or acks:
            commands = construct_ACommands(buy, topack, load, queries, acks)
            print("sending commands to world server\n", commands)
            # send Acommand to world server
            send_command(commands, world_socket)
        
        # receive AResponse from world server
        read_sockets, write_sockets, error_sockets = select.select([world_socket], [], [], 5.0)
        if world_socket not in read_sockets:
            print("no response from world server")
        else:
            AResponse = receive_AResponse(world_socket)
            print("received response from world server\n", AResponse)
            if len(AResponse.acks) > 0:
                acksList = construct_acksList_from_response(AResponse)
        
                print("acksList", acksList)
                # update the database to ACK and send acks to UPS server
                ACK_request(acksList)
            seqnumList = construct_seqnumList_from_response(AResponse)
            if len(seqnumList) > 0:
                ACK_world(seqnumList, world_socket)
            proceed_after_ACK(AResponse, acksList, ups_socket)
            
        # DB query
        # for each ACK, get the query result which has the same seqnum as ACK
            # change the status from OPEN to ACK
            # if type == APurchaseMore
                # Add a Pack rquest with OPEN status and package_id from the query result
            # if type == PACK 
                # with package_id, get user_id (optional), warehouse_id, x, y from query
                # with package id, get all the products from query 
                    # create AItem for each description and count of the product
                # create AsendTruck with package_id, warehouse_id, user_id, x, y, and AItem
                # create and send AMessage with ASendTruck type to UPS server
            # if type == LOAD 
                # with package_id, get truck_id and warehouse_id
                # Create and send AMessage with ATruckLoaded type to UPS server