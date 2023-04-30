from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import invocated_files.amazon_ups_pb2 as amazon_ups_pb2
import invocated_files.world_amazon_pb2 as world_amazon_pb2
from construct_msg import *
from worldAPI_query import *


def send_command(commands, socket):
    encoded_msg = commands.SerializeToString()
    _EncodeVarint(socket.send, len(encoded_msg), None)
    socket.send(encoded_msg)

def receive(socket):
    var_int_buff = []
    while True:
        try:
            buf = socket.recv(1)
            var_int_buff += buf
            msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        except Exception as e:
            print("error in receive")
            print(e)
            raise e
        if new_pos != 0:
            break
    whole_msg = socket.recv(msg_len)
    return whole_msg

def receive_AResponse(socket):
    # Receive AResponses message from the world server
    whole_msg = whole_msg = receive(socket)
    responses = world_amazon_pb2.AResponses()
    responses.ParseFromString(whole_msg)
    return responses

def receive_AConnected(socket):
    # Receive AResponses message from the world server
    whole_msg = whole_msg = receive(socket)
    responses = world_amazon_pb2.AConnected()
    responses.ParseFromString(whole_msg)
    return responses

def receive_UtoAzConnect(socket):
    whole_msg = receive(socket)
    responses = amazon_ups_pb2.UtoAzConnect()
    responses.ParseFromString(whole_msg)
    return responses


def ACK_request(acksList):
    # get a list of acks from the AResponse
    for ack in acksList:
        print("Ack id ")
        print(ack)
        try:
            update_request_status_to_ack(ack) 
        except:
            print("Some Ack error")

def ACK_world(seqnumList, world_socket):
    # create ACommands_ACK to send to world server
    ACommands_ACK = construct_ACK(seqnumList)
    print("sending ACK to world server\n", ACommands_ACK)
    send_command(ACommands_ACK, world_socket)
   
        
    # print("received response from world server", AResponse)
    # # get a list of acks from the AResponse
    # acksList = construct_acksList_from_response(AResponse)
    # # update the database to ACK
    # for ack in acksList:
    #     update_request_status_to_ack(ack) 
    # # create ACommands_ACK to send to world server
    # ACommands_ACK = construct_ACK(acksList)
    # print("sending ACK to world server", ACommands_ACK)
    # send_command(ACommands_ACK, world_socket)

def proceed_after_ACK(AResponse, acksList, ups_socket):
    print("start of proceed_after_ACK")

    #special case for APurchaseMore
    if len(AResponse.arrived) > 0:
        print("in special case for APurchaseMore")
        print("ackList: ", acksList)
        for ack in acksList:
            # check if ack is a valid request_id
            if ack <= get_sizeof_request():
                request = get_request_with_ack(ack)
                if request.type == "purchase":
                    package_id = request.pk_id
                    print("add_open_request")
                    add_open_request(package_id, "pack")
    
    
    for ready in AResponse.ready:
        package_id = ready.shipid
        update_package_status(package_id, "packed")
        package = get_Package(package_id)
        warehouse_id = 1
        user_id = package.user_id
        x = package.destination_x
        y = package.destination_y
        orders = getOrdersWithPackageid(package_id)
        items = []
        for order in orders:
            product = getProductWithProductid(order.product_id)
            description = product.description
            count = order.quantity
            item = construct_AItem(description, count)
            items.append(item)
            # warehouse_id = order.warehouse_id
        Amessage = construct_ASendTruck(package_id, warehouse_id, user_id, x, y, items)
        print("sending Amessage to ups server\n", Amessage)
        send_command(Amessage, ups_socket)

    
    for loaded in AResponse.loaded:
        package_id = loaded.shipid
        update_package_status(package_id, "loaded to truck")
        package = get_Package(package_id)
        truck_id = package.truck_id
        warehouse_id = 1
        # orders = getOrdersWithPackageid(package_id)
        # for order in orders:
        #     warehouse_id = order.warehouse_id
        Amessage = construct_ATruckLoaded(truck_id, warehouse_id, package_id)
        print("sending Amessage to ups server\n", Amessage)
        send_command(Amessage, ups_socket)

    print("end of proceed_after_ACK")

    # for ack in acksList:
    #     request = get_request_with_ack(ack)
    #     if request.type == "purchase":
    #         package_id = request.pk_id
    #         add_open_request(package_id, "pack")
    #     elif request.type == "pack":
    #         package_id = request.pk_id
    #         update_package_status(package_id, "packed")
    #         package = get_Package(package_id)
    #         warehouse_id = 0
    #         user_id = package.user_id
    #         x = package.destination_x
    #         y = package.destination_y
    #         orders = getOrdersWithPackageid(package_id)
    #         items = []
    #         for order in orders:
    #             product = getProductWithProductid(order.product_id)
    #             description = product.description
    #             count = order.quantity
    #             item = construct_AItem(description, count)
    #             items.append(item)
    #             warehouse_id = order.warehouse_id
    #         Amessage = construct_ASendTruck(package_id, warehouse_id, user_id, x, y, items)
           
    #         send_command(Amessage, world_socket)
    #     elif request.type == "load":
    #         package_id = request.pk_id
    #         update_package_status(package_id, "loaded to truck")
    #         package = get_Package(package_id)
    #         truck_id = package.truck_id
    #         warehouse_id = 0
    #         orders = getOrdersWithPackageid(package_id)
    #         for order in orders:
    #             warehouse_id = order.warehouse_id
    #         Amessage = construct_ATruckLoaded(truck_id, warehouse_id, package_id)
            
    #         send_command(Amessage, world_socket)

    # # DB query
    #     # for each ACK, get the query result which has the same seqnum as ACK
    #         # change the status from OPEN to ACK
    #         # if type == APurchaseMore
    #             # Add a Pack rquest with OPEN status and package_id from the query result
    #         # if type == PACK 
    #             # with package_id, get user_id (optional), warehouse_id, x, y from query
    #             # with package id, get all the products from query 
    #                 # create AItem for each description and count of the product
    #             # create AsendTruck with package_id, warehouse_id, user_id, x, y, and AItem
    #             # create and send AMessage with ASendTruck type to UPS server
    #         # if type == LOAD 
    #             # with package_id, get truck_id and warehouse_id
    #             # Create and send AMessage with ATruckLoaded type to UPS server