# 🛰️ RIP_Routing 

A routing daemon based on the **RIP-2 (Routing Information Protocol v2)** specification.  
Implements distance-vector routing with support for **Split Horizon with Poison Reverse**, triggered updates, timeout handling, and more.

📄 *[Read the report](https://github.com/Jadeshi1998/RIPv2/blob/github/doc/Shunzhi%26Yumeng.pdf)* 


*👍 Yumeng Shi & Shunzhi Zhang*
---

## 🧪 How to Run
The each router need to open separately.
```bash
python3 main.py ../router/router1.txt
python3 main.py ../router/router2.txt
python3 main.py ../router/router3.txt
python3 main.py ../router/router4.txt
```

## 📊 Grade

**Overall Grade:** `83% / A-`

---

## 🔄 Tasks – Main Loop

- 🖨️ **Print Routing Table**  
  Print the current routing table to the console.

- 📤 **Periodic Routing Updates**  
  Periodically send the routing table to the socket for each input port with a variance of 30 seconds ± 5 seconds.
  - If any **first hops** in the table match the neighbor, set the metric to **infinite (16)**.  
  - This implements **Split Horizon with Poison Reverse**.

- ⏱️ **Timeout and Garbage Collection**  
  - Traverse the routing table and increment the age of each entry.
  - If `timeout`, then:
    - Set `metric = 16`
    - Set `garbage flag = TRUE`
  - If `garbage flag = TRUE` and `age > 6 × timeout`, delete the entry.

- 📥 **Read and Update from Sockets**  
  - Update the routing table if a **new destination** is received with **finite cost**.
  - For an existing destination:
    - If `current_metric > packet_metric + link_cost` → reset age and update route.
    - If route was received unchanged (same `dest`, `nexthop`, `cost`) → reset age.
    - If received with same `dest`, `nexthop`, and **metric = 16** → reset age, set cost to 16, and mark for garbage collection.

- 🚨 **Triggered Updates**  
  - Send only when **routes become invalid** (i.e., when `metric = 16`).
  - Triggered updates include **only affected routes**, not the full table.

- ✅ **Packet Validation**  
  Check that:
  - Destination and next-hop `routerID` are in `[1, 64000]` and are **not self**
  - Cost is **non-negative** and **clamped at 16**

---

The testing is running under this graph.
<img width="468" alt="Screenshot 2025-06-14 at 21 58 24" src="https://github.com/user-attachments/assets/6c2f6f00-4000-4a77-9e61-f5c35244440c" />



## ⚙️ Configuration
- 🧪 Create sample configuration files for router testing.
- ✅ Implement tests to validate the configuration file format and parsing.
