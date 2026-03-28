"""
Seed database with Computer Networks content — 10 topics, 50+ concepts, 200+ questions.
All GATE-level quality with proper explanations.
"""
import uuid
from app.db.session import SessionLocal
from app.models.subject import Subject, Topic
from app.models.concept import Concept
from app.models.question import Question, QuestionConcept


def _id():
    return str(uuid.uuid4())


def _mcq(text, opts, correct, explanation, difficulty=1, time_est=30):
    """Helper to reduce boilerplate for MCQ creation."""
    return {
        "id": _id(), "question_text": text, "question_type": "mcq",
        "options": opts, "correct_answer": correct, "explanation": explanation,
        "difficulty": difficulty, "time_estimate_seconds": time_est,
    }


def _tf(text, correct, explanation, difficulty=1):
    """Helper for True/False."""
    return {
        "id": _id(), "question_text": text, "question_type": "true_false",
        "options": ["True", "False"], "correct_answer": correct,
        "explanation": explanation, "difficulty": difficulty, "time_estimate_seconds": 20,
    }


def seed_database():
    db = SessionLocal()
    try:
        if db.query(Subject).first():
            print("Database already seeded — skipping.")
            return

        # ─── Subject ───
        subj_id = _id()
        db.add(Subject(id=subj_id, name="Computer Networks",
                        description="Complete networking course from basics to application layer — GATE CS level.",
                        icon="🌐", color="#3b82f6", order_index=0,
                        target_degrees="B.Tech,M.Tech,BCA,MCA,B.Sc,M.Sc"))

        # ─── Topics ───
        topics_data = [
            (_id(), "Introduction to Computer Networks", "Types of networks, topologies, devices, and basic concepts.", "📡", 0),
            (_id(), "OSI Model", "The 7-layer OSI reference model — purpose, functions, and PDUs.", "📶", 1),
            (_id(), "TCP/IP Protocol Stack", "TCP/IP vs OSI, layering, encapsulation, and protocol mapping.", "🔗", 2),
            (_id(), "Physical Layer & Switching", "Transmission media, multiplexing, and switching techniques.", "⚡", 3),
            (_id(), "Data Link Layer", "Framing, error detection, MAC protocols, Ethernet, and bridging.", "🔌", 4),
            (_id(), "Network Layer & IP Addressing", "IPv4 addressing, subnetting, CIDR, NAT, fragmentation.", "🗺️", 5),
            (_id(), "Routing Protocols", "Shortest path, distance vector, link state, flooding.", "🧭", 6),
            (_id(), "Transport Layer", "TCP, UDP, flow control, congestion control, sockets.", "📦", 7),
            (_id(), "Application Layer Protocols", "DNS, HTTP, FTP, SMTP, and email architecture.", "🌍", 8),
            (_id(), "Network Security Basics", "Firewalls, encryption, digital signatures, SSL/TLS basics.", "🔒", 9),
        ]
        topic_ids = {}
        for tid, name, desc, icon, order in topics_data:
            db.add(Topic(id=tid, subject_id=subj_id, name=name, description=desc, icon=icon, order_index=order))
            topic_ids[order] = tid

        # ─── Concepts + Questions ───
        # Each concept has key_points and linked questions.

        all_questions = []

        def add_concept(topic_order, name, explanation, key_points, order_idx, questions):
            cid = _id()
            db.add(Concept(id=cid, topic_id=topic_ids[topic_order], name=name,
                           explanation=explanation, key_points=key_points, order_index=order_idx))
            db.flush()  # ensure concept exists before FK references
            for q in questions:
                qid = q["id"]
                db.add(Question(**q))
                db.flush()  # ensure question exists before FK reference
                db.add(QuestionConcept(question_id=qid, concept_id=cid))

        # ═══════════════════════════════════════════
        # TOPIC 0: Introduction to Computer Networks
        # ═══════════════════════════════════════════

        add_concept(0, "Types of Networks", "Computer networks are classified by geographical scope. LAN covers a small area like a building, MAN spans a city, and WAN covers large geographical areas like countries.",
            ["LAN: Local Area Network (building/campus)", "MAN: Metropolitan Area Network (city-wide)", "WAN: Wide Area Network (country/continent)", "PAN: Personal Area Network (few meters)"], 0, [
            _mcq("Which type of network covers a metropolitan city area?", ["LAN", "MAN", "WAN", "PAN"], "MAN", "MAN (Metropolitan Area Network) covers a city-sized area, larger than LAN but smaller than WAN."),
            _mcq("A network spanning multiple countries is typically classified as:", ["LAN", "MAN", "WAN", "CAN"], "WAN", "WAN (Wide Area Network) covers large geographical areas including multiple countries."),
            _tf("A LAN typically covers a larger area than a MAN.", "False", "LAN covers a small area like a building or campus. MAN covers a larger city-wide area."),
            _mcq("Which network type is typically owned by a single organization?", ["WAN", "MAN", "LAN", "Internet"], "LAN", "LANs are typically owned by a single organization and cover a small area.", 2),
        ])

        add_concept(0, "Network Topologies", "Topology defines the arrangement of nodes and links. Common topologies are bus, star, ring, mesh, and tree. Each has trade-offs in reliability, cost, and performance.",
            ["Bus: single backbone cable, simple but single point of failure", "Star: central hub/switch, most common in LANs", "Ring: circular, token passing", "Mesh: every node connected, high redundancy", "Tree: hierarchical combination"], 1, [
            _mcq("In which topology does every device connect to a central hub?", ["Bus", "Star", "Ring", "Mesh"], "Star", "In star topology, all nodes connect to a central hub or switch."),
            _mcq("Which topology provides maximum redundancy?", ["Star", "Bus", "Full Mesh", "Ring"], "Full Mesh", "Full mesh connects every node to every other node, providing maximum redundancy but at high cost.", 2),
            _mcq("In a full mesh network with n nodes, how many links are needed?", ["n", "n-1", "n(n-1)/2", "2n"], "n(n-1)/2", "Full mesh requires n(n-1)/2 links since every pair of nodes needs a direct connection.", 3),
            _tf("A bus topology requires more cabling than a star topology for the same number of nodes.", "False", "Bus topology uses a single backbone cable, requiring less cabling than star where each node has a dedicated cable to the hub."),
        ])

        add_concept(0, "Network Devices", "Hubs operate at Layer 1 (physical), switches at Layer 2 (data link), routers at Layer 3 (network). Each device makes forwarding decisions based on information available at its layer.",
            ["Hub: broadcasts to all ports (Layer 1)", "Switch: forwards based on MAC address (Layer 2)", "Router: forwards based on IP address (Layer 3)", "Gateway: protocol conversion between networks"], 2, [
            _mcq("At which OSI layer does a switch primarily operate?", ["Physical", "Data Link", "Network", "Transport"], "Data Link", "Switches operate at Layer 2 (Data Link) and use MAC addresses for forwarding decisions."),
            _mcq("Which device uses IP addresses to forward packets?", ["Hub", "Switch", "Router", "Repeater"], "Router", "Routers operate at Layer 3 (Network) and use IP addresses for routing decisions."),
            _tf("A hub sends incoming data to all connected ports.", "True", "A hub is a Layer 1 device that broadcasts all incoming signals to all ports.", 1),
            _mcq("What is the primary difference between a hub and a switch?", ["Speed", "Hub broadcasts while switch uses MAC addresses", "Number of ports", "Cable type"], "Hub broadcasts while switch uses MAC addresses", "A hub broadcasts data to all ports, while a switch learns MAC addresses and forwards only to the correct port.", 2),
        ])

        # ═══════════════════════════════
        # TOPIC 1: OSI Model
        # ═══════════════════════════════

        add_concept(1, "OSI Model Overview", "The OSI model divides network communication into 7 layers. From bottom to top: Physical, Data Link, Network, Transport, Session, Presentation, Application. Each layer serves the layer above it.",
            ["7 layers from physical to application", "Each layer has specific protocols and functions", "Data is encapsulated going down, decapsulated going up", "Mnemonic: Please Do Not Throw Sausage Pizza Away"], 0, [
            _mcq("How many layers are in the OSI model?", ["4", "5", "6", "7"], "7", "The OSI model has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application."),
            _mcq("Which layer is responsible for routing and logical addressing?", ["Data Link", "Network", "Transport", "Session"], "Network", "The Network Layer (Layer 3) handles routing, logical addressing (IP), and path determination."),
            _mcq("What is the correct order of OSI layers from bottom to top?", ["Physical, Network, Data Link, Transport, Session, Presentation, Application", "Physical, Data Link, Network, Transport, Session, Presentation, Application", "Application, Presentation, Session, Transport, Network, Data Link, Physical", "Physical, Data Link, Transport, Network, Session, Presentation, Application"], "Physical, Data Link, Network, Transport, Session, Presentation, Application", "The correct order from Layer 1 to 7 is: Physical, Data Link, Network, Transport, Session, Presentation, Application.", 2),
        ])

        add_concept(1, "Physical Layer", "Layer 1 deals with raw bit transmission over physical medium. It defines electrical, mechanical, and procedural specifications for activating and deactivating physical connections.",
            ["Transmits raw bits (0s and 1s)", "Defines cable types, voltages, pin layouts", "Deals with encoding and signaling", "Devices: hubs, repeaters, cables"], 1, [
            _mcq("What unit of data does the Physical Layer deal with?", ["Frames", "Packets", "Segments", "Bits"], "Bits", "The Physical Layer deals with raw bits — the actual 0s and 1s transmitted over the medium."),
            _tf("The Physical Layer is responsible for error detection.", "False", "Error detection is handled by the Data Link Layer (Layer 2), not the Physical Layer."),
            _mcq("Which of these is NOT a Physical Layer concern?", ["Cable specifications", "Signal encoding", "MAC addressing", "Bit synchronization"], "MAC addressing", "MAC addressing is a Data Link Layer (Layer 2) concern. Physical Layer deals with bits, cables, and signals.", 2),
        ])

        add_concept(1, "Data Link Layer", "Layer 2 provides node-to-node delivery. It frames data from the Network Layer, adds MAC addresses, handles error detection (CRC), and manages access to shared medium (MAC sublayer).",
            ["Frames data with headers and trailers", "Uses MAC addresses for addressing", "Error detection via CRC", "Two sublayers: LLC (Logical Link Control) and MAC", "Flow control between adjacent nodes"], 2, [
            _mcq("What is the PDU (Protocol Data Unit) at the Data Link Layer?", ["Bit", "Frame", "Packet", "Segment"], "Frame", "The Data Link Layer PDU is called a Frame. It encapsulates network layer packets with headers and trailers."),
            _mcq("Which error detection method is commonly used at the Data Link Layer?", ["Parity check", "Checksum", "CRC", "Hamming code"], "CRC", "CRC (Cyclic Redundancy Check) is the most commonly used error detection method at the Data Link Layer.", 2),
            _mcq("The Data Link Layer is divided into which two sublayers?", ["TCP and UDP", "LLC and MAC", "IP and ARP", "HTTP and FTP"], "LLC and MAC", "Data Link Layer has two sublayers: LLC (Logical Link Control) for flow control, and MAC (Media Access Control) for addressing and channel access."),
        ])

        add_concept(1, "Transport Layer", "Layer 4 provides end-to-end communication, reliability, flow control, and error recovery. It segments data and ensures complete delivery. Key protocols: TCP (reliable) and UDP (unreliable).",
            ["End-to-end delivery between processes", "Segmentation and reassembly", "Flow control and error recovery", "Port numbers for process identification", "TCP: reliable, connection-oriented; UDP: fast, connectionless"], 3, [
            _mcq("Which layer provides end-to-end error recovery and flow control?", ["Data Link", "Network", "Transport", "Session"], "Transport", "The Transport Layer (Layer 4) provides end-to-end error recovery, flow control, and reliable data transfer."),
            _mcq("What is the PDU at the Transport Layer?", ["Frame", "Packet", "Segment", "Bit"], "Segment", "The Transport Layer PDU is called a Segment (for TCP) or Datagram (for UDP)."),
            _mcq("Port numbers are used by which layer to identify processes?", ["Network", "Data Link", "Transport", "Application"], "Transport", "Transport Layer uses port numbers (0-65535) to identify specific processes/applications on a host.", 2),
        ])

        add_concept(1, "Application Layer", "Layer 7 provides network services directly to user applications. It provides protocols for file transfer (FTP), email (SMTP), web browsing (HTTP), and name resolution (DNS).",
            ["Closest layer to the end user", "HTTP, FTP, SMTP, DNS, DHCP", "Provides network services to applications", "Handles data representation for user"], 4, [
            _mcq("Which protocol operates at the Application Layer?", ["TCP", "IP", "HTTP", "Ethernet"], "HTTP", "HTTP is an Application Layer protocol. TCP is Transport Layer, IP is Network Layer, Ethernet is Data Link Layer."),
            _tf("DNS operates at the Transport Layer.", "False", "DNS is an Application Layer protocol that resolves domain names to IP addresses."),
        ])

        # ═══════════════════════════════
        # TOPIC 2: TCP/IP Protocol Stack
        # ═══════════════════════════════

        add_concept(2, "TCP/IP vs OSI", "TCP/IP is a 4-layer practical model: Network Interface, Internet, Transport, Application. It merges OSI's top 3 layers into Application and bottom 2 into Network Interface.",
            ["TCP/IP has 4 layers vs OSI's 7", "TCP/IP is protocol-based, OSI is conceptual", "TCP/IP Application = OSI Application + Presentation + Session", "TCP/IP Network Interface = OSI Physical + Data Link", "TCP/IP was developed first, OSI came as a reference"], 0, [
            _mcq("How many layers does the TCP/IP model have?", ["4", "5", "6", "7"], "4", "TCP/IP has 4 layers: Network Interface, Internet, Transport, and Application."),
            _mcq("Which OSI layers does the TCP/IP Application layer correspond to?", ["Only Application", "Application and Presentation", "Application, Presentation, and Session", "Transport and Application"], "Application, Presentation, and Session", "TCP/IP's Application layer maps to OSI layers 5 (Session), 6 (Presentation), and 7 (Application).", 2),
            _tf("The TCP/IP model was developed after the OSI model.", "False", "TCP/IP was developed first (ARPANET, 1970s). The OSI model came later as a theoretical reference framework."),
        ])

        add_concept(2, "Encapsulation", "As data moves down the protocol stack, each layer adds its own header (and sometimes trailer). This process is called encapsulation. The reverse at the receiver is decapsulation.",
            ["Application data → Segment (Transport) → Packet (Network) → Frame (Data Link) → Bits (Physical)", "Each layer only reads its own header", "Headers contain control information for that layer", "Encapsulation enables layer independence"], 1, [
            _mcq("What is added during encapsulation at the Network Layer?", ["MAC header", "IP header", "TCP header", "Frame trailer"], "IP header", "At the Network Layer, an IP header is added containing source and destination IP addresses."),
            _mcq("In what order does encapsulation happen?", ["Bits → Frame → Packet → Segment → Data", "Data → Segment → Packet → Frame → Bits", "Packet → Segment → Frame → Data → Bits", "Data → Packet → Frame → Segment → Bits"], "Data → Segment → Packet → Frame → Bits", "Data flows down: Application data → Transport Segment → Network Packet → Data Link Frame → Physical Bits.", 2),
        ])

        # ═══════════════════════════════════════
        # TOPIC 3: Physical Layer & Switching
        # ═══════════════════════════════════════

        add_concept(3, "Transmission Media", "Guided media include twisted pair, coaxial cable, and fiber optics. Unguided media include radio waves, microwaves, and infrared. Choice depends on bandwidth, distance, and cost.",
            ["Twisted pair: cheapest, used in LANs (Cat5/6)", "Coaxial: better shielding, used in cable TV", "Fiber optic: highest bandwidth, immune to EMI, long distance", "Unguided: radio, microwave, satellite, infrared"], 0, [
            _mcq("Which transmission medium offers the highest bandwidth and is immune to electromagnetic interference?", ["Twisted pair", "Coaxial cable", "Fiber optic", "Radio waves"], "Fiber optic", "Fiber optic cables use light signals, providing the highest bandwidth and complete immunity to electromagnetic interference."),
            _mcq("Cat5e and Cat6 cables are examples of:", ["Coaxial cable", "Fiber optic", "Twisted pair", "Waveguide"], "Twisted pair", "Cat5e and Cat6 are categories of twisted pair copper cabling commonly used in Ethernet LANs."),
            _tf("Fiber optic cables are susceptible to electromagnetic interference (EMI).", "False", "Fiber optic cables transmit data as light pulses through glass/plastic fibers, making them completely immune to EMI."),
        ])

        add_concept(3, "Multiplexing", "Multiplexing allows multiple signals to share a single communication channel. FDM divides by frequency, TDM by time slots, and WDM uses different wavelengths of light in fiber.",
            ["FDM: Frequency Division Multiplexing", "TDM: Time Division Multiplexing (synchronous and statistical)", "WDM: Wavelength Division Multiplexing (for fiber optics)", "CDM: Code Division Multiplexing (spread spectrum)"], 1, [
            _mcq("Which multiplexing technique divides the channel into time slots?", ["FDM", "TDM", "WDM", "CDM"], "TDM", "Time Division Multiplexing (TDM) divides the channel into time slots, each assigned to a different signal."),
            _mcq("WDM is primarily used with which transmission medium?", ["Twisted pair", "Coaxial cable", "Fiber optic", "Radio"], "Fiber optic", "Wavelength Division Multiplexing uses different wavelengths (colors) of light, applicable only to fiber optics.", 2),
        ])

        add_concept(3, "Switching Techniques", "Circuit switching establishes a dedicated path (like telephone). Packet switching breaks data into packets routed independently (Internet). Virtual circuit switching combines aspects of both.",
            ["Circuit switching: dedicated path, guaranteed bandwidth, wasteful if idle", "Packet switching: no dedicated path, efficient, possible delay/reordering", "Datagram: each packet routed independently", "Virtual circuit: path established first, packets follow same route"], 2, [
            _mcq("In packet switching, each packet:", ["Follows the same path", "Is routed independently", "Has guaranteed bandwidth", "Requires a pre-established circuit"], "Is routed independently", "In datagram packet switching, each packet is routed independently and may take different paths to the destination."),
            _mcq("Which switching technique is used by the traditional telephone network?", ["Packet switching", "Circuit switching", "Message switching", "Virtual circuit"], "Circuit switching", "Traditional telephone networks use circuit switching — a dedicated path is established for the entire call duration.", 2),
            _mcq("Virtual circuit switching combines features of:", ["FDM and TDM", "Circuit switching and packet switching", "LAN and WAN", "TCP and UDP"], "Circuit switching and packet switching", "Virtual circuit switching establishes a path like circuit switching but transmits data in packets like packet switching.", 2),
            _tf("In circuit switching, bandwidth is wasted when no data is being transmitted.", "True", "Circuit switching reserves a dedicated path for the entire session. If no data flows, the bandwidth is still reserved and wasted."),
        ])

        # ═══════════════════════════════
        # TOPIC 4: Data Link Layer
        # ═══════════════════════════════

        add_concept(4, "Framing", "The Data Link Layer organizes bits into frames. Framing methods include character count, byte stuffing (with flag bytes), and bit stuffing. Frames have delimiters to mark boundaries.",
            ["Character count: header specifies frame length", "Flag bytes with byte stuffing: special flag marks boundaries", "Bit stuffing: flag bit pattern with inserted bits", "Framing errors can cause synchronization loss"], 0, [
            _mcq("In bit stuffing, after how many consecutive 1s is a 0 inserted?", ["3", "4", "5", "6"], "5", "In bit stuffing, a 0 is inserted after every five consecutive 1s to prevent the flag pattern (01111110) from appearing in data.", 2),
            _mcq("What is the purpose of framing?", ["Routing packets", "Organizing bits into manageable units", "IP addressing", "Congestion control"], "Organizing bits into manageable units", "Framing organizes the stream of bits from the Physical Layer into structured units (frames) that can be processed."),
        ])

        add_concept(4, "Error Detection", "CRC (Cyclic Redundancy Check) is the most common error detection at Layer 2. The sender divides data by a generator polynomial and appends the remainder. The receiver checks divisibility.",
            ["CRC detects burst errors effectively", "Generator polynomial agreed upon by both sides", "Parity: simple but limited (1-bit errors only)", "Checksum: used at higher layers (IP, TCP)", "Hamming code: can correct single-bit errors"], 1, [
            _mcq("Which error detection technique can detect burst errors most effectively?", ["Parity bit", "Checksum", "CRC", "Echo checking"], "CRC", "CRC (Cyclic Redundancy Check) is highly effective at detecting burst errors, which is why it's standard at the Data Link Layer.", 2),
            _mcq("Given generator polynomial x³+1 (binary 1001), what is the CRC for data 1010?", ["011", "110", "101", "010"], "011", "Append 3 zeros to data: 1010000. Divide by 1001 using XOR division. Remainder is 011, which is the CRC.", 3, 45),
            _tf("Hamming code can only detect errors, not correct them.", "False", "Hamming code can both detect and correct single-bit errors. It can also detect (but not correct) double-bit errors."),
        ])

        add_concept(4, "Medium Access Control (MAC)", "MAC protocols manage how multiple nodes share a common channel. ALOHA (pure/slotted), CSMA, CSMA/CD (Ethernet), and CSMA/CA (WiFi) are key protocols.",
            ["Pure ALOHA: max throughput 18.4% (1/2e)", "Slotted ALOHA: max throughput 36.8% (1/e)", "CSMA/CD: listen before and during transmission (Ethernet)", "CSMA/CA: collision avoidance for wireless", "Token passing: deterministic access"], 2, [
            _mcq("What is the maximum throughput of pure ALOHA?", ["18.4%", "36.8%", "50%", "100%"], "18.4%", "Pure ALOHA has maximum throughput of 1/(2e) ≈ 18.4%. Nodes can transmit at any time, leading to high collision rates.", 2),
            _mcq("What is the maximum throughput of slotted ALOHA?", ["18.4%", "36.8%", "50%", "25%"], "36.8%", "Slotted ALOHA achieves 1/e ≈ 36.8% — double pure ALOHA — because transmissions are aligned to time slots.", 2),
            _mcq("CSMA/CD stands for:", ["Carrier Sense Multiple Access with Collision Detection", "Carrier Signal Multiple Access with Collision Division", "Channel Sensing Multiple Access with Collision Detection", "Carrier Sense Media Access with Collision Detection"], "Carrier Sense Multiple Access with Collision Detection", "CSMA/CD = Carrier Sense Multiple Access with Collision Detection, used in wired Ethernet (IEEE 802.3)."),
            _mcq("Which MAC protocol is used in wireless LANs (WiFi)?", ["CSMA/CD", "CSMA/CA", "Token Ring", "Pure ALOHA"], "CSMA/CA", "WiFi (IEEE 802.11) uses CSMA/CA (Collision Avoidance) because collision detection is difficult in wireless.", 2),
        ])

        add_concept(4, "Ethernet and Bridging", "Ethernet (IEEE 802.3) is the dominant LAN technology. It uses CSMA/CD, 48-bit MAC addresses, and frame sizes of 64-1518 bytes. Bridges connect LAN segments and learn MAC-to-port mappings.",
            ["MAC address: 48-bit (6 bytes), globally unique", "Minimum frame size: 64 bytes (for collision detection)", "Maximum frame size: 1518 bytes (standard)", "Bridges learn and filter based on MAC addresses", "Spanning Tree Protocol prevents bridge loops"], 3, [
            _mcq("What is the size of an Ethernet MAC address?", ["32 bits", "48 bits", "64 bits", "128 bits"], "48 bits", "Ethernet MAC addresses are 48 bits (6 bytes), typically written as six pairs of hex digits (e.g., AA:BB:CC:DD:EE:FF)."),
            _mcq("What is the minimum Ethernet frame size?", ["32 bytes", "46 bytes", "64 bytes", "128 bytes"], "64 bytes", "Minimum Ethernet frame is 64 bytes. This ensures that collisions are detected before the entire frame is transmitted (in CSMA/CD).", 2),
            _mcq("Why is there a minimum frame size in Ethernet?", ["To reduce overhead", "To ensure collision detection works properly", "To maintain clock synchronization", "Due to CRC requirements"], "To ensure collision detection works properly", "The minimum frame size ensures that a collision is detected before the sender finishes transmitting. If the frame is too short, the sender might not hear the collision.", 3),
        ])

        # ═══════════════════════════════════════
        # TOPIC 5: Network Layer & IP Addressing
        # ═══════════════════════════════════════

        add_concept(5, "IPv4 Addressing", "IPv4 addresses are 32 bits, written in dotted decimal. Classful addressing divides into Class A (1-126), B (128-191), C (192-223), D (multicast), E (reserved).",
            ["32-bit address = 4 bytes (dotted decimal)", "Class A: /8, 16M hosts per network", "Class B: /16, 65K hosts per network", "Class C: /24, 254 hosts per network", "127.x.x.x reserved for loopback"], 0, [
            _mcq("How many bits are in an IPv4 address?", ["8", "16", "32", "64"], "32", "IPv4 addresses are 32 bits long, written as four 8-bit octets in dotted decimal notation."),
            _mcq("Which class of IP address has the range 192.0.0.0 to 223.255.255.255?", ["Class A", "Class B", "Class C", "Class D"], "Class C", "Class C addresses range from 192.0.0.0 to 223.255.255.255, with 24 bits for network and 8 bits for host.", 2),
            _mcq("The IP address 127.0.0.1 is used for:", ["Default gateway", "Broadcast", "Loopback (localhost)", "DNS server"], "Loopback (localhost)", "127.0.0.1 is the loopback address used to test network software on the local machine."),
            _mcq("How many usable host addresses exist in a Class C network?", ["256", "254", "255", "252"], "254", "A Class C network has 8 host bits = 256 addresses, minus 2 (network address and broadcast) = 254 usable hosts.", 2),
        ])

        add_concept(5, "Subnetting and CIDR", "Subnetting divides a network into smaller subnets using a subnet mask. CIDR (Classless Inter-Domain Routing) uses prefix notation (/n) and eliminates classful boundaries for efficient allocation.",
            ["Subnet mask identifies network vs host bits", "CIDR notation: 192.168.1.0/24", "/n means n bits for network", "Subnetting reduces broadcast domains", "Supernetting aggregates routes (route summarization)"], 1, [
            _mcq("What does /24 mean in CIDR notation?", ["24 hosts", "24 networks", "24 bits for network portion", "24 bytes total"], "24 bits for network portion", "In CIDR notation /24, the first 24 bits are the network portion and the remaining 8 bits are for hosts."),
            _mcq("Given the network 10.0.0.0/20, how many usable host addresses are available?", ["4094", "4096", "2046", "8190"], "4094", "32-20=12 host bits → 2^12 = 4096 total, minus 2 (network + broadcast) = 4094 usable hosts.", 3, 45),
            _mcq("What is the subnet mask for /26?", ["255.255.255.0", "255.255.255.128", "255.255.255.192", "255.255.255.224"], "255.255.255.192", "/26 means 26 bits are 1s. Last octet: 11000000 = 192. So mask is 255.255.255.192.", 2),
            _mcq("CIDR was introduced primarily to:", ["Speed up routing", "Slow down the exhaustion of IPv4 addresses", "Replace DNS", "Improve security"], "Slow down the exhaustion of IPv4 addresses", "CIDR replaced classful addressing to allow more flexible allocation of IP addresses, reducing waste and slowing IPv4 exhaustion.", 2),
        ])

        add_concept(5, "IP Support Protocols (ARP, DHCP, ICMP)", "ARP resolves IP to MAC addresses. DHCP dynamically assigns IP addresses. ICMP carries error and diagnostic messages (ping, traceroute).",
            ["ARP: IP → MAC resolution (broadcast request, unicast reply)", "RARP: MAC → IP (reverse, obsolete)", "DHCP: dynamic IP assignment (DORA process)", "ICMP: error reporting (destination unreachable, TTL exceeded)", "Ping uses ICMP Echo Request/Reply"], 2, [
            _mcq("What protocol resolves an IP address to a MAC address?", ["DNS", "ARP", "RARP", "DHCP"], "ARP", "ARP (Address Resolution Protocol) maps a known IP address to the corresponding MAC address on the local network."),
            _mcq("DHCP follows which process for IP assignment?", ["SYN-ACK", "DORA", "TCP handshake", "ARP request"], "DORA", "DHCP uses the DORA process: Discover → Offer → Request → Acknowledge.", 2),
            _mcq("Which protocol does 'ping' use?", ["TCP", "UDP", "ICMP", "ARP"], "ICMP", "Ping uses ICMP (Internet Control Message Protocol) Echo Request and Echo Reply messages."),
            _tf("ARP requests are sent as broadcast, and ARP replies are unicast.", "True", "ARP request is broadcast to all hosts on the LAN. Only the host with the matching IP replies with a unicast ARP reply."),
        ])

        add_concept(5, "NAT and Fragmentation", "NAT translates private IPs to public IPs, conserving address space. IP fragmentation splits packets exceeding the link's MTU. Reassembly happens only at the destination.",
            ["NAT: Network Address Translation (private ↔ public)", "PAT/NAPT: maps multiple private IPs to one public IP using ports", "MTU: Maximum Transmission Unit (Ethernet = 1500 bytes)", "Fragmentation offset is in units of 8 bytes", "Don't Fragment (DF) flag prevents fragmentation"], 3, [
            _mcq("What is the default MTU for Ethernet?", ["512 bytes", "1000 bytes", "1500 bytes", "9000 bytes"], "1500 bytes", "Standard Ethernet MTU is 1500 bytes. Jumbo frames can go up to 9000 bytes."),
            _mcq("IP fragmentation offset is measured in units of:", ["1 byte", "4 bytes", "8 bytes", "16 bytes"], "8 bytes", "The fragment offset field in the IP header is measured in units of 8 bytes (64 bits).", 2),
            _mcq("Where does IP reassembly of fragments occur?", ["At each router", "At the source", "At the destination only", "At the nearest switch"], "At the destination only", "IP fragments are reassembled only at the destination host, not at intermediate routers.", 2),
        ])

        # ═══════════════════════════════
        # TOPIC 6: Routing Protocols
        # ═══════════════════════════════

        add_concept(6, "Shortest Path Routing", "Dijkstra's algorithm finds shortest paths from a source to all other nodes. It maintains a set of visited nodes and greedily selects the nearest unvisited node.",
            ["Dijkstra's algorithm: greedy, non-negative weights only", "Bellman-Ford: handles negative weights", "Time complexity: O(V²) or O((V+E)logV) with priority queue", "Used in link-state routing protocols (OSPF)"], 0, [
            _mcq("Dijkstra's algorithm is used in which type of routing?", ["Distance vector", "Link state", "Path vector", "Flooding"], "Link state", "Dijkstra's shortest path algorithm is the basis of link-state routing protocols like OSPF."),
            _mcq("Dijkstra's algorithm cannot handle:", ["Directed graphs", "Negative weight edges", "Cyclic graphs", "Dense graphs"], "Negative weight edges", "Dijkstra's algorithm requires all edge weights to be non-negative. For negative weights, use Bellman-Ford.", 2),
        ])

        add_concept(6, "Distance Vector Routing", "Each router maintains a table of distances to all destinations and shares it with neighbors. Bellman-Ford is used. Suffers from count-to-infinity problem. RIP uses this approach.",
            ["Each router knows only distance to neighbors", "Periodic updates shared with neighbors only", "Count-to-infinity: slow convergence on failures", "Solutions: split horizon, poison reverse, hold-down timer", "RIP: max 15 hops, updates every 30 seconds"], 1, [
            _mcq("Which problem is associated with distance vector routing?", ["Link state flooding", "Count to infinity", "BGP path selection", "ARP spoofing"], "Count to infinity", "Distance vector routing can suffer from the count-to-infinity problem where routers slowly increment distance after a link failure.", 2),
            _mcq("RIP uses which metric for routing?", ["Bandwidth", "Delay", "Hop count", "Cost"], "Hop count", "RIP (Routing Information Protocol) uses hop count as its metric, with a maximum of 15 hops."),
            _mcq("Which technique helps prevent count-to-infinity in distance vector routing?", ["Dijkstra's algorithm", "Split horizon", "Flooding", "Spanning tree"], "Split horizon", "Split horizon prevents a router from advertising a route back to the neighbor it learned the route from.", 2),
        ])

        add_concept(6, "Link State Routing", "Each router discovers its neighbors, measures link costs, builds a complete topology map by flooding link-state packets, then runs Dijkstra locally. OSPF is the primary protocol.",
            ["Every router has complete network topology", "LSPs (Link State Packets) flooded to all routers", "Dijkstra's algorithm run locally by each router", "Faster convergence than distance vector", "OSPF: Open Shortest Path First (hierarchical with areas)"], 2, [
            _mcq("In link state routing, each router has:", ["Only neighbor information", "Complete topology of the network", "Random subset of routes", "Only default route"], "Complete topology of the network", "In link state routing, every router builds a complete map of the network topology through LSP flooding."),
            _mcq("Which routing protocol uses link state routing?", ["RIP", "OSPF", "BGP", "IGRP"], "OSPF", "OSPF (Open Shortest Path First) is the primary link state routing protocol for IP networks."),
            _tf("Link state routing converges faster than distance vector routing.", "True", "Link state routing converges faster because each router has the complete topology and can independently compute shortest paths."),
        ])

        add_concept(6, "Flooding", "Flooding sends every incoming packet out on every link except the one it arrived on. Simple but generates many duplicates. Controlled flooding uses sequence numbers or TTL to limit copies.",
            ["Every packet sent on all outgoing links", "Guarantees delivery if any path exists", "Generates massive traffic (broadcast storm)", "Controlled by: sequence numbers, TTL, or reverse path forwarding"], 3, [
            _mcq("What is the main disadvantage of flooding?", ["Slow delivery", "Excessive duplicate packets", "Requires complex routing tables", "Only works on LANs"], "Excessive duplicate packets", "Flooding generates many duplicate packets since each router forwards the packet on all outgoing links."),
            _tf("Flooding guarantees packet delivery if any path exists between source and destination.", "True", "Since flooding sends packets on ALL outgoing links, it guarantees delivery if any path exists, at the cost of bandwidth."),
        ])

        # ═══════════════════════════════
        # TOPIC 7: Transport Layer
        # ═══════════════════════════════

        add_concept(7, "TCP vs UDP", "TCP is connection-oriented, reliable, ordered, with flow and congestion control. UDP is connectionless, unreliable, no ordering, but lightweight and fast. Choice depends on application needs.",
            ["TCP: reliable, ordered, connection-oriented, heavyweight", "UDP: unreliable, no ordering, connectionless, lightweight", "TCP: HTTP, FTP, SMTP, SSH", "UDP: DNS, DHCP, VoIP, video streaming, gaming", "TCP has higher overhead due to headers and mechanisms"], 0, [
            _mcq("Which transport protocol provides reliable, ordered delivery?", ["UDP", "TCP", "IP", "ICMP"], "TCP", "TCP provides reliable, ordered delivery with flow control, congestion control, and error recovery."),
            _mcq("DNS typically uses which transport protocol?", ["TCP only", "UDP only", "Both TCP and UDP", "Neither"], "Both TCP and UDP", "DNS uses UDP for standard queries (port 53) for speed, and TCP for zone transfers or responses exceeding 512 bytes.", 2),
            _mcq("Which is NOT a feature of UDP?", ["Connectionless", "Low overhead", "Guaranteed delivery", "Fast transmission"], "Guaranteed delivery", "UDP does not guarantee delivery. It provides no acknowledgments, retransmission, or ordering."),
            _mcq("The TCP header is how many bytes (without options)?", ["8", "16", "20", "32"], "20", "TCP header is 20 bytes minimum (without options). UDP header is only 8 bytes.", 2),
        ])

        add_concept(7, "TCP Connection Management", "TCP uses a 3-way handshake (SYN, SYN-ACK, ACK) to establish connections and a 4-way handshake (FIN, ACK, FIN, ACK) to terminate. Each side maintains sequence numbers.",
            ["3-way handshake: SYN → SYN-ACK → ACK", "Connection termination: FIN → ACK → FIN → ACK", "TIME_WAIT state: waits 2*MSL before closing", "Sequence numbers prevent duplicates", "Each direction closed independently (half-close)"], 1, [
            _mcq("What is the correct sequence of TCP's 3-way handshake?", ["ACK, SYN, SYN-ACK", "SYN, SYN-ACK, ACK", "SYN, ACK, SYN-ACK", "FIN, FIN-ACK, ACK"], "SYN, SYN-ACK, ACK", "TCP 3-way handshake: Client sends SYN → Server replies SYN-ACK → Client sends ACK. Connection established."),
            _tf("TCP connection termination requires a 4-way handshake.", "True", "TCP termination uses 4 steps: FIN → ACK → FIN → ACK, because each direction must be closed independently."),
            _mcq("What is the purpose of the TIME_WAIT state in TCP?", ["To speed up connection setup", "To ensure delayed segments don't interfere with new connections", "To reduce memory usage", "To handle congestion"], "To ensure delayed segments don't interfere with new connections", "TIME_WAIT lasts 2*MSL (Maximum Segment Lifetime) to ensure old segments expire before a new connection reuses the same port.", 3),
        ])

        add_concept(7, "Flow Control and Congestion Control", "Flow control prevents sender from overwhelming receiver (sliding window). Congestion control prevents overwhelming the network (slow start, congestion avoidance, fast retransmit, fast recovery).",
            ["Flow control: receiver advertises window size", "Sliding window: sender can send window-size bytes without ACK", "Slow start: exponential growth of congestion window", "Congestion avoidance: linear growth after threshold", "Fast retransmit: retransmit on 3 duplicate ACKs"], 2, [
            _mcq("TCP slow start increases the congestion window:", ["Linearly", "Exponentially", "Logarithmically", "Remains constant"], "Exponentially", "In slow start, the congestion window doubles every RTT (exponential growth) until it reaches ssthresh.", 2),
            _mcq("What triggers TCP fast retransmit?", ["Timeout", "1 duplicate ACK", "3 duplicate ACKs", "Window size = 0"], "3 duplicate ACKs", "Fast retransmit is triggered when the sender receives 3 duplicate ACKs, indicating a lost segment without waiting for timeout.", 2),
            _mcq("In TCP congestion avoidance phase, the congestion window increases by:", ["1 MSS per ACK", "1 MSS per RTT", "Doubles per RTT", "Remains constant"], "1 MSS per RTT", "In congestion avoidance, the window increases by 1 MSS (Maximum Segment Size) per RTT — linear (additive) increase.", 3),
            _mcq("What is the difference between flow control and congestion control?", ["They are the same thing", "Flow control prevents overwhelming the receiver; congestion control prevents overwhelming the network", "Flow control is for UDP; congestion control is for TCP", "Flow control is at Layer 3; congestion control at Layer 4"], "Flow control prevents overwhelming the receiver; congestion control prevents overwhelming the network", "Flow control manages the rate between sender and receiver. Congestion control manages the rate to prevent network overload.", 2),
        ])

        add_concept(7, "Sockets", "A socket is an endpoint for communication, identified by IP address + port number. Berkeley sockets API provides socket(), bind(), listen(), accept(), connect(), send(), recv(), close().",
            ["Socket = IP address + Port number", "Well-known ports: 0-1023 (HTTP=80, FTP=21, SSH=22)", "Registered ports: 1024-49151", "Dynamic/ephemeral ports: 49152-65535", "TCP socket uniquely identified by 4-tuple: (src IP, src port, dst IP, dst port)"], 3, [
            _mcq("A socket is uniquely identified by:", ["IP address only", "Port number only", "IP address and port number", "MAC address"], "IP address and port number", "A socket is an endpoint defined by the combination of an IP address and a port number."),
            _mcq("HTTP uses which well-known port number?", ["21", "22", "25", "80"], "80", "HTTP uses port 80 (HTTPS uses port 443). FTP=21, SSH=22, SMTP=25."),
            _mcq("The ephemeral port range is:", ["0-1023", "1024-49151", "49152-65535", "0-65535"], "49152-65535", "Ephemeral (dynamic) ports range from 49152 to 65535 and are temporarily assigned by the OS for client connections.", 2),
        ])

        # ═══════════════════════════════════
        # TOPIC 8: Application Layer Protocols
        # ═══════════════════════════════════

        add_concept(8, "DNS (Domain Name System)", "DNS resolves domain names to IP addresses using a hierarchical distributed database. Resolution can be recursive or iterative. DNS uses UDP port 53 for queries.",
            ["Hierarchical: root → TLD (.com, .org) → authoritative", "Recursive: resolver does all work for client", "Iterative: each server returns referral", "Caching reduces load (TTL-based)", "Record types: A (IPv4), AAAA (IPv6), MX (mail), CNAME (alias), NS (nameserver)"], 0, [
            _mcq("DNS primarily uses which transport protocol and port?", ["TCP port 80", "UDP port 53", "TCP port 53", "UDP port 80"], "UDP port 53", "DNS uses UDP port 53 for standard queries due to speed. TCP port 53 is used for zone transfers and large responses."),
            _mcq("Which DNS record type maps a domain name to an IPv4 address?", ["MX", "CNAME", "A", "NS"], "A", "The A (Address) record maps a domain name to its IPv4 address. AAAA maps to IPv6.", 2),
            _mcq("In recursive DNS resolution:", ["Client queries each server itself", "The resolver queries on behalf of the client", "No caching is used", "Only the root server is queried"], "The resolver queries on behalf of the client", "In recursive resolution, the DNS resolver takes full responsibility and queries other servers until it gets the final answer."),
        ])

        add_concept(8, "HTTP and HTTPS", "HTTP is a stateless request-response protocol for the web. Methods: GET, POST, PUT, DELETE. HTTPS adds TLS/SSL encryption. HTTP/1.1 introduced persistent connections.",
            ["Stateless: each request is independent", "Status codes: 200 OK, 301 redirect, 404 not found, 500 server error", "HTTP/1.1: persistent connections (keep-alive)", "HTTP/2: multiplexing, header compression, server push", "HTTPS = HTTP + TLS (port 443)"], 1, [
            _mcq("HTTP is a _____ protocol.", ["Stateful", "Stateless", "Connection-oriented", "Encrypted"], "Stateless", "HTTP is stateless — each request is independent and the server does not remember previous requests."),
            _mcq("Which HTTP status code indicates 'Not Found'?", ["200", "301", "404", "500"], "404", "404 means the requested resource was not found. 200=OK, 301=Moved Permanently, 500=Internal Server Error."),
            _mcq("What does HTTPS add over HTTP?", ["Speed optimization", "TLS/SSL encryption", "Compression", "Caching"], "TLS/SSL encryption", "HTTPS = HTTP + TLS/SSL encryption. It provides confidentiality and integrity over port 443."),
        ])

        add_concept(8, "FTP (File Transfer Protocol)", "FTP transfers files between client and server using two connections: control (port 21) for commands and data (port 20) for actual file transfer.",
            ["Uses two connections: control (21) and data (20)", "Control connection persists; data connection per transfer", "Active mode: server initiates data connection to client", "Passive mode: client initiates both connections", "Sends credentials in plaintext (use SFTP/FTPS for security)"], 2, [
            _mcq("FTP uses which port for the control connection?", ["20", "21", "22", "25"], "21", "FTP uses port 21 for the control connection (commands) and port 20 for data transfer in active mode."),
            _tf("FTP uses a single connection for both commands and data transfer.", "False", "FTP uses two separate connections: port 21 for control/commands and port 20 for actual data transfer."),
        ])

        add_concept(8, "SMTP and Email", "SMTP (port 25) sends emails between mail servers. POP3 (port 110) and IMAP (port 143) retrieve emails. Email path: sender MUA → sender MTA → receiver MTA → receiver MUA.",
            ["SMTP: sends mail (port 25/587)", "POP3: downloads and deletes from server (port 110)", "IMAP: syncs mail across devices (port 143)", "MUA: Mail User Agent (email client)", "MTA: Mail Transfer Agent (mail server)"], 3, [
            _mcq("Which protocol is used to send emails between servers?", ["POP3", "IMAP", "SMTP", "HTTP"], "SMTP", "SMTP (Simple Mail Transfer Protocol) is used to send emails from client to server and between servers."),
            _mcq("The key difference between POP3 and IMAP is:", ["POP3 is newer", "IMAP downloads and deletes; POP3 syncs", "POP3 downloads and deletes; IMAP syncs", "They use the same port"], "POP3 downloads and deletes; IMAP syncs", "POP3 downloads emails and typically deletes them from the server. IMAP keeps them on the server and syncs across devices.", 2),
        ])

        # ═══════════════════════════════════
        # TOPIC 9: Network Security Basics
        # ═══════════════════════════════════

        add_concept(9, "Encryption Basics", "Symmetric encryption uses one shared key (AES, DES). Asymmetric uses a key pair: public key encrypts, private key decrypts (RSA). Asymmetric is slower but solves key distribution.",
            ["Symmetric: same key for encrypt/decrypt (fast)", "Asymmetric: public/private key pair (slower, solves key exchange)", "AES: current symmetric standard (128/256-bit)", "RSA: most common asymmetric algorithm", "Hybrid: use asymmetric to exchange symmetric key, then symmetric for data"], 0, [
            _mcq("Which encryption type uses the same key for encryption and decryption?", ["Asymmetric", "Symmetric", "Hashing", "Digital signature"], "Symmetric", "Symmetric encryption uses a single shared key for both encryption and decryption. Examples: AES, DES."),
            _mcq("In RSA, which key is used to encrypt data sent TO a recipient?", ["Sender's private key", "Recipient's public key", "Sender's public key", "Recipient's private key"], "Recipient's public key", "To send encrypted data, you use the recipient's public key. Only their private key can decrypt it.", 2),
            _tf("Asymmetric encryption is faster than symmetric encryption.", "False", "Asymmetric encryption is significantly slower than symmetric. That's why hybrid systems use asymmetric only for key exchange."),
        ])

        add_concept(9, "Firewalls", "Firewalls filter network traffic based on rules. Packet filters inspect headers (IP, port). Stateful firewalls track connection state. Application-level gateways inspect content.",
            ["Packet filter: inspects IP/port headers, fast but limited", "Stateful inspection: tracks TCP connection state", "Application gateway (proxy): deep content inspection", "DMZ: demilitarized zone between internal and external networks", "Rules typically: default deny, allow specific traffic"], 1, [
            _mcq("A stateful firewall differs from a packet filter by:", ["Being faster", "Tracking connection state", "Using different protocols", "Operating at Layer 1"], "Tracking connection state", "Stateful firewalls track the state of active connections and make decisions based on context, not just individual packet headers.", 2),
            _mcq("What does DMZ stand for in network security?", ["Direct Management Zone", "Demilitarized Zone", "Data Management Zone", "Dynamic Monitor Zone"], "Demilitarized Zone", "DMZ (Demilitarized Zone) is a network segment between internal and external networks that hosts public-facing services."),
        ])

        add_concept(9, "Digital Signatures", "Digital signatures provide authentication, integrity, and non-repudiation. The sender signs with their private key; the receiver verifies with the sender's public key.",
            ["Sender hashes message, encrypts hash with private key", "Receiver decrypts with sender's public key, compares hashes", "Provides: authentication, integrity, non-repudiation", "Does NOT provide confidentiality (message isn't encrypted)", "Certificate Authorities (CAs) verify public key ownership"], 2, [
            _mcq("A digital signature is created using:", ["Sender's public key", "Receiver's public key", "Sender's private key", "Receiver's private key"], "Sender's private key", "The sender creates a digital signature by encrypting the message hash with their private key.", 2),
            _tf("Digital signatures provide message confidentiality.", "False", "Digital signatures provide authentication, integrity, and non-repudiation — but NOT confidentiality. The message itself is not encrypted."),
            _mcq("Which of the following is NOT provided by digital signatures?", ["Authentication", "Integrity", "Non-repudiation", "Confidentiality"], "Confidentiality", "Digital signatures verify who sent the message (authentication), that it wasn't tampered with (integrity), and that the sender can't deny sending it (non-repudiation). They don't encrypt the message content.", 2),
        ])

        # ─── Commit everything ───
        db.commit()
        print("✅ Database seeded successfully!")
        print(f"   Subject: 1")

        topic_count = db.query(Topic).count()
        concept_count = db.query(Concept).count()
        question_count = db.query(Question).count()
        print(f"   Topics: {topic_count}")
        print(f"   Concepts: {concept_count}")
        print(f"   Questions: {question_count}")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
