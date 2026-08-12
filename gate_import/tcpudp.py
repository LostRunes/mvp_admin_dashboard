import json
import os

TOPIC = "TCP, UDP and IP"

def opt(label, text, correct=False):
    return {"label": label, "text": text, "is_correct": correct}

def src(year, qnum, marks, set_=None):
    return {"year": year, "set": set_, "question_number": qnum, "marks": marks}

Q = []

def add(question_text, qtype, marks, difficulty, concepts, tags, is_numerical,
        formula_based, est_time, options, correct_answer_text, explanation, pyq_sources):
    Q.append({
        "question_text": question_text,
        "question_type": qtype,
        "marks": marks,
        "difficulty": difficulty,
        "topics": [TOPIC],
        "concepts": concepts,
        "tags": tags,
        "is_numerical": is_numerical,
        "formula_based": formula_based,
        "estimated_solve_time_seconds": est_time,
        "options": options,
        "correct_answer_text": correct_answer_text,
        "explanation": explanation,
        "pyq_sources": pyq_sources
    })

# 3.1
add(
"Which of the following assertions is FALSE about the Internet Protocol (IP)? (a) It is possible for a computer to have multiple IP addresses (b) IP packets from the same source to the same destination can take different routes in the network (c) IP ensures that a packet is farwarded if it is unable to reach its destination within a given number of hopes (d) The packet source cannot set the route of an outgoing packets; the route is determined only by the routing tables in the routers on the way",
"MCQ", 1, "medium", ["IP addressing", "Packet routing", "TTL"], ["ip protocol", "routing tables", "multihoming"],
False, False, 60,
[opt("A","It is possible for a computer to have multiple IP addresses"),
 opt("B","IP packets from the same source to the same destination can take different routes in the network"),
 opt("C","IP ensures that a packet is forwarded if it is unable to reach its destination within a given number of hops", True),
 opt("D","The packet source cannot set the route of an outgoing packet; the route is determined only by the routing tables in the routers on the way")],
None,
"Choice (a) is true since IP addresses are tied to network connections, not host computers, so a host with multiple network connections can have multiple IP addresses. Choice (b) is true because packet-switched routing can send packets from the same source-destination pair over different routes. Choice (c) is false: IP actually discards a packet if it cannot reach its destination within a given number of hops, it does not guarantee forwarding. Choice (d) is true since routing tables in intermediate routers, not the source, determine the path.",
[src(2003,"3.1",1)]
)

# 3.2
add(
"Which of the following functionalities must be implemented by a transport protocol over and above the network protocol? (a) Recovery from packet losses (b) Detection of duplicate packets (c) Packet delivery in the correct order (d) End to end connectivity",
"MCQ", 1, "easy", ["Transport layer", "Network layer"], ["transport protocol", "end-to-end connectivity", "TCP vs UDP"],
False, False, 45,
[opt("A","Recovery from packet losses"),
 opt("B","Detection of duplicate packets"),
 opt("C","Packet delivery in the correct order"),
 opt("D","End to end connectivity", True)],
None,
"A transport protocol provides end-to-end connectivity that shields upper layers from the details of the intervening network or networks. A transport protocol can be connection-oriented (TCP) or connectionless (UDP); the other listed functions are not mandatory for every transport protocol.",
[src(2003,"3.2",1)]
)

# 3.3
add(
"The subnet mask for a particular network is 255.255.31.0. Which of the following pairs of IP addresses could belong to this network? (a) 172.57.88.62 and 172.56.87.23.2 (b) 10.35.28.2 and 10.35.29.4 (c) 191.203.31.87 and 191.234.31.88 (d) 128.8.129.43 and 128.8.161.55",
"MCQ", 2, "medium", ["Subnetting", "Subnet mask"], ["subnet mask", "same network check", "binary AND"],
True, True, 120,
[opt("A","172.57.88.62 and 172.56.87.23.2"),
 opt("B","10.35.28.2 and 10.35.29.4"),
 opt("C","191.203.31.87 and 191.234.31.88"),
 opt("D","128.8.129.43 and 128.8.161.55", True)],
None,
"The subnet mask 255.255.31.0 in binary is 11111111.11111111.00011111.00000000. Performing the bitwise AND of each candidate address pair with this mask shows that only the pair 128.8.129.43 and 128.8.161.55 produce the same network address, so they belong to the same network.",
[src(2003,"3.3",2)]
)

# 3.4
add(
"Which of the following is NOT true with respect to a transparent bridge and a router? (a) Both bridge and router selectively forward data packets (b) A bridge uses IP addresses while a router uses MAC addresses (c) A bridge builds up its routing table by inspecting incoming packets (d) A router can connect between a LAN and a WAN",
"MCQ", 1, "easy", ["Bridges", "Routers", "OSI layers"], ["transparent bridge", "MAC address", "layer 2 vs layer 3"],
False, False, 45,
[opt("A","Both bridge and router selectively forward data packets"),
 opt("B","A bridge uses IP addresses while a router uses MAC addresses", True),
 opt("C","A bridge builds up its routing table by inspecting incoming packets"),
 opt("D","A router can connect between a LAN and a WAN")],
None,
"A bridge operates at the data link layer and therefore uses MAC addresses, while a router operates at the network layer and uses IP addresses. Choice (b) states the reverse of this, so it is the false statement.",
[src(2004,"3.4",1)]
)

# 3.5
add(
"Which one of the following statements is FALSE? (a) TCP guarantees a minimum communication rate (b) TCP ensures in-order delivery (c) TCP reacts to congestion by reducing sender window size (d) TCP employs retransmission to compensate for packet loss",
"MCQ", 1, "medium", ["TCP services", "Congestion control"], ["tcp guarantees", "in-order delivery", "retransmission"],
False, False, 60,
[opt("A","TCP guarantees a minimum communication rate", True),
 opt("B","TCP ensures in-order delivery"),
 opt("C","TCP reacts to congestion by reducing sender window size"),
 opt("D","TCP employs retransmission to compensate for packet loss")],
None,
"TCP does not guarantee a minimum transmission rate; a sending process is not permitted to transmit at any rate it wishes, and TCP congestion control may force the sender to use a low average rate. All other statements about TCP's behaviour are true.",
[src(2004,"3.5",1)]
)

# 3.6
add(
"A subnet has been assigned a subnet mask of 255.255.255.192. What is the maximum number of hosts that can belong to this subnet? (a) 14 (b) 30 (c) 62 (d) 126",
"MCQ", 1, "easy", ["Subnetting", "Host count calculation"], ["subnet mask", "host bits", "CIDR"],
True, True, 60,
[opt("A","14"), opt("B","30"), opt("C","62", True), opt("D","126")],
None,
"A mask of 255.255.255.192 leaves 6 host bits, giving 2^6 - 2 = 62 usable host addresses.",
[src(2004,"3.6",1)]
)

# 3.7
add(
"In TCP, a unique sequence number assigned to each (a) byte (b) word (c) segment (d) message",
"MCQ", 1, "easy", ["TCP sequence numbers"], ["tcp sequencing", "byte stream"],
False, False, 30,
[opt("A","byte", True), opt("B","word"), opt("C","segment"), opt("D","message")],
None,
"TCP sequences each byte in the connection's byte stream; the sequence number assigned to a segment indicates the sequence number of its first byte, and the next segment's sequence number equals the previous one plus the number of bytes sent.",
[src(2004,"3.7",1)]
)

# 3.8
add(
"In the TCP/IP protocol suite, which one of the following is NOT part of the IP header? (a) Fragment Offset (b) Source IP address (c) Destination IP address (d) Destination port number",
"MCQ", 2, "easy", ["IP header fields"], ["ip header", "port number", "fragment offset"],
False, False, 45,
[opt("A","Fragment Offset"), opt("B","Source IP address"), opt("C","Destination IP address"), opt("D","Destination port number", True)],
None,
"Port numbers belong to the transport layer, used for process-to-process delivery; the IP header (network layer) has nothing to do with port numbers.",
[src(2004,"3.8",2)]
)

# 3.9
add(
"A TCP message consisting of 2100 bytes is passed to IP for delivery across two networks. The first network can carry a maximum payload of 1200 bytes per frame and the second network can carry a maximum payload of 400 bytes per frame, excluding network overhead. Assume that IP overhead per packet is 20 bytes. What is the total IP overhead in the second network for this transmission? (a) 40 bytes (b) 80 bytes (c) 120 bytes (d) 160 bytes",
"MCQ", 2, "hard", ["IP fragmentation", "Overhead calculation"], ["ip fragmentation", "MTU", "payload splitting"],
True, True, 180,
[opt("A","40 bytes"), opt("B","80 bytes"), opt("C","120 bytes", True), opt("D","160 bytes")],
None,
"The 2100-byte payload is split in the first network into 1200 and 900 bytes (payload must be a multiple of 8 bytes, so 900 becomes 904 with padding). In the second network (max payload 400 bytes), the 1200-byte fragment splits into 400+400+400 bytes with 20-byte headers each, and the 900-byte fragment splits into 400+400+104 bytes with 20-byte headers each, giving 6 fragments total. Total IP overhead in the second network is 6 x 20 = 120 bytes.",
[src(2004,"3.9",2)]
)

# 3.10
add(
"Suppose that the maximum transmit window size for a TCP connection is 12000 bytes. Each packet consists of 2000 bytes. At some point of time, the connection is in slow-start phase with a current transmit window of 4000 bytes. Subsequently, the transmitter receives two acknowledgement. Assume that no packets are lost and there are no time-outs. What is the maximum possible value of the current transmit window? (a) 4000 bytes (b) 8000 bytes (c) 10000 bytes (d) 12000 bytes",
"MCQ", 2, "medium", ["TCP slow start", "Congestion window"], ["slow start", "congestion window growth", "MSS"],
True, True, 120,
[opt("A","4000 bytes"), opt("B","8000 bytes", True), opt("C","10000 bytes"), opt("D","12000 bytes")],
None,
"In slow start, the sender's window increases by one MSS (2000 bytes) for each ACK received. Starting from 4000 bytes with two ACKs received, the window grows to 4000 + 2x2000 = 8000 bytes.",
[src(2004,"3.10",2)]
)

# 3.11
add(
"The routing table of a router is shown below: Destination 128.75.43.0/Subnet Mask 255.255.255.0/Interface Eth0; Destination 128.75.43.128/Subnet Mask 255.255.255.128/Interface Eth1; Destination 192.12.17.5/Subnet Mask 255.255.255.255/Interface Eth3; default/Interface Eth2. On which interfaces will the router forward packets addressed to destinations 128.75.43.16 and 192.12.17.10 respectively? (a) Eth1 and Eth2 (b) Eth0 and Eth2 (c) Eth0 and Eth3 (d) Eth1 and Eth3",
"MCQ", 2, "medium", ["Longest prefix matching", "Routing tables"], ["routing table", "longest prefix match", "subnet mask"],
True, True, 120,
[opt("A","Eth1 and Eth2", True), opt("B","Eth0 and Eth2"), opt("C","Eth0 and Eth3"), opt("D","Eth1 and Eth3")],
None,
"Applying each subnet mask to 128.75.43.16 shows it matches 128.75.43.0 with mask 255.255.255.128 (Eth1) since this is the longest matching prefix. The address 192.12.17.10 does not match the /32 entry for 192.12.17.5, so it is forwarded via the default route Eth2.",
[src(2004,"3.11",2)]
)

# Common data 3.12/3.13 shared context
CD_1213 = "Common Data for Q.3.12 and Q.3.13: Consider three IP networks A, B and C. Host HA in network A sends messages each containing 180 bytes of application data to a host HC in network C. The TCP layer prefixes a 20 byte header to the message. This passes through an intermediate network B. The maximum packet size, including 20 byte IP header, in each network is: A: 1000 bytes, B: 100 bytes, C: 1000 bytes. The network A and B are connected through a 1 Mbps link, while B and C are connected by a 512 Kbps link (bps = bits per second)."

# 3.12
add(
CD_1213 + " Assuming that the packets are correctly delivered, how many bytes, including headers, are delivered to the IP layer at the destination for one application message, in the best case? Consider only data packets. (a) 200 (b) 220 (c) 240 (d) 260",
"MCQ", 2, "hard", ["IP fragmentation", "TCP/IP header overhead"], ["packet fragmentation", "network B bottleneck", "header overhead"],
True, True, 180,
[opt("A","200"), opt("B","220"), opt("C","240"), opt("D","260", True)],
None,
"Network A sends a 180+20=200 byte message. Network B allows a maximum packet size of 100 bytes including a 20-byte header, so the message must be split further with additional 20-byte headers per fragment. Working through the fragmentation across A, B and C, the total bytes delivered to the IP layer at the destination for this message, including all headers, is 100+100+60 = 260 bytes.",
[src(2004,"3.12",2)]
)

# 3.13
add(
CD_1213 + " What is the rate at which application data is transferred to host HC? Ignore errors, acknowledgments, and other overheads. (a) 325.5 Kbps (b) 354.5 Kbps (c) 409.6 Kbps (d) 512.0 Kbps",
"MCQ", 2, "hard", ["Effective throughput", "Header overhead ratio"], ["effective data rate", "link bandwidth", "overhead ratio"],
True, True, 180,
[opt("A","325.5 Kbps"), opt("B","354.5 Kbps", True), opt("C","409.6 Kbps"), opt("D","512.0 Kbps")],
None,
"The total bytes delivered to network C (including TCP and IP headers) is 260 bytes, of which 180 bytes is effective application data. The effective throughput is therefore (180/260) x 512 Kbps = 354.46 Kbps, using the slower 512 Kbps link between B and C.",
[src(2004,"3.13",2)]
)

# 3.14
add(
"Packets of the same session may be routed through different paths in (a) TCP, but not UDP (b) TCP and UDP (c) UDP, but not TCP (d) Neither UDP, nor TCP",
"MCQ", 1, "easy", ["Packet switching", "Transport protocols"], ["packet routing", "connectionless routing", "session packets"],
False, False, 45,
[opt("A","TCP, but not UDP"), opt("B","TCP and UDP", True), opt("C","UDP, but not TCP"), opt("D","Neither UDP, nor TCP")],
None,
"Routing of packets from source to destination is a network layer function that depends on the routing algorithm, independent of whether the transport protocol above is TCP or UDP, so packets of both can take different paths.",
[src(2005,"3.14",1)]
)

# 3.15
add(
"The address resolution protocol (ARP) is used for (a) Finding the IP address from the DNS (b) Finding the IP address of the default gateway (c) Finding the IP address that corresponds to a MAC address (d) Finding the MAC address that corresponds to an IP address",
"MCQ", 1, "easy", ["ARP"], ["address resolution protocol", "MAC address", "IP to MAC mapping"],
False, False, 30,
[opt("A","Finding the IP address from the DNS"), opt("B","Finding the IP address of the default gateway"), opt("C","Finding the IP address that corresponds to a MAC address"), opt("D","Finding the MAC address that corresponds to an IP address", True)],
None,
"ARP allows a host to find the MAC (physical) address of a target host on the same physical network, given only the target's IP address.",
[src(2005,"3.15",1)]
)

# 3.16
add(
"An organization has a class B network and wishes to form subnets for 64 departments. The subnet mask would be (a) 255.255.0.0 (b) 255.255.64.0 (c) 255.255.128.0 (d) 255.255.252.0",
"MCQ", 1, "medium", ["Subnetting", "Class B network"], ["class B subnetting", "subnet mask calculation"],
True, True, 90,
[opt("A","255.255.0.0"), opt("B","255.255.64.0"), opt("C","255.255.128.0"), opt("D","255.255.252.0", True)],
None,
"To form 64 = 2^6 subnets from a class B network's third octet, 6 bits must be borrowed for the subnet ID, giving a mask of 255.255.252.0.",
[src(2005,"3.16",1)]
)

# 3.17
add(
"In a packet switching network, packets are routed from source to destination along a single path having two intermediate nodes. If the message size is 24 bytes and each packet contains a header of 3 bytes, then the optimum packet size is (a) 4 (b) 6 (c) 7 (d) 9",
"MCQ", 2, "medium", ["Packet switching", "Optimum packet size"], ["packet size optimization", "header overhead", "store and forward"],
True, True, 150,
[opt("A","4"), opt("B","6"), opt("C","7"), opt("D","9", True)],
None,
"With a 3-byte header per packet and message size 24 bytes, checking each candidate packet size for the number of required packets and resulting transmission overhead shows that a packet size of 9 bytes (yielding a data portion of 6 bytes per packet, needing 4 packets) minimizes transmission time among the options.",
[src(2005,"3.17",2)]
)

# 3.18
add(
"Suppose the round trip propagation delay for a 10 Mbps Ethernet having 48-bit jamming signal is 46.4 microseconds. The minimum frame size is: (a) 94 (b) 416 (c) 464 (d) 512",
"MCQ", 2, "medium", ["Ethernet", "Minimum frame size"], ["CSMA/CD", "round trip delay", "collision detection"],
True, True, 120,
[opt("A","94"), opt("B","416"), opt("C","464", True), opt("D","512")],
None,
"The minimum frame size must be at least the round trip propagation delay multiplied by the bandwidth: 46.4 microseconds x 10 Mbps = 464 bits.",
[src(2005,"3.18",2)]
)

# 3.19
add(
"On a TCP connection, current congestion window size is Congestion Window = 4 KB. The window size advertised by the receiver is Advertise Window = 6 KB. The last byte sent by the sender is LastByteSent = 10240 and the last byte acknowledged by the receiver is LastByteAcked = 8192. The current window size at the sender is (a) 2048 bytes (b) 4096 bytes (c) 6144 bytes (d) 8192 bytes",
"MCQ", 2, "medium", ["TCP flow control", "Congestion window"], ["congestion window", "advertised window", "sender window calculation"],
True, True, 120,
[opt("A","2048 bytes"), opt("B","4096 bytes", True), opt("C","6144 bytes"), opt("D","8192 bytes")],
None,
"The current sender window size is the minimum of the congestion window and the advertised window: min(4 KB, 6 KB) = 4 KB = 4096 bytes.",
[src(2005,"3.19",2)]
)

# 3.20
add(
"In a communication network, a packet of length L bits takes link L1 with a probability of p1 or link L2 with probability of p2. Link L1 and L2 have bit error probability of b1 and b2 respectively. The probability that the packet will be received without error via either L1 or L2 is (a) (1-b1)^L p1 + (1-b2)^L p2 (b) [1-(b1+b2)^L]p1 p2 (c) (1-b1)^L (1-b2)^L p1 p2 (d) 1 - (b1^L p1 + b2^L p2)",
"MCQ", 2, "hard", ["Probability of transmission error", "Bit error probability"], ["error probability", "bit error rate", "conditional probability"],
True, True, 150,
[opt("A","(1-b1)^L p1 + (1-b2)^L p2", True),
 opt("B","[1-(b1+b2)^L]p1 p2"),
 opt("C","(1-b1)^L (1-b2)^L p1 p2"),
 opt("D","1 - (b1^L p1 + b2^L p2)")],
None,
"The required probability is the probability of choosing L1 times the probability of no error on L1 for all L bits, plus the corresponding term for L2: p1(1-b1)^L + p2(1-b2)^L.",
[src(2005,"3.20",2)]
)

# 3.21
add(
"A company has a class C network address of 204.204.204.0. It wishes to have three subnets, one with 100 hosts and two with 50 hosts each. Which one of the following options represents a feasible set of subnet address/subnet mask pairs? (a) 204.204.204.128/255.255.255.192, 204.204.204.0/255.255.255.128, 204.204.204.64/255.255.255.128 (b) 204.204.204.0/255.255.255.192, 204.204.204.192/255.255.255.128, 204.204.204.64/255.255.255.128 (c) 204.204.204.128/255.255.255.128, 204.204.204.192/255.255.255.192, 204.204.204.224/255.255.255.192 (d) 204.204.204.128/255.255.255.128, 204.204.204.64/255.255.255.192, 204.204.204.0/255.255.255.192",
"MCQ", 2, "hard", ["Variable length subnetting", "Class C network"], ["VLSM", "class C subnetting", "subnet address calculation"],
True, True, 180,
[opt("A","204.204.204.128/255.255.255.192, 204.204.204.0/255.255.255.128, 204.204.204.64/255.255.255.128"),
 opt("B","204.204.204.0/255.255.255.192, 204.204.204.192/255.255.255.128, 204.204.204.64/255.255.255.128"),
 opt("C","204.204.204.128/255.255.255.128, 204.204.204.192/255.255.255.192, 204.204.204.224/255.255.255.192"),
 opt("D","204.204.204.128/255.255.255.128, 204.204.204.64/255.255.255.192, 204.204.204.0/255.255.255.192", True)],
None,
"For the 100-host subnet, 7 host bits are needed (mask 255.255.255.128, subnet address 204.204.204.128). The remaining address space is split for the two 50-host subnets requiring 6 host bits each (mask 255.255.255.192), giving subnet addresses 204.204.204.64 and 204.204.204.0.",
[src(2005,"3.21",2)]
)

# 3.22
add(
"Which of the following statements is TRUE? (a) Both Ethernet frame and IP packet include checksum fields (b) Ethernet frame includes a checksum field and IP packet includes a CRC field (c) Ethernet frame includes a CRC field and IP packet includes a checksum field (d) Both Ethernet frame and IP packet include CRC fields",
"MCQ", 1, "medium", ["Error detection", "Ethernet frame", "IP header"], ["CRC", "checksum", "error detection fields"],
False, False, 60,
[opt("A","Both Ethernet frame and IP packet include checksum fields"),
 opt("B","Ethernet frame includes a checksum field and IP packet includes a CRC field"),
 opt("C","Ethernet frame includes a CRC field and IP packet includes a checksum field", True),
 opt("D","Both Ethernet frame and IP packet include CRC fields")],
None,
"Ethernet uses a Cyclic Redundancy Check (CRC) to detect transmission errors, while IP and most higher layer protocols of the Internet suite use a checksum algorithm to validate packet integrity.",
[src(2006,"3.22",1)]
)

# 3.23
add(
"For which one of the following reasons does Internet Protocol (IP) use the time-to-live (TTL) field in the IP datagram header? (a) Ensure packets reach destination within that time (b) Discard packets that reach later than that time (c) Prevent packets from looping indefinitely (d) Limit the time for which a packet gets queued in intermediate routers",
"MCQ", 1, "easy", ["TTL field", "IP header"], ["time to live", "packet looping", "IP header field"],
False, False, 45,
[opt("A","Ensure packets reach destination within that time"),
 opt("B","Discard packets that reach later than that time"),
 opt("C","Prevent packets from looping indefinitely", True),
 opt("D","Limit the time for which a packet gets queued in intermediate routers")],
None,
"TTL limits the lifespan of a packet in the network; once the prescribed hop count or time span has elapsed, the packet is discarded, which prevents it from circulating indefinitely due to routing loops.",
[src(2006,"3.23",1)]
)

# 3.24
add(
"A router uses the following routing table: Destination 144.16.0.0/Mask 255.255.0.0/Interface eth0; 144.16.64.0/255.255.224.0/eth1; 144.16.68.0/255.255.255.0/eth2; 144.16.68.64/255.255.255.224/eth3. A packet bearing a destination address 144.16.68.117 arrives at the router. On which interface will it be forwarded? (a) eth0 (b) eth1 (c) eth2 (d) eth3",
"MCQ", 2, "medium", ["Longest prefix matching", "Routing tables"], ["routing table lookup", "longest prefix match", "subnet mask"],
True, True, 120,
[opt("A","eth0"), opt("B","eth1"), opt("C","eth2", True), opt("D","eth3")],
None,
"Matching the destination address against each routing table entry, the route with the longest matching mask (255.255.255.0, matching 144.16.68.0) is used, so the packet is forwarded to eth2.",
[src(2006,"3.24",2)]
)

# 3.25
add(
"Suppose that it takes 1 unit of time to transmit a packet (of fixed size) on a communication link. The link layer uses a window flow control protocol with a window size of N packets. Each packet causes an ack or a nak to be generated by the receiver, and ack/nak transmission times are negligible. Further, the round trip time on the link is equal to N units. Consider time i > N. If only acks have been received till time i (no naks), then the throughput evaluated at the transmitter at time i (in packets per unit time) is (a) (1-N)/i (b) i/(N+i) (c) 1 (d) 1 - e^(i/N)",
"MCQ", 2, "hard", ["Window flow control", "Throughput calculation"], ["sliding window", "throughput", "round trip time"],
True, True, 150,
[opt("A","(1-N)/i", True), opt("B","i/(N+i)"), opt("C","1"), opt("D","1 - e^(i/N)")],
None,
"Since acks arrive continuously within the round trip time N, the number of acks received by time i is (i - N). Throughput evaluated at time i is therefore (i-N)/i, which is equivalent to (1-N)/i in the form given.",
[src(2006,"3.25",2)]
)

# 3.26
add(
"A link of capacity 100 Mbps is carrying traffic from a number of sources. Each source generates an on-off traffic stream; when the source is on, the rate of traffic is 10 Mbps, and when the source is off, the rate of traffic is zero. The duty cycle, which is the ratio of on-time to off-time, is 1:2. When there is no buffer at the link, the minimum number of sources that can be multiplexed on the link so that link capacity is not wasted and no data loss occurs is S1. Assuming that all sources are synchronized and that the link is provided with a large buffer, the maximum number of sources that can be multiplexed so that no data loss occurs is S2. The values of S1 and S2 are, respectively, (a) 10 and 30 (b) 12 and 25 (c) 5 and 33 (d) 15 and 22",
"MCQ", 2, "hard", ["Traffic multiplexing", "On-off traffic model"], ["duty cycle", "multiplexing", "buffered links"],
True, True, 180,
[opt("A","10 and 30", True), opt("B","12 and 25"), opt("C","5 and 33"), opt("D","15 and 22")],
None,
"For the unbuffered (no data loss, no waste) case, capacity is fully used exactly when 10 sources are each on simultaneously without waste: 10 Mbps x 10 = 100 Mbps, giving S1 = 10. With a large buffer and a 1:2 duty cycle, the expected long-term bandwidth usage per source is (1/3) x 10 Mbps, so the maximum number of sources without data loss on average is S2 = 30.",
[src(2006,"3.26",2)]
)

# 3.27
add(
"A program on machine X attempts to open a UDP connection to port 5376 on a machine Y, and a TCP connection to port 8632 on machine Z. However, there are no applications listening at the corresponding ports on Y and Z. An ICMP Port Unreachable error will be generated by (a) Y but not Z (b) Z but not Y (c) Neither Y nor Z (d) Both Y and Z",
"MCQ", 2, "medium", ["ICMP", "Port unreachable error"], ["ICMP error", "closed port behaviour", "UDP vs TCP response"],
False, False, 90,
[opt("A","Y but not Z"), opt("B","Z but not Y"), opt("C","Neither Y nor Z", True), opt("D","Both Y and Z")],
None,
"The book's answer key marks this as (c). Its explanation notes that whether an ICMP port unreachable error is generated depends on how the host reacts to a closed port for each transport protocol, independent of the transport layer protocol used.",
[src(2006,"3.27",2)]
)

# 3.28
add(
"A subnetted Class B network has the following broadcast address: 144.16.95.255. Its subnet mask (a) is necessarily 255.255.224.0 (b) is necessarily 255.255.240.0 (c) is necessarily 255.255.248.0 (d) could be any one of 255.255.224.0, 255.255.240.0, 255.255.248.0",
"MCQ", 2, "hard", ["Broadcast address", "Subnet mask"], ["broadcast address", "subnet mask ambiguity", "class B network"],
True, True, 150,
[opt("A","is necessarily 255.255.224.0"),
 opt("B","is necessarily 255.255.240.0"),
 opt("C","is necessarily 255.255.248.0"),
 opt("D","could be any one of 255.255.224.0, 255.255.240.0, 255.255.248.0", True)],
None,
"All host bits of a broadcast address are 1. Checking 144.16.95.255 in binary against masks with different numbers of borrowed subnet bits shows that all host bits remain 1 for subnet masks 255.255.224.0, 255.255.240.0, and 255.255.248.0, so any of these could be the actual mask.",
[src(2006,"3.28",2)]
)

# 3.29
add(
"Two computers C1 and C2 are configured as follows. C1 has IP address 203.197.2.53 and netmask 255.255.128.0. C2 has IP address 203.197.75.201 and netmask 255.255.192.0. Which one of the following statements is true? (a) C1 and C2 both assume they are on the same network (b) C2 assumes C1 is on same network, but C1 assumes C2 is on a different network (c) C1 assumes C2 is on same network, but C2 assumes C1 is on a different network (d) C1 and C2 both assume they are on different networks",
"MCQ", 2, "hard", ["Netmask mismatch", "Network address calculation"], ["netmask mismatch", "network address", "asymmetric subnetting"],
True, True, 150,
[opt("A","C1 and C2 both assume they are on the same network"),
 opt("B","C2 assumes C1 is on same network, but C1 assumes C2 is on a different network"),
 opt("C","C1 assumes C2 is on same network, but C2 assumes C1 is on a different network", True),
 opt("D","C1 and C2 both assume they are on different networks")],
None,
"Applying C1's netmask (255.255.128.0) to both IP addresses gives the same network address, so C1 assumes C2 is on the same network. Applying C2's netmask (255.255.192.0) to both addresses gives different network addresses, so C2 assumes C1 is on a different network.",
[src(2006,"3.29",2)]
)

# 3.30
add(
"Consider the following statements about the timeout value used in TCP. (i) The timeout value is set to the RTT (Round Trip Time) measured during TCP connection establishment for the entire duration of the connection. (ii) Appropriate RTT estimation algorithm is used to set the timeout value of a TCP connection. (iii) Timeout value is set to twice the propagation delay from the sender to the receiver. Which of the following choices hold? (a) (i) is false, but (ii) and (iii) are true (b) (i) and (iii) are false, but (ii) is true (c) (i) and (ii) are false, but (iii) is true (d) (i), (ii) and (iii) are false",
"MCQ", 1, "medium", ["TCP timeout", "RTT estimation"], ["retransmission timeout", "RTT estimation algorithm"],
False, False, 90,
[opt("A","(i) is false, but (ii) and (iii) are true"),
 opt("B","(i) and (iii) are false, but (ii) is true", True),
 opt("C","(i) and (ii) are false, but (iii) is true"),
 opt("D","(i), (ii) and (iii) are false")],
None,
"TCP uses an appropriate RTT estimation algorithm to dynamically set the timeout value throughout the connection, not a fixed value from connection establishment or a fixed multiple of propagation delay, so only statement (ii) is true.",
[src(2007,"3.30",1)]
)

# 3.31
add(
"Consider a TCP connection in a state where there are no outstanding ACKs. The sender sends two segments back to back. The sequence numbers of the first and second segments are 230 and 290 respectively. The first segment was lost, but the second segment was received correctly by the receiver. Let X be the amount of data carried in the first segment (in bytes), and Y be the ACK number sent by the receiver. The values of X and Y (in that order) are (a) 60 and 290 (b) 230 and 291 (c) 60 and 231 (d) 60 and 230",
"MCQ", 1, "medium", ["TCP sequence numbers", "Acknowledgement number"], ["sequence number", "ack number", "cumulative acknowledgement"],
True, True, 120,
[opt("A","60 and 290"), opt("B","230 and 291"), opt("C","60 and 231"), opt("D","60 and 230", True)],
None,
"The first segment carries X = 290 - 230 = 60 bytes of data. Since the first segment was lost, the receiver has only received the second (out-of-order) segment, so it re-acknowledges the expected next byte, which is the start of the first segment, giving ACK number Y = 230.",
[src(2007,"3.31",1)]
)

# 3.32
add(
"The address of a class B host is to be split into subnets with a 6-bit subnet number. What is the maximum number of subnets and the maximum number of hosts in each subnet? (a) 62 subnets and 262142 hosts (b) 64 subnets and 262142 hosts (c) 62 subnets and 1022 hosts (d) 64 subnets and 1024 hosts",
"MCQ", 2, "medium", ["Class B subnetting", "Subnet and host count"], ["subnet count", "host count", "class B address"],
True, True, 120,
[opt("A","62 subnets and 262142 hosts"), opt("B","64 subnets and 262142 hosts"), opt("C","62 subnets and 1022 hosts", True), opt("D","64 subnets and 1024 hosts")],
None,
"A class B address has 16 host bits. With 6 bits used for subnetting, the maximum number of subnets is 2^6 - 2 = 62, and the remaining 10 host bits give a maximum of 2^10 - 2 = 1022 hosts per subnet.",
[src(2007,"3.32",2)]
)

# 3.33
add(
"What is the maximum size of data that the application layer can pass on to the TCP layer below? (a) Any size (b) 2^16 bytes - size of TCP header (c) 2^16 bytes (d) 1500 bytes",
"MCQ", 1, "easy", ["TCP segmentation"], ["application data size", "TCP segmentation limits"],
False, False, 45,
[opt("A","Any size", True), opt("B","2^16 bytes - size of TCP header"), opt("C","2^16 bytes"), opt("D","1500 bytes")],
None,
"There is no maximum limit on the amount of data the application layer can pass to TCP; TCP itself is responsible for segmenting the byte stream into appropriately sized segments.",
[src(2008,"3.33",1)]
)

# 3.34
add(
"Which of the following system calls results in the sending of SYN packets? (a) socket (b) bind (c) listen (d) connect",
"MCQ", 1, "easy", ["Socket API", "TCP connection setup"], ["socket programming", "SYN packet", "connect() call"],
False, False, 45,
[opt("A","socket"), opt("B","bind"), opt("C","listen"), opt("D","connect", True)],
None,
"The connect() system call on the client side initiates the TCP three-way handshake by sending a SYN packet to synchronize with the server.",
[src(2008,"3.34",1)]
)

# 3.35
add(
"Which of the following statements are TRUE? S1: TCP handles both congestion and flow control S2: UDP handles congestion but not flow control S3: Fast retransmit deals with congestion but not flow control S4: Slow start mechanism deals with both congestion and flow control (a) S1, S2 and S3 only (b) S1 and S3 only (c) S3 and S4 only (d) S1, S3 and S4 only",
"MCQ", 2, "medium", ["TCP congestion control", "Flow control"], ["congestion control", "flow control", "fast retransmit", "slow start"],
False, False, 120,
[opt("A","S1, S2 and S3 only"), opt("B","S1 and S3 only", True), opt("C","S3 and S4 only"), opt("D","S1, S3 and S4 only")],
None,
"TCP performs both congestion and flow control (S1 true). UDP has neither congestion nor flow control (S2 false). Fast retransmit and fast recovery are congestion control mechanisms only (S3 true). Slow start uses both the congestion window and the advertised window, but is primarily a congestion control mechanism combined with the receiver's flow-control window, making S4 false in this context.",
[src(2008,"3.35",2)]
)

# 3.36
add(
"The three way handshake for TCP connection establishment is shown below: Client sends SYN to Server; Server responds with SYN+ACK; Client sends ACK to Server. Which of the following statements are TRUE? S1: Loss of SYN + ACK from the server will not establish a connection S2: Loss of ACK from the client cannot establish the connection S3: The server moves LISTEN -> SYN_RCVD -> SYN_SENT -> ESTABLISHED in the state machine on no packet loss S4: The server moves LISTEN -> SYN_RCVD -> ESTABLISHED in the state machine on no packet loss (a) S2 and S3 only (b) S1 and S4 only (c) S1 and S3 only (d) S2 and S4 only",
"MCQ", 2, "medium", ["TCP three-way handshake", "TCP state machine"], ["three way handshake", "TCP states", "SYN_RCVD", "ESTABLISHED"],
False, False, 120,
[opt("A","S2 and S3 only"), opt("B","S1 and S4 only", True), opt("C","S1 and S3 only"), opt("D","S2 and S4 only")],
None,
"The server starts in LISTEN, moves to SYN_RCVD on receiving SYN, sends SYN+ACK, and moves to ESTABLISHED once the client's ACK is received (S4 true, S3 false). If the SYN+ACK from the server is lost, the client never sends its ACK, so the connection is not established (S1 true). If the client's ACK is lost, the connection can still eventually be established through retransmission, so S2 is false.",
[src(2008,"3.36",2)]
)

# 3.37
add(
"Host X has IP address 192.168.1.97 and is connected through two routers R1 and R2 to another host Y with IP address 192.168.1.80. Router R1 has IP addresses 192.168.1.135 and 192.168.1.110. R2 has IP addresses 192.168.1.67 and 192.168.1.155. The netmask used in the network is 255.255.255.224. Given the information above, how many distinct subnets are guaranteed to already exist in the network? (a) 1 (b) 2 (c) 3 (d) 6",
"MCQ", 2, "hard", ["Subnet identification", "Multi-router topology"], ["subnet identification", "netmask application", "multi-homed routers"],
True, True, 150,
[opt("A","1"), opt("B","2"), opt("C","3", True), opt("D","6")],
None,
"Applying the netmask 255.255.255.224 to each of the six given IP addresses yields three distinct subnet identifiers, so at least 3 distinct subnets are guaranteed to exist.",
[src(2008,"3.37",2)]
)

# 3.38
add(
"Which IP address should X configure its gateway as? (Continuing the scenario of host X, routers R1, R2, and host Y with netmask 255.255.255.224) (a) 192.168.1.67 (b) 192.168.1.110 (c) 192.168.1.135 (d) 192.168.1.155",
"MCQ", 2, "medium", ["Default gateway configuration", "Same subnet check"], ["gateway configuration", "same subnet", "netmask"],
True, True, 120,
[opt("A","192.168.1.67"), opt("B","192.168.1.110", True), opt("C","192.168.1.135"), opt("D","192.168.1.155")],
None,
"For host X to reach its gateway directly, the gateway's IP address must lie in the same subnet as X under the given netmask. Checking each router interface address against X's subnet shows that 192.168.1.110 is the interface on R1 sharing X's subnet.",
[src(2008,"3.38",2)]
)

# 3.39
add(
"In the slow start phase of the TCP congesting control algorithm, the size of the congestion window (a) Does not increase (b) Increases linearly (c) Increases quadratically (d) Increases exponentially",
"MCQ", 2, "easy", ["TCP slow start"], ["slow start", "congestion window growth", "exponential growth"],
False, False, 45,
[opt("A","Does not increase"), opt("B","Increases linearly"), opt("C","Increases quadratically"), opt("D","Increases exponentially", True)],
None,
"In slow start, the congestion window increases by one segment for every ACK received, which results in approximately doubling the window every round trip time, i.e. exponential growth.",
[src(2008,"3.39",2)]
)

# 3.40
add(
"If a class B network on the Internet has a subnet mask of 255.255.248.0, what is the maximum number of hosts per subnet? (a) 1022 (b) 1023 (c) 2046 (d) 2047",
"MCQ", 2, "medium", ["Class B subnetting", "Host count"], ["subnet mask", "host bits", "class B network"],
True, True, 90,
[opt("A","1022"), opt("B","1023"), opt("C","2046", True), opt("D","2047")],
None,
"The mask 255.255.248.0 leaves 11 host bits, giving a maximum of 2^11 - 2 = 2046 usable host addresses per subnet.",
[src(2008,"3.40",2)]
)

# 3.41
add(
"A client process P needs to make a TCP connection to a server process S. Consider the following situation: the server process S executes a socket(), a bind() and a listen() system call in that order, following which it is preempted. Subsequently, the client process P executes a socket() system call followed by connect() system call to connect to the server process S. The server process has not executed any accept() system call. Which one of the following events could take place? (a) connect() system call returns successfully (b) connect() system call blocks (c) connect() system call returns an error (d) connect() system call results in a core dump",
"MCQ", 2, "medium", ["Socket API", "TCP connect() semantics"], ["socket programming", "listen queue", "TCP handshake without accept"],
False, False, 90,
[opt("A","connect() system call returns successfully"),
 opt("B","connect() system call blocks"),
 opt("C","connect() system call returns an error"),
 opt("D","connect() system call results in a core dump")],
None,
"Since the server has already called listen(), the OS-level connection queue can accept and complete the three-way handshake even before an explicit accept() call, so the client's connect() can return successfully.",
[src(2008,"3.41",2)]
)

# 3.42
add(
"While opening a TCP connection, the initial sequence number is to be derived using a time-of-day (ToD) clock that keeps running even when the host is down. The low order 32 bits of the counter of the ToD clock is to be used for the initial sequence numbers. The clock counter increments once per millisecond. The maximum packet lifetime is given to be 64s. Which one of the choices given below is closest to the minimum permissible rate at which sequence numbers used for packets of a connection can increase? (a) 0.015/s (b) 0.064/s (c) 0.135/s (d) 0.327/s",
"MCQ", 2, "hard", ["Initial sequence number", "Clock-driven ISN"], ["ISN generation", "sequence number wraparound", "maximum packet lifetime"],
True, True, 150,
[opt("A","0.015/s"), opt("B","0.064/s", True), opt("C","0.135/s"), opt("D","0.327/s")],
None,
"With the maximum packet lifetime of 64 seconds, the clock counter must not repeat the same sequence value within that time. Since the counter increments once per millisecond, the minimum permissible rate of increase is 1/64 = 0.064 per second.",
[src(2009,"3.42",2)]
)

# 3.43
add(
"One of the header fields in an IP datagram is the Time-to-Live (TTL) field. Which of the following statements best explains the need for this field? (a) It can be used to prioritize packets (b) It can be used to reduce delays (c) It can be used to optimize throughput (d) It can be used to prevent packet looping",
"MCQ", 1, "easy", ["TTL field"], ["time to live", "packet looping", "IP header"],
False, False, 45,
[opt("A","It can be used to prioritize packets"),
 opt("B","It can be used to reduce delays"),
 opt("C","It can be used to optimize throughput"),
 opt("D","It can be used to prevent packet looping", True)],
None,
"TTL limits the lifespan of a data packet in a network. Once the prescribed hop count or timespan elapses, the packet is discarded, preventing it from looping indefinitely.",
[src(2010,"3.43",1)]
)

# 3.44
add(
"Suppose computers A and B have IP addresses 10.105.1.113 and 10.105.1.91 respectively and they both use the same netmask N. Which of the values of N given below should not be used if A and B should belong to the same network? (a) 255.255.255.0 (b) 255.255.255.128 (c) 255.255.255.192 (d) 255.255.255.224",
"MCQ", 2, "hard", ["Netmask selection", "Same network verification"], ["netmask", "network address matching", "binary AND"],
True, True, 150,
[opt("A","255.255.255.0"), opt("B","255.255.255.128"), opt("C","255.255.255.192"), opt("D","255.255.255.224", True)],
None,
"Applying each candidate netmask to the two IP addresses shows that with mask 255.255.255.224, the network portions of the two addresses differ, so this mask would place A and B on different networks and should not be used.",
[src(2010,"3.44",2)]
)

# 3.45
add(
"A layer-4 firewall (a device that can look at all protocol headers up to the transport layer) CANNOT (a) block entire HTTP traffic during 9:00 pm and 5:00 am (b) block all ICMP traffic (c) stop incoming traffic from a specific IP address but allow outgoing traffic to the same IP address (d) block TCP traffic from a specific user on a multi-user system during 9:00 pm and 5:00 am",
"MCQ", 1, "medium", ["Firewalls", "OSI layers"], ["layer 4 firewall", "packet filtering", "user-level blocking"],
False, False, 90,
[opt("A","block entire HTTP traffic during 9:00 pm and 5:00 am", True),
 opt("B","block all ICMP traffic"),
 opt("C","stop incoming traffic from a specific IP address but allow outgoing traffic to the same IP address"),
 opt("D","block TCP traffic from a specific user on a multi-user system during 9:00 pm and 5:00 am")],
None,
"To block traffic from a specific user requires application-layer information, which a layer-4 firewall cannot inspect; it can, however, block HTTP traffic by port, since HTTP typically uses a well-known port at the transport layer.",
[src(2011,"3.45",1)]
)

# 3.46
add(
"Which of the following transport layer protocols is used to support electronic mail? (a) SMTP (b) IP (c) TCP (d) UDP",
"MCQ", 1, "easy", ["Transport protocols for applications"], ["SMTP", "TCP", "email protocol"],
False, False, 30,
[opt("A","SMTP"), opt("B","IP"), opt("C","TCP", True), opt("D","UDP")],
None,
"UDP and TCP are transport layer protocols, and TCP is the one used to support electronic mail (SMTP runs over TCP).",
[src(2012,"3.46",1)]
)

# 3.47
add(
"In the IPv4 addressing format, the number of networks allowed under Class C addresses is (a) 2^14 (b) 2^7 (c) 2^21 (d) 2^24",
"MCQ", 1, "easy", ["IPv4 address classes"], ["class C addressing", "network bits", "host bits"],
True, True, 45,
[opt("A","2^14"), opt("B","2^7"), opt("C","2^21", True), opt("D","2^24")],
None,
"A Class C address has 24 bits for the network ID and 8 bits for the host ID; the first 3 bits of the network ID are fixed (110), leaving 21 bits to represent 2^21 networks.",
[src(2012,"3.47",1)]
)

# 3.48
add(
"An Internet Service Provider (ISP) has the following chunk of CIDR-based IP addresses available with it: 245.248.128.0/20. The ISP wants to give half of this chunk of addresses to Organization A, and a quarter to Organization B, while retaining the remaining with itself. Which of the following is a valid allocation of addresses to A and B? (a) 245.248.136.0/21 and 245.248.128.0/22 (b) 245.248.128.0/21 and 245.248.128.0/22 (c) 245.248.132.0/22 and 245.248.132.0/21 (d) 245.248.136.0/24 and 245.248.132.0/21",
"MCQ", 2, "hard", ["CIDR", "Address block allocation"], ["CIDR allocation", "address space splitting", "subnetting"],
True, True, 180,
[opt("A","245.248.136.0/21 and 245.248.128.0/22", True),
 opt("B","245.248.128.0/21 and 245.248.128.0/22"),
 opt("C","245.248.132.0/22 and 245.248.132.0/21"),
 opt("D","245.248.136.0/24 and 245.248.132.0/21")],
None,
"The /20 block has 2^12 addresses. Half (a /21 block) should go to Organization A, and a quarter (a /22 block) to Organization B, without overlapping address ranges. Checking the options shows that 245.248.136.0/21 for A and 245.248.128.0/22 for B is a valid, non-overlapping allocation.",
[src(2012,"3.48",2)]
)

# 3.49
add(
"Consider an instance of TCP's Additive Increase Multiplicative Decrease (AIMD) algorithm where the window size at the start of the slow start phase is 2 MSS and the threshold at the start of the first transmission is 8 MSS. Assume that a time-out occurs during the fifth transmission. Find the congestion window size at the end of the tenth transmission. (a) 8 MSS (b) 14 MSS (c) 7 MSS (d) 12 MSS",
"MCQ", 2, "hard", ["TCP AIMD", "Slow start and congestion avoidance"], ["AIMD", "slow start", "congestion avoidance", "timeout"],
True, True, 180,
[opt("A","8 MSS"), opt("B","14 MSS"), opt("C","7 MSS", True), opt("D","12 MSS")],
None,
"Starting at 2 MSS with threshold 8 MSS, the window doubles each round in slow start (2,4,8) then increases linearly (9,10) until a timeout occurs during the 5th transmission. After timeout, the new threshold becomes half the current window (5 MSS), the window resets to 2 MSS and slow start resumes (2,4,5) before again increasing linearly (6,7), giving 7 MSS at the end of the tenth transmission.",
[src(2012,"3.49",2)]
)

# 3.50
add(
"In an IPv4 datagram, the M bit is 0, the value of HLEN is 10, the value of total length is 400 and the fragment offset value is 300. The position of the datagram, the sequence numbers of the first and the last bytes of the payload, respectively are (a) Last fragment, 2400 and 2789 (b) First fragment, 2400 and 2759 (c) Last fragment, 2400 and 2759 (d) Middle fragment, 300 and 689",
"MCQ", 2, "hard", ["IPv4 fragmentation", "Fragment offset calculation"], ["fragment offset", "HLEN", "MF bit", "last fragment"],
True, True, 150,
[opt("A","Last fragment, 2400 and 2789"), opt("B","First fragment, 2400 and 2759"), opt("C","Last fragment, 2400 and 2759", True), opt("D","Middle fragment, 300 and 689")],
None,
"M=0 means this is the last fragment. HLEN=10 means header length = 40 bytes, so payload = 400-40 = 360 bytes. Fragment offset 300 x 8 = 2400 gives the sequence number of the first payload byte; the last byte's sequence number is 2400+360-1 = 2759.",
[src(2013,"3.50",2)]
)

# 3.51
add(
"Let the size of congestion window of a TCP connection be 32 KB when a timeout occurs. The round trip time of the connection is 100 msec and the maximum segment size used is 2 KB. The time taken (in msec) by the TCP connection to get back to 32 KB congestion window is ______.",
"NAT", 2, "hard", ["TCP slow start after timeout", "Congestion window recovery"], ["timeout recovery", "slow start", "congestion avoidance"],
True, True, 180, [],
"1100",
"After a timeout with congestion window 32 KB, the new threshold is 16 KB, and slow start begins from 2 KB, doubling each RTT (2,4,8,16) then increasing linearly by 2 KB per RTT in congestion avoidance (18,20,...,32), taking 11 RTTs in total. At 100 msec per RTT, this is 11 x 100 = 1100 msec.",
[src(2014,"3.51",2,1)]
)

# 3.52
add(
"Consider a selective repeat sliding window protocol that uses a frame size of 1 KB to send data on a 1.5 Mbps link with a one-way latency of 50 msec. To achieve a link utilization of 60%, the minimum number of bits required to represent the sequence number field is ______.",
"NAT", 2, "hard", ["Selective repeat protocol", "Sliding window sequence number bits"], ["selective repeat", "sequence number bits", "link utilization"],
True, True, 180, [],
"5",
"Transmission time TT = (1024x8)/(1.5x10^6) = 5.46 ms. For 60% utilization, 60 = (N x 5.46)/(5.46 + 2x50) x 100, giving N approximately 11.58, so N=12 is needed. For selective repeat, window size N = 2^(m-1), so m = log2(N)+1 = 5 bits.",
[src(2014,"3.52",2,1)]
)

# 3.53
add(
"Which one of the following socket API functions converts an unconnected active TCP socket into a passive socket? (a) connect (b) bind (c) listen (d) accept",
"MCQ", 1, "easy", ["Socket API"], ["passive socket", "listen() call", "socket programming"],
False, False, 30,
[opt("A","connect"), opt("B","bind"), opt("C","listen", True), opt("D","accept")],
None,
"The listen() call converts an unconnected active TCP socket into a passive socket, ready to accept incoming connection requests.",
[src(2014,"3.53",1,2)]
)

# 3.54
add(
"In the diagram shown below, L1 is an Ethernet LAN and L2 is a Token-Ring LAN. An IP packet originates from sender S and traverses to R, as shown. The links within each ISP and across the two ISPs, are all point-to-point optical links. The initial value of the TTL field is 32. The maximum possible value of the TTL field when R receives the datagram is ______.",
"NAT", 1, "medium", ["TTL decrement", "Hop counting"], ["TTL field", "hop count", "multi-network path"],
True, False, 90, [],
"26",
"The TTL field is decremented by 1 at each hop the packet passes through. Given the initial TTL of 32 and the path shown passing through 6 hops from S to R, the maximum possible TTL value on arrival at R is 32 - 6 = 26.",
[src(2014,"3.54",1,2)]
)

# 3.55
add(
"Consider the store and forward packet switched network given below. Assume that the bandwidth of each link is 10^6 bytes/sec. A user on host A sends a file of size 10^3 bytes to host B through routers R1 and R2 in three different ways. In the first case a single packet containing the complete file is transmitted from A to B. In the second case, the file is split into 10 equal parts, and these packets are transmitted from A to B. In the third case, the file is split into 20 equal parts and these packets are sent from A to B. Each packet contains 100 bytes of header information along with the user data. Consider only transmission time and ignore processing, queuing and propagation delays. Also assume that there are no errors during transmission. Let T1, T2 and T3 be the times taken to transmit the file in the first, second and third case respectively. Which one of the following is CORRECT? (a) T1 < T2 < T3 (b) T1 > T2 > T3 (c) T2 = T3, T3 < T1 (d) T1 = T3, T3 > T2",
"MCQ", 2, "hard", ["Store and forward switching", "Packetization overhead"], ["store and forward", "packet header overhead", "transmission time"],
True, True, 180,
[opt("A","T1 < T2 < T3"), opt("B","T1 > T2 > T3"), opt("C","T2 = T3, T3 < T1"), opt("D","T1 = T3, T3 > T2", True)],
None,
"Computing the total transmission time (including store-and-forward delay at each router) for each packetization scheme shows T1 = 26.4 msec, T2 = 19.2 msec, and T3 = 26.4 msec, so T1 = T3 and both are greater than T2.",
[src(2014,"3.55",2,2)]
)

# 3.56
add(
"Host A (on TCP/IPv4 network A) sends an IP datagram D to host B (also on TCP/IPv4 network B). Assume that no error occurred during the transmission of D. When D reaches B, which of the following IP header field(s) may be different from that of the original datagram D? (i) TTL (ii) Checksum (iii) Fragment Offset (a) (i) only (b) (i) and (ii) only (c) (ii) and (iii) only (d) (i), (ii) and (iii)",
"MCQ", 1, "medium", ["IP header modification in transit"], ["TTL change", "checksum recalculation", "fragmentation en route"],
False, False, 90,
[opt("A","(i) only"), opt("B","(i) and (ii) only"), opt("C","(ii) and (iii) only"), opt("D","(i), (ii) and (iii)", True)],
None,
"TTL changes at every hop; the checksum is recomputed at every hop because TTL changes; and the fragment offset may change if the datagram gets fragmented along the path. So all three fields may differ.",
[src(2014,"3.56",1,3)]
)

# 3.57
add(
"An IP router implementing Classless Inter-domain Routing (CIDR) receives a packet with address 131.23.151.76. The router's routing table has the following entries: Prefix 131.16.0.0/12 -> Interface 3; 131.28.0.0/14 -> Interface 5; 131.19.0.0/16 -> Interface 2; 131.22.0.0/15 -> Interface 1. The identifier of the output interface on which this packet will be forwarded is ______.",
"NAT", 2, "hard", ["CIDR", "Longest prefix matching"], ["CIDR routing", "longest prefix match", "prefix matching"],
True, True, 150, [],
"1",
"Converting the destination address and each prefix to binary and matching bit-by-bit, the longest matching prefix is 131.22.0.0/15, which corresponds to Interface 1.",
[src(2014,"3.57",2,3)]
)

# 3.58
add(
"Every host in an IPv4 network has a 1-second resolution real-time clock with battery backup. Each host needs to generate up to 1000 unique identifiers per second. Assume that each host has a globally unique IPv4 address. Design a 50-bit globally unique ID for this purpose. After what period (in seconds) will the identifiers generated by a host wrap around? ______",
"NAT", 2, "hard", ["Unique identifier design", "Clock-based wraparound"], ["unique ID design", "clock resolution", "wraparound period"],
True, True, 150, [],
"256",
"To generate 1000 unique identifiers per second, ceil(log2(1000)) = 10 bits are needed. With a 50-bit ID and a 32-bit globally unique IP address (constant), 8 bits remain for the clock counter, which changes once every second, so the identifiers wrap around after 2^8 = 256 seconds.",
[src(2014,"3.58",2,3)]
)

# 3.59
add(
"An IP router with a Maximum Transmission Unit (MTU) of 1500 bytes has received an IP packet of size 4404 bytes with an IP header of length 20 bytes. The values of the relevant fields in the header of the third IP fragment generated by the router for this packet are (a) MF bit: 0, Datagram Length: 1444; Offset: 370 (b) MF bit: 1, Datagram Length: 1424; Offset: 185 (c) MF bit: 1, Datagram Length: 1500; Offset: 370 (d) MF bit: 0, Datagram Length: 1424; Offset: 2960",
"MCQ", 2, "hard", ["IP fragmentation", "MTU-based fragmenting"], ["MTU", "fragment offset", "MF bit", "fragment sizes"],
True, True, 180,
[opt("A","MF bit: 0, Datagram Length: 1444; Offset: 370", True),
 opt("B","MF bit: 1, Datagram Length: 1424; Offset: 185"),
 opt("C","MF bit: 1, Datagram Length: 1500; Offset: 370"),
 opt("D","MF bit: 0, Datagram Length: 1424; Offset: 2960")],
None,
"With MTU 1500 and header 20 bytes, each fragment can carry up to 1480 bytes of payload. The 4404-byte packet (4384 bytes payload) splits into fragments of 1480, 1480, and 1424 bytes payload. The third (last) fragment has datagram length 1424+20=1444, MF bit 0, and offset (1480+1480)/8 = 370.",
[src(2014,"3.59",2,3)]
)

# 3.60
add(
"Suppose two hosts use a TCP connection to transfer a large file. Which of the following statements is/are FALSE with respect to the TCP connection? 1. If the sequence number of a segment is m, then the sequence number of the subsequent segment is always m+1. 2. If the estimated round trip time at any given point of time is t sec, the value of the retransmission timeout is always set to greater than or equal to t sec. 3. The size of the advertised window never changes during the course of the TCP connection. 4. The number of unacknowledged bytes at the sender is always less than or equal to the advertised window. (a) 3 only (b) 1 and 3 only (c) 1 and 4 only (d) 2 and 4 only",
"MCQ", 1, "medium", ["TCP sequence numbers", "TCP flow control window"], ["sequence numbers", "retransmission timeout", "advertised window"],
False, False, 120,
[opt("A","3 only"), opt("B","1 and 3 only", True), opt("C","1 and 4 only"), opt("D","2 and 4 only")],
None,
"Statement 1 is false since the next segment's sequence number depends on the number of bytes in the current segment, not always +1. Statement 2 is true since RTO is always set >= estimated RTT. Statement 3 is false since the receiver's advertised window can change as buffer space changes. Statement 4 is true, so the false statements are 1 and 3.",
[src(2015,"3.60",1,1)]
)

# 3.61
add(
"Which one of the following fields of an IP header is NOT modified by a typical IP router? (a) Checksum (b) Source address (c) Time to Live (TTL) (d) Length",
"MCQ", 1, "easy", ["IP header modification"], ["source address", "TTL modification", "checksum recalculation"],
False, False, 45,
[opt("A","Checksum"), opt("B","Source address", True), opt("C","Time to Live (TTL)"), opt("D","Length")],
None,
"A typical IP router does not modify the source address field; it may modify TTL, checksum, and length (if fragmentation occurs) as the packet passes through.",
[src(2015,"3.61",1,1)]
)

# 3.62
add(
"Identify the correct order in which a server process must invoke the function calls accept, bind, listen, and recv according to UNIX socket API. (a) listen, accept, bind, recv (b) bind, listen, accept, recv (c) bind, accept, listen, recv (d) accept, listen, bind, recv",
"MCQ", 1, "easy", ["Socket API sequence"], ["socket programming", "bind listen accept recv order"],
False, False, 45,
[opt("A","listen, accept, bind, recv"), opt("B","bind, listen, accept, recv", True), opt("C","bind, accept, listen, recv"), opt("D","accept, listen, bind, recv")],
None,
"The standard server-side socket API sequence is bind(), listen(), accept(), and then recv().",
[src(2015,"3.62",1,2)]
)

# 3.63
add(
"Assume that the bandwidth for a TCP connection is 1048560 bits/sec. Let alpha be the value of RTT in milliseconds (rounded off to the nearest integer) after which the TCP window scale option is needed. Let beta be the maximum possible window size with window scale option. Then the values of alpha and beta are (a) 63 milliseconds, 65535 x 2^14 (b) 63 milliseconds, 65535 x 2^16 (c) 500 milliseconds, 65535 x 2^14 (d) 500 milliseconds, 65535 x 2^16",
"MCQ", 2, "hard", ["TCP window scale option", "Bandwidth-delay product"], ["window scale option", "bandwidth delay product", "RTT threshold"],
True, True, 150,
[opt("A","63 milliseconds, 65535 x 2^14"), opt("B","63 milliseconds, 65535 x 2^16"), opt("C","500 milliseconds, 65535 x 2^14", True), opt("D","500 milliseconds, 65535 x 2^16")],
None,
"The window scale option becomes necessary once the maximum window size of 65535 bytes is insufficient for the bandwidth-delay product, occurring around RTT = (65535x8)/1048560 = 500 ms. The window scale option uses 14 bits of scaling, giving a maximum window size of 65535 x 2^14.",
[src(2015,"3.63",2,2)]
)

# 3.64
add(
"Consider the following routing table at an IP router: Network No. 128.96.170.0/Net Mask 255.255.254.0/Interface 0; 128.96.168.0/255.255.254.0/Interface 1; 128.96.166.0/255.255.254.0/R2; 128.96.164.0/255.255.252.0/R3; 0.0.0.0/Default/R4. For each IP address in Group-I identify the correct choice of the next hop from Group-II using the entries from the routing table above. List-I: A. 128.96.171.92, B. 128.96.167.151, C. 128.96.163.121, D. 128.96.165.121. List-II: 1. Interface 0, 2. Interface 1, 3. R2, 4. R3, 5. R4. Codes: (a) A-1 B-3 C-5 D-4 (b) A-1 B-4 C-2 D-5 (c) A-2 B-3 C-4 D-5 (d) A-2 B-3 C-5 D-4",
"MCQ", 2, "hard", ["Routing table lookup", "Longest prefix matching"], ["routing table", "next hop determination", "subnet matching"],
True, True, 150,
[opt("A","A-1 B-3 C-5 D-4", True), opt("B","A-1 B-4 C-2 D-5"), opt("C","A-2 B-3 C-4 D-5"), opt("D","A-2 B-3 C-5 D-4")],
None,
"Matching each IP address against the routing table entries: 128.96.171.92 matches 128.96.170.0/23 (Interface 0); 128.96.167.151 matches 128.96.166.0/23 (R2); 128.96.163.121 matches no specific entry, so goes to default (R4); 128.96.165.121 matches 128.96.164.0/22 (R3).",
[src(2015,"3.64",2,2)]
)

# 3.65
add(
"Host A sends a UDP datagram containing 8880 bytes of user data to host B over an Ethernet LAN. Ethernet frames may carry data up to 1500 bytes (i.e. MTU = 1500 bytes). Size of UDP header is 8 bytes and size of IP header is 20 bytes. There is no option field in IP header. How many total number of IP fragments will be transmitted and what will be the contents of offset field in the last fragment? (a) 6 and 925 (b) 6 and 7400 (c) 7 and 1110 (d) 7 and 8880",
"MCQ", 2, "hard", ["UDP over IP fragmentation", "Fragment offset"], ["UDP datagram", "IP fragmentation", "offset field calculation"],
True, True, 180,
[opt("A","6 and 925"), opt("B","6 and 7400"), opt("C","7 and 1110", True), opt("D","7 and 8880")],
None,
"Total data to send (UDP header + payload) = 8880+8 = 8888 bytes. Each Ethernet frame can carry a maximum payload of 1500-20=1480 bytes. Splitting 8888 bytes into 1480-byte fragments needs 7 fragments (6 full fragments of 1480 bytes and 1 of 8 bytes), with the last fragment's offset = 1110 (in units of 8 bytes, i.e. 8880/8).",
[src(2015,"3.65",2,2)]
)

# 3.66
add(
"Consider the following statements: I. TCP connections are full duplex. II. TCP has no option for selective acknowledgment. III. TCP connections are message streams. (a) Only I is correct (b) Only I and II are correct (c) Only II and III are correct (d) All of I, II and III are correct",
"MCQ", 1, "medium", ["TCP connection properties"], ["full duplex", "selective acknowledgement", "byte stream vs message stream"],
False, False, 60,
[opt("A","Only I is correct", True), opt("B","Only I and II are correct"), opt("C","Only II and III are correct"), opt("D","All of I, II and III are correct")],
None,
"TCP connections are full duplex, so statement I is correct. TCP does support selective acknowledgment as an option, so II is false. TCP is a byte-stream protocol, not a message-stream protocol, so III is false.",
[src(2015,"3.66",1,3)]
)

# 3.67
add(
"In the network 200.10.11.144/27, the fourth octet (in decimal) of the last IP address of the network which can be assigned to a host is ______.",
"NAT", 2, "medium", ["Subnet host address range"], ["CIDR notation", "last usable host address", "subnet calculation"],
True, True, 90, [],
"158",
"A /27 mask gives 32 addresses per subnet (5 host bits). The subnet containing 200.10.11.144 spans 200.10.11.128 to 200.10.11.159; the last usable host address (excluding the broadcast address 159) has fourth octet 158.",
[src(2015,"3.67",2,3)]
)

# 3.68
add(
"An IP datagram of size 1000 bytes arrives at a router. The router has to forward this packet on a link whose MTU (maximum transmission unit) is 100 bytes. Assume that the size of the IP header is 20 bytes. The number of fragments that the IP datagram will be divided into for transmission is ______.",
"NAT", 2, "medium", ["IP fragmentation", "Number of fragments"], ["MTU", "fragmentation count", "IP header"],
True, True, 90, [],
"13",
"Each fragment can carry a maximum payload of 100-20=80 bytes. The original payload is 1000-20=980 bytes, requiring ceil(980/80) = 13 fragments.",
[src(2016,"3.68",2,1)]
)

# 3.69
add(
"For a host machine that uses the token bucket algorithm for congestion control, the token bucket has a capacity of 1 megabyte and the maximum output rate is 20 megabytes per second. Tokens arrive at a rate to sustain output at a rate of 10 megabytes per second. The token bucket is currently full and the machine needs to send 12 megabytes of data. The minimum time required to transmit the data is ______ seconds.",
"NAT", 2, "hard", ["Token bucket algorithm", "Traffic shaping"], ["token bucket", "burst transmission", "congestion control"],
True, True, 150, [],
"1.1",
"Using the token bucket formula, with capacity 1 MB, arrival rate 10 MBps, and output rate 20 MBps, the burst of 1 MB is sent at 20 MBps taking 0.05 s (this transmits 1 MB), and afterward data can only be sent at the token arrival rate. Combining these, the total time to send 12 MB works out to 1.1 seconds.",
[src(2016,"3.69",2,1)]
)

# 3.70
add(
"Consider socket API on a Linux machine that supports connected UDP sockets. A connected UDP socket is a UDP socket on which connect function has already been called. Which of the following statements is/are CORRECT? I. A connected UDP socket can be used to communicate with multiple peers simultaneously. II. A process can successfully call connect function again for an already connected UDP socket. (a) I only (b) II only (c) Both I and II (d) Neither I nor II",
"MCQ", 1, "medium", ["Connected UDP sockets"], ["connected UDP socket", "connect() semantics", "socket reuse"],
False, False, 90,
[opt("A","I only"), opt("B","II only", True), opt("C","Both I and II"), opt("D","Neither I nor II")],
None,
"A connected UDP socket is bound to a single peer, so it cannot be used to talk to multiple peers simultaneously (I false). However, connect() can be called again on an already-connected UDP socket to change its associated peer, similar to how bind() associates a local address (II true).",
[src(2017,"3.70",1,2)]
)

# 3.71
add(
"The maximum number of IPv4 router addresses that can be listed in the record route (RR) option field of an IPv4 header is ______.",
"NAT", 1, "medium", ["IP options", "Record route option"], ["record route option", "IP options field size", "IPv4 header"],
True, True, 90, [],
"9",
"The IP options and padding field allows a maximum of 40 bytes. Each IPv4 address occupies 4 bytes, and some bytes are used for option overhead, so a maximum of 9 router addresses can be recorded in the record route option.",
[src(2017,"3.71",1,2)]
)

# 3.72
add(
"Consider the following statements about the routing protocols, Routing Information Protocol (RIP) and Open Shortest Path First (OSPF) in an IPv4 network. I. RIP uses distance vector routing. II. RIP packets are sent using UDP. III. OSPF packets are sent using TCP. IV. OSPF operation is based on link-state routing. Which of the statements above are CORRECT? (a) I and IV only (b) I, II and III only (c) I, II and IV only (d) II, III and IV only",
"MCQ", 1, "medium", ["Routing protocols", "RIP vs OSPF"], ["distance vector routing", "link state routing", "RIP", "OSPF"],
False, False, 90,
[opt("A","I and IV only"), opt("B","I, II and III only"), opt("C","I, II and IV only", True), opt("D","II, III and IV only")],
None,
"RIP uses distance vector routing over UDP (I, II true). OSPF is based on link-state routing, but its packets run directly over IP, not over TCP (III false, IV true).",
[src(2017,"3.72",1,2)]
)

# 3.73
add(
"Consider a TCP client and a TCP server running on two different machines. After completing data transfer, the TCP client calls close to terminate the connection and a FIN segment is sent to the TCP server. Server-side TCP responds by sending an ACK, which is received by the client-side TCP. As per the TCP connection state diagram (RFC 793), in which state does the client-side TCP connection wait for the FIN from the server-side TCP? (a) LAST-ACK (b) TIME-WAIT (c) FIN-WAIT-1 (d) FIN-WAIT-2",
"MCQ", 1, "medium", ["TCP connection termination", "TCP state machine"], ["FIN-WAIT-2", "connection teardown", "half-close"],
False, False, 90,
[opt("A","LAST-ACK"), opt("B","TIME-WAIT"), opt("C","FIN-WAIT-1"), opt("D","FIN-WAIT-2", True)],
None,
"After sending FIN and receiving the ACK for it, the client moves from FIN-WAIT-1 to FIN-WAIT-2, where it waits for the server's own FIN before moving to TIME-WAIT.",
[src(2017,"3.73",1,1)]
)

# 3.74
add(
"Consider a long-lived TCP session with an end-to-end bandwidth of 1 Gbps (=10^9 bits-per-second). The session starts with a sequence number of 1234. The minimum time (in seconds, rounded to the closest integer) before this sequence number can be used again is ______.",
"NAT", 1, "hard", ["TCP sequence number wraparound"], ["sequence number wraparound", "32-bit sequence space", "bandwidth"],
True, True, 120, [],
"34 or 35",
"The 32-bit sequence number space has 2^32 possible values. At a rate of 10^9 bits per second (i.e., 1.25x10^8 bytes/sec), the time to cycle through all 2^32 sequence numbers is 2^32/1.25x10^8 which is approximately 34.36 seconds, rounding to 34 or 35 seconds.",
[src(2018,"3.74",1)]
)

# 3.75
add(
"Consider the following statements regarding the slow start phase of the TCP congestion control algorithm. Note that cwnd stands for the TCP congestion window and MSS denotes the Maximum Segment Size. (i) The cwnd increases by 2 MSS on every successful acknowledgement. (ii) The cwnd approximately doubles on every successful acknowledgement. (iii) The cwnd increases by 1 MSS every round trip time. (iv) The cwnd approximately doubles every round trip time. Which one of the following is correct? (a) Only (ii) and (iii) are true (b) Only (i) and (iii) are true (c) Only (iv) is true (d) Only (i) and (iv) are true",
"MCQ", 1, "medium", ["TCP slow start behaviour"], ["slow start", "cwnd doubling", "round trip time"],
False, False, 90,
[opt("A","Only (ii) and (iii) are true"), opt("B","Only (i) and (iii) are true"), opt("C","Only (iv) is true", True), opt("D","Only (i) and (iv) are true")],
None,
"In slow start, the congestion window increases by one MSS for every ACK received within a round trip time, which results in the window approximately doubling every round trip time, matching statement (iv) only.",
[src(2018,"3.75",1)]
)

# 3.76
add(
"Match the following: Field: P. UDP Header's Port Number, Q. Ethernet MAC Address, R. IPv6 Next Header, S. TCP Header's Sequence Number. Length in bits: I. 48, II. 8, III. 32, IV. 16. (a) P-III, Q-IV, R-II, S-I (b) P-II, Q-I, R-IV, S-III (c) P-IV, Q-I, R-III, S-II (d) P-IV, Q-I, R-II, S-III",
"MCQ", 1, "medium", ["Protocol header field sizes"], ["port number length", "MAC address length", "IPv6 next header length", "sequence number length"],
False, False, 90,
[opt("A","P-III, Q-IV, R-II, S-I"), opt("B","P-II, Q-I, R-IV, S-III"), opt("C","P-IV, Q-I, R-III, S-II", True), opt("D","P-IV, Q-I, R-II, S-III")],
None,
"UDP port numbers are 16 bits, Ethernet MAC addresses are 48 bits, and the TCP sequence number field is 32 bits, matching option (c)'s pairing for these fields.",
[src(2018,"3.76",1)]
)

# 3.77
add(
"Consider three machines M, N and P with IP addresses 100.10.5.2, 100.10.5.5 and 100.10.5.6 respectively. The subnet mask is set to 255.255.255.252 for all the three machines. Which one of the following is true? (a) M, N and P all belong to the same subnet (b) Only N and P belong to the same subnet (c) M, N, and P belong to three different subnets (d) Only M and N belong to the same subnet",
"MCQ", 2, "medium", ["Subnet membership check"], ["subnet mask", "network address matching", "small subnet"],
True, True, 120,
[opt("A","M, N and P all belong to the same subnet"), opt("B","Only N and P belong to the same subnet", True), opt("C","M, N, and P belong to three different subnets"), opt("D","Only M and N belong to the same subnet")],
None,
"Applying the /30 mask to each address: M's network address differs from N and P's, while N and P (addresses 5 and 6) share the same network address, so only N and P belong to the same subnet.",
[src(2019,"3.77",2)]
)

# 3.78
add(
"Consider a TCP connection between a client and a server with the following specifications: the round trip time is 6 ns, the size of the receiver advertised window is 50 KB, slow-start threshold at the client is 32 KB, and the maximum segment size is 2 KB. The connection is established at time t = 0. Assume that there are no timeouts and errors during transmission. Then the size of the congestion window (in KB) at time t + 60 ms after all acknowledgments are processed is ______.",
"NAT", 2, "hard", ["TCP slow start and congestion avoidance", "Window growth over time"], ["slow start", "congestion avoidance", "advertised window cap"],
True, True, 180, [],
"44",
"At t=0 there are no timeouts. Threshold = 32 KB, MSS = 2 KB. The congestion window grows exponentially in slow start until it reaches the threshold, then linearly in congestion avoidance, capped by the receiver's advertised window of 50 KB. After the elapsed rounds within 60 ms, the resulting window size works out to 44 KB.",
[src(2020,"3.78",2)]
)

# 3.79
add(
"An organization requires a range of IP addresses to assign one to each of its 1500 computers. The organization has approached an Internet Service Provider (ISP) for this task. The ISP uses CIDR and serves the requests from the available IP address space 202.61.0.0/17. The ISP wants to assign an address space to the organization which will minimize the number of routing entries in the ISP's router using route aggregation. Which of the following address spaces are potential candidates from which the ISP can allot any one to the organization? I. 202.61.84.0/21 II. 202.61.104.0/21 III. 202.61.64.0/21 IV. 202.61.144.0/21 (a) I and IV only (b) III and IV only (c) I and II only (d) II and III only",
"MCQ", 2, "hard", ["CIDR", "Route aggregation"], ["route aggregation", "CIDR block alignment", "address space allocation"],
True, True, 150,
[opt("A","I and IV only"), opt("B","III and IV only"), opt("C","I and II only"), opt("D","II and III only", True)],
None,
"A /21 block for 1500 hosts must be properly aligned (its starting address must be a multiple of the block size, 2^11=2048, i.e. multiple of 8 in the third octet). Checking each candidate's starting address for correct /21 alignment shows only II (202.61.104.0) and III (202.61.64.0) are valid /21 blocks within the /17 space.",
[src(2020,"3.79",2)]
)

# 3.80
add(
"A TCP server application is programmed to listen on port number P on host S. A TCP client is connected to the TCP server over the network. Consider that while the TCP connection was active, the server machine S crashed and rebooted. Assume that the client does not use the TCP keepalive timer. Which of the following behaviors is/are possible? (a) If the client sends a packet after the server reboot, it will receive a FIN segment. (b) If the client was waiting to receive a packet, it may wait indefinitely. (c) The TCP server application on S can listen on P after reboot. (d) If the client sends a packet after the server reboot, it will receive a RST segment.",
"MSQ", 2, "hard", ["TCP connection recovery after crash"], ["server crash", "half-open connection", "RST segment", "port reuse after reboot"],
False, False, 150,
[opt("A","If the client sends a packet after the server reboot, it will receive a FIN segment."),
 opt("B","If the client was waiting to receive a packet, it may wait indefinitely.", True),
 opt("C","The TCP server application on S can listen on P after reboot.", True),
 opt("D","If the client sends a packet after the server reboot, it will receive a RST segment.", True)],
None,
"If the client is only waiting to receive data (not sending), it will never learn the connection was lost and may wait indefinitely (a half-open connection), making (b) true. A server can bind and listen on the same port again after reboot, making (c) true. If the client sends data after reboot, the rebooted server (which has no memory of the connection) replies with an RST, not a FIN, making (d) true and (a) false.",
[src(2021,"3.80",2,1)]
)

# 3.81
CD_81 = "Consider two hosts P and Q connected through a router R. The maximum transfer unit (MTU) value of the link between P and R is 1500 bytes, and between R and Q is 820 bytes. A TCP segment of size 1400 bytes was transferred from P to Q through R, with IP identification value as 0x1234. Assume that the IP header size is 20 bytes. Further, the packet is allowed to be fragmented, i.e., Don't Fragment (DF) flag in the IP header is not set by P."
add(
CD_81 + " Which of the following statements is/are correct? (a) Two fragments are created at R and the IP datagram size carrying the second fragment is 620 bytes. (b) If the second fragment is lost, P is required to resend the whole TCP segment. (c) TCP destination port can be determined by analysing only the second fragment. (d) If the second fragment is lost, R will resend the fragment with the IP identification value 0x1234.",
"MSQ", 2, "hard", ["IP fragmentation at intermediate router", "TCP over fragmented IP"], ["fragmentation at router", "fragment loss recovery", "TCP port in fragments"],
True, True, 180,
[opt("A","Two fragments are created at R and the IP datagram size carrying the second fragment is 620 bytes.", True),
 opt("B","If the second fragment is lost, P is required to resend the whole TCP segment.", True),
 opt("C","TCP destination port can be determined by analysing only the second fragment."),
 opt("D","If the second fragment is lost, R will resend the fragment with the IP identification value 0x1234.")],
None,
"At R, the 1400-byte TCP segment (with 20-byte IP header, total 1420 bytes) must be fragmented for the 820-byte MTU link: the first fragment carries 800 bytes of data (820 total with header), and the second carries 600 bytes of data (620 total with header), so (a) is correct. Since fragment loss is only recovered end-to-end by TCP retransmission (not by routers), if the second IP fragment is lost, P (the TCP sender) must resend the entire TCP segment, so (b) is correct. TCP port information is only present in the first fragment, so (c) is false. Routers do not buffer or resend fragments, so (d) is false.",
[src(2021,"3.81",2,1)]
)

# 3.82
add(
"Consider the three-way handshake mechanism followed during TCP connection establishment between hosts P and Q. Let X and Y be two random 32-bit starting sequence numbers chosen by P and Q respectively. Suppose P sends a TCP connection request message to Q with a TCP segment having SYN bit = 1, SEQ number = X, and ACK bit = 0. Suppose Q accepts the connection request. Which one of the following choices represents the information present in the TCP segment header that is sent by Q to P? (a) SYN bit = 1, SEQ number = Y, ACK bit = 1, ACK number = X+1, FIN bit = 0 (b) SYN bit = 1, SEQ number = Y, ACK bit = 1, ACK number = X, FIN bit = 0 (c) SYN bit = 0, SEQ number = X+1, ACK bit = 0, ACK number = Y, FIN bit = 1 (d) SYN bit = 1, SEQ number = X+1, ACK bit = 0, ACK number = Y, FIN bit = 0",
"MCQ", 1, "medium", ["TCP three-way handshake", "SYN-ACK segment fields"], ["SYN+ACK", "sequence and ack numbers", "handshake fields"],
False, False, 90,
[opt("A","SYN bit = 1, SEQ number = Y, ACK bit = 1, ACK number = X+1, FIN bit = 0", True),
 opt("B","SYN bit = 1, SEQ number = Y, ACK bit = 1, ACK number = X, FIN bit = 0"),
 opt("C","SYN bit = 0, SEQ number = X+1, ACK bit = 0, ACK number = Y, FIN bit = 1"),
 opt("D","SYN bit = 1, SEQ number = X+1, ACK bit = 0, ACK number = Y, FIN bit = 0")],
None,
"Q's SYN+ACK response has SYN=1 (starting its own sequence with Y), ACK=1 acknowledging X+1 (the next byte expected from P), and FIN=0 since the connection is being established, not closed.",
[src(2021,"3.82",1,2)]
)

# 3.83
add(
"Consider the data transfer using TCP over a 1 Gbps link. Assuming that the maximum segment lifetime (MSL) is set to 60 seconds, the minimum number of bits required for the sequence number field of the TCP header, to prevent the sequence number space from wrapping around during MSL is ______.",
"NAT", 2, "hard", ["TCP sequence number space", "Wraparound prevention"], ["sequence number bits", "MSL", "bandwidth calculation"],
True, True, 150, [],
"33",
"At 1 Gbps = 2^30/8 bytes/sec, the number of bytes sent in 60 seconds (MSL) is (2^30/8) x 60. Taking log base 2 of this value gives approximately 32.9, so a minimum of 33 bits are required for the sequence number field.",
[src(2022,"3.83",2)]
)

# 3.84
add(
"Suppose you are asked to design a new reliable byte-stream transport protocol like TCP. This protocol, named myTCP, runs over a 100 Mbps network with Round Trip Time of 150 milliseconds and the maximum segment lifetime of 2 minutes. Which of the following is/are valid lengths of the Sequence Number field in the myTCP header? (a) 30 bits (b) 32 bits (c) 34 bits (d) 36 bits",
"MSQ", 2, "hard", ["Sequence number field sizing", "Bandwidth-delay and MSL"], ["sequence number sizing", "MSL", "bandwidth-based calculation"],
True, True, 180,
[opt("A","30 bits"), opt("B","32 bits", True), opt("C","34 bits", True), opt("D","36 bits", True)],
None,
"At 100 Mbps and MSL of 2 minutes, the total number of bytes transmitted in one MSL is 120 x 100 x 2^20/8 bytes, requiring at least 31 bits for the sequence number to avoid wraparound within the MSL. Any sequence field size of 31 bits or more is valid, so 32, 34 and 36 bits are all valid but 30 bits is not.",
[src(2023,"3.84",2)]
)

# 3.85
add(
"Suppose in a web browser, you click on the www.gate-2023.in URL. The browser cache is empty. The IP address for this URL is not cached in your local host, so a DNS lookup is triggered (by the local DNS server deployed on your local host) over the 3-tier DNS hierarchy in an iterative mode. No resource records are cached anywhere across all DNS servers. Let RTT denote the round trip time between your local host and DNS servers in the DNS hierarchy. The round trip time between your local host and the web server hosting www.gate-2023.in is also equal to RTT. The HTML file associated with the URL is small enough to have negligible transmission time and negligible rendering time by your web browser, which references 10 equally small objects on the same web server. Which of the following statements is/are CORRECT about the minimum elapsed time between clicking on the URL and your browser fully rendering it? (a) 7 RTTs, in case of non-persistent HTTP with 5 parallel TCP connections. (b) 5 RTTs, in case of persistent HTTP with pipelining. (c) 9 RTTs, in case of non-persistent HTTP with 5 parallel TCP connections. (d) 6 RTTs, in case of persistent HTTP with pipelining.",
"MSQ", 2, "hard", ["DNS resolution time", "HTTP persistent vs non-persistent connections"], ["iterative DNS lookup", "non-persistent HTTP", "persistent HTTP pipelining", "RTT counting"],
True, True, 180,
[opt("A","7 RTTs, in case of non-persistent HTTP with 5 parallel TCP connections."),
 opt("B","5 RTTs, in case of persistent HTTP with pipelining."),
 opt("C","9 RTTs, in case of non-persistent HTTP with 5 parallel TCP connections.", True),
 opt("D","6 RTTs, in case of persistent HTTP with pipelining.", True)],
None,
"Iterative DNS resolution across the 3-tier hierarchy takes 3 RTTs. For persistent HTTP with pipelining, an additional 3 RTTs (1 for TCP setup, 1 for sending all 10 pipelined requests, 1 for closing) are needed, giving 6 RTTs total. For non-persistent HTTP with 5 parallel connections, TCP setup takes 2 RTTs and object retrieval (10 objects over 5 connections) takes 2 rounds of 2 RTTs each = 4 RTTs, giving 3 + 2 + 4 = 9 RTTs total.",
[src(2023,"3.85",2)]
)

# 3.86
add(
"The forwarding table of a router is shown below: Subnet Number 200.150.0.0/Subnet mask 255.250.0.0/Interface ID 1; 200.150.64.0/255.255.224.0/2; 200.150.68.0/255.255.255.0/3; 200.150.68.64/255.255.255.224/4; Default/0. A packet addressed to destination address 200.150.68.118 arrives at the router. It will be forwarded to the interface with ID ______.",
"NAT", 2, "medium", ["Longest prefix matching", "Forwarding table lookup"], ["forwarding table", "longest prefix match", "interface selection"],
True, True, 120, [],
"3",
"Matching 200.150.68.118 against each entry's subnet mask, the longest matching prefix is 200.150.68.0/255.255.255.0, corresponding to Interface ID 3.",
[src(2023,"3.86",2)]
)

# 3.87
add(
"TCP client P successfully establishes a connection to TCP server Q. Let Np denote the sequence number in the SYN sent from P to Q. Let Nq denote the acknowledgement number in the SYN ACK from Q to P. Which of the following statements is/are CORRECT? (a) The acknowledgement number Nq is equal to Np. (b) The sequence number Nq is always 0 for a new connection. (c) The acknowledgement number Nq is equal to Np + 1. (d) The sequence number Np is chosen randomly by P.",
"MSQ", 1, "medium", ["TCP handshake sequence and ack numbers"], ["SYN sequence number", "ACK number in SYN-ACK", "random ISN"],
False, False, 90,
[opt("A","The acknowledgement number Nq is equal to Np."),
 opt("B","The sequence number Nq is always 0 for a new connection."),
 opt("C","The acknowledgement number Nq is equal to Np + 1.", True),
 opt("D","The sequence number Np is chosen randomly by P.", True)],
None,
"The acknowledgement number in the SYN-ACK is always Np+1, acknowledging receipt of P's SYN (making c correct). The initial sequence number Np is chosen randomly (not always 0) by the sender to establish a fresh connection, so (d) is correct.",
[src(2024,"3.87",1,1)]
)

# 3.88
add(
"Which of the following fields is/are modified in the IP header of a packet going out of a network address translation (NAT) device from an internal network to an external network? (a) Total Length (b) Source IP (c) Destination IP (d) Header Checksum",
"MSQ", 1, "medium", ["Network Address Translation (NAT)"], ["NAT", "source IP rewriting", "checksum recomputation"],
False, False, 90,
[opt("A","Total Length"), opt("B","Source IP", True), opt("C","Destination IP"), opt("D","Header Checksum", True)],
None,
"A NAT device rewrites the private source IP address to its own public address for outgoing packets (Source IP changes), and because the header content changes, the Header Checksum must be recomputed. Total Length and Destination IP are unaffected.",
[src(2024,"3.88",1,1)]
)

# 3.89
add(
"Consider sending an IP datagram of size 1420 bytes (including 20 bytes of IP header) from a sender to a receiver over a path of two links with a router between them. The first link (sender to router) has an MTU (Maximum Transmission Unit) size of 542 bytes, while the second link (router to receiver) has an MTU size of 360 bytes. The number of fragments that would be delivered at the receiver is ______.",
"NAT", 2, "hard", ["Two-stage IP fragmentation"], ["MTU fragmentation", "fragment of a fragment", "two-link path"],
True, True, 180, [],
"6",
"On the first link (MTU 542), the payload of 1400 bytes is fragmented into pieces of up to 522 bytes payload each: 3 fragments (522, 522, 356). On the second link (MTU 360, i.e. payload up to 340 bytes), each of those fragments must be further split; the total number of fragments delivered at the receiver works out to 6.",
[src(2024,"3.89",2,1)]
)

# 3.90
add(
"Consider the entries shown below in the forwarding table of an IP router. Each entry consists of an IP prefix and the corresponding next hop router for packets whose destination IP address matches the prefix. The notation '/N' in a prefix indicates a subnet mask with the most significant N bits set to 1. Prefix 10.1.1.0/24 -> R1; 10.1.1.128/25 -> R2; 10.1.1.64/26 -> R3; 10.1.1.192/26 -> R4. This router forwards 20 packets each to 5 hosts. The IP addresses of the hosts are 10.1.1.16, 10.1.1.72, 10.1.1.132, 10.1.1.191, and 10.1.1.205. The number of packets forwarded via the next hop router R2 is ______.",
"NAT", 2, "hard", ["Longest prefix matching", "Traffic distribution across next hops"], ["longest prefix match", "forwarding table", "packet counting"],
True, True, 150, [],
"40",
"Matching each host address against the longest matching prefix: 10.1.1.132 and 10.1.1.191 both fall in 10.1.1.128/25, matching R2 (since /25 is longer/more specific than /24). With 20 packets to each of these 2 hosts, R2 receives 20x2=40 packets.",
[src(2024,"3.90",2,1)]
)

# 3.91
add(
"Which of the following fields of an IP header is/are always modified by any router before it forwards the IP packet? (a) Time to Live (TTL) (b) Header Checksum (c) Protocol (d) Source IP Address",
"MSQ", 1, "medium", ["Fields always modified by routers"], ["TTL decrement", "header checksum recomputation"],
False, False, 90,
[opt("A","Time to Live (TTL)", True), opt("B","Header Checksum", True), opt("C","Protocol"), opt("D","Source IP Address")],
None,
"Every router decrements the TTL field by at least 1 before forwarding, and because TTL changes, the Header Checksum must be recomputed at every hop. Protocol and Source IP Address are not modified in normal forwarding.",
[src(2024,"3.91",1,2)]
)

# 3.92
add(
"Which of the following statements about IPv4 fragmentation is/are TRUE? (a) The fragmentation of an IP datagram is performed only at the source of the datagram. (b) The reassembly of fragments is performed at all intermediate routers along the path from the source to the destination. (c) The reassembly of fragments is performed only at the destination of the datagram. (d) The fragmentation of an IP datagram is performed at any IP router which finds that the size of the datagram to be transmitted exceeds the MTU.",
"MSQ", 1, "medium", ["IPv4 fragmentation and reassembly"], ["fragmentation location", "reassembly at destination"],
False, False, 90,
[opt("A","The fragmentation of an IP datagram is performed only at the source of the datagram."),
 opt("B","The reassembly of fragments is performed at all intermediate routers along the path from the source to the destination."),
 opt("C","The reassembly of fragments is performed only at the destination of the datagram.", True),
 opt("D","The fragmentation of an IP datagram is performed at any IP router which finds that the size of the datagram to be transmitted exceeds the MTU.", True)],
None,
"IPv4 fragmentation can occur at any router along the path whenever the outgoing link's MTU is smaller than the datagram, not just at the source, making (a) false and (d) true. Reassembly of fragments happens only at the final destination, not at intermediate routers, making (b) false and (c) true.",
[src(2024,"3.92",1,2)]
)

# 3.93
add(
"Which one of the following CIDR prefixes exactly represents the range of IP address 10.12.2.0 to 10.12.3.255? (a) 10.12.0.0/22 (b) 10.12.2.0/22 (c) 10.12.2.0/24 (d) 10.12.2.0/23",
"MCQ", 2, "medium", ["CIDR prefix range calculation"], ["CIDR prefix", "address range", "subnet size"],
True, True, 90,
[opt("A","10.12.0.0/22"), opt("B","10.12.2.0/22"), opt("C","10.12.2.0/24"), opt("D","10.12.2.0/23", True)],
None,
"The range 10.12.2.0 to 10.12.3.255 spans 512 addresses (2^9), corresponding to a /23 prefix, and the starting address 10.12.2.0 is correctly aligned for a /23 block.",
[src(2024,"3.93",2,2)]
)

# 3.94
add(
"Consider a TCP connection operating at a point of time with the congestion window of size 12 MSS (Maximum Segment Size), when a timeout occurs due to packet loss. Assuming that all the segments transmitted in the next two RTTs (Round Trip Time) are acknowledged correctly, the congestion window size (in MSS) during the third RTT will be ______.",
"NAT", 2, "hard", ["TCP timeout recovery", "Slow start after timeout"], ["timeout", "slow start", "ssthresh calculation"],
True, True, 150, [],
"4",
"On timeout, the new threshold is set to half the current window: 12/2 = 6 MSS, and cwnd resets to 1 MSS, entering slow start. In the first RTT after timeout, cwnd doubles to 2 MSS (still below threshold); in the second RTT, cwnd doubles to 4 MSS; so during the third RTT the congestion window size is 4 MSS.",
[src(2024,"3.94",2,2)]
)

# 3.95
add(
"Identify the ONE CORRECT matching between the OSI layers and their corresponding functionalities as shown. OSI Layers: (a) Network layer, (b) Transport layer, (c) Datalink layer. Functionalities: (I) Packet routing, (II) Framing and error handling, (III) Host to host communication. (a) (a)-(I), (b)-(II), (c)-(III) (b) (a)-(I), (b)-(III), (c)-(II) (c) (a)-(II), (b)-(I), (c)-(III) (d) (a)-(III), (b)-(II), (c)-(I)",
"MCQ", 1, "easy", ["OSI model layer functions"], ["OSI layers", "network layer function", "transport layer function", "data link layer function"],
False, False, 60,
[opt("A","(a)-(I), (b)-(II), (c)-(III)"),
 opt("B","(a)-(I), (b)-(III), (c)-(II)", True),
 opt("C","(a)-(II), (b)-(I), (c)-(III)"),
 opt("D","(a)-(III), (b)-(II), (c)-(I)")],
None,
"Packet routing is the responsibility of the Network layer, host-to-host (end-to-end) communication is the responsibility of the Transport layer, and framing and error handling is the responsibility of the Data Link layer.",
[src(2025,"3.95",1,1)]
)

# 3.96
add(
"Consider the 3-way handshaking protocol for TCP connection establishment. Let the three packets exchanged during the connection establishment be denoted as P1, P2, and P3, in order. Which of the following option(s) is/are TRUE with respect to TCP header flags that are set in the packets? (a) P3: SYN = 1, ACK = 1 (b) P2: SYN = 1, ACK = 1 (c) P2: SYN = 0, ACK = 1 (d) P1: SYN = 1",
"MSQ", 1, "medium", ["TCP three-way handshake flags"], ["SYN flag", "ACK flag", "handshake packet flags"],
False, False, 90,
[opt("A","P3: SYN = 1, ACK = 1"),
 opt("B","P2: SYN = 1, ACK = 1", True),
 opt("C","P2: SYN = 0, ACK = 1"),
 opt("D","P1: SYN = 1", True)],
None,
"In the three-way handshake, P1 (client's SYN) has SYN=1, ACK=0. P2 (server's SYN+ACK) has both SYN=1 and ACK=1. P3 (client's final ACK) has SYN=0, ACK=1, so P3 does not have SYN=1.",
[src(2025,"3.96",1,1)]
)

# 3.97
add(
"A packet with the destination IP address 145.36.109.70 arrives at a router whose routing table is shown. Subnet Address 145.36.0.0/16 Interface E1; 145.36.128.0/17 Interface E2; 145.36.64.0/18 Interface E3; 145.36.255.0/24 Interface E4; Default Interface E5. Which interface will the packet be forwarded to? (a) E3 (b) E1 (c) E2 (d) E5",
"MCQ", 2, "medium", ["Longest prefix matching", "Routing table lookup"], ["routing table", "longest prefix match", "subnet interface selection"],
True, True, 120,
[opt("A","E3", True), opt("B","E1"), opt("C","E2"), opt("D","E5")],
None,
"Matching 145.36.109.70 against each prefix, it falls within 145.36.64.0/18 (E3), the longest matching prefix among the given entries.",
[src(2025,"3.97",2,1)]
)

# 3.98
add(
"Suppose a message of size 15000 bytes is transmitted from a source to a destination using IPv4 protocol via two routers as shown in the figure. Each router has a defined maximum transmission unit (MTU) as shown in the figure, including IP header. Router-1 (MTU = 5000 bytes), Router-2 (MTU = 3000 bytes). The number of fragments that will be delivered to the destination is ______. (Answer in integer)",
"NAT", 2, "hard", ["Multi-hop IP fragmentation"], ["MTU", "successive fragmentation", "fragment count"],
True, True, 180, [],
"7",
"At Router-1 (MTU 5000, header 20 bytes), the 15000-byte message is split into fragments of up to 4980 bytes payload each. At Router-2 (MTU 3000, i.e. payload up to 2980 bytes), each of those fragments is further split. Working through both stages of fragmentation gives a total of 7 fragments delivered to the destination.",
[src(2025,"3.98",2,1)]
)

# 3.99
add(
"Consider the following statements: (i) Address Resolution Protocol (ARP) provides a mapping from an IP address to the corresponding hardware (link-layer) address. (ii) A single TCP segment from a sender S to a receiver R cannot carry both data from S to R and acknowledgement for a segment from R to S. Which ONE of the following is CORRECT? (a) Both (i) and (ii) are TRUE (b) (i) is TRUE and (ii) is FALSE (c) (i) is FALSE and (ii) is TRUE (d) Both (i) and (ii) are FALSE",
"MCQ", 1, "medium", ["ARP function", "TCP piggybacking"], ["ARP mapping", "TCP piggybacking", "bidirectional data and ACK"],
False, False, 90,
[opt("A","Both (i) and (ii) are TRUE"), opt("B","(i) is TRUE and (ii) is FALSE", True), opt("C","(i) is FALSE and (ii) is TRUE"), opt("D","Both (i) and (ii) are FALSE")],
None,
"ARP does map an IP address to the corresponding hardware (MAC) address, so (i) is true. TCP supports piggybacking, allowing a single segment to carry both data and an acknowledgement simultaneously, so (ii) is false.",
[src(2025,"3.99",1,2)]
)

# 3.100
add(
"A machine receives an IPv4 datagram. The protocol field of the IPv4 header has the protocol number of a protocol X. Which ONE of the following is NOT a possible candidate for X? (a) Internet Control Message Protocol (ICMP) (b) Internet Group Management Protocol (IGMP) (c) Open Shortest Path First (OSPF) (d) Routing Information Protocol (RIP)",
"MCQ", 1, "medium", ["IP protocol field values"], ["protocol field", "ICMP", "IGMP", "OSPF", "RIP over UDP"],
False, False, 90,
[opt("A","Internet Control Message Protocol (ICMP)"), opt("B","Internet Group Management Protocol (IGMP)"), opt("C","Open Shortest Path First (OSPF)"), opt("D","Routing Information Protocol (RIP)", True)],
None,
"ICMP, IGMP, and OSPF each have their own dedicated protocol number in the IPv4 header's protocol field. RIP, however, runs over UDP, so its packets appear with UDP's protocol number in the IP header rather than a dedicated RIP protocol number, making RIP not a possible value for X.",
[src(2025,"3.100",1,2)]
)

# 3.101
add(
"Consider a network that uses Ethernet and IPv4. Assume that IPv4 headers do not use any options field. Each Ethernet frame can carry a maximum of 1500 bytes in its data field. A UDP segment is transmitted. The payload (data) in the UDP segment is 7488 bytes. Which ONE of the following choices has the CORRECT total number of fragments transmitted and the size of the last fragment including IPv4 header? (a) 5 fragments, 1488 bytes (b) 6 fragments, 88 bytes (c) 6 fragments, 108 bytes (d) 6 fragments, 116 bytes",
"MCQ", 1, "hard", ["UDP over IP fragmentation", "Last fragment size"], ["UDP payload", "IP fragmentation", "last fragment size calculation"],
True, True, 150,
[opt("A","5 fragments, 1488 bytes"), opt("B","6 fragments, 88 bytes"), opt("C","6 fragments, 108 bytes"), opt("D","6 fragments, 116 bytes", True)],
None,
"Total data to send (UDP header 8 bytes + 7488 bytes payload) = 7496 bytes. Each Ethernet frame with a 20-byte IP header can carry up to 1480 bytes of payload. This requires ceil(7496/1480) = 6 fragments, with the last fragment carrying 7496 - 5x1480 = 96 bytes of payload plus 20 bytes IP header = 116 bytes total.",
[src(2025,"3.101",1,2)]
)

# 3.102
add(
"With respect to a TCP connection between a client and a server, which one of the following statements is true? (a) The client and server use a two-way handshake mechanism before the start of data transmission. (b) The server cannot initiate closing of the connection before the client initiates closing of the connection. (c) The TCP connection is half-duplex. (d) The client and server can initiate closing of the connection at the same time.",
"MCQ", 1, "medium", ["TCP connection establishment and termination"], ["simultaneous close", "full duplex TCP", "connection termination"],
False, False, 90,
[opt("A","The client and server use a two-way handshake mechanism before the start of data transmission."),
 opt("B","The server cannot initiate closing of the connection before the client initiates closing of the connection."),
 opt("C","The TCP connection is half-duplex."),
 opt("D","The client and server can initiate closing of the connection at the same time.", True)],
None,
"TCP connections are established via a three-way handshake and are full-duplex, so (a) and (c) are false. Either side (client or server) may initiate closing the connection, and TCP even supports a simultaneous close where both sides send FIN at the same time, so (d) is correct and (b) is false.",
[src(2026,"3.102",1,1)]
)

# 3.103
add(
"Which of the following statements is/are true with respect to the interaction of a web browser with a web server using HTTP 1.1? (a) HTTP 1.1 facilitates downloading multiple objects of the same webpage over the same TCP connection, if the objects are stored in the same server. (b) HTTP 1.1 facilitates downloading multiple objects of the same webpage over the same TCP connection, even if the objects are stored in different servers. (c) HTTP 1.1 facilitates sending a request for downloading one object without waiting for a previously requested object to be downloaded completely. (d) HTTP 1.1 facilitates downloading multiple webpages on the same server to be downloaded over a single TCP connection.",
"MSQ", 1, "medium", ["HTTP 1.1 persistent connections and pipelining"], ["persistent HTTP", "pipelining", "single server multiple objects"],
False, False, 120,
[opt("A","HTTP 1.1 facilitates downloading multiple objects of the same webpage over the same TCP connection, if the objects are stored in the same server.", True),
 opt("B","HTTP 1.1 facilitates downloading multiple objects of the same webpage over the same TCP connection, even if the objects are stored in different servers."),
 opt("C","HTTP 1.1 facilitates sending a request for downloading one object without waiting for a previously requested object to be downloaded completely.", True),
 opt("D","HTTP 1.1 facilitates downloading multiple webpages on the same server to be downloaded over a single TCP connection.", True)],
None,
"HTTP 1.1's persistent connections allow multiple objects from the same server to be fetched over one TCP connection (a true), and pipelining allows a client to send a new request before the previous response arrives (c true). Since a TCP connection is between one client and one server, a single connection cannot span different servers (b false). Multiple webpages from the same server can also be fetched over a single persistent connection (d true).",
[src(2026,"3.103",1,1)]
)

# 3.104
add(
"A TCP sender successfully establishes a connection with a TCP receiver and starts the transmission of segments. The TCP congestion control mechanism's slow-start threshold is set to 10000 segments. Assume that the round-trip time is fixed at 1 millisecond. Assume that the sender always has data to send, the segments are numbered from 1, and no segment is lost. Let t denote the time (in milliseconds) at which the transmission of segment number 2000 starts. Which one of the following options is correct? (a) 9 <= t < 10 (b) 10 <= t < 11 (c) 11 <= t < 12 (d) 12 <= t < 13",
"MCQ", 2, "hard", ["TCP slow start segment timing"], ["slow start", "cumulative segments sent", "RTT-based timing"],
True, True, 150,
[opt("A","9 <= t < 10"), opt("B","10 <= t < 11", True), opt("C","11 <= t < 12"), opt("D","12 <= t < 13")],
None,
"In slow start, the congestion window (in segments) doubles each RTT: 1,2,4,8,...,512,1024. The cumulative number of segments sent after 10 RTTs is 1023 and after 11 RTTs is 2047, so segment number 2000 starts transmission during the 11th millisecond window, i.e., 10 <= t < 11.",
[src(2026,"3.104",2,1)]
)

# 3.105
add(
"An ISP having an address block 202.16.0.0/15 assigns a block of 6000 IP addresses to a client, using the classless internet domain routing (CIDR) super-netting approach. Which of the following address blocks can be assigned by the ISP? (a) 202.16.0.0/19 (b) 202.17.64.0/19 (c) 202.16.32.0/19 (d) 202.17.24.0/19",
"MSQ", 2, "hard", ["CIDR super-netting", "Address block alignment"], ["CIDR alignment", "super-netting", "address block validity"],
True, True, 180,
[opt("A","202.16.0.0/19", True), opt("B","202.17.64.0/19", True), opt("C","202.16.32.0/19", True), opt("D","202.17.24.0/19")],
None,
"A /19 block contains 2^13=8192 addresses, sufficient for 6000 hosts, and must be properly aligned within the /15 space. Checking each option's starting address in binary against the /19 boundary shows that 202.16.0.0/19, 202.17.64.0/19, and 202.16.32.0/19 are all correctly aligned valid blocks, while 202.17.24.0/19 is not properly aligned.",
[src(2026,"3.105",2,1)]
)

# 3.106
add(
"Which one of the following protocols may need to broadcast some of its messages? (a) SMTP (b) FTP (c) DHCP (d) HTTP",
"MCQ", 1, "easy", ["Broadcast-using protocols"], ["DHCP broadcast", "application layer protocols"],
False, False, 45,
[opt("A","SMTP"), opt("B","FTP"), opt("C","DHCP", True), opt("D","HTTP")],
None,
"DHCP uses broadcast messages (destination address 255.255.255.255) so that a client without a configured IP address can discover a DHCP server on the local network.",
[src(2026,"3.106",1,2)]
)

# 3.107
add(
"If an IP network uses a subnet mask of 255.255.240.0, the maximum number of IP addresses that can be assigned to network interfaces is ______. (answer in integer)",
"NAT", 1, "medium", ["Host address count from subnet mask"], ["subnet mask", "host bits", "usable address count"],
True, True, 90, [],
"4094",
"The mask 255.255.240.0 leaves 12 host bits, giving a maximum of 2^12 - 2 = 4094 usable addresses that can be assigned to network interfaces.",
[src(2026,"3.107",1,2)]
)

# 3.108
add(
"Consider a new TCP connection between a sender and a receiver. The receiver advertised window is constant at 48 KB, the maximum segment size (MSS) is 2 KB, and the slow start threshold for TCP congestion control is 16 KB. Assume that there are no timeouts or duplicate acknowledgements. The number of rounds of transmission required for the congestion control algorithm of the TCP connection to reach the congestion avoidance phase is ______. (Answer in integer) Note: 1K = 2^10",
"NAT", 2, "hard", ["TCP slow start to congestion avoidance transition"], ["slow start threshold", "congestion avoidance transition", "window doubling"],
True, True, 150, [],
"4",
"In slow start, the congestion window doubles each round starting from 1 MSS (2 KB): 2 KB, 4 KB, 8 KB, 16 KB. The window reaches the slow-start threshold of 16 KB after 4 rounds, at which point the connection transitions to congestion avoidance.",
[src(2026,"3.108",2,2)]
)

output = {
    "subject": {"subject_name": "Computer Networks", "subject_code": "CN"},
    "topics": [{"topic_name": TOPIC, "summary": "This chapter covers the transport layer protocols TCP and UDP along with IPv4 addressing, subnetting, CIDR, fragmentation, routing table lookups, and TCP congestion/flow control mechanisms."}],
    "questions": Q
}

output_path = os.path.join(os.path.dirname(__file__), "cn_tcp_udp_ip.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("Saved to", output_path)
print("Total questions:", len(Q))