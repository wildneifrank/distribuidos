import MulticastReceiver as mrcv

multicast_group = '224.0.0.1'
multicast_port = 5000
interface_ip = mrcv.get_active_interface_ip("wifi0")


receiver = mrcv.MulticastReceiver(multicast_group, multicast_port, interface_ip)
sender_ip = receiver.receive_multicast_messages()

    # Para fechar os sockets quando terminar, você pode chamar os métodos 'close':
receiver.close()