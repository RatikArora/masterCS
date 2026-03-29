"""
Seed script: Add GATE-level questions for thin Computer Networks concepts.
Total: 80 new questions across 11 concepts.
"""

from app.db.session import SessionLocal
from sqlalchemy import text
import json
import uuid

# ── Concept IDs ──────────────────────────────────────────────────────────────
FLOODING       = "56544f9e-d67a-447f-9095-37c505979ae7"
FRAMING        = "86b966fc-8bfd-461f-9e0c-fa71e20e306a"
SMTP_EMAIL     = "280de3f3-346f-4fc1-9b35-b6dd78da52a1"
SOCKETS        = "6e10a303-6913-42fd-9584-9610fed53250"
FTP            = "893ecf7b-d4d5-4929-8318-be7a6d60eaa3"
PHYSICAL       = "671bcbfd-1ba7-4a1f-aa25-fcb9fe253c10"
DLL            = "8db98554-de1c-4d8f-9192-d41073310575"
APP_LAYER      = "fe0a3e22-8b10-4966-8ce5-4cc0b2e341db"
TCP_UDP        = "7c0a45dc-ad19-46ed-8b26-3052a8515904"
TRANSPORT      = "b29551a9-8148-4074-a972-aa899ab58266"
IP_SUPPORT     = "3f93ad03-347b-41c4-8ce7-39b0bdff1337"

questions = []

# ═══════════════════════════════════════════════════════════════════════════════
# 1. FLOODING — 10 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": FLOODING,
        "text": "In a network with 8 routers, a source floods a packet with TTL = 3. What is the maximum number of hops the packet can traverse before being discarded?",
        "difficulty": 2,
        "options": {"A": "3 hops from the source router", "B": "8 hops from the source router", "C": "7 hops from the source router", "D": "4 hops from the source router"},
        "correct_answer": "A",
        "explanation": "TTL limits the hop count; packet is discarded when TTL reaches 0 after 3 hops."
    },
    {
        "concept_id": FLOODING,
        "text": "Which technique does Reverse Path Forwarding (RPF) use to prevent duplicate flooding packets in a network?",
        "difficulty": 2,
        "options": {"A": "Forwards only if packet arrived on the shortest path interface", "B": "Maintains a complete routing table of all destinations seen", "C": "Uses cryptographic hashing to verify packet source identity", "D": "Assigns unique sequence numbers to each forwarded data packet"},
        "correct_answer": "A",
        "explanation": "RPF accepts a packet only if it arrives on the interface used to reach the source, ensuring loop-free forwarding."
    },
    {
        "concept_id": FLOODING,
        "text": "Sequence-number controlled flooding avoids broadcast storms by requiring each router to:",
        "difficulty": 2,
        "options": {"A": "discard packets with a previously seen (source, seq) pair", "B": "forward packets only along the shortest-path spanning tree", "C": "limit the total number of outgoing copies to at most two", "D": "increment the TTL field before forwarding packet onward"},
        "correct_answer": "A",
        "explanation": "Routers track (source, sequence-number) pairs and drop duplicates, preventing infinite retransmissions."
    },
    {
        "concept_id": FLOODING,
        "text": "A fully connected mesh network has 6 nodes. If Node A initiates uncontrolled flooding (no TTL, no sequence numbers), what problem occurs?",
        "difficulty": 1,
        "options": {"A": "Packets circulate indefinitely causing a broadcast storm", "B": "Only adjacent neighbors receive the flooded data packet", "C": "The network partitions into two separate flooding zones", "D": "Packets are automatically routed via the shortest path"},
        "correct_answer": "A",
        "explanation": "Without any loop-prevention mechanism, packets bounce between nodes forever, causing a broadcast storm."
    },
    {
        "concept_id": FLOODING,
        "text": "In selective flooding, a router forwards an incoming packet only on:",
        "difficulty": 2,
        "options": {"A": "the single interface leading to destination", "B": "all interfaces including the arrival interface", "C": "interfaces in the approximate direction of destination", "D": "interfaces that have the lowest congestion levels"},
        "correct_answer": "C",
        "explanation": "Selective flooding forwards on lines going approximately in the right direction, reducing traffic over pure flooding."
    },
    {
        "concept_id": FLOODING,
        "text": "Which of the following is **NOT** an advantage of flooding as a routing technique?",
        "difficulty": 1,
        "options": {"A": "Extremely robust against node failures", "B": "Guarantees shortest-path delivery always", "C": "Highly efficient in bandwidth utilization", "D": "Requires no routing table maintenance"},
        "correct_answer": "C",
        "explanation": "Flooding wastes significant bandwidth by sending many duplicate copies; efficiency is its main drawback."
    },
    {
        "concept_id": FLOODING,
        "text": "A spanning tree overlay is constructed for flooding to primarily achieve which goal?",
        "difficulty": 3,
        "options": {"A": "Eliminate all redundant packet copies in the network", "B": "Reduce latency by selecting the fastest network links", "C": "Increase reliability by adding extra forwarding pathways", "D": "Authenticate the source of each flooded network packet"},
        "correct_answer": "A",
        "explanation": "A spanning tree ensures each node receives exactly one copy, eliminating loops and duplicate packets."
    },
    {
        "concept_id": FLOODING,
        "text": "In a network of N routers with average degree d, the number of duplicate packets generated by uncontrolled flooding of one packet is approximately:",
        "difficulty": 3,
        "options": {"A": "O(N × d) duplicate copies generated", "B": "O(N) duplicate copies generated total", "C": "O(d²) duplicate copies generated total", "D": "O(log N) duplicate copies generated"},
        "correct_answer": "A",
        "explanation": "Each of N routers forwards on d links, generating O(N×d) copies minus the original N-1 needed."
    },
    {
        "concept_id": FLOODING,
        "text": "Controlled flooding using TTL is considered inferior to sequence-number flooding because:",
        "difficulty": 3,
        "options": {"A": "TTL-based flooding still permits many duplicate copies within the TTL horizon", "B": "TTL-based flooding cannot reach nodes that are within the specified hop limit", "C": "TTL values are not supported by modern Internet Protocol packet headers", "D": "TTL-based flooding requires pre-computed routing tables at every router"},
        "correct_answer": "A",
        "explanation": "TTL limits distance but doesn't prevent duplicates within that radius; sequence numbers eliminate duplicates."
    },
    {
        "concept_id": FLOODING,
        "text": "Which protocol uses a variant of controlled flooding with sequence numbers to distribute link-state information?",
        "difficulty": 2,
        "options": {"A": "RIP (Routing Information Protocol)", "B": "OSPF (Open Shortest Path First)", "C": "BGP (Border Gateway Protocol)", "D": "EIGRP (Enhanced Interior Gateway)"},
        "correct_answer": "B",
        "explanation": "OSPF uses reliable flooding with sequence numbers to distribute LSAs across the network area."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 2. FRAMING — 10 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": FRAMING,
        "text": "In bit stuffing used by HDLC, a `0` is inserted after every sequence of how many consecutive `1`s in the data?",
        "difficulty": 1,
        "options": {"A": "After every 4 consecutive 1 bits", "B": "After every 5 consecutive 1 bits", "C": "After every 6 consecutive 1 bits", "D": "After every 7 consecutive 1 bits"},
        "correct_answer": "B",
        "explanation": "HDLC inserts a 0 after five consecutive 1s to prevent the flag pattern `01111110` from appearing in data."
    },
    {
        "concept_id": FRAMING,
        "text": "The original data stream is `01111110 01111100`. After HDLC bit stuffing, how many bits are added?",
        "difficulty": 3,
        "options": {"A": "Exactly 1 bit is inserted into the stream", "B": "Exactly 2 bits are inserted into the stream", "C": "Exactly 3 bits are inserted into the stream", "D": "Exactly 4 bits are inserted into the stream"},
        "correct_answer": "C",
        "explanation": "First byte has `11111` → stuff 1 bit; second byte has `11111` → stuff 1 bit; continued `1` makes another → 3 stuffed bits total."
    },
    {
        "concept_id": FRAMING,
        "text": "In byte-stuffing (character stuffing), if the flag byte is `0x7E` and escape byte is `0x7D`, how is a data byte `0x7E` transmitted?",
        "difficulty": 2,
        "options": {"A": "Replaced by the two-byte sequence 0x7D 0x5E", "B": "Replaced by the two-byte sequence 0x7E 0x7E", "C": "Replaced by the two-byte sequence 0x7D 0x7D", "D": "Replaced by the three-byte sequence 0x7D 0x7E 0x5E"},
        "correct_answer": "A",
        "explanation": "PPP byte stuffing replaces 0x7E with 0x7D followed by 0x5E (XOR with 0x20)."
    },
    {
        "concept_id": FRAMING,
        "text": "Which framing method uses a special bit pattern `01111110` as the frame delimiter at both ends of a frame?",
        "difficulty": 1,
        "options": {"A": "Character count framing method", "B": "HDLC flag-based framing method", "C": "Length field based framing method", "D": "UTF-8 sentinel framing method"},
        "correct_answer": "B",
        "explanation": "HDLC uses the flag byte 01111110 (0x7E) to mark frame boundaries."
    },
    {
        "concept_id": FRAMING,
        "text": "A major disadvantage of character-count framing is that:",
        "difficulty": 2,
        "options": {"A": "a corrupted count field causes loss of frame synchronization", "B": "it cannot be used with any binary data transmission protocol", "C": "it requires bit-stuffing which adds significant data overhead", "D": "it only works with fixed-size frames of predetermined length"},
        "correct_answer": "A",
        "explanation": "If the count field is corrupted, the receiver cannot find the next frame boundary, losing synchronization."
    },
    {
        "concept_id": FRAMING,
        "text": "PPP (Point-to-Point Protocol) uses which framing technique to handle transparency?",
        "difficulty": 2,
        "options": {"A": "Bit stuffing after five ones", "B": "Byte stuffing with escape codes", "C": "Character count in the header", "D": "Fixed-length frame boundaries"},
        "correct_answer": "B",
        "explanation": "PPP uses byte stuffing with 0x7D as escape byte to achieve data transparency."
    },
    {
        "concept_id": FRAMING,
        "text": "If 500 bytes of payload contain 12 occurrences of the flag byte (0x7E) and 3 occurrences of escape byte (0x7D), the overhead added by byte stuffing is:",
        "difficulty": 3,
        "options": {"A": "12 extra bytes are added total", "B": "15 extra bytes are added total", "C": "24 extra bytes are added total", "D": "30 extra bytes are added total"},
        "correct_answer": "B",
        "explanation": "Each flag/escape byte in data requires one extra escape byte: 12 + 3 = 15 bytes overhead."
    },
    {
        "concept_id": FRAMING,
        "text": "The Frame Check Sequence (FCS) field in a data link frame is primarily used for:",
        "difficulty": 1,
        "options": {"A": "detecting transmission errors using CRC", "B": "encrypting the frame payload for security", "C": "indicating the frame's priority in queue", "D": "identifying the network layer protocol type"},
        "correct_answer": "A",
        "explanation": "FCS contains a CRC value used to detect bit errors introduced during transmission."
    },
    {
        "concept_id": FRAMING,
        "text": "In HDLC, the frame format includes flag, address, control, data, FCS, and flag. What is the minimum frame size excluding flags?",
        "difficulty": 3,
        "options": {"A": "2 bytes (address + control only)", "B": "4 bytes (address + control + FCS)", "C": "6 bytes (addr + ctrl + data + FCS)", "D": "8 bytes (full minimum HDLC frame)"},
        "correct_answer": "B",
        "explanation": "Minimum HDLC frame has 1-byte address, 1-byte control, 2-byte FCS = 4 bytes (data can be empty)."
    },
    {
        "concept_id": FRAMING,
        "text": "Length-field based framing (as used in some protocols) embeds the frame length in the header. Compared to flag-based framing, this approach:",
        "difficulty": 2,
        "options": {"A": "avoids the need for any stuffing but is error-sensitive", "B": "requires both bit stuffing and a length verification step", "C": "cannot support variable-length frames in any configuration", "D": "is immune to single-bit errors in the frame header field"},
        "correct_answer": "A",
        "explanation": "Length fields eliminate stuffing overhead but a corrupted length field causes desynchronization."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 3. SMTP AND EMAIL — 10 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": SMTP_EMAIL,
        "text": "Which SMTP command is used to specify the sender's email address during a mail transaction?",
        "difficulty": 1,
        "options": {"A": "HELO sender@domain.com command", "B": "MAIL FROM:<sender@domain.com>", "C": "RCPT TO:<sender@domain.com>", "D": "SEND FROM:<sender@domain.com>"},
        "correct_answer": "B",
        "explanation": "MAIL FROM specifies the reverse-path (sender's address) for the mail transaction."
    },
    {
        "concept_id": SMTP_EMAIL,
        "text": "IMAP differs from POP3 primarily because IMAP:",
        "difficulty": 2,
        "options": {"A": "keeps emails on the server and supports folder management", "B": "downloads all emails and immediately deletes from server", "C": "uses TCP port 25 for both sending and retrieving messages", "D": "encrypts all messages using TLS before any transmission"},
        "correct_answer": "A",
        "explanation": "IMAP maintains messages on server, supports folders, search, and partial fetch unlike POP3's download-and-delete."
    },
    {
        "concept_id": SMTP_EMAIL,
        "text": "The standard port numbers for SMTP, SMTP with STARTTLS, and SMTPS (implicit TLS) are respectively:",
        "difficulty": 2,
        "options": {"A": "25, 587, and 465 respectively", "B": "25, 465, and 587 respectively", "C": "110, 587, and 993 respectively", "D": "587, 25, and 143 respectively"},
        "correct_answer": "A",
        "explanation": "SMTP uses port 25, submission with STARTTLS uses 587, and implicit TLS (SMTPS) uses 465."
    },
    {
        "concept_id": SMTP_EMAIL,
        "text": "MIME (Multipurpose Internet Mail Extensions) was introduced primarily to allow SMTP to handle:",
        "difficulty": 2,
        "options": {"A": "non-ASCII data like images, audio, and attachments", "B": "concurrent connections to multiple mail server instances", "C": "encrypted communication between SMTP server relays", "D": "routing of emails across different autonomous network systems"},
        "correct_answer": "A",
        "explanation": "MIME extends SMTP to support non-text attachments, character sets, and multipart message bodies."
    },
    {
        "concept_id": SMTP_EMAIL,
        "text": "In the SMTP protocol, after the client sends `DATA`, the server indicates readiness with which reply code?",
        "difficulty": 3,
        "options": {"A": "250 OK, message accepted for delivery", "B": "354 Start mail input, end with <CRLF>.<CRLF>", "C": "220 Service ready for new SMTP session", "D": "221 Closing the current SMTP connection now"},
        "correct_answer": "B",
        "explanation": "Reply code 354 signals the client to begin sending message content, terminated by a lone dot on a line."
    },
    {
        "concept_id": SMTP_EMAIL,
        "text": "SPF (Sender Policy Framework) prevents email spoofing by:",
        "difficulty": 3,
        "options": {"A": "publishing authorized sending IPs in the domain's DNS TXT record", "B": "encrypting the email body with the sender's private RSA key pair", "C": "verifying the recipient's identity through a challenge-response test", "D": "digitally signing each email header using a domain-specific token"},
        "correct_answer": "A",
        "explanation": "SPF uses DNS TXT records to list authorized mail servers, letting receivers verify sender legitimacy."
    },
    {
        "concept_id": SMTP_EMAIL,
        "text": "DKIM (DomainKeys Identified Mail) works by:",
        "difficulty": 3,
        "options": {"A": "listing authorized IP addresses in the domain DNS SPF records", "B": "adding a digital signature to email headers verified via DNS public key", "C": "encrypting the entire email body using symmetric AES-256 encryption", "D": "requiring two-factor authentication before any email can be sent"},
        "correct_answer": "B",
        "explanation": "DKIM signs email headers with a private key; receivers verify using the public key published in DNS."
    },
    {
        "concept_id": SMTP_EMAIL,
        "text": "The POP3 and IMAPS protocols use which TCP port numbers respectively?",
        "difficulty": 2,
        "options": {"A": "Port 110 and port 993 respectively", "B": "Port 143 and port 995 respectively", "C": "Port 993 and port 110 respectively", "D": "Port 995 and port 143 respectively"},
        "correct_answer": "A",
        "explanation": "POP3 uses port 110 (unencrypted) and IMAPS uses port 993 (IMAP over TLS)."
    },
    {
        "concept_id": SMTP_EMAIL,
        "text": "SMTP is described as a **push** protocol, meaning:",
        "difficulty": 1,
        "options": {"A": "the sending server initiates connection and pushes the email to receiver", "B": "the receiving server periodically pulls emails from the sending server", "C": "the client downloads emails by requesting them from the mail server", "D": "emails are stored locally and never transmitted over any network link"},
        "correct_answer": "A",
        "explanation": "SMTP pushes email from sender's MTA to receiver's MTA; retrieval uses pull protocols like POP3/IMAP."
    },
    {
        "concept_id": SMTP_EMAIL,
        "text": "In email store-and-forward delivery, an intermediate mail relay server:",
        "difficulty": 2,
        "options": {"A": "accepts the email, stores it temporarily, then forwards to next MTA hop", "B": "establishes a direct TCP connection between original sender and receiver", "C": "decrypts the email content and re-encrypts with the receiver's public key", "D": "converts the email from SMTP format into POP3 format for final delivery"},
        "correct_answer": "A",
        "explanation": "Store-and-forward means each MTA stores the message and independently forwards it to the next hop."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 4. SOCKETS — 10 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": SOCKETS,
        "text": "A socket is uniquely identified in TCP by which combination of parameters?",
        "difficulty": 1,
        "options": {"A": "Source IP, source port, destination IP, destination port", "B": "Source IP address and destination IP address only", "C": "Source port number and destination port number only", "D": "Protocol type and the destination IP address only"},
        "correct_answer": "A",
        "explanation": "A TCP socket is identified by the 4-tuple: (source IP, source port, dest IP, dest port)."
    },
    {
        "concept_id": SOCKETS,
        "text": "The `listen()` system call in socket programming specifies:",
        "difficulty": 2,
        "options": {"A": "the maximum number of pending connections in the backlog queue", "B": "the IP address and port number to bind the server socket to", "C": "the timeout duration for each individual client data connection", "D": "the maximum data buffer size for receiving incoming client data"},
        "correct_answer": "A",
        "explanation": "listen(sockfd, backlog) marks the socket as passive and sets the maximum pending connection queue size."
    },
    {
        "concept_id": SOCKETS,
        "text": "In a concurrent TCP server, which system call creates a **new** socket for each accepted client connection?",
        "difficulty": 2,
        "options": {"A": "The bind() system call creates it", "B": "The accept() system call creates it", "C": "The connect() system call creates it", "D": "The socket() system call creates it"},
        "correct_answer": "B",
        "explanation": "accept() creates and returns a new connected socket descriptor for each client; the listening socket continues."
    },
    {
        "concept_id": SOCKETS,
        "text": "Ephemeral ports are typically assigned from which range by the operating system?",
        "difficulty": 2,
        "options": {"A": "Port range 49152 to 65535 assigned dynamically", "B": "Port range 0 to 1023 reserved for privileged use", "C": "Port range 1024 to 4999 for registered services", "D": "Port range 8000 to 9999 for web applications"},
        "correct_answer": "A",
        "explanation": "IANA designates 49152-65535 as dynamic/ephemeral ports assigned by the OS for client connections."
    },
    {
        "concept_id": SOCKETS,
        "text": "The `SOCK_DGRAM` socket type provides which kind of communication service?",
        "difficulty": 1,
        "options": {"A": "Connectionless, unreliable datagram delivery service", "B": "Connection-oriented, reliable byte stream service", "C": "Connection-oriented, message-boundary preserving service", "D": "Connectionless, reliable and ordered delivery service"},
        "correct_answer": "A",
        "explanation": "SOCK_DGRAM provides connectionless, unreliable datagram service (UDP), preserving message boundaries."
    },
    {
        "concept_id": SOCKETS,
        "text": "The `select()` system call in socket programming enables a server to:",
        "difficulty": 3,
        "options": {"A": "monitor multiple file descriptors for readiness simultaneously", "B": "create multiple threads to handle each client request separately", "C": "increase the maximum segment size for each TCP socket connection", "D": "bind a single socket to multiple port numbers at the same time"},
        "correct_answer": "A",
        "explanation": "select() multiplexes I/O, allowing a single-threaded server to monitor multiple sockets for read/write readiness."
    },
    {
        "concept_id": SOCKETS,
        "text": "A web server on port 80 receives connections from 500 clients. How many sockets does the server have open (minimum)?",
        "difficulty": 3,
        "options": {"A": "At least 501 sockets (1 listening + 500 connected)", "B": "Exactly 500 sockets (one per connected client only)", "C": "Exactly 1 socket shared among all 500 client connections", "D": "At least 1000 sockets (2 per connected client pair)"},
        "correct_answer": "A",
        "explanation": "One listening socket plus one connected socket per client = 501 minimum sockets."
    },
    {
        "concept_id": SOCKETS,
        "text": "The correct order of socket system calls for a TCP **client** is:",
        "difficulty": 2,
        "options": {"A": "socket() → connect() → send()/recv() → close()", "B": "socket() → bind() → listen() → accept() → close()", "C": "socket() → listen() → connect() → recv() → close()", "D": "bind() → socket() → accept() → send() → close()"},
        "correct_answer": "A",
        "explanation": "TCP clients create a socket, connect to server, exchange data, then close the connection."
    },
    {
        "concept_id": SOCKETS,
        "text": "Which well-known port range (0-1023) requires **root/administrator privileges** to bind on Unix systems?",
        "difficulty": 1,
        "options": {"A": "Ports 0 through 1023 require superuser privileges", "B": "Ports 1024 through 49151 require superuser privilege", "C": "Ports 49152 through 65535 require superuser privilege", "D": "All 65536 ports require superuser binding privileges"},
        "correct_answer": "A",
        "explanation": "Well-known ports (0-1023) are privileged; binding requires root/administrator access on Unix systems."
    },
    {
        "concept_id": SOCKETS,
        "text": "In UDP socket programming, the server does NOT call `listen()` or `accept()` because:",
        "difficulty": 2,
        "options": {"A": "UDP is connectionless; no connection setup is needed at all", "B": "UDP automatically handles connection setup in the kernel layer", "C": "the bind() call implicitly performs listen and accept for UDP", "D": "UDP uses a separate handshake that replaces listen and accept"},
        "correct_answer": "A",
        "explanation": "UDP is connectionless; there is no connection to listen for or accept, data is sent/received directly."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 5. FTP — 10 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": FTP,
        "text": "FTP uses **two** separate TCP connections. The control connection uses port 21 and the data connection uses port:",
        "difficulty": 1,
        "options": {"A": "Port 20 for active mode data transfer", "B": "Port 22 for active mode data transfer", "C": "Port 23 for active mode data transfer", "D": "Port 25 for active mode data transfer"},
        "correct_answer": "A",
        "explanation": "FTP active mode uses port 21 for control and port 20 for data transfer."
    },
    {
        "concept_id": FTP,
        "text": "In FTP **passive mode**, who initiates the data connection?",
        "difficulty": 2,
        "options": {"A": "The FTP server initiates data connection to the client", "B": "The FTP client initiates data connection to the server", "C": "Both client and server simultaneously open connections", "D": "A third-party proxy server initiates the data connection"},
        "correct_answer": "B",
        "explanation": "In passive mode, the server sends a port via PASV reply and the client connects to it, solving firewall issues."
    },
    {
        "concept_id": FTP,
        "text": "Which FTP command is used to retrieve (download) a file from the server?",
        "difficulty": 1,
        "options": {"A": "STOR filename.txt command", "B": "RETR filename.txt command", "C": "LIST filename.txt command", "D": "DELE filename.txt command"},
        "correct_answer": "B",
        "explanation": "RETR (retrieve) downloads a file from server to client; STOR uploads, LIST shows directory contents."
    },
    {
        "concept_id": FTP,
        "text": "FTP is considered a **stateful** protocol because:",
        "difficulty": 2,
        "options": {"A": "the server maintains the client's current directory and transfer mode", "B": "each FTP command is independent and carries all required state info", "C": "the control connection is closed and reopened for each new command", "D": "FTP does not support any session persistence between client commands"},
        "correct_answer": "A",
        "explanation": "FTP server tracks client state: current directory, transfer mode, authentication across the session."
    },
    {
        "concept_id": FTP,
        "text": "The key difference between SFTP and FTPS is:",
        "difficulty": 3,
        "options": {"A": "SFTP runs over SSH on port 22; FTPS adds TLS/SSL to standard FTP", "B": "SFTP uses port 21 with encryption; FTPS uses port 22 without it", "C": "SFTP is a subset of FTP commands; FTPS supports all FTP commands", "D": "SFTP requires no authentication; FTPS requires certificate exchange"},
        "correct_answer": "A",
        "explanation": "SFTP is an entirely different protocol running over SSH (port 22); FTPS wraps FTP in TLS/SSL."
    },
    {
        "concept_id": FTP,
        "text": "In active FTP, a client behind a NAT firewall often fails because:",
        "difficulty": 3,
        "options": {"A": "the server cannot initiate an inbound connection to the client's private IP", "B": "the client cannot resolve the server's DNS hostname from behind the NAT", "C": "the control connection on port 21 is blocked by the NAT firewall rules", "D": "the server does not support TCP connections from NATted IP address ranges"},
        "correct_answer": "A",
        "explanation": "Active FTP requires server-to-client data connection; NAT blocks inbound connections to private IPs."
    },
    {
        "concept_id": FTP,
        "text": "FTP anonymous access typically uses which username and password convention?",
        "difficulty": 1,
        "options": {"A": "Username 'anonymous' with email as the password", "B": "Username 'guest' with no password value required", "C": "Username 'public' with 'public' as the password", "D": "Username 'ftp' with the server's hostname as pass"},
        "correct_answer": "A",
        "explanation": "Anonymous FTP conventionally uses 'anonymous' as username and the user's email as courtesy password."
    },
    {
        "concept_id": FTP,
        "text": "Binary transfer mode in FTP differs from ASCII mode in that binary mode:",
        "difficulty": 2,
        "options": {"A": "transfers the file byte-for-byte without any character conversion", "B": "converts line endings between different operating system standards", "C": "compresses the file data before transmitting over the data connection", "D": "encrypts file contents using the negotiated session encryption key"},
        "correct_answer": "A",
        "explanation": "Binary mode sends exact bytes; ASCII mode converts line endings (e.g., CRLF ↔ LF) between systems."
    },
    {
        "concept_id": FTP,
        "text": "FTP restart markers (REST command) allow:",
        "difficulty": 3,
        "options": {"A": "resuming interrupted file transfers from a specified byte offset", "B": "restarting the FTP server process without disconnecting any clients", "C": "resetting the current working directory to the server's root path", "D": "clearing the server's transfer log and starting a new session log"},
        "correct_answer": "A",
        "explanation": "REST sets a byte offset; a subsequent RETR/STOR resumes transfer from that point after interruption."
    },
    {
        "concept_id": FTP,
        "text": "During an FTP session, the control connection remains open while data connections:",
        "difficulty": 2,
        "options": {"A": "are opened and closed for each individual file transfer operation", "B": "remain open for the entire duration of the FTP client session", "C": "are shared among multiple concurrent file transfer operations", "D": "use UDP instead of TCP for faster data transfer performance"},
        "correct_answer": "A",
        "explanation": "FTP creates a new data connection for each transfer (file, directory listing) and closes it after."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 6. PHYSICAL LAYER — 7 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": PHYSICAL,
        "text": "A noiseless channel has a bandwidth of 4 kHz. Using the Nyquist theorem with 16 signal levels, the maximum data rate is:",
        "difficulty": 2,
        "options": {"A": "32 kbps (32,000 bits per second)", "B": "16 kbps (16,000 bits per second)", "C": "64 kbps (64,000 bits per second)", "D": "8 kbps (8,000 bits per second)"},
        "correct_answer": "A",
        "explanation": "Nyquist: `C = 2B × log₂(L)` = 2×4000×log₂(16) = 2×4000×4 = 32,000 bps = 32 kbps."
    },
    {
        "concept_id": PHYSICAL,
        "text": "A channel has bandwidth 3 kHz and SNR of 31 dB (S/N ≈ 1259). Using Shannon's theorem, the maximum capacity is approximately:",
        "difficulty": 3,
        "options": {"A": "Approximately 30.8 kbps capacity", "B": "Approximately 15.4 kbps capacity", "C": "Approximately 61.6 kbps capacity", "D": "Approximately 10.3 kbps capacity"},
        "correct_answer": "A",
        "explanation": "`C = B × log₂(1 + S/N)` = 3000 × log₂(1260) ≈ 3000 × 10.3 ≈ 30,900 bps ≈ 30.8 kbps."
    },
    {
        "concept_id": PHYSICAL,
        "text": "Manchester encoding differs from NRZ-L encoding primarily because Manchester encoding:",
        "difficulty": 2,
        "options": {"A": "guarantees a signal transition in the middle of every single bit period", "B": "uses three voltage levels instead of two for signal representation", "C": "eliminates the need for any clock synchronization between devices", "D": "doubles the effective data rate by encoding two bits per transition"},
        "correct_answer": "A",
        "explanation": "Manchester encoding has a transition at mid-bit (low→high = 1, high→low = 0), providing self-clocking."
    },
    {
        "concept_id": PHYSICAL,
        "text": "In QAM-16 modulation, each symbol represents how many bits?",
        "difficulty": 2,
        "options": {"A": "4 bits per symbol transmitted", "B": "2 bits per symbol transmitted", "C": "8 bits per symbol transmitted", "D": "16 bits per symbol transmitted"},
        "correct_answer": "A",
        "explanation": "QAM-16 has 16 constellation points; log₂(16) = 4 bits per symbol."
    },
    {
        "concept_id": PHYSICAL,
        "text": "Differential Manchester encoding uses a transition at the **beginning** of a bit interval to represent:",
        "difficulty": 3,
        "options": {"A": "A binary 0 (no transition = 1)", "B": "A binary 1 (no transition = 0)", "C": "A start-of-frame synchronization bit", "D": "An error detection parity indicator"},
        "correct_answer": "A",
        "explanation": "In Differential Manchester, a transition at the start of bit = 0; no transition at start = 1. Mid-bit transition always present."
    },
    {
        "concept_id": PHYSICAL,
        "text": "Signal attenuation is typically measured in:",
        "difficulty": 1,
        "options": {"A": "Decibels (dB) per unit distance", "B": "Hertz (Hz) per unit bandwidth", "C": "Bits per second (bps) per link", "D": "Watts (W) per unit transmission"},
        "correct_answer": "A",
        "explanation": "Attenuation is measured in decibels (dB), representing the logarithmic ratio of output to input signal power."
    },
    {
        "concept_id": PHYSICAL,
        "text": "ASK (Amplitude Shift Keying) is most susceptible to which type of impairment?",
        "difficulty": 2,
        "options": {"A": "Noise interference causing amplitude distortion in the signal", "B": "Frequency drift from oscillator instability at the transmitter", "C": "Phase jitter from timing errors in the demodulator circuit", "D": "Multipath propagation causing constructive interference only"},
        "correct_answer": "A",
        "explanation": "ASK encodes data in amplitude; noise directly affects amplitude, making ASK the most noise-susceptible scheme."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 7. DATA LINK LAYER — 7 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": DLL,
        "text": "In Go-Back-N protocol with a window size of 7, the minimum number of sequence number bits required is:",
        "difficulty": 2,
        "options": {"A": "3 bits (supports up to N = 7 window)", "B": "4 bits (supports up to N = 15 window)", "C": "7 bits (one bit per window position)", "D": "2 bits (supports up to N = 3 window)"},
        "correct_answer": "A",
        "explanation": "Go-Back-N requires sequence numbers ≥ window + 1 = 8; ceil(log₂(8)) = 3 bits."
    },
    {
        "concept_id": DLL,
        "text": "Selective Repeat protocol with 3-bit sequence numbers can support a maximum window size of:",
        "difficulty": 3,
        "options": {"A": "Window size of 4 (half of 2³)", "B": "Window size of 7 (which is 2³ − 1)", "C": "Window size of 8 (which equals 2³)", "D": "Window size of 3 (which is 2³ − 5)"},
        "correct_answer": "A",
        "explanation": "Selective Repeat: max window = 2^(n-1) = 2^2 = 4, to distinguish new frames from retransmissions."
    },
    {
        "concept_id": DLL,
        "text": "Piggybacking in data link protocols refers to the technique of:",
        "difficulty": 2,
        "options": {"A": "attaching ACK information to outgoing data frames in both directions", "B": "sending duplicate frames on separate links for improved reliability", "C": "fragmenting large data frames into smaller sub-frames for sending", "D": "compressing frame headers to reduce the per-frame transmission overhead"},
        "correct_answer": "A",
        "explanation": "Piggybacking embeds acknowledgments in data frames going in the reverse direction, improving efficiency."
    },
    {
        "concept_id": DLL,
        "text": "The two sublayers of the Data Link Layer in the IEEE 802 model are:",
        "difficulty": 1,
        "options": {"A": "LLC (Logical Link Control) and MAC (Media Access Control)", "B": "TCP (Transport Control) and IP (Internet Protocol) sublayers", "C": "PHY (Physical) and NET (Network) sublayers of the model", "D": "DLC (Data Link Control) and FCS (Frame Check Sequence)"},
        "correct_answer": "A",
        "explanation": "IEEE 802 splits DLL into LLC (upper, protocol multiplexing) and MAC (lower, media access)."
    },
    {
        "concept_id": DLL,
        "text": "In Stop-and-Wait ARQ, if the propagation delay is 20 ms, frame transmission time is 5 ms, and ACK processing is negligible, the link utilization is:",
        "difficulty": 3,
        "options": {"A": "Approximately 11.1% link utilization", "B": "Approximately 20.0% link utilization", "C": "Approximately 25.0% link utilization", "D": "Approximately 50.0% link utilization"},
        "correct_answer": "A",
        "explanation": "Utilization = Tt/(Tt + 2×Tp) = 5/(5 + 40) ≈ 0.111 = 11.1%. Stop-and-Wait is inefficient for high delay."
    },
    {
        "concept_id": DLL,
        "text": "In Go-Back-N, if frame 5 is lost but frames 6, 7, and 8 are received, the receiver:",
        "difficulty": 2,
        "options": {"A": "discards frames 6, 7, 8 and sends NAK or duplicate ACK for frame 4", "B": "buffers frames 6, 7, 8 and waits for retransmission of frame 5", "C": "accepts frames 6, 7, 8 and sends individual ACKs for each of them", "D": "requests retransmission of only frame 5 using a selective reject"},
        "correct_answer": "A",
        "explanation": "Go-Back-N discards out-of-order frames; receiver keeps sending ACK for last in-order frame (frame 4)."
    },
    {
        "concept_id": DLL,
        "text": "HDLC (High-level Data Link Control) operates in which of the following modes?",
        "difficulty": 2,
        "options": {"A": "NRM (Normal Response Mode) and ABM (Asynchronous Balanced Mode)", "B": "Simplex mode and half-duplex mode for data link transmission", "C": "Synchronous mode and asynchronous mode for character framing", "D": "Connection mode and connectionless mode for frame delivery"},
        "correct_answer": "A",
        "explanation": "HDLC supports NRM (primary/secondary), ABM (peer-to-peer), and ARM (Asynchronous Response Mode)."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 8. APPLICATION LAYER — 7 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": APP_LAYER,
        "text": "In non-persistent HTTP, a TCP connection is closed after:",
        "difficulty": 1,
        "options": {"A": "each individual object (request/response pair) is delivered", "B": "all objects on the web page have been completely transferred", "C": "a configurable timeout period expires with no new requests", "D": "the server detects the client has closed the browser window"},
        "correct_answer": "A",
        "explanation": "Non-persistent HTTP opens a new TCP connection per object; persistent HTTP reuses connections."
    },
    {
        "concept_id": APP_LAYER,
        "text": "A web proxy cache improves performance primarily by:",
        "difficulty": 2,
        "options": {"A": "serving cached responses locally without contacting the origin server", "B": "compressing all HTTP responses using gzip before sending to clients", "C": "converting HTTPS requests to HTTP for faster processing at server", "D": "redirecting all client requests to the geographically nearest server"},
        "correct_answer": "A",
        "explanation": "Proxy caches store copies of responses; subsequent requests are served locally, reducing latency and bandwidth."
    },
    {
        "concept_id": APP_LAYER,
        "text": "A web page with 1 base HTML file and 10 referenced images requires how many TCP connections with **non-persistent HTTP** (no parallel connections)?",
        "difficulty": 2,
        "options": {"A": "11 sequential TCP connections total", "B": "10 sequential TCP connections total", "C": "1 single TCP connection is sufficient", "D": "2 TCP connections for the transfer"},
        "correct_answer": "A",
        "explanation": "Non-persistent HTTP: 1 connection for HTML + 10 connections for images = 11 connections."
    },
    {
        "concept_id": APP_LAYER,
        "text": "HTTP cookies are primarily used to:",
        "difficulty": 1,
        "options": {"A": "maintain state information across multiple stateless HTTP transactions", "B": "encrypt the communication channel between client browser and server", "C": "compress HTTP response bodies to reduce total network bandwidth usage", "D": "authenticate the server's identity to the client via digital certificate"},
        "correct_answer": "A",
        "explanation": "Cookies provide state management over stateless HTTP, tracking sessions, preferences, and identity."
    },
    {
        "concept_id": APP_LAYER,
        "text": "The HTTP PUT method differs from POST in that PUT is:",
        "difficulty": 3,
        "options": {"A": "idempotent — repeated requests produce the same result as a single request", "B": "non-idempotent — each request creates a new resource on the server side", "C": "used exclusively to delete resources identified by the request target URI", "D": "restricted to sending only URL-encoded form data in the request body"},
        "correct_answer": "A",
        "explanation": "PUT is idempotent (same result regardless of repetition); POST may create new resources each time."
    },
    {
        "concept_id": APP_LAYER,
        "text": "A CDN (Content Delivery Network) reduces latency by:",
        "difficulty": 2,
        "options": {"A": "distributing content to edge servers geographically closer to end users", "B": "increasing the bandwidth of the origin server's network uplink capacity", "C": "compressing all content using lossy algorithms before any transmission", "D": "routing all traffic through a single optimized high-speed backbone link"},
        "correct_answer": "A",
        "explanation": "CDNs cache content at edge locations worldwide, serving users from nearby servers to reduce latency."
    },
    {
        "concept_id": APP_LAYER,
        "text": "In the client-server model, the server process must:",
        "difficulty": 1,
        "options": {"A": "run continuously and listen for incoming client connection requests", "B": "initiate connections to each client when it has data ready to send", "C": "discover clients using broadcast or multicast on the local network", "D": "register with a central directory before accepting client requests"},
        "correct_answer": "A",
        "explanation": "In client-server architecture, the server runs a daemon/service that passively listens for client connections."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 9. TCP vs UDP — 6 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": TCP_UDP,
        "text": "The TCP header is a minimum of 20 bytes while the UDP header is exactly:",
        "difficulty": 1,
        "options": {"A": "8 bytes (4 fields × 2 bytes each)", "B": "12 bytes (6 fields × 2 bytes each)", "C": "16 bytes (4 fields × 4 bytes each)", "D": "20 bytes (same minimum as the TCP)"},
        "correct_answer": "A",
        "explanation": "UDP header has 4 fields: source port, dest port, length, checksum — each 2 bytes = 8 bytes total."
    },
    {
        "concept_id": TCP_UDP,
        "text": "UDP checksum computation includes a **pseudo-header** containing source/destination IP addresses. This is done to:",
        "difficulty": 3,
        "options": {"A": "verify the datagram reached the correct destination host and port", "B": "encrypt the UDP payload using IP addresses as the encryption key", "C": "enable fragmentation and reassembly at the network layer boundary", "D": "allow routers to modify the checksum during packet forwarding hop"},
        "correct_answer": "A",
        "explanation": "The pseudo-header ensures the UDP segment was delivered to the intended IP and port, detecting misdelivery."
    },
    {
        "concept_id": TCP_UDP,
        "text": "DNS primarily uses UDP for queries but switches to TCP when:",
        "difficulty": 2,
        "options": {"A": "the response exceeds 512 bytes or for zone transfer operations", "B": "the DNS server is unreachable via UDP on port 53 initially", "C": "the client requires encrypted DNS resolution using DNSSEC protocol", "D": "multiple DNS queries need to be pipelined in a single session"},
        "correct_answer": "A",
        "explanation": "DNS uses TCP for responses >512 bytes (truncated flag set) and for zone transfers (AXFR/IXFR)."
    },
    {
        "concept_id": TCP_UDP,
        "text": "TCP provides reliable delivery through all of the following mechanisms **EXCEPT**:",
        "difficulty": 2,
        "options": {"A": "Forward error correction using redundant parity bits in segments", "B": "Sequence numbers to detect out-of-order or duplicate data segments", "C": "Acknowledgments with retransmission timers for lost segment recovery", "D": "Checksum verification to detect corrupted segments during transit"},
        "correct_answer": "A",
        "explanation": "TCP uses ARQ (retransmission), not FEC. It relies on checksums, sequence numbers, and ACKs for reliability."
    },
    {
        "concept_id": TCP_UDP,
        "text": "For real-time video streaming, UDP is preferred over TCP because:",
        "difficulty": 2,
        "options": {"A": "retransmitting lost packets causes unacceptable playback delay jitter", "B": "UDP provides better error correction than TCP for video data streams", "C": "TCP does not support multicast delivery needed for live streaming", "D": "UDP guarantees ordered delivery which is essential for video frames"},
        "correct_answer": "A",
        "explanation": "TCP retransmissions add variable delay; real-time video tolerates some loss but not latency/jitter from retransmission."
    },
    {
        "concept_id": TCP_UDP,
        "text": "The connection setup overhead for TCP (3-way handshake) requires a minimum of how many RTTs before data transfer begins?",
        "difficulty": 2,
        "options": {"A": "1.5 RTTs (SYN, SYN-ACK, ACK+data)", "B": "1.0 RTT (single round trip suffices)", "C": "2.0 RTTs (two complete round trips)", "D": "3.0 RTTs (three complete round trips)"},
        "correct_answer": "A",
        "explanation": "TCP 3-way handshake: SYN (0.5 RTT) → SYN-ACK (1 RTT) → ACK+data (1.5 RTT) before data reaches server."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 10. TRANSPORT LAYER (OSI) — 6 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": TRANSPORT,
        "text": "The transport layer provides **process-to-process** delivery using which addressing mechanism?",
        "difficulty": 1,
        "options": {"A": "Port numbers to identify specific application processes", "B": "MAC addresses to identify network interface hardware cards", "C": "IP addresses to identify host machines on the global network", "D": "Session IDs to identify individual user login connections"},
        "correct_answer": "A",
        "explanation": "Transport layer uses port numbers (0-65535) to multiplex/demultiplex data to specific application processes."
    },
    {
        "concept_id": TRANSPORT,
        "text": "Transport layer multiplexing allows:",
        "difficulty": 2,
        "options": {"A": "multiple application processes to share a single network connection", "B": "a single process to connect to multiple physical network interfaces", "C": "data to be routed across multiple autonomous systems efficiently", "D": "frames to be multiplexed at the data link layer using time slots"},
        "correct_answer": "A",
        "explanation": "Multiplexing at transport layer lets multiple apps share the network; demultiplexing delivers to correct process."
    },
    {
        "concept_id": TRANSPORT,
        "text": "Segmentation at the transport layer involves:",
        "difficulty": 2,
        "options": {"A": "breaking application data into smaller units that fit the network MTU", "B": "combining multiple small packets into one large frame for efficiency", "C": "encrypting each data segment with a unique session key for security", "D": "routing data segments along different paths to the same destination"},
        "correct_answer": "A",
        "explanation": "Transport layer segments application data into appropriately sized units for network layer transmission."
    },
    {
        "concept_id": TRANSPORT,
        "text": "The transport layer sits between which two layers in the OSI model?",
        "difficulty": 1,
        "options": {"A": "Between network layer (below) and session layer (above)", "B": "Between data link layer (below) and network layer (above)", "C": "Between session layer (below) and presentation layer (above)", "D": "Between physical layer (below) and data link layer (above)"},
        "correct_answer": "A",
        "explanation": "Transport is Layer 4 in OSI, sitting between Network (Layer 3) and Session (Layer 5)."
    },
    {
        "concept_id": TRANSPORT,
        "text": "Quality of Service (QoS) at the transport layer can involve:",
        "difficulty": 3,
        "options": {"A": "specifying throughput, delay, and error rate requirements for a connection", "B": "selecting the physical transmission medium based on bandwidth capacity", "C": "assigning MAC addresses to frames based on priority tagging in VLAN", "D": "choosing the optimal routing path using distance vector table algorithms"},
        "correct_answer": "A",
        "explanation": "Transport QoS specifies connection requirements: throughput guarantees, maximum delay, acceptable error rate."
    },
    {
        "concept_id": TRANSPORT,
        "text": "Transport layer demultiplexing uses which fields from the incoming segment to deliver data to the correct socket?",
        "difficulty": 2,
        "options": {"A": "Destination port number (and source port + IPs for TCP connections)", "B": "Only the source IP address field from the network layer IP header", "C": "The TTL (Time-To-Live) and protocol field from the IP packet header", "D": "The frame sequence number assigned by the data link layer protocol"},
        "correct_answer": "A",
        "explanation": "UDP demux uses dest port; TCP demux uses the full 4-tuple (src IP, src port, dest IP, dest port)."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# 11. IP SUPPORT PROTOCOLS — 7 questions
# ═══════════════════════════════════════════════════════════════════════════════
questions += [
    {
        "concept_id": IP_SUPPORT,
        "text": "In the DHCP DORA process, the four message types exchanged in order are:",
        "difficulty": 2,
        "options": {"A": "Discover, Offer, Request, and Acknowledge", "B": "Detect, Open, Reply, and Acknowledge", "C": "Discover, Open, Request, and Accept msg", "D": "Demand, Offer, Receive, and Allocate msg"},
        "correct_answer": "A",
        "explanation": "DHCP DORA: client broadcasts Discover, server sends Offer, client Requests, server Acknowledges."
    },
    {
        "concept_id": IP_SUPPORT,
        "text": "A gratuitous ARP request is sent by a host to:",
        "difficulty": 3,
        "options": {"A": "detect IP address conflicts and update other hosts' ARP cache entries", "B": "request the MAC address of the default gateway for external routing", "C": "discover all hosts currently connected to the local area network", "D": "flush its own ARP cache and rebuild entries from network responses"},
        "correct_answer": "A",
        "explanation": "Gratuitous ARP queries for own IP; detects duplicates and lets other hosts update stale ARP cache entries."
    },
    {
        "concept_id": IP_SUPPORT,
        "text": "ICMP Time Exceeded messages (type 11) are used by the `traceroute` utility to:",
        "difficulty": 2,
        "options": {"A": "identify each intermediate router by incrementing TTL from 1 to N", "B": "measure the bandwidth capacity of each link along the network path", "C": "authenticate each router's identity using cryptographic verification", "D": "establish a persistent TCP connection to each intermediate router"},
        "correct_answer": "A",
        "explanation": "Traceroute sends packets with increasing TTL; each router sends ICMP Time Exceeded, revealing its address."
    },
    {
        "concept_id": IP_SUPPORT,
        "text": "ARP resolves which type of address mapping?",
        "difficulty": 1,
        "options": {"A": "Maps a known IP address to an unknown MAC (hardware) address", "B": "Maps a known MAC address to an unknown IP (logical) address", "C": "Maps a known hostname to an unknown IP (logical) address value", "D": "Maps a known port number to an unknown process ID on host"},
        "correct_answer": "A",
        "explanation": "ARP maps IP → MAC for local delivery; RARP does the reverse (MAC → IP), now replaced by DHCP."
    },
    {
        "concept_id": IP_SUPPORT,
        "text": "DHCP lease renewal is typically attempted by the client at what fraction of the lease duration (T1 timer)?",
        "difficulty": 3,
        "options": {"A": "At 50% of the total DHCP lease duration (T1 timer value)", "B": "At 25% of the total DHCP lease duration (T1 timer value)", "C": "At 75% of the total DHCP lease duration (T1 timer value)", "D": "At 90% of the total DHCP lease duration (T1 timer value)"},
        "correct_answer": "A",
        "explanation": "T1 (renewal timer) defaults to 50% of lease; T2 (rebinding timer) defaults to 87.5% of lease."
    },
    {
        "concept_id": IP_SUPPORT,
        "text": "The ICMP Echo Request and Echo Reply messages are used by which common network diagnostic tool?",
        "difficulty": 1,
        "options": {"A": "The ping utility for reachability testing", "B": "The nslookup utility for DNS resolution", "C": "The netstat utility for socket statistics", "D": "The arp utility for ARP cache inspection"},
        "correct_answer": "A",
        "explanation": "Ping sends ICMP Echo Requests (type 8) and receives Echo Replies (type 0) to test host reachability."
    },
    {
        "concept_id": IP_SUPPORT,
        "text": "An ARP request is sent as a **broadcast** while the ARP reply is sent as a **unicast** because:",
        "difficulty": 2,
        "options": {"A": "the sender doesn't know the target's MAC but the target knows the sender's MAC", "B": "broadcast replies would cause network congestion on large enterprise networks", "C": "ARP protocol specification mandates broadcast for all message types sent", "D": "unicast requests cannot traverse switches and routers on local segments"},
        "correct_answer": "A",
        "explanation": "ARP request is broadcast since target MAC is unknown; reply is unicast because sender's MAC was in the request."
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Now redistribute correct answers so they are not all "A"
# ═══════════════════════════════════════════════════════════════════════════════
import random

random.seed(42)  # Reproducible

for i, q in enumerate(questions):
    # Determine target answer letter based on even distribution
    target_letters = ["A", "B", "C", "D"]
    target = target_letters[i % 4]

    if target != q["correct_answer"]:
        # Swap the content of the target slot with the current correct answer slot
        current_correct = q["correct_answer"]
        q["options"][target], q["options"][current_correct] = (
            q["options"][current_correct],
            q["options"][target],
        )
        q["correct_answer"] = target

# ═══════════════════════════════════════════════════════════════════════════════
# Insert into database
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    db = SessionLocal()
    try:
        inserted = 0
        for q in questions:
            qid = str(uuid.uuid4())
            db.execute(
                text(
                    """INSERT INTO questions (id, question_text, question_type, difficulty, options, correct_answer, explanation)
                       VALUES (:id, :text, :type, :diff, :opts, :ans, :expl)"""
                ),
                {
                    "id": qid,
                    "text": q["text"],
                    "type": "mcq",
                    "diff": q["difficulty"],
                    "opts": json.dumps(q["options"]),
                    "ans": q["correct_answer"],
                    "expl": q["explanation"],
                },
            )
            db.execute(
                text(
                    "INSERT INTO question_concepts (question_id, concept_id) VALUES (:qid, :cid)"
                ),
                {"qid": qid, "cid": q["concept_id"]},
            )
            inserted += 1
        db.commit()
        print(f"✓ Inserted {inserted} questions successfully")

        # Verify final counts
        concept_ids = [
            (FLOODING, "Flooding"),
            (FRAMING, "Framing"),
            (SMTP_EMAIL, "SMTP and Email"),
            (SOCKETS, "Sockets"),
            (FTP, "FTP"),
            (PHYSICAL, "Physical Layer"),
            (DLL, "Data Link Layer"),
            (APP_LAYER, "Application Layer"),
            (TCP_UDP, "TCP vs UDP"),
            (TRANSPORT, "Transport Layer"),
            (IP_SUPPORT, "IP Support Protocols"),
        ]
        print("\n── Final Question Counts ──")
        total = 0
        for cid, name in concept_ids:
            row = db.execute(
                text(
                    "SELECT COUNT(*) FROM question_concepts WHERE concept_id = :cid"
                ),
                {"cid": cid},
            ).scalar()
            total += row
            print(f"  {name:<25s} → {row:>3d} questions")
        print(f"  {'TOTAL':<25s} → {total:>3d} questions")

    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
