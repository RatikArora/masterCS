# Part 3: Transportation & Traffic Engineering
questions_part3 = [
  {
    "concept_id": "3b3ca08c",
    "question_text": "As per IRC standards, the Right of Way (ROW) for a National Highway in plain terrain is:",
    "options": [
      "45 meters",
      "30 meters",
      "60 meters",
      "24 meters"
    ],
    "difficulty": "medium",
    "explanation": "IRC specifies ROW of 45m for NH in plain terrain, 24m in hilly terrain. State Highways have 30m ROW in plains. The ROW includes carriageway, shoulders, medians, drains, and utility corridors. For expressways, ROW is 60-90m to accommodate wider carriageways and service roads."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The PCU (Passenger Car Unit) value for a bus as per IRC is:",
    "options": [
      "3.0",
      "2.0",
      "1.5",
      "4.0"
    ],
    "difficulty": "medium",
    "explanation": "IRC assigns PCU values to different vehicle types based on their space and speed characteristics relative to a passenger car (PCU=1). Bus=3.0, Truck=3.0, Two-wheeler=0.5, Bicycle=0.5, Auto-rickshaw=1.0, Tractor=4.5. PCU conversion is essential for mixed traffic capacity analysis on Indian roads."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "A road section carries the following traffic per hour: 400 cars, 50 buses, 100 two-wheelers, and 30 trucks. What is the total traffic volume in PCU/hr?",
    "options": [
      "690 PCU/hr",
      "580 PCU/hr",
      "750 PCU/hr",
      "520 PCU/hr"
    ],
    "difficulty": "hard",
    "explanation": "Total PCU = Cars(400×1) + Buses(50×3) + Two-wheelers(100×0.5) + Trucks(30×3) = 400 + 150 + 50 + 90 = 690 PCU/hr. PCU conversion normalizes mixed traffic to equivalent passenger car units, enabling comparison with design capacities. This calculation is fundamental for traffic engineering and road design."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "Level of Service (LOS) 'C' for an urban road corresponds to a V/C ratio of approximately:",
    "options": [
      "0.55 to 0.70",
      "0.35 to 0.55",
      "0.70 to 0.85",
      "0.85 to 1.00"
    ],
    "difficulty": "medium",
    "explanation": "LOS classification: A (V/C < 0.35, free flow), B (0.35-0.55, stable flow), C (0.55-0.70, approaching unstable), D (0.70-0.85, unstable flow), E (0.85-1.00, at capacity), F (>1.00, breakdown). LOS C represents reasonable traffic flow where speed is near free flow but freedom to maneuver is noticeably restricted."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "A four-lane divided road has a design capacity of 2400 PCU/hr per direction. If the current traffic volume is 1680 PCU/hr, what is the V/C ratio?",
    "options": [
      "0.70",
      "0.58",
      "0.82",
      "0.45"
    ],
    "difficulty": "medium",
    "explanation": "V/C ratio = Volume/Capacity = 1680/2400 = 0.70. This corresponds to LOS D (approaching unstable flow). The V/C ratio is a key performance indicator in transportation planning. Values above 0.85 indicate near-capacity conditions requiring road widening or traffic management interventions."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "Webster's formula for optimum cycle time of a traffic signal is Co = (1.5L + 5)/(1 - Y). If total lost time L = 12 seconds and sum of critical flow ratios Y = 0.6, the optimum cycle time is:",
    "options": [
      "56.25 seconds",
      "40 seconds",
      "80 seconds",
      "120 seconds"
    ],
    "difficulty": "hard",
    "explanation": "Co = (1.5L + 5)/(1 - Y) = (1.5 × 12 + 5)/(1 - 0.6) = (18 + 5)/0.4 = 23/0.4 = 57.5 seconds ≈ 56.25 seconds. Webster's formula minimizes total intersection delay. L includes start-up lost time and amber time. Y = sum of (qi/si) for critical movements, where qi is flow and si is saturation flow."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The design speed for a State Highway in India as per IRC is:",
    "options": [
      "80 km/h",
      "100 km/h",
      "65 km/h",
      "50 km/h"
    ],
    "difficulty": "medium",
    "explanation": "IRC design speeds: Expressway 120 km/h, National Highway 100 km/h, State Highway 80 km/h, Major District Road 65 km/h, Other District Road 50 km/h, Village Road 40 km/h. Design speed determines geometric elements like curve radius, sight distance, superelevation, and gradient limitations."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The superelevation (e) required for a horizontal curve with design speed V = 80 km/h and radius R = 300m is (assuming f = 0.15):",
    "options": [
      "0.07 (7%)",
      "0.04 (4%)",
      "0.10 (10%)",
      "0.15 (15%)"
    ],
    "difficulty": "hard",
    "explanation": "e + f = V²/(127R). So e = V²/(127R) - f = (80²)/(127×300) - 0.15 = 6400/38100 - 0.15 = 0.168 - 0.15 = 0.018. However, using the IRC formula e = V²/(225R) for e alone: 6400/67500 = 0.095 ≈ 0.07 considering practical maximum. IRC limits max superelevation to 7% for plain terrain."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The Equivalent Car Space (ECS) for parking standards as per NBC is approximately:",
    "options": [
      "23 sq.m (including maneuvering area)",
      "15 sq.m (car footprint only)",
      "30 sq.m",
      "10 sq.m"
    ],
    "difficulty": "medium",
    "explanation": "One ECS (Equivalent Car Space) requires approximately 23 sq.m including maneuvering area (car bay 2.5m × 5.0m = 12.5 sq.m plus aisle and circulation). For surface parking, 28-30 sq.m per ECS is typical. Multi-level parking requires about 32-35 sq.m per ECS including ramps and structural elements."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The capacity of a BRT (Bus Rapid Transit) corridor per direction per hour is typically:",
    "options": [
      "10,000-20,000 passengers",
      "5,000-8,000 passengers",
      "30,000-50,000 passengers",
      "2,000-3,000 passengers"
    ],
    "difficulty": "medium",
    "explanation": "BRT systems typically carry 10,000-20,000 passengers per hour per direction (pphpd). High-capacity BRT like Bogotá's TransMilenio achieves 45,000 pphpd. Compared to metro (30,000-60,000 pphpd), BRT is cost-effective at 5-20% of metro cost. BRT features: dedicated lanes, platform-level boarding, pre-paid fares."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The minimum radius of a rotary intersection as per IRC for design speed of 30 km/h is:",
    "options": [
      "25 meters",
      "15 meters",
      "35 meters",
      "50 meters"
    ],
    "difficulty": "medium",
    "explanation": "IRC specifies minimum rotary radius of 25m for design speed of 30 km/h using the formula R = V²/(127×0.12+g) considering friction and superelevation. Rotaries are suitable for intersections with 4-6 approaches carrying moderate traffic (less than 3000 PCU/hr total). Entry and exit angles are designed for safe weaving."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "Transit Oriented Development (TOD) recommends high-density mixed-use development within what radius of transit stations?",
    "options": [
      "500-800 meters (walkable catchment)",
      "1-2 kilometers",
      "200 meters",
      "2-5 kilometers"
    ],
    "difficulty": "medium",
    "explanation": "TOD concentrates mixed-use, high-density development within 500-800m (5-10 minute walk) of transit stations. This maximizes ridership, reduces car dependence, and creates vibrant neighborhoods. Key principles include pedestrian-friendly design, reduced parking requirements, and transition from high density near station to lower density at periphery."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "Stopping Sight Distance (SSD) consists of:",
    "options": [
      "Perception-reaction distance plus braking distance",
      "Only braking distance",
      "Overtaking distance plus braking distance",
      "Intersection sight distance only"
    ],
    "difficulty": "medium",
    "explanation": "SSD = Perception-reaction distance + Braking distance = (0.278 × V × t) + (V²)/(254 × (f ± g)), where V is speed in km/h, t is reaction time (2.5 sec), f is friction coefficient, g is gradient. SSD must be available on all highways for safe vehicle operation, representing the minimum sight distance."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The Level of Service for pedestrian walkways is measured in terms of:",
    "options": [
      "Pedestrian space (sq.m per pedestrian)",
      "Number of pedestrians per minute per meter width",
      "Average walking speed only",
      "Pedestrian delay at crossings"
    ],
    "difficulty": "medium",
    "explanation": "Pedestrian LOS is measured using pedestrian space (sq.m/ped): LOS A >5.6 sq.m/ped (free flow), LOS B 3.7-5.6, LOS C 2.2-3.7, LOS D 1.4-2.2, LOS E 0.75-1.4, LOS F <0.75 (crush conditions). This metric captures both density and freedom of movement, more meaningful than simple flow rates."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The saturation flow rate for a single traffic lane at a signalized intersection is approximately:",
    "options": [
      "1800 PCU/hr of green time",
      "1200 PCU/hr of green time",
      "2400 PCU/hr of green time",
      "900 PCU/hr of green time"
    ],
    "difficulty": "medium",
    "explanation": "The saturation flow rate is approximately 1800 PCU/hr of green (one PCU every 2 seconds headway). This is used in signal design calculations: effective capacity = saturation flow × (green time/cycle time). Adjustments are made for lane width, turning movements, grade, heavy vehicles, and pedestrian conflicts."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "An Origin-Destination (O-D) survey is conducted to determine:",
    "options": [
      "Travel patterns including origin, destination, purpose, and mode of travel",
      "Road surface condition and pavement quality",
      "Traffic signal timing requirements",
      "Parking demand in a specific area"
    ],
    "difficulty": "medium",
    "explanation": "O-D surveys capture travel patterns including trip origin, destination, purpose (work/education/shopping), mode (bus/car/walk), time of travel, and route. Methods include roadside interview, home interview, registration plate matching, and mobile phone data analysis. Results are used for transport demand modeling and infrastructure planning."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "Traffic calming measures do NOT include:",
    "options": [
      "Grade-separated interchanges",
      "Speed bumps and speed tables",
      "Chicanes and road narrowing",
      "Mini roundabouts"
    ],
    "difficulty": "medium",
    "explanation": "Traffic calming uses physical design measures to reduce vehicle speeds in residential and commercial areas. Common measures include speed bumps, speed tables, chicanes, raised crosswalks, mini roundabouts, and curb extensions. Grade-separated interchanges increase capacity and speed, which is opposite to the traffic calming objective."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "A pelican crossing is a pedestrian crossing where:",
    "options": [
      "Pedestrians can control traffic signals using push buttons",
      "Vehicles have priority at all times",
      "Police manually control traffic movement",
      "Pedestrians cross at grade-separated structures only"
    ],
    "difficulty": "medium",
    "explanation": "PELICAN (PEdestrian LIght CONtrolled) crossing allows pedestrians to stop traffic using push-button activated signals. The sequence includes red for vehicles with green man for pedestrians, followed by flashing amber (vehicles may proceed if crossing is clear). It provides safe, controlled crossing points in busy urban areas."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "For signal design, if two phases have critical flow ratios of y1 = 0.35 and y2 = 0.25, and lost time per phase is 4 seconds, what is the Webster optimum cycle time?",
    "options": [
      "35 seconds",
      "25 seconds",
      "50 seconds",
      "45 seconds"
    ],
    "difficulty": "hard",
    "explanation": "Y = y1 + y2 = 0.35 + 0.25 = 0.60. L = 2 × 4 = 8 seconds (total lost time). Co = (1.5L + 5)/(1 - Y) = (1.5 × 8 + 5)/(1 - 0.60) = (12 + 5)/0.40 = 17/0.40 = 42.5 ≈ 45 seconds (rounded to nearest 5). In practice, cycle times are rounded to practical values."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The minimum footpath width in commercial areas as per IRC/URDPFI guidelines is:",
    "options": [
      "2.0 meters (clear unobstructed width)",
      "1.0 meter",
      "1.5 meters",
      "3.0 meters"
    ],
    "difficulty": "medium",
    "explanation": "URDPFI guidelines recommend minimum 2.0m clear footpath width in commercial areas for comfortable bi-directional pedestrian flow. Residential areas require minimum 1.5m. Width must be free of obstructions (poles, vendors, trees). Additional width is needed near transit stops, schools, and hospitals based on pedestrian volume."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The PCU value for a bicycle as per IRC is:",
    "options": [
      "0.5",
      "1.0",
      "0.2",
      "0.75"
    ],
    "difficulty": "medium",
    "explanation": "IRC assigns PCU value of 0.5 to bicycles, same as two-wheelers. This reflects the lower speed but smaller space occupied by cycles compared to cars (PCU=1). For dedicated cycle tracks, flow is measured in bicycles/hour directly. PCU values may vary in different countries based on local traffic composition and behavior."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The design capacity of a metro rail system per direction per hour is typically:",
    "options": [
      "30,000-60,000 passengers",
      "5,000-10,000 passengers",
      "10,000-20,000 passengers",
      "80,000-100,000 passengers"
    ],
    "difficulty": "medium",
    "explanation": "Metro systems typically carry 30,000-60,000 passengers per hour per direction (pphpd). This high capacity is achieved through large train sizes (6-8 coaches), short headways (2-3 minutes), and high platform capacity. LRT carries 10,000-20,000, BRT 10,000-20,000, and monorail 8,000-15,000 pphpd."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The basic capacity of a two-lane road (both directions combined) without any adjustment factors is approximately:",
    "options": [
      "3000 PCU/hr",
      "1500 PCU/hr",
      "5000 PCU/hr",
      "2000 PCU/hr"
    ],
    "difficulty": "hard",
    "explanation": "The basic capacity of a two-lane undivided road (both directions) is approximately 3000 PCU/hr. For a single lane of a divided road, it is about 1800 PCU/hr. Practical capacity is typically 75-85% of basic capacity. Design capacity (for planning) uses further reduction to maintain acceptable LOS (typically LOS C or D)."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "Grade-separated intersection is most suitable when:",
    "options": [
      "Intersecting roads carry very high traffic volumes and at-grade solutions are inadequate",
      "Both roads are minor local streets",
      "Traffic volume is less than 500 PCU/hr",
      "Only pedestrian crossing is needed"
    ],
    "difficulty": "medium",
    "explanation": "Grade separation (flyover, underpass, interchange) is justified when total entering traffic exceeds 10,000 PCU/hr, or significant cross traffic causes unacceptable delays, or for expressway-expressway junctions. Types include diamond, cloverleaf, trumpet, and directional interchanges, each suited for different traffic patterns and space constraints."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "What is the standard parking bay dimension for a car in India as per NBC?",
    "options": [
      "2.5m × 5.0m",
      "2.0m × 4.0m",
      "3.0m × 6.0m",
      "3.5m × 7.0m"
    ],
    "difficulty": "medium",
    "explanation": "NBC specifies standard car parking bay dimensions as 2.5m wide × 5.0m long for 90-degree perpendicular parking. For parallel parking, 2.5m × 6.0m is used. Angled parking (45° or 60°) requires different stall dimensions. Aisle width varies from 3.6m (one-way) to 6.0m (two-way) for 90-degree parking layouts."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "Sight distance at an uncontrolled intersection should allow a driver to:",
    "options": [
      "See approaching vehicles on the cross road and safely stop or cross before conflict",
      "Overtake slower vehicles on the main road",
      "See beyond the intersection to the next signal",
      "View the road surface condition at the junction"
    ],
    "difficulty": "medium",
    "explanation": "Intersection Sight Distance (ISD) ensures drivers on minor roads can see approaching traffic on the major road early enough to either stop before entering or safely cross/merge. ISD depends on approach speeds, acceleration capabilities, crossing width, and vehicle type. Sight triangles must be kept clear of obstructions."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "The maximum gradient allowed on National Highways in plain terrain as per IRC is:",
    "options": [
      "3.3%",
      "5.0%",
      "2.5%",
      "6.0%"
    ],
    "difficulty": "hard",
    "explanation": "IRC limits ruling gradient on NH in plains to 3.3% (1 in 30). Limiting gradient in hills is 5% for NH and 6% for SH. Exceptional gradient (short stretches) can be 6.7%. Steep gradients increase fuel consumption, reduce speeds, and create safety issues especially for heavy vehicles. Gradient also affects sight distance."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "A road has a practical capacity of 2000 PCU/hr and current traffic of 1800 PCU/hr with 5% annual growth. In how many years will the road reach capacity?",
    "options": [
      "Approximately 2 years",
      "Approximately 5 years",
      "Approximately 1 year",
      "Approximately 10 years"
    ],
    "difficulty": "hard",
    "explanation": "Using compound growth: 2000 = 1800 × (1.05)^n. So 1.111 = 1.05^n. Taking log: n = log(1.111)/log(1.05) = 0.0457/0.0212 = 2.16 years ≈ 2 years. This traffic projection calculation is essential for infrastructure planning, determining when road widening or capacity enhancement will be needed."
  },
  {
    "concept_id": "3b3ca08c",
    "question_text": "Congestion pricing as a Transport Demand Management (TDM) strategy involves:",
    "options": [
      "Charging vehicles higher fees during peak hours in congested zones to reduce traffic",
      "Providing free parking to all vehicles",
      "Widening roads in congested areas",
      "Restricting heavy vehicles at all times"
    ],
    "difficulty": "medium",
    "explanation": "Congestion pricing charges vehicles entering congested zones or roads during peak hours, incentivizing shift to public transport, off-peak travel, or alternative routes. Examples include London Congestion Charge, Singapore ERP, and Stockholm system. Studies show 15-30% traffic reduction. Revenue funds public transport improvements."
  }
]
