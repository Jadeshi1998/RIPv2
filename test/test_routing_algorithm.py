import time
import routing_table as rt
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
                    print(f"New route to {destination} via {src_router_id} with cost {new_cost} added.")
                    rt.new_route(destination, src_router_id, new_cost,table,time = time.time(), garbage=False)
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



#This is the test for G1 
table1 = {
    2: {'next_hop': 2, 'cost': 1, 'garbage': False, 'last_update_time': time.time()},
    4: {'next_hop': 2, 'cost': 1, 'garbage': False, 'last_update_time': time.time()}}
# header:[command,version,src_router_id]'  entry:(destination,metric)
packet2 = {'header': [2, 2, 2], 'entry': [[1, 1],[3, 5],[4, 1]]}

def test_add_new_route():
    router_ID = 1
    new_routing_table, update = routing_algorithms(router_ID, table1, packet2)
    assert update == True
    assert new_routing_table[3]['cost'] == 6
    assert new_routing_table[3]['next_hop'] == 2
    assert new_routing_table[3]['garbage'] == False
    print("test_add_new_route passed.")

table11 = {
    2: {'next_hop': 2, 'cost': 1, 'garbage': False, 'last_update_time': time.time()},
    4: {'next_hop': 4, 'cost': 3, 'garbage': False, 'last_update_time': time.time()},
    3: {'next_hop': 2, 'cost': 6, 'garbage': False, 'last_update_time': time.time()}}
packet22 = {'header': [2, 2, 2], 'entry': [[1, 1],[3, 5],[4, 1]]}

def test_update_existing_route():
    router_ID = 1
    new_routing_table, update = routing_algorithms(router_ID, table11, packet22)
    assert update == True
    assert new_routing_table[4]['cost'] == 2, "Expected cost to be 6"
    assert new_routing_table[4]['next_hop'] == 2, "Expected next_hop to be 6"
    assert new_routing_table[4]['garbage'] == False, "Expected garbage to be False"
    print("test_update_existing_route passed.")


test_add_new_route()
test_update_existing_route()
