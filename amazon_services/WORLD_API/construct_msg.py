from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import invocated_files.amazon_ups_pb2 as amazon_ups_pb2
import invocated_files.world_amazon_pb2 as world_amazon_pb2


# Amazon to world server
def construct_AInitWarehouse(id, x, y):
    init_warehouse = world_amazon_pb2.AInitWarehouse()
    init_warehouse.id = id
    init_warehouse.x = x
    init_warehouse.y = y
    return init_warehouse

def construct_AConnect(worldid, initwh, isAmazon):
    connect = world_amazon_pb2.AConnect()
    connect.worldid = worldid
    connect.initwh.extend(initwh)
    connect.isAmazon = isAmazon
    return connect

def construct_AProcuct(id, description, count):
    product = world_amazon_pb2.AProduct()
    product.id = id
    product.description = description
    product.count = count
    return product

def construct_APurchaseMore(whnum, things, seqnum):
    purchase_more = world_amazon_pb2.APurchaseMore()
    purchase_more.whnum = 1
    purchase_more.things.extend(things)
    purchase_more.seqnum = seqnum
    return purchase_more

def construct_APack(whnum, things, packageid, seqnum):
    pack = world_amazon_pb2.APack()
    pack.whnum = 1
    pack.things.extend(things)
    pack.shipid = packageid
    pack.seqnum = seqnum
    return pack
    
def construct_APutOnTruck(whnum, truckid, packageid, seqnum):
    put_on_truck = world_amazon_pb2.APutOnTruck()
    put_on_truck.whnum = 1
    put_on_truck.truckid = truckid
    put_on_truck.shipid = packageid
    put_on_truck.seqnum = seqnum
    return put_on_truck

def construct_AQuery(packageid, seqnum):
    query = world_amazon_pb2.AQuery()
    query.packageid = packageid
    query.seqnum = seqnum
    return query

def construct_ACommands(buy, topack, load, queries, acks):
    commands = world_amazon_pb2.ACommands()
    if buy is not None:
        commands.buy.extend(buy)
    if topack is not None:
        commands.topack.extend(topack)
    if load is not None:
        commands.load.extend(load)
    if queries is not None:
        commands.queries.extend(queries)
    #commands.simspeed = simspeed
    #commands.disconnect = disconnect
    if acks is not None:
        commands.acks.extend(acks)
    return commands

def construct_acksList_from_response(AResponse):
    acks = []
    # for arrived_msg in AResponse.arrived:
    #     acks.append(arrived_msg.seqnum)
    # for packed_msg in AResponse.ready:
    #     acks.append(packed_msg.seqnum)
    # for loaded_msg in AResponse.loaded:
    #     acks.append(loaded_msg.seqnum)
    # for error_msg in AResponse.error:
    #     acks.append(error_msg.seqnum)
    # for status_msg in AResponse.packagestatus:
    #     acks.append(status_msg.seqnum)
    for ack in AResponse.acks:
        acks.append(ack)
    return acks

def construct_seqnumList_from_response(AResponse):
    sequence = []
    for arrived_msg in AResponse.arrived:
        sequence.append(arrived_msg.seqnum)
    for packed_msg in AResponse.ready:
        sequence.append(packed_msg.seqnum)
    for loaded_msg in AResponse.loaded:
        sequence.append(loaded_msg.seqnum)
    for error_msg in AResponse.error:
        sequence.append(error_msg.seqnum)
    for status_msg in AResponse.packagestatus:
        sequence.append(status_msg.seqnum)
    
    return sequence

def construct_ACK(acks):
    ACommands_ACK = world_amazon_pb2.ACommands()
    ACommands_ACK.acks.extend(acks)
    return ACommands_ACK

# Amazon to UPS client
def construct_AzConnected(worldid, result):
    Az_connected = amazon_ups_pb2.AzConnected()
    Az_connected.worldid = worldid
    Az_connected.result = result
    return Az_connected

def construct_AItem(description, count):
    item = amazon_ups_pb2.AItem()
    item.description = description
    item.count = count
    return item

def construct_ASendTruck(package_id, warehouse_id, user_id, x, y, items):
    AMessage = amazon_ups_pb2.AMessage()
   
    AMessage.sendTruck.package_id = package_id
    AMessage.sendTruck.warehouse_id = warehouse_id
    AMessage.sendTruck.user_id = user_id
    AMessage.sendTruck.x = x
    AMessage.sendTruck.y = y
    AMessage.sendTruck.items.extend(items)
    return AMessage

def construct_ATruckLoaded(truck_id, warehouse_id, package_id):
    AMessage = amazon_ups_pb2.AMessage()
    AMessage.truckLoaded.truck_id = truck_id
    AMessage.truckLoaded.warehouse_id = warehouse_id
    AMessage.truckLoaded.package_id = package_id
    return AMessage

def construct_AMessage(sendTruck, truckLoaded):
    message = amazon_ups_pb2.AMessage()
    message.sendTruck.extend(sendTruck)
    message.truckLoaded.extend(truckLoaded)
    return message