import socket
import struct
from protoBuff import MulticastMessage_pb2 as mumes

def multicast_sender(type):
    multicast_group = '224.0.0.1'
    multicast_port = 5000

    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    multicast_socket.bind(('', multicast_port))
    mreq = struct.pack('4sL', socket.inet_aton(multicast_group), socket.INADDR_ANY)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Escutando mensagens do grupo {multicast_group}:{multicast_port}")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    interface_ip = s.getsockname()[0]
    s.close()

    try:
        message = mumes.MulticastMessage()
        message.ip = interface_ip
        message.port = 8002
        message.udpport = 5000
        message.type = type

        message_bytes = message.SerializeToString()
        multicast_socket.sendto(message_bytes, (multicast_group, multicast_port))

        
    except KeyboardInterrupt:
        pass
    finally:    
        multicast_socket.close()