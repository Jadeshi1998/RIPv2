"""
    信息的存储地在router内部储存记录了当前网络的拓扑结构和最佳路径。
    Routing Table Structure
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |     Dest(key)   |   Next Hop   |   Cost   |   Garbage(bool)    |
    +---------------+---------------+-------------------------------+

"""
import time

METRIC_INFINITY = 16

def new_route(destination, next_hop, cost,routing_table,time = time.time(), garbage=False):
    """Add or update a route in the routing table."""
    if not (1 <= cost < METRIC_INFINITY):
        raise ValueError(f"ERROR: Invalid metric {cost}. Must be in range 1-15.")
    routing_table[destination] = {
    'next_hop': next_hop,
    'cost': cost,
    'last_update_time': time,
    'garbage': garbage,
    'timeout': None
    }
    #print(f'Route added: {destination} -> Next Hop: {next_hop}, Cost: {cost}, Garbage: {garbage}')
    return routing_table
def remove_route(destination,routing_table):
    """Remove a route from the routing table."""
    if destination in routing_table:
        del routing_table[destination]
        print("  ")
        print("!"*40)
        print(f"Route to {destination} expired 180s -> remove_route")
    return routing_table

def flag_garbage(destination,routing_table):
    """ Flag a route as garbage. """
    if destination in routing_table:
        routing_table[destination]['garbage'] = True
        print("  ")
        print("!"*40)
        print(f"Route to {destination} expired 120s -> garbage collection")
    return routing_table
def set_infinity(destination,routing_table):
    """ Set a route's metric to infinity. """
    if destination in routing_table:
        routing_table[destination]['cost'] = METRIC_INFINITY
    return routing_table


#test_routing_table()
