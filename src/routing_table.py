"""
    Routing Table Structure
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Dest(key) |  Next Hop | Cost | update timer  |  garbage   | 
    +-------------+-----------+------+---------------+------------+
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
    }

def remove_route(destination,routing_table):
    """Remove a route from the routing table."""
    if destination in routing_table:
        del routing_table[destination]
        print("  ")
        print("!"*40)
        print(f"Route to {destination} garbage collection 180s -> remove_route")
    return routing_table

def flag_garbage(destination,routing_table):
    """ Flag a route as garbage. """
    if destination in routing_table:
        routing_table[destination]['garbage'] = True
        print("  ")
        print("!"*40)
        print(f"Route to {destination} expired 180s -> garbage collection")
    return routing_table

def set_infinity(destination,routing_table):
    """ Set a route's metric to infinity. """
    if destination in routing_table:
        routing_table[destination]['cost'] = METRIC_INFINITY
    return routing_table


