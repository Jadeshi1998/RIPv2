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


def test_new_route():
    routing_table = {}
    destination = 3
    next_hop = 5
    cost = 2
    new_route(3, 5, 2, routing_table)
    assert destination in routing_table
    assert routing_table[destination]['next_hop'] == next_hop
    assert routing_table[destination]['cost'] == cost
    assert not routing_table[destination]['garbage']
    print("test_new_route pass.")

def test_remove_route():
    routing_table = {3: {'next_hop': 5, 'cost': 2, 'garbage': False}}
    destination = 3
    remove_route(destination, routing_table)
    assert destination not in routing_table
    print("test_remove_route pass.")

def test_flag_garbage():
    routing_table = {3: {'next_hop': 5, 'cost': 2, 'garbage': False}}
    destination = 3
    flag_garbage(destination, routing_table)
    assert routing_table[destination]['garbage']
    print("test_flag_garbage pass.")

def test_set_infinity():
    routing_table = {3: {'next_hop': 5, 'cost': 2, 'garbage': False}}
    destination = 3
    set_infinity(destination, routing_table)
    assert routing_table[destination]['cost'] == METRIC_INFINITY
    print("test_set_infinity pass.")


test_new_route()
test_remove_route()
test_flag_garbage()
test_set_infinity()