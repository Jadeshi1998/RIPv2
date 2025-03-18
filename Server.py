"""
This acting as server in a router.
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

global router_ID
global routing_table
global split_horizon

router_ID = None
routing_table = {}
split_horizon_port = [] 

def init(config_filename):
    """Initialize the routing table inside a router from config file,
    also grnerate the first round RIP packet , this pkt will pass to send to the neighbors in port
    """
    global routing_table  
    global router_ID  

    neighbor_mapping={}
    
    config = cfg.read_config(config_filename)
    for router in config['output_ports']:
        #Output_ports = [peer_port, cost, peer_ID]
        peer_port = router[0]
        cost = router[1]
        peer_ID = router[2]
        #new_route(destination, next_hop, cost)
        neighbor_mapping[peer_port] = peer_ID
        table.new_route(peer_ID, peer_ID, cost)
    routing_table = table.table()
    #print(routing_table)
    input_ports = config['input_ports']
    neighbor_port = [i[0] for i in config['output_ports']]
    router_ID = config['router_id']
    rip_pkt = packet.rip_packet(router_ID, routing_table)
    return input_ports, neighbor_port , rip_pkt , neighbor_mapping

def pkt_to_str(rip_pkt):
    """Convert a RIP packet from dictionary to a string for sending over UDP."""
    header_str = ','.join(map(str, rip_pkt['header']))
    entries_str = ';'.join(','.join(map(str, entry)) for entry in rip_pkt['entry'])
    packet_str = f'header={header_str} || entries={entries_str}'
    return packet_str
    
def str_to_pkt(pkt_str):
    """Convert a RIP packet from a string to a dictionary for processing."""
    parts = pkt_str.split(" || ")
    header_str = parts[0].split("=")[1]
    entries_str = parts[1].split("=")[1]
    header = list(map(int, header_str.split(",")))
    entries = [list(map(int, entry.split(","))) for entry in entries_str.split(";") if entry]
    return {'header': header, 'entry': entries}


def create_and_bind(input_ports):
    """Create and bind UDP sockets for each input port."""
    sockets = []
    for port in input_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', port))
        sockets.append(sock)
        #print(f"Listening on UDP port {port}")
    return sockets

def send_to_neighbors(sock, neighbor_port, rip_pkt):
    """Send a routing table to each neighbor using the specified socket."""
    global split_horizon_port
    
    neighbor_ip = '127.0.0.1'
    str_pck = pkt_to_str(rip_pkt)
    if neighbor_port not in split_horizon_port:
        sock.sendto(str_pck.encode(), (neighbor_ip, neighbor_port))
        print(f"Sent routing packet to port: {neighbor_port}")


def periodic_update(sock, neighbors, rip_pkt):
    """Send periodic updates to neighbors.
       every 30 +/- 5 seconds
    """
    for neighbor_port in neighbors:
        send_to_neighbors(sock, neighbor_port, rip_pkt)

def manage_timers():
    """
       route timeouts : 180 seconds
       garbage collection: 120 seconds
       current_time = 10
       next_time = 11
    """
    next_time = time.time() + 1
    while True:
        current_time = time.time()
        if current_time >= next_time:
            for destination, route_info in list(routing_table.items()):
                if current_time - route_info['last_update'] > 180:
                    route_info['metric'] = 16
                    route_info['garbage_timer'] = current_time + 120
                    print(f"Route to {destination} expired -> garbage collection")

                if 'garbage_timer' in route_info and current_time > route_info['garbage_timer']:
                    del routing_table[destination]
                    print(f"Route to {destination} removed.")

            next_time = current_time + 1
        time.sleep(0.1)  # Sleep for a short time to prevent busy-waiting

def main(config_filename):
    """Run the server to listen on multiple UDP sockets and send to neighbors."""
    global routing_table  
    global router_ID     
    global split_horizon_port

    input_ports, neighbors, rip_pkt, neighbor_mapping = init(config_filename)
    print(f'init routing table: {routing_table}')
    sockets = create_and_bind(input_ports)
    send_socket = sockets[0]  # First socket for sending
    for neighbor_port in neighbors:
        send_to_neighbors(send_socket, neighbor_port, rip_pkt)

    next_periodic_update_time = time.time() + 30 + random.uniform(-5, 5)
    
    try:
        while True:
            current_time = time.time()
            rip_pkt = packet.rip_packet(router_ID, routing_table)
            if  current_time >= next_periodic_update_time:
                for neighbor_port in neighbors:
                    send_to_neighbors(send_socket, neighbor_port, rip_pkt)
                next_periodic_update_time = current_time + 30 + random.uniform(-5, 5)

            #manage_timers()
            
            neighbor_id = None
            #wait for any socket to have data
            readable, _writable_, _exceptional_ = select.select(sockets, [], [],1)
            for sock in readable:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                txt = data.decode()
                pkt = str_to_pkt(data.decode())
                recive_port = addr[1]
                print(f"Received data from port {recive_port}: {pkt}")
                #from a port not in the relationship when init
                if recive_port not in neighbor_mapping:
                    neighbor_mapping[recive_port] = pkt['header'][0]

                #running algorithm with input pkt, output a new table and a bool
                routing_table,update= ra.routing_algorithms(router_ID ,routing_table, pkt)
                if update:
                    split_horizon_id = ra.split_horizon(routing_table)
                
                    for id in split_horizon_id:
                        # Find the corresponding port for the given ID in neighbor_mapping
                        for port, neighbor_id in neighbor_mapping.items():
                            if neighbor_id == id:
                                split_horizon_port.append(port)
                    neighbor_id = neighbor_mapping[recive_port]
                    poisoned_packet = packet.set_poisoned_reverse(router_ID, routing_table, neighbor_id)
                    for neighbor_port in neighbors:
                        send_to_neighbors(sock, neighbor_port, poisoned_packet)
                    print(f'Update routing table: {routing_table}')
                   
                
                #######################################

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        for sock in sockets:
            sock.close()