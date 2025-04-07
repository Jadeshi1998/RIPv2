import time
METRIC_INFINITY = 16

def routing_algorithms(router_ID, table, packet):  
    """Return a format of updated routing table."""

    update = False
    # Received a packet, update the routing table
    # Record where it came from -> src_router_id
    src_router_id = packet['header'][2]
    # Record 'entry', e.g., [(2, 1), (6, 5), (7, 8)]

    for entry in packet['entry']:
        destination = entry[0]
        metric = entry[1]
        # If the destination is not the current router_ID, avoid using itself
        if destination != router_ID:
            # If metric is greater than 16, metric = inf = 16
            new_cost = metric + table.get(src_router_id, {}).get('cost', 0)
            if new_cost > METRIC_INFINITY:
                new_cost = METRIC_INFINITY

            # Scenario 1: If the destination is not in the current routing table, add a new destination
            if destination not in table:
                if new_cost < METRIC_INFINITY:
                    table[destination] = {'next_hop': src_router_id, 'cost': new_cost, 'garbage': False, 'last_update_time': time.time()}
                    update = True
    
            else:
                # Scenario 2: If the next_hop is the same and there is a better path, update
                if src_router_id == table[destination]['next_hop']:
                    if new_cost < table[destination]['cost']:
                        table[destination]['cost'] = new_cost 
                        table[destination]['garbage'] = False
                        table[destination]['last_update_time'] = time.time()
                        update = True
                # Scenario 3: If the next_hop is different and there is a better path, update to use src_router_id as next_hop
                if new_cost < table[destination]['cost']:
                    table[destination]['next_hop'] = src_router_id
                    table[destination]['cost'] = new_cost
                    table[destination]['garbage'] = False
                    table[destination]['last_update_time'] = time.time()
                    update = True

    return table, update


def timer_update(table, port_id,pkt):
    current_time = time.time()
    pkt_destinations =[]
    src_router_id = pkt['header'][2]
    for entry in pkt['entry']:
        destination = entry[0]
        pkt_destinations.append(destination)
    for destination, route_info in table.items():
        if route_info['next_hop'] == port_id:
            if destination in pkt_destinations or destination == src_router_id:
                table[destination]['last_update_time'] = current_time
    return table

# Example routing tables
table1 = {
    2: {'next_hop': 2, 'cost': 1, 'garbage': False, 'last_update_time': time.time()},
    6: {'next_hop': 6, 'cost': 5, 'garbage': False, 'last_update_time': time.time()},
    7: {'next_hop': 7, 'cost': 8, 'garbage': False, 'last_update_time': time.time()}}
table2 = {
    1: {'next_hop': 1, 'cost': 1, 'garbage': False, 'last_update_time': time.time()},
    3: {'next_hop': 3, 'cost': 3, 'garbage': False, 'last_update_time': time.time()}}
table3 = {
    2: {'next_hop': 2, 'cost': 3, 'garbage': False, 'last_update_time': time.time()},
    4: {'next_hop': 4, 'cost': 4, 'garbage': False, 'last_update_time': time.time()}}
table4 = {
    3: {'next_hop': 3, 'cost': 4, 'garbage': False, 'last_update_time': time.time()},
    5: {'next_hop': 5, 'cost': 2, 'garbage': False, 'last_update_time': time.time()},
    7: {'next_hop': 7, 'cost': 6, 'garbage': False, 'last_update_time': time.time()}}
table5 = {
    4: {'next_hop': 4, 'cost': 2, 'garbage': False, 'last_update_time': time.time()},
    6: {'next_hop': 6, 'cost': 1, 'garbage': False, 'last_update_time': time.time()}}
table6 = {
    1: {'next_hop': 1, 'cost': 5, 'garbage': False, 'last_update_time': time.time()},
    5: {'next_hop': 5, 'cost': 1, 'garbage': False, 'last_update_time': time.time()}}

# 'header:[command,version,src_router_id]'  entry:(destination,metric)
packet1 = {'header': [2, 2, 1], 'entry': [[2, 1], [6, 5], [7, 8]]}
packet2 = {'header': [2, 2, 2], 'entry': [[1, 1], [3, 3]]}
packet3 = {'header': [2, 2, 3], 'entry': [[2, 3], [4, 4]]}
packet4 = {'header': [2, 2, 4], 'entry': [[3, 4], [5, 2], [7, 6]]}
packet5 = {'header': [2, 2, 5], 'entry': [[4, 2], [6, 1]]}
packet6 = {'header': [2, 2, 6], 'entry': [[1, 5], [5, 1]]}
packet7 = {'header': [2, 2, 6], 'entry': [[1, 8], [4, 6]]}

# router_ID is the router number of this routing table, 1, simulating receiving packet 6 from "neighbor" router 6
# router_ID = 1
# new_routing_table_1, update = routing_algorithms(router_ID, table1, packet6)
# print(f'router_ID 1 : {new_routing_table_1}\n')

# Originally, table 2 only had paths to 2, 6, and 7. Through router 6's update "(1, 5), (5, 16)", it excluded the loop to 1 and added a new path to 5.
# routing_table_2, update = routing_algorithms(router_ID, new_routing_table_1, packet7)
# print(f'router_ID next : {routing_table_2}\n')

# router_ID is the router number of this routing table, 2, simulating receiving packet 5 from "neighbor" router 5
# router_ID = 2
# routing_table = routing_algorithms(router_ID, table2, packet3)
# print(f'router_ID 2 : {routing_table}')
# Originally, table 2 only had paths to 1 and 3. Through router 5's update "(4, 2 + cost to 2), (6, 1 + cost to 1)", it added new paths to 4 and 6.