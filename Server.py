"""
Server creates as many UDP sockets as it has input ports and binds
one socket to each input port. One of the input sockets can be used for
sending UDP datagrams to neighbors.
"""
import socket
import select
import threading
import time
import random

import config as cfg
import route_algorithms as ra
import Routing_table as table
import RIP_packet as packet

router_ID = None
routing_table = {}
def init(config_filename):
    config = cfg.read_config(config_filename)
    for router in config['output_ports']:
        #Output_ports = [peer_port, metric, peer_ID]
        #new_route(destination, next_hop, cost)
        table.new_route(router[2], router[2], router[1])
    routing_table = table.table()
    print(routing_table)
    input_ports = config['input_ports']
    neighbor_port = [i[0] for i in config['output_ports']]
    router_ID = config['router_id']
    rip_pkt = packet.rip_packet(router_ID, routing_table)

    return routing_table , input_ports, neighbor_port , rip_pkt

def pkt_tostr(rip_pkt):
    header_str = ','.join(map(str, rip_pkt['header']))
    entries_str = ';'.join(','.join(map(str, entry)) for entry in rip_pkt['entry'])
    packet_str = f'header={header_str} | entries={entries_str}'

    return packet_str
    


def create_and_bind(input_ports):
    """Create and bind UDP sockets for each input port."""
    sockets = []
    for port in input_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', port))
        sockets.append(sock)
        print(f"Listening on UDP port {port}")
    return sockets

def send_to_neighbors(sock, neighbors, pkt):
    """Send a routing table to each neighbor using the specified socket."""
    neighbor_ip = '127.0.0.1'
    for neighbor_port in neighbors:
        sock.sendto(pkt.encode(), (neighbor_ip, neighbor_port))
        print(f"Sent routing packet to port: {neighbor_port}")



def periodic_update(sock, neighbors, pkt):
    """Send periodic updates to neighbors.every 30 +/- 5 seconds"""
    while True:
        time.sleep( 30 + random.uniform(-5, 5))
        send_to_neighbors(sock, neighbors, pkt)

def manage_route_timers():
    """Manage 
       route timeouts : 180 seconds
       garbage collection: 120 seconds
       """
    while True:
        current_time = time.time()
        for destination, route_info in list(routing_table.items()):
            if current_time - route_info['last_update'] > 180:
                # Mark route as expired
                # Set metric to 16
                route_info['metric'] = 16
                # Set garbage collection timer
                route_info['garbage_timer'] = current_time + 120
                print(f"Route to {destination} expired -> garbage collection")

            if 'garbage_timer' in route_info and current_time > route_info['garbage_timer']:
                # Remove route after been garbaged 
                del routing_table[destination]
                print(f"Route to {destination} removed.")

        time.sleep(1)  # Check every 1 second


def main(config_filename):
    """Run the server to listen on multiple UDP sockets and send to neighbors."""
    routing_table , input_ports, neighbors , rip_pkt =  init(config_filename)
    pkt = pkt_tostr(rip_pkt)
    sockets = create_and_bind(input_ports)
    send_socket = sockets[0]  # First socket for sending
    # Start periodic update thread
    threading.Thread(target=periodic_update, args=(send_socket, neighbors,pkt), daemon=True).start()
    # Start route management thread
    threading.Thread(target=manage_route_timers, daemon=True).start()

    try:
        while True:
            #wait for any socket to have data
            readable, _writable_, _exceptional_ = select.select(sockets, [], [])
            for sock in readable:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                print(f"Received data from {addr}: {data.decode()}")
                #######################################
                # process_raw_data(data.decode())
                # algratim to process the received data
                #
                #######################################

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        for sock in sockets:
            sock.close()

