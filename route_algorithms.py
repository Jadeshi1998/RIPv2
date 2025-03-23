import time
table1 = {
    2: {'next_hop': 2, 'cost': 1, 'garbage': False,'last_update_time':time.time(),'timeout':120},
    6: {'next_hop': 6, 'cost': 5, 'garbage': False},
    7: {'next_hop': 7, 'cost': 8, 'garbage': False}}
table2 = {
    1: {'next_hop': 1, 'cost': 1, 'garbage': False},
    3: {'next_hop': 3, 'cost': 3, 'garbage': False}}
table3 = {
    2: {'next_hop': 2, 'cost': 3, 'garbage': False},
    4: {'next_hop': 4, 'cost': 4, 'garbage': False}}
table4 = {
    3: {'next_hop': 3, 'cost': 4, 'garbage': False},
    5: {'next_hop': 5, 'cost': 2, 'garbage': False},
    7: {'next_hop': 7, 'cost': 6, 'garbage': False}}
table5 = {
    4: {'next_hop': 4, 'cost': 2, 'garbage': False},
    6: {'next_hop': 6, 'cost': 1, 'garbage': False}}
table6 = {
    1: {'next_hop': 1, 'cost': 5, 'garbage': False},
    5: {'next_hop': 5, 'cost': 1, 'garbage': False}}

#'header:[command,version,src_router_id]'  entry:(destionation,metric)
packet1 = {'header': [2, 2, 1], 'entry': [[2, 1], [6, 5], [7, 8]]}
packet2 = {'header': [2, 2, 2], 'entry': [[1, 1], [3, 3]]}
packet3 = {'header': [2, 2, 3], 'entry': [[2, 3], [4, 4]]}
packet4 = {'header': [2, 2, 4], 'entry': [[3, 4], [5, 2], [7, 6]]}
packet5 = {'header': [2, 2, 5], 'entry': [[4, 2], [6, 1]]}
packet6 = {'header': [2, 2, 6], 'entry': [[1, 5], [5, 1]]}
packet7 = {'header': [2, 2, 6], 'entry': [[1, 8], [4, 6]]}

import time


    
def routing_algorithms(router_ID ,table, packet):  
    """Return a format of updated routing table."""

    update = False
    #收到一个pkt，更新routing table
    #记录来自哪里 -> src_router_id
    src_router_id = packet['header'][2]
    #记录'entry', eg.[(2, 1), (6, 5), (7, 8)]

    for entry in packet['entry']:
        destination = entry[0]
        metric = entry[1]
        #如果destination不是当前router_ID，避免出现自己用自己
        if destination != router_ID:
            #如果metric大于16，metric = inf = 16
            new_cost = metric + table.get(src_router_id, {}).get('cost', 0)
            if new_cost > 16:
                new_cost = 16

            #scenario 1: 如果destination不在当前的routing table中，加入新的destination
            if destination not in table:
                if new_cost < 16:
                    table[destination] = {'next_hop': src_router_id, 'cost': new_cost  , 'garbage': False , 'last_update_time' : time.time(), 'timeout': None}
                    update = True
    
            else:
                #scenario 2: 如果next_hop相同,有更好的路径，更新
                if src_router_id == table[destination]['next_hop']:
                    if new_cost  < table[destination]['cost']:
                        table[destination]['cost'] = new_cost 
                        table[destination]['garbage']= False
                        table[destination]['last_update_time'] = time.time()
                        table[destination]['timeout']= None
                        update = True
                #scenario 3: 如果next_hop不同,如果有更好的路径,更新为用src_router_id为next_hop
                if new_cost < table[destination]['cost']:
                    table[destination]['next_hop'] =  src_router_id
                    table[destination]['cost'] = new_cost
                    table[destination]['garbage']= False
                    table[destination]['last_update_time'] = time.time()
                    table[destination]['timeout']= None
                    update = True


    return table,update


def timer_update(table,port_id):
    current_time = time.time()
  
    for destination, route_info in table.items():
        if route_info['next_hop'] == port_id:
            table[destination]['last_update_time'] = current_time
    return table

#router_ID为该路由表的路由器编号1号，模拟收到来自“邻居”6号路由器的6号包
#router_ID = 1
#new_routing_table_1,update = routing_algorithms(router_ID , table1, packet6)
#print(f'router_ID 1 : {new_routing_table_1}\n')

#原本2号的表只有到2，6和7的路径，通过路由器6的更新“(1, 5), (5, 16)”，排除了到1号的回路，加入了新的路径到5。
#routing_table_2 ,update= routing_algorithms(router_ID , new_routing_table_1, packet7)
#print(f'router_ID next : {routing_table_2}\n')

#router_ID为该路由表的路由器编号2号，模拟收到来自“邻居”5号路由器的5号包
#router_ID = 2
#routing_table = routing_algorithms(router_ID , table2, packet3)
#print(f'router_ID 2 : {routing_table}')
#原本2号的表只有到1和3的路径，通过路由器5的更新“(4, 2+自己到2 cost), (6, 1+自己到1 cost)”，加入了新的路径到4和6。