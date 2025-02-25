"""
Server creates as many UDP sockets as it has input ports and binds
one socket to each input port. One of the input sockets can be used for
sending UDP datagrams to neighbors.
"""
import socket
import select

def create_and_bind(input_ports):
    """Create and bind UDP sockets for each input port."""
    sockets = []
    for port in input_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', port))
        sockets.append(sock)
        print(f"Listening on UDP port {port}")
    return sockets

def send_to_neighbors(sock, neighbors, table):
    """Send a routing table to each neighbor using the specified socket."""
    neighbor_ip = '127.0.0.1'
    for neighbor in neighbors:
        neighbor_ip,neighbor_port = neighbor
        sock.sendto(table.encode(), (neighbor_ip,neighbor_port ))
        print(f"Sent routing table to port : {neighbor_port}")

def poison_send_to_neighbors(table, out_ports):
    '''send packet to destination router with poison'''

def server(input_ports, neighbors):
    """Run the server to listen on multiple UDP sockets and send to neighbors."""
    sockets = create_and_bind(input_ports)
    send_socket = sockets[0]  # First socket for sending
    try:
        while True:
            #wait for any socket to have data
            readable, _writable_, _exceptional_ = select.select(sockets, [], [])
            for sock in readable:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                print(f"Received data from {addr}: {data.decode()}")
                # process the received data
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        for sock in sockets:
            sock.close()

# Example:
input_ports = [6110, 6211, 7345]
neighbors = [('127.0.0.1', 5000), ('127.0.0.1', 5002)]
server(input_ports, neighbors)