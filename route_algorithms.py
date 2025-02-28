table1 = {2: [1, 2, False], 6: [5, 6, False], 7: [8, 7, False]}
table2 = {1: [1, 1, False], 3: [3, 3, False]}
table3 = {2: [3, 2, False], 4: [4, 4, False]}
table4 = {3: [4, 3, False], 5: [2, 5, False], 7: [6, 7, False]}
table5 = {4: [2, 4, False], 6: [1, 6, False]}
table6 = {1: [5, 1, False], 5: [1, 5, False]}
# destionation:[metric,next hop,garbage_flag]
packet1 = {'header': [2, 2, 1], 'entry': [(1, 2), (5, 6), (8, 7)]}
packet2 = {'header': [2, 2, 2], 'entry': [(1, 1), (3, 3)]}
packet3 = {'header': [2, 2, 3], 'entry': [(3, 2), (4, 4)]}
packet4 = {'header': [2, 2, 4], 'entry': [(4, 3), (2, 5), (6, 7)]}
packet5 = {'header': [2, 2, 5], 'entry': [(2, 4), (1, 6)]}
packet6 = {'header': [2, 2, 6], 'entry': [(5, 1), (16, 5)]}

#'header:[command,version,src]'  entry:(destionation,metric)

##implement  Split Horizon+Poison Reverse  ##在这里，或者processer里面##
#水平分割 Split Horizon：RIP从某个接口学到的路由，不会从该接口再发回给邻居路由器。
#毒性反转 Poison Reverse:从某个接口学到路由后，从原接口发回邻居路由器，并将该路由的开销设置为16（即指明该路由不可达）。
#https://support.huawei.com/enterprise/zh/doc/EDOC1100112408/6063042

def routing_algorithms(table, packet):
    '''return a format of current routing table'''
    #initilize received routing table
    dst_id = table.keys()
    ndst = []
    for k in packet['entry']:
        ndst.append(k[1])
    src = packet['header'][2]

    #produrce routing table
    for i in range(len(ndst)):
        if ndst[i] != router_id:

            next_hop = src
      
            # Apply Split Horizon with Poison Reverse
            #if ???
            #    metric = 16  # Poison Reverse: set metric to 16 if learned from the same interface
            #else:
            metric = table[src][0] + packet['entry'][i][0]

            if metric >16:
                metric = 16

            # if not exist, make new
            if ndst[i] not in dst_id:
                table[ndst[i]] = [metric, next_hop, False]
            #if next hop is not changed
            if next_hop == table[ndst[i]][1]:
                table[ndst[i]] = [metric, next_hop, False] if ndst[i] in table else [metric, next_hop, False]

            # if a better path
            if metric < table[ndst[i]][0]:
                table[ndst[i]] = [metric, next_hop, False]              
            
    return table

router_id = 1
routing_table = routing_algorithms(table1, packet6)
print(routing_table)