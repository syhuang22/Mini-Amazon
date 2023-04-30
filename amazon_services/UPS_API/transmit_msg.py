from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import invocated_files.amazon_ups_pb2 as amazon_ups_pb2
import invocated_files.world_amazon_pb2 as world_amazon_pb2


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

def receive_UMessage(socket):
    whole_msg = receive(socket)
    responses = amazon_ups_pb2.UMessage()
    responses.ParseFromString(whole_msg)
    return responses

def receive_UtoAzConnect(socket):
    whole_msg = receive(socket)
    responses = amazon_ups_pb2.UtoAzConnect()
    responses.ParseFromString(whole_msg)
    return responses