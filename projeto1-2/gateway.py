import socket
import struct
import time
from protoBuff import MulticastMessage_pb2 as mumes  # Importe a definição de mensagem gerada pelo protobuf

# Configurações do multicast
multicast_group = '224.0.0.1'
multicast_port = 5000

# Crie um socket UDP para multicast
multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Configurar o socket para permitir que outros programas usem a mesma porta
multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Junte-se ao grupo multicast
multicast_socket.bind(('', multicast_port))
mreq = struct.pack('4sL', socket.inet_aton(multicast_group), socket.INADDR_ANY)
multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Escutando mensagens do grupo {multicast_group}:{multicast_port}")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
interface_ip =s.getsockname()[0]
s.close()


try:
    while True:
        print('foi')
        message = mumes.MulticastMessage()
        message.sender = interface_ip
        message.content = "Este dispositivo está online"

        # Serialize a mensagem protobuf em bytes
        message_bytes = message.SerializeToString()

        # Envie a mensagem serializada como um pacote UDP multicast
        multicast_socket.sendto(message_bytes, (multicast_group, multicast_port))

        # Espere por um curto período antes de enviar novamente (pode ajustar isso conforme necessário)
        time.sleep(5)

except KeyboardInterrupt:
    pass
finally:
    multicast_socket.close()
