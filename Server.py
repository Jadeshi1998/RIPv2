"""
This acting as server in a router.
Server creates as many UDP sockets as it has input ports and binds
one socket to each input port. One of the input sockets can be used for
sending UDP datagrams to neighbors.
"""
import socket
import select
import time
import random
import copy


import config as cfg
import route_algorithms as ra
import Routing_table as table
import RIP_packet as packet

global router_ID
global neighbor_mapping 



router_ID = None
neighbor_mapping={}
#neighbor_mapping = {port: neighbor_id}

def init(config_filename):
    """Initialize the routing table inside a router from config file,
    also grnerate the first round RIP packet , this pkt will pass to send to the neighbors in port
    """
    global router_ID  
    global neighbor_mapping 

    routing_table = {}
    config = cfg.read_config(config_filename)
    for router in config['output_ports']:
        #Output_ports = [peer_port, cost, peer_ID]
        peer_port = router[0]
        cost = router[1]
        peer_ID = router[2]
        #new_route(destination, next_hop, cost)
        neighbor_mapping[peer_port] = peer_ID
        table.new_route(peer_ID, peer_ID, cost,routing_table)
    origin_routing_table = routing_table
    input_ports = config['input_ports']
    neighbor_port = [i[0] for i in config['output_ports']]
    router_ID = config['router_id']
    rip_pkt = packet.rip_packet(router_ID, origin_routing_table)
    return origin_routing_table,input_ports, neighbor_port , rip_pkt 

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
    return sockets

def send_to_neighbors(sock, neighbor_port, rip_pkt):
    """Send the rip pk to each neighbor using the specified socket."""
    neighbor_ip = '127.0.0.1'
    str_pck = pkt_to_str(rip_pkt)
    sock.sendto(str_pck.encode(), (neighbor_ip, neighbor_port))

def trigger_update(routing_table,send_socket,neighbors):
    """ triverse each neighbors, Get rip pk ready then to send to neighbors port."""
    global router_ID   
    global neighbor_mapping 
    for neighbor_port in neighbors:
        for destination, route_info in routing_table.items():
            #1: {'next_hop': 1, 'cost': 1, 'garbage': False},
            neighbor_id = neighbor_mapping[neighbor_port]
            rip_pkt = packet.rip_packet(router_ID, routing_table)
            if (route_info['next_hop'] == neighbor_id) and destination != neighbor_id:
                rip_pkt = packet.set_poisoned_reverse(router_ID, routing_table, neighbor_id)
        send_to_neighbors(send_socket, neighbor_port, rip_pkt)

def add_neighbor_router_back(routing_table,neighbor_id,origin_routing_table,pkt):
    """
    If a neighbor router is back to alive
    Add this neighbor router back to the routing table.
    The rest of the routing table will be updated by the routing algorithm.
    """
    current_time = time.time()
    update = False
    if neighbor_id in routing_table:
        if routing_table[neighbor_id]['garbage'] == True:
            #back connection with this router
            routing_table[neighbor_id]['garbage'] = False
            routing_table[neighbor_id]['last_update_time'] = current_time
            routing_table[neighbor_id]['cost'] = origin_routing_table[neighbor_id]['cost']
            update = True
    #running algorithm with input pkt, output a new table and a bool
    if neighbor_id  not in routing_table:
        routing_table[neighbor_id] = {'next_hop': neighbor_id, 'cost': pkt['header'][2], 'garbage': False, 'last_update_time': current_time}
        update = True
    return update

def check_alive(destinations_to_check,routing_table):
    """Check if the route in the routing table is still alive."""
    current_time = time.time()
    for destination in destinations_to_check:
        route_info = routing_table[destination]
        #180s not recive from this port:
        if current_time - route_info['last_update_time'] > 30 and route_info['garbage'] == False:
            routing_table = table.set_infinity(destination,routing_table)
            routing_table = table.flag_garbage(destination,routing_table)
        if route_info['garbage'] == True and current_time - route_info['last_update_time'] >= 35:
            routing_table = table.remove_route(destination,routing_table)
    return routing_table

def print_routing_table(routing_table):
    """Nicer look in print the contents of the routing table."""
    print("  ")
    print("#" * 20 + "Routing Table:" + "#" * 20)
    for destination, info in routing_table.items():
        print(f"               Destination: {destination}")
        print(f"   Next Hop: {info['next_hop']}    Cost: {info['cost']}    Garbage: {info['garbage']}")
        print(f"   Last Update Time: {info['last_update_time']}")
        print("-" * 50)

def print_RIP(receive_port,pkt):
    """Nicer look in print the contents of a received RIP packet."""
    print("  ")
    print(f"Received data from port {receive_port}:")
    print("Header:")
    print(f"  Version: {pkt['header'][0]}")
    print(f"  Type: {pkt['header'][1]}")
    print(f"  Length: {pkt['header'][2]}")
    print("Entries:")
    for entry in pkt['entry']:
        print(f"  Destination: {entry[0]}, Cost: {entry[1]}")
                    #from a port not in the relationship when init


def main(config_filename):
    """Run the server to listen on multiple UDP sockets and send to neighbors."""
    global router_ID   
    global neighbor_mapping 

######################-------------init-------------########################
    origin_routing_table,input_ports, neighbors, init_rip_pkt= init(config_filename)
    # Make a copy of the original routing avoid point to the same dictionary object in memory. 
    routing_table = copy.deepcopy(origin_routing_table)
    print_routing_table(routing_table)
    sockets = create_and_bind(input_ports)
    send_socket = sockets[0]  # First socket for sending
    for neighbor_port in neighbors:
        send_to_neighbors(send_socket, neighbor_port, init_rip_pkt)
######################-------------init-------------########################

    next_periodic_update_time = time.time() + 30 + random.uniform(-5, 5)
    next_sec = time.time() + 1

#-------------------------------deamon loop----------------------------------------------------#
    try:
        while True:
            current_time = time.time()
           
            if len(routing_table) != 0:
                if  current_time >= next_periodic_update_time:
                    trigger_update(routing_table,send_socket,neighbors)
                    print_routing_table(routing_table)
                    next_periodic_update_time = current_time + 30 + random.uniform(-5, 5)
                if current_time >= next_sec:
                    # avoid modifying the dictionary while iterating over it
                    destinations_to_check = list(routing_table.keys())
                    routing_table = check_alive(destinations_to_check,routing_table)
                    next_sec = current_time + 1

#-------------------------------listen----------------------------------------------------#
            #wait for any socket to have data
            readable, _writable_, _exceptional_ = select.select(sockets, [], [],1)
            for sock in readable:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                pkt = str_to_pkt(data.decode())
                receive_port = addr[1]
                print_RIP(receive_port,pkt)
                
                if receive_port not in neighbor_mapping:
                    neighbor_mapping[receive_port] = pkt['header'][0]
                neighbor_id = neighbor_mapping[receive_port]
                routing_table = ra.timer_update(routing_table,neighbor_id)
                 
                update = add_neighbor_router_back(routing_table,neighbor_id,origin_routing_table,pkt)

                routing_table, update= ra.routing_algorithms(router_ID ,routing_table, pkt)
                print_routing_table(routing_table)
                if update:
                    trigger_update(routing_table,send_socket,neighbors)
 #--------------------------------------------------------------------------------#

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        for sock in sockets:
            sock.close()