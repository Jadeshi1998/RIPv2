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


import config_processer as cfg
import routing_algorithm as ra
import routing_table as table
import RIP_packet as packet

global router_ID
global neighbor_mapping 



router_ID = None
#neighbor_mapping saves the mapping between port and router ID
#neighbor_mapping = {port: neighbor_id}
neighbor_mapping={}

def init(config_filename):
    """Initialize the routing table inside a router from config file,
    also grnerate the first round RIP packet , this pkt will pass to send to the neighbors in port
    """
    global router_ID  
    global neighbor_mapping 

    # Use table format to store a original routing information.
    origin_routing_info = {}

    config = cfg.read_config(config_filename)
    router_ID = config['router_id']
    input_ports = config['input_ports']
    neighbor_port = [i[0] for i in config['output_ports']]

    for router in config['output_ports']:
        #Output_ports = [peer_port, cost, peer_ID]
        peer_port = router[0]
        cost = router[1]
        peer_ID = router[2]
        neighbor_mapping[peer_port] = peer_ID
        table.new_route(peer_ID, peer_ID, cost,origin_routing_info)
    
    #rip_pkt = packet.rip_packet(router_ID, origin_routing_info[neighbor_mapping[peer_port]])
    return origin_routing_info,input_ports, neighbor_port

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
        neighbor_id = neighbor_mapping[neighbor_port]
        rip_pkt = packet.set_poisoned_reverse(router_ID, routing_table, neighbor_id)
        send_to_neighbors(send_socket, neighbor_port, rip_pkt)

def add_neighbor_router_back(routing_table,neighbor_id,origin_routing_info,pkt):
    """
    If a neighbor router is back to alive
    Add this neighbor router back to the routing table.
    The rest of the routing table will be updated by the routing algorithm.
    """
    current_time = time.time()
    update = False
    #scenario 1: Back connection with this router before removing it
    if neighbor_id in routing_table:
        # 1. Set the garbage flag to False, and update the last update time
        if routing_table[neighbor_id]['garbage'] == True:
            routing_table[neighbor_id]['garbage'] = False
            routing_table[neighbor_id]['last_update_time'] = current_time
            routing_table[neighbor_id]['cost'] = origin_routing_info[neighbor_id]['cost']
            update = True

        # 2. If the original cost of this neighbor router is smaller than the cost it in the routing table
        #    Use the original cost
        if routing_table[neighbor_id]['cost'] > origin_routing_info[neighbor_id]['cost']:
            routing_table[neighbor_id]['cost'] = origin_routing_info[neighbor_id]['cost']
            routing_table[neighbor_id]['next_hop'] = neighbor_id
            routing_table[neighbor_id]['last_update_time'] = current_time
            update = True

    #scenario 2:  if the neighbor router is been removal      
    if neighbor_id  not in routing_table:
       routing_table[neighbor_id] = {'next_hop': neighbor_id, 'cost': origin_routing_info[neighbor_id]['cost'], 'garbage': False, 'last_update_time': current_time}
       update = True
    return update

def check_alive(destinations_to_check,routing_table,send_socket,neighbors):
    """Check if the route in the routing table is still alive."""
    current_time = time.time()
    for destination in destinations_to_check:
        route_info = routing_table[destination]
        #180s not recive from this port:
        if current_time - route_info['last_update_time'] > 120 and route_info['garbage'] == False:
            routing_table = table.set_infinity(destination,routing_table)
            routing_table = table.flag_garbage(destination,routing_table)
            print(f"@@@@ router invalid trigger update send to neighbors@@@@")
            trigger_update(routing_table,send_socket,neighbors)
        if route_info['garbage'] == True and current_time - route_info['last_update_time'] >= 180:
            routing_table = table.remove_route(destination,routing_table)
            print(f"@@@@ router invalid trigger update send to neighbors@@@@")
            trigger_update(routing_table,send_socket,neighbors)
    return routing_table

def print_routing_table(routing_table):
    """Nicer look in print the contents of the routing table."""
    print("  ")
    print("#" * 20 + "Routing Table" + "#" * 20)
    for destination, info in routing_table.items():
        print(f"               Destination: {destination}")
        print(f"   Next Hop: {info['next_hop']}    Cost: {info['cost']}    Garbage: {info['garbage']}")
        print(f"   Last Update Time: {info['last_update_time']}")
        print("-" * 50)
    print("#" * 50)
    print("  ")

def print_RIP(receive_port,pkt):
    """Nicer look in print the contents of a received RIP packet."""
    print("  ")
    print("-" * 50)
    print(f"Received data from port {receive_port}:")
    print("Header:")
    print(f"  Version: {pkt['header'][0]}")
    print(f"  Type: {pkt['header'][1]}")
    print(f"  Source_Router: {pkt['header'][2]}")
    print("Entries:")
    for entry in pkt['entry']:
        print(f"  Destination: {entry[0]}, Cost: {entry[1]}")
    print("-" * 50)
    print("  ")

def check_pkt(pkt):
    """Check if the received packet is valid."""
    if 'header' not in pkt or 'entry' not in pkt:
        raise ValueError("ERROR: Invalid packet format,must contain 'header' and 'entry'")
    #check header
    if len(pkt['header']) != 3:
        raise ValueError("ERROR: Invalid packet header length, must be 3")
    if pkt['header'][0] !=2:
        raise ValueError("ERROR: Invalid command, must be 2")
    if pkt['header'][1] != 2:
        raise ValueError("ERROR: Invalid version, must be 2")
    if pkt['header'][2] <= 0:
        raise ValueError("ERROR: Invalid source router ID, must be positive integer")
    if pkt['header'][2] > 64000:
        raise ValueError("ERROR: Invalid source router ID, must be less than 64000")
    #check entry
    if len(pkt['entry']) == 0:
        raise ValueError("ERROR: Invalid packet entry, must contain at least one entry")
    for entry in pkt['entry']:
        if len(entry) != 2:
            raise ValueError("ERROR: Invalid entry , must be [destination, metric] ")
        if entry[0] <= 0:
            raise ValueError("ERROR: Invalid destination router ID, must be positive integer")
        if entry[0] > 64000:
            raise ValueError("ERROR: Invalid destination router ID, must be less than 64000")
        if entry[1] < 0 or entry[1] > 16:
            raise ValueError("ERROR: Invalid metric, must be in range 0-16")
    return pkt

def main(config_filename):
    """Run the server to listen on multiple UDP sockets and send to neighbors."""
    global router_ID   
    global neighbor_mapping 

######################-------------init-------------########################
    origin_routing_info,input_ports, neighbors = init(config_filename)
    # Creat a empty routing table
    routing_table = {}
    print(" --------------Initial Routing Table--------------")
    print_routing_table(routing_table)
    sockets = create_and_bind(input_ports)
    send_socket = sockets[0]  # First socket for sending
    for neighbor_port in neighbors:
        #Create single route RIP packet for each neighbor and send
        neighbor_id = neighbor_mapping[neighbor_port]
        neighbor_routing_info = {neighbor_id:origin_routing_info[neighbor_id]}
        rip_pkt = packet.rip_packet(router_ID, neighbor_routing_info)
        send_to_neighbors(send_socket, neighbor_port, rip_pkt)

######################-------------init-------------########################

    next_periodic_update_time = time.time() + 30 + random.uniform(-5, 5)
    next_sec = time.time() + 1

#-------------------------------deamon loop----------------------------------------------------#
    try:
        while True:
            current_time = time.time()
           
            if  current_time >= next_periodic_update_time:
                    # Send the routing table to all neighbors every 30 seconds
                trigger_update(routing_table,send_socket,neighbors)
                print(f"!!!!!!!! 30s trigger update send to neighbors {neighbors}!!!!!!!!")
                print_routing_table(routing_table)
                next_periodic_update_time = current_time + 30 + random.uniform(-5, 5)
            if current_time >= next_sec:
                # avoid modifying the dictionary while iterating over it
                destinations_to_check = list(routing_table.keys())
                routing_table = check_alive(destinations_to_check,routing_table,send_socket,neighbors)
                next_sec = current_time + 1

#-------------------------------listen----------------------------------------------------#
            #wait for any socket to have data
            readable, _writable_, _exceptional_ = select.select(sockets, [], [],1)
            for sock in readable:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                pkt = str_to_pkt(data.decode())
                receive_port = addr[1]
                
                pkt=check_pkt(pkt)

                print_RIP(receive_port,pkt)
                
                if receive_port not in neighbor_mapping:
                    neighbor_mapping[receive_port] = pkt['header'][2]

                neighbor_id = neighbor_mapping[receive_port]
                
                routing_table = ra.timer_update(routing_table,neighbor_id,pkt)
                update = add_neighbor_router_back(routing_table,neighbor_id,origin_routing_info,pkt)
                if update:
                    print(f"@@@@@@@@@ Neighbor {neighbor_id} is back to alive @@@@@@@@@")
                    print(f"@@@@@@@@@@@@@@@@ Routing table update @@@@@@@@@@@@@@@@@")
                    print_routing_table(routing_table)
                routing_table, update= ra.routing_algorithms(router_ID ,routing_table, pkt)
                if update:
                    print(f"Routing table update from {receive_port}:")
                    print_routing_table(routing_table)
 #--------------------------------------------------------------------------------#

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        for sock in sockets:
            sock.close()