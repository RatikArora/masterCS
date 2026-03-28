"""
Expanded Architecture & Planning question bank.
Adds Sections 3-7 (Part A) + Part B1 + Part B2 topics and questions.
"""
import uuid
import random
from app.db.session import SessionLocal
from app.models.subject import Subject, Topic
from app.models.concept import Concept
from app.models.question import Question, QuestionConcept

ARCH_SUBJECT_ID = "13d35960-9f22-4c56-a749-3ff627e2a8d9"


def make_q(text, options, correct, explanation, difficulty=2, qtype="mcq"):
    """Create a question dict with shuffled options."""
    opts = list(options)
    random.shuffle(opts)
    return {
        "id": str(uuid.uuid4()),
        "question_text": text,
        "question_type": qtype,
        "options": opts,
        "correct_answer": correct,
        "explanation": explanation,
        "difficulty": difficulty,
        "time_estimate_seconds": 60 if difficulty == 1 else 90 if difficulty == 2 else 120,
    }


# ─── SECTION 3: Environmental Planning and Design ───

ENV_TOPICS = [
    {
        "name": "Ecosystem & Ecology",
        "desc": "Natural and man-made ecosystems, ecological principles",
        "concepts": [
            {
                "name": "Natural Ecosystems",
                "explanation": "Ecosystems formed without human intervention — forests, wetlands, grasslands, marine systems.",
                "key_points": ["Biotic & abiotic components", "Food chains & webs", "Energy flow", "Nutrient cycling"],
                "questions": [
                    make_q("Which is NOT a component of a natural ecosystem?", ["Producers", "Consumers", "Decomposers", "Concrete structures"], "Concrete structures", "Concrete structures are man-made and not part of natural ecosystems.", 1),
                    make_q("In an ecosystem, energy flows in which direction?", ["Unidirectional", "Bidirectional", "Circular", "Random"], "Unidirectional", "Energy flows unidirectionally from sun → producers → consumers → decomposers.", 1),
                    make_q("The 10% law of energy transfer was proposed by:", ["Lindeman", "Odum", "Tansley", "Haeckel"], "Lindeman", "Lindeman's 10% law states only ~10% of energy is transferred between trophic levels.", 2),
                    make_q("Which ecosystem has the highest net primary productivity?", ["Tropical rainforest", "Temperate grassland", "Desert", "Tundra"], "Tropical rainforest", "Tropical rainforests have the highest NPP due to warm temperatures and high rainfall.", 2),
                    make_q("Biogeochemical cycles involve the movement of:", ["Nutrients through biotic and abiotic components", "Only water through the atmosphere", "Energy from sun to earth", "Pollutants through cities"], "Nutrients through biotic and abiotic components", "Biogeochemical cycles move nutrients like carbon, nitrogen, phosphorus through living and non-living components.", 1),
                    make_q("A climax community in ecological succession is characterized by:", ["Maximum species diversity and stability", "Rapid population growth", "Pioneer species dominance", "Low biomass"], "Maximum species diversity and stability", "Climax communities represent the final stable stage of ecological succession.", 2),
                    make_q("The term 'ecosystem' was coined by:", ["A.G. Tansley", "Ernst Haeckel", "Charles Darwin", "E.P. Odum"], "A.G. Tansley", "Arthur George Tansley coined the term 'ecosystem' in 1935.", 2),
                    make_q("Which of the following is a man-made ecosystem?", ["Aquarium", "Forest", "Ocean", "Wetland"], "Aquarium", "Aquariums are artificial ecosystems created and maintained by humans.", 1),
                ],
            },
            {
                "name": "Ecological Principles in Design",
                "explanation": "Application of ecological concepts to architecture and urban planning — biomimicry, green infrastructure, ecological footprint.",
                "key_points": ["Carrying capacity", "Ecological footprint", "Green infrastructure", "Biomimicry"],
                "questions": [
                    make_q("Ecological footprint measures:", ["Human demand on Earth's ecosystems", "Building floor area ratio", "Carbon emissions only", "Biodiversity index"], "Human demand on Earth's ecosystems", "Ecological footprint quantifies human demand on Earth's biological capacity.", 1),
                    make_q("Carrying capacity in urban planning refers to:", ["Maximum population an area can sustain", "Load-bearing capacity of soil", "Traffic volume of roads", "Building height limit"], "Maximum population an area can sustain", "Carrying capacity is the maximum population an environment can sustain indefinitely.", 2),
                    make_q("Biomimicry in architecture means:", ["Design inspired by nature's forms and processes", "Using only natural materials", "Building inside forests", "Planting trees on buildings"], "Design inspired by nature's forms and processes", "Biomimicry applies nature's strategies and patterns to solve design challenges.", 2),
                    make_q("Green infrastructure includes:", ["Parks, green roofs, bioswales, urban forests", "Steel and concrete structures", "Highways and flyovers", "Underground parking"], "Parks, green roofs, bioswales, urban forests", "Green infrastructure uses natural systems to provide environmental services.", 1),
                    make_q("The concept of 'urban heat island' refers to:", ["Higher temperatures in cities than surrounding rural areas", "Islands with high temperature", "Heating systems in buildings", "Volcanic activity near cities"], "Higher temperatures in cities than surrounding rural areas", "Urban heat islands occur due to dense construction, dark surfaces, and reduced vegetation.", 2),
                    make_q("Which principle suggests that waste from one process becomes input for another?", ["Industrial ecology / Cradle to cradle", "FIFO principle", "Pareto principle", "Le Corbusier's modulor"], "Industrial ecology / Cradle to cradle", "Cradle-to-cradle design eliminates waste by treating outputs as inputs for new processes.", 3),
                    make_q("Biophilic design primarily aims to:", ["Connect building occupants with nature", "Maximize floor area", "Reduce construction cost", "Increase building height"], "Connect building occupants with nature", "Biophilic design incorporates natural elements to improve human well-being.", 2),
                ],
            },
        ],
    },
    {
        "name": "Environmental Pollution & Control",
        "desc": "Types, causes, controls and abatement strategies for pollution",
        "concepts": [
            {
                "name": "Air & Water Pollution",
                "explanation": "Sources, effects, and control measures for air and water pollution in built environments.",
                "key_points": ["SPM and RSPM", "BOD and COD", "Effluent treatment", "Air quality index"],
                "questions": [
                    make_q("BOD stands for:", ["Biochemical Oxygen Demand", "Biological Oxygen Deficit", "Basic Organic Decomposition", "Bacterial Oxidation Density"], "Biochemical Oxygen Demand", "BOD measures dissolved oxygen needed by organisms to decompose organic matter in water.", 1),
                    make_q("Which pollutant is the primary cause of acid rain?", ["SO₂ and NOₓ", "CO₂", "O₃", "CH₄"], "SO₂ and NOₓ", "Sulphur dioxide and nitrogen oxides react with water vapor to form sulphuric and nitric acid.", 2),
                    make_q("The acceptable noise level for residential areas as per CPCB standards is:", ["55 dB (day), 45 dB (night)", "75 dB (day), 65 dB (night)", "65 dB (day), 55 dB (night)", "85 dB (day), 75 dB (night)"], "55 dB (day), 45 dB (night)", "CPCB standards prescribe 55 dB daytime and 45 dB nighttime for residential zones.", 2),
                    make_q("COD is always:", ["Greater than or equal to BOD", "Less than BOD", "Equal to BOD", "Unrelated to BOD"], "Greater than or equal to BOD", "COD measures total chemical oxidation capacity, which is always ≥ BOD (biological oxidation).", 2),
                    make_q("Particulate matter PM2.5 refers to particles with diameter less than:", ["2.5 micrometers", "2.5 millimeters", "2.5 nanometers", "25 micrometers"], "2.5 micrometers", "PM2.5 particles are ≤2.5 micrometers and can penetrate deep into lungs.", 1),
                    make_q("Eutrophication is caused by:", ["Excess nutrients (nitrogen, phosphorus) in water bodies", "Oil spills in oceans", "Heavy metal contamination", "Thermal pollution"], "Excess nutrients (nitrogen, phosphorus) in water bodies", "Excess nutrients cause algal blooms, depleting dissolved oxygen and killing aquatic life.", 2),
                    make_q("National Ambient Air Quality Standards (NAAQS) in India are set by:", ["CPCB", "NBCC", "BIS", "MoEFCC directly"], "CPCB", "The Central Pollution Control Board sets NAAQS under the Environment Protection Act.", 2),
                ],
            },
            {
                "name": "Pollution Control Strategies",
                "explanation": "Methods and technologies for pollution abatement in urban and architectural contexts.",
                "key_points": ["EIA process", "Pollution control devices", "Green building norms", "Waste minimization"],
                "questions": [
                    make_q("EIA stands for:", ["Environmental Impact Assessment", "Ecological Impact Analysis", "Environmental Infrastructure Audit", "Energy Integration Assessment"], "Environmental Impact Assessment", "EIA evaluates environmental effects of proposed development projects.", 1),
                    make_q("Which device is used to control particulate air pollution from industries?", ["Electrostatic precipitator", "Catalytic converter", "UV filter", "Activated sludge"], "Electrostatic precipitator", "ESPs use electric charges to remove fine particles from exhaust gases.", 2),
                    make_q("The EIA notification in India was first issued in:", ["1994", "2000", "1986", "2006"], "1994", "The first EIA notification was issued in 1994 under the Environment Protection Act, 1986.", 3),
                    make_q("Zero liquid discharge (ZLD) means:", ["All wastewater is treated and reused, none discharged", "No water is used in the process", "Liquid waste is stored underground", "Only clean water is discharged"], "All wastewater is treated and reused, none discharged", "ZLD systems recover all water from wastewater, producing only solid waste.", 2),
                    make_q("Buffer zones around industrial areas primarily serve to:", ["Reduce impact of pollution on residential areas", "Provide parking space", "Increase land value", "Enable road widening"], "Reduce impact of pollution on residential areas", "Buffer zones (green belts) between industrial and residential areas mitigate pollution impacts.", 1),
                    make_q("GRIHA is India's:", ["Green building rating system", "Groundwater regulation act", "Geological risk assessment tool", "Grid-connected renewable energy standard"], "Green building rating system", "GRIHA (Green Rating for Integrated Habitat Assessment) is India's national green building rating system.", 2),
                ],
            },
        ],
    },
    {
        "name": "Sustainable Development & Climate",
        "desc": "Sustainable development goals, climate change, and climate-responsive design",
        "concepts": [
            {
                "name": "Sustainable Development Goals",
                "explanation": "UN SDGs and their application to built environment — Goal 11 (Sustainable Cities), Goal 13 (Climate Action).",
                "key_points": ["17 SDGs", "SDG 11 - Sustainable Cities", "Triple bottom line", "Brundtland Report"],
                "questions": [
                    make_q("The Brundtland Report (1987) defined sustainable development as:", ["Meeting present needs without compromising future generations", "Maximum economic growth", "Zero carbon emissions", "Preserving all natural areas"], "Meeting present needs without compromising future generations", "The Brundtland Commission's definition is the most widely accepted definition of sustainability.", 1),
                    make_q("How many Sustainable Development Goals (SDGs) were adopted by the UN in 2015?", ["17", "15", "21", "12"], "17", "The 2030 Agenda includes 17 SDGs covering social, economic, and environmental dimensions.", 1),
                    make_q("SDG 11 focuses on:", ["Sustainable cities and communities", "Climate action", "Clean water", "Affordable energy"], "Sustainable cities and communities", "SDG 11 aims to make cities inclusive, safe, resilient, and sustainable.", 2),
                    make_q("The triple bottom line framework includes:", ["People, Planet, Profit", "Air, Water, Land", "Past, Present, Future", "Design, Build, Operate"], "People, Planet, Profit", "Triple bottom line evaluates sustainability across social, environmental, and economic dimensions.", 2),
                    make_q("LEED certification is associated with:", ["Green building standards", "Earthquake resistance", "Fire safety compliance", "Heritage conservation"], "Green building standards", "LEED (Leadership in Energy and Environmental Design) certifies green buildings.", 1),
                    make_q("Net Zero Energy Building (NZEB) means:", ["Annual energy consumption equals on-site renewable energy production", "Building uses no electricity", "Building is not connected to grid", "Zero construction energy"], "Annual energy consumption equals on-site renewable energy production", "NZEBs balance energy consumption with renewable energy generated on-site.", 2),
                ],
            },
            {
                "name": "Climate Responsive Design",
                "explanation": "Design strategies that respond to local climate conditions — passive cooling, solar orientation, natural ventilation.",
                "key_points": ["Passive design strategies", "Solar orientation", "Thermal mass", "Mahoney tables"],
                "questions": [
                    make_q("Mahoney tables are used to:", ["Determine climate-appropriate design strategies", "Calculate structural loads", "Estimate project costs", "Plan traffic flow"], "Determine climate-appropriate design strategies", "Mahoney tables analyze climatic data to recommend design strategies like ventilation and insulation.", 2),
                    make_q("In hot-dry climate, the recommended building form is:", ["Compact with thick walls and small openings", "Light structure with large windows", "Elevated on stilts", "Glass curtain wall"], "Compact with thick walls and small openings", "Compact forms with high thermal mass minimize heat gain in hot-dry climates.", 2),
                    make_q("The Trombe wall is a passive solar heating technique that uses:", ["A dark-colored thermal mass wall behind glass", "Underground heat exchange", "Wind turbines on walls", "Reflective roof coating"], "A dark-colored thermal mass wall behind glass", "Trombe walls absorb solar radiation and slowly release heat into the building interior.", 2),
                    make_q("Stack effect in buildings refers to:", ["Air movement due to temperature difference between inside and outside", "Structural stacking of floors", "Stacking of HVAC units", "Storage arrangement in warehouses"], "Air movement due to temperature difference between inside and outside", "Stack effect drives natural ventilation through buoyancy — warm air rises and exits at top.", 2),
                    make_q("In warm-humid climates, the primary design strategy is:", ["Cross ventilation with elevated structures", "Thick massive walls", "Underground construction", "Minimal window openings"], "Cross ventilation with elevated structures", "Warm-humid climates need maximum airflow for evaporative cooling and moisture removal.", 1),
                    make_q("Earth air tunnel (EAT) systems utilize:", ["Constant underground temperature for pre-cooling/heating air", "Earthquake-resistant tunnels", "Rainwater harvesting underground", "Underground parking ventilation"], "Constant underground temperature for pre-cooling/heating air", "EATs use stable underground temperatures (~25°C) to temper incoming air passively.", 3),
                    make_q("The Solar Passive Architecture concept was popularized in India by:", ["Architect Laurie Baker", "Le Corbusier", "Charles Correa", "B.V. Doshi"], "Architect Laurie Baker", "Laurie Baker pioneered cost-effective, climate-responsive architecture in India.", 3),
                    make_q("Albedo of a surface refers to:", ["Proportion of solar radiation reflected", "Heat absorption capacity", "Sound insulation value", "Wind resistance coefficient"], "Proportion of solar radiation reflected", "High albedo surfaces (light colors) reflect more solar radiation, reducing heat gain.", 2),
                ],
            },
        ],
    },
]

# ─── SECTION 4: Urban Design, Landscape and Conservation ───

URBAN_TOPICS = [
    {
        "name": "Urban Design Theory & Practice",
        "desc": "Concepts, theories, and elements of urban design",
        "concepts": [
            {
                "name": "Urban Design Elements",
                "explanation": "Key elements — urban form, spaces, structure, pattern, fabric, texture, grain, figure-ground.",
                "key_points": ["Figure-ground theory", "Urban morphology", "Serial vision (Cullen)", "Imageability (Lynch)"],
                "questions": [
                    make_q("Kevin Lynch's 'Image of the City' identified five elements:", ["Paths, Edges, Districts, Nodes, Landmarks", "Streets, Buildings, Parks, Plazas, Monuments", "Zones, Roads, Centers, Boundaries, Markets", "Corridors, Walls, Neighborhoods, Hubs, Towers"], "Paths, Edges, Districts, Nodes, Landmarks", "Lynch identified these five elements as key to how people perceive and navigate cities.", 1),
                    make_q("The concept of 'Serial Vision' was introduced by:", ["Gordon Cullen", "Kevin Lynch", "Jan Gehl", "Christopher Alexander"], "Gordon Cullen", "Cullen's 'Townscape' (1961) introduced serial vision — the experience of moving through urban space.", 2),
                    make_q("Figure-ground theory in urban design analyzes:", ["Relationship between built mass (figure) and open space (ground)", "Building height vs. depth ratio", "Foreground vs background in architecture", "Population density mapping"], "Relationship between built mass (figure) and open space (ground)", "Figure-ground maps show solid/void relationships revealing urban spatial patterns.", 2),
                    make_q("Jane Jacobs advocated for:", ["Mixed-use neighborhoods with diverse street life", "Large-scale urban renewal projects", "Separated land use zones", "Automobile-centric planning"], "Mixed-use neighborhoods with diverse street life", "Jacobs criticized modernist planning and championed vibrant, mixed-use communities.", 2),
                    make_q("The concept of 'place-making' focuses on:", ["Creating meaningful public spaces that promote well-being", "Maximizing building density", "Historical preservation only", "Traffic management"], "Creating meaningful public spaces that promote well-being", "Place-making strengthens connection between people and places they share.", 1),
                    make_q("Urban grain refers to:", ["Fineness or coarseness of urban fabric", "Soil texture in urban areas", "Building material quality", "Color scheme of buildings"], "Fineness or coarseness of urban fabric", "Fine grain = small blocks/lots (walkable), coarse grain = large blocks (auto-dependent).", 2),
                    make_q("Christopher Alexander's 'Pattern Language' proposes:", ["253 design patterns from regions to rooms", "A universal building code", "Mathematical city planning", "Computer-aided design method"], "253 design patterns from regions to rooms", "Pattern Language (1977) identifies 253 recurring design patterns at all scales.", 3),
                ],
            },
            {
                "name": "Heritage Conservation & Urban Renewal",
                "explanation": "Principles of heritage conservation, adaptive reuse, urban renewal strategies.",
                "key_points": ["Venice Charter", "INTACH", "Adaptive reuse", "Conservation vs Preservation"],
                "questions": [
                    make_q("The Venice Charter (1964) deals with:", ["Conservation and restoration of monuments and sites", "Urban transportation planning", "Environmental protection", "Housing policies"], "Conservation and restoration of monuments and sites", "The International Charter for the Conservation and Restoration of Monuments and Sites.", 1),
                    make_q("INTACH stands for:", ["Indian National Trust for Art and Cultural Heritage", "International Trust for Architecture and Cultural Heritage", "Indian Natural and Cultural Heritage", "Institute of National Art and Cultural History"], "Indian National Trust for Art and Cultural Heritage", "INTACH was founded in 1984 to protect India's natural and cultural heritage.", 2),
                    make_q("Adaptive reuse in conservation means:", ["Converting old buildings for new functions while preserving character", "Demolishing and rebuilding exactly", "Using only traditional materials", "Freezing buildings in original state"], "Converting old buildings for new functions while preserving character", "Adaptive reuse gives new life to heritage structures while retaining their architectural value.", 1),
                    make_q("The difference between conservation and preservation is:", ["Conservation allows sympathetic changes; preservation maintains original state", "They are the same", "Conservation is for nature; preservation for buildings", "Preservation is temporary; conservation is permanent"], "Conservation allows sympathetic changes; preservation maintains original state", "Conservation permits sensitive modification, while preservation aims to maintain exact original condition.", 2),
                    make_q("UNESCO World Heritage Sites in India include:", ["Taj Mahal, Red Fort, Jaipur City", "Only the Taj Mahal", "Mumbai's Gateway of India only", "No sites in India"], "Taj Mahal, Red Fort, Jaipur City", "India has 42 UNESCO World Heritage Sites including these prominent examples.", 1),
                    make_q("The Burra Charter is associated with:", ["ICOMOS Australia — conservation of places of cultural significance", "British building regulations", "Indian heritage legislation", "American urban renewal"], "ICOMOS Australia — conservation of places of cultural significance", "The Burra Charter (1979, revised 2013) provides conservation guidance for places of cultural significance.", 3),
                    make_q("In heritage zones, FAR is typically:", ["Restricted to maintain character of the area", "Maximized for development", "Not applicable", "Same as commercial zones"], "Restricted to maintain character of the area", "Heritage zone regulations typically restrict FAR and height to protect the historic character.", 2),
                ],
            },
        ],
    },
    {
        "name": "Landscape Design & Site Planning",
        "desc": "Landscape design principles, site planning, public spaces",
        "concepts": [
            {
                "name": "Landscape Design Principles",
                "explanation": "Elements and principles of landscape architecture — hard/soft landscaping, plant selection, grading, drainage.",
                "key_points": ["Hardscape vs softscape", "Xeriscaping", "Landscape grading", "Visual hierarchy"],
                "questions": [
                    make_q("Hardscape elements in landscape design include:", ["Paving, walls, pergolas, water features", "Trees, shrubs, lawns", "Soil, mulch, compost", "Birds, insects, wildlife"], "Paving, walls, pergolas, water features", "Hardscape refers to non-living, constructed elements in landscape design.", 1),
                    make_q("Xeriscaping is a landscaping approach that:", ["Minimizes water use through drought-resistant plants", "Uses excessive water features", "Focuses on tropical plants", "Eliminates all vegetation"], "Minimizes water use through drought-resistant plants", "Xeriscaping uses native, drought-tolerant plants to reduce irrigation needs.", 2),
                    make_q("Contour grading in site planning is done to:", ["Control water drainage and create usable slopes", "Increase building height", "Improve soil fertility", "Mark property boundaries"], "Control water drainage and create usable slopes", "Contour grading reshapes land to direct water flow and create functional outdoor spaces.", 2),
                    make_q("The recommended slope for pedestrian walkways is:", ["Not more than 1:12 (8.33%)", "1:4 (25%)", "1:2 (50%)", "Any slope is acceptable"], "Not more than 1:12 (8.33%)", "ADA and NBC standards recommend maximum 1:12 slope for universal accessibility.", 2),
                    make_q("A berm in landscape design is:", ["A mound of earth used for screening or directing drainage", "A type of tree", "A water fountain", "A paving pattern"], "A mound of earth used for screening or directing drainage", "Berms provide visual screening, noise reduction, and drainage control.", 2),
                    make_q("Frederick Law Olmsted is known for designing:", ["Central Park, New York", "Taj Mahal gardens", "Palace of Versailles", "Hyde Park, London"], "Central Park, New York", "Olmsted co-designed Central Park (1858) and is considered the father of American landscape architecture.", 2),
                ],
            },
        ],
    },
]

# ─── SECTION 5 & 6: Planning Process & Housing ───

PLANNING_TOPICS = [
    {
        "name": "Urban Planning Theories & Smart Cities",
        "desc": "Planning concepts, theories, Eco-City, Smart City, Ekistics",
        "concepts": [
            {
                "name": "Planning Theories & Concepts",
                "explanation": "Major urban planning theories — Garden City (Howard), CIAM, Neighbourhood Unit (Perry), Ekistics (Doxiadis).",
                "key_points": ["Garden City", "Neighbourhood Unit", "CIAM & Athens Charter", "New Urbanism"],
                "questions": [
                    make_q("Ebenezer Howard's Garden City concept proposed:", ["Self-contained communities surrounded by greenbelts", "High-rise apartment blocks", "Linear city along transport routes", "Underground cities"], "Self-contained communities surrounded by greenbelts", "Howard's Garden Cities of To-morrow (1898) envisioned balanced urban-rural communities.", 1),
                    make_q("Clarence Perry's Neighbourhood Unit was based on:", ["An elementary school as the center serving ~5000 people", "A shopping mall as center", "A factory as employment center", "A railway station as hub"], "An elementary school as the center serving ~5000 people", "Perry's 1929 concept used the school as the community nucleus within walking distance.", 2),
                    make_q("The Athens Charter (1933) was formulated by:", ["CIAM (Congrès Internationaux d'Architecture Moderne)", "UNESCO", "World Bank", "UNDP"], "CIAM (Congrès Internationaux d'Architecture Moderne)", "CIAM's Athens Charter promoted functional zoning — living, working, recreation, circulation.", 2),
                    make_q("Ekistics, the science of human settlements, was developed by:", ["Constantinos Doxiadis", "Le Corbusier", "Patrick Geddes", "Frank Lloyd Wright"], "Constantinos Doxiadis", "Doxiadis developed Ekistics to study human settlements at all scales.", 2),
                    make_q("Patrick Geddes introduced the concept of:", ["Survey-Analysis-Plan methodology", "Radiant City", "Broadacre City", "Linear City"], "Survey-Analysis-Plan methodology", "Geddes pioneered the systematic survey-analysis-plan approach to town planning.", 2),
                    make_q("The Smart City Mission in India was launched in:", ["2015", "2010", "2020", "2018"], "2015", "The Smart City Mission was launched in June 2015 covering 100 cities.", 2),
                    make_q("Le Corbusier's 'Radiant City' concept emphasized:", ["High-rise towers in open green space with separated functions", "Low-rise garden communities", "Organic city growth", "Mixed-use traditional streets"], "High-rise towers in open green space with separated functions", "Ville Radieuse proposed towers in parks with strict functional separation.", 2),
                    make_q("Transit Oriented Development (TOD) focuses on:", ["High-density mixed-use development near transit stations", "Car-dependent suburban planning", "Industrial development along highways", "Rural development near airports"], "High-density mixed-use development near transit stations", "TOD creates compact, walkable communities centered on public transit hubs.", 1),
                ],
            },
        ],
    },
    {
        "name": "Housing & Neighbourhood Planning",
        "desc": "Housing typologies, densities, affordable housing, neighbourhood design",
        "concepts": [
            {
                "name": "Housing Typologies & Densities",
                "explanation": "Types of housing — detached, semi-detached, row, apartments. Density standards and calculations.",
                "key_points": ["Gross vs net density", "FAR calculation", "Ground coverage", "Dwelling units per hectare"],
                "questions": [
                    make_q("Gross density is calculated by:", ["Total dwelling units divided by total area including roads and open spaces", "Dwelling units divided by net residential area only", "Building area divided by plot area", "Population divided by built-up area"], "Total dwelling units divided by total area including roads and open spaces", "Gross density includes all land within the area — roads, parks, facilities, etc.", 2),
                    make_q("FAR (Floor Area Ratio) is calculated as:", ["Total built-up area / Plot area", "Ground coverage × Number of floors", "Building height / Plot width", "Carpet area / Plot area"], "Total built-up area / Plot area", "FAR = sum of all floor areas ÷ total plot area. It controls building intensity.", 1),
                    make_q("Row housing is characterized by:", ["Units sharing side walls in a linear arrangement", "Independent units with all-side setbacks", "Vertical stacking of units", "Circular arrangement around a courtyard"], "Units sharing side walls in a linear arrangement", "Row houses (terraced houses) share party walls, providing efficient land use.", 1),
                    make_q("As per URDPFI Guidelines, the recommended neighborhood size is:", ["10,000 to 15,000 population", "1,000 to 2,000 population", "50,000 to 100,000 population", "500 to 1,000 population"], "10,000 to 15,000 population", "URDPFI guidelines recommend neighborhood populations of 10,000-15,000 as planning units.", 2),
                    make_q("Affordable housing in India under PMAY is defined for households with annual income up to:", ["₹18 lakhs (MIG-II category)", "₹5 lakhs only", "₹50 lakhs", "₹1 crore"], "₹18 lakhs (MIG-II category)", "PMAY covers EWS (<₹3L), LIG (₹3-6L), MIG-I (₹6-12L), and MIG-II (₹12-18L).", 2),
                    make_q("Cluster housing differs from conventional layout by:", ["Grouping units around shared open spaces", "Placing all units in a single row", "Maximum lot coverage per unit", "Underground construction"], "Grouping units around shared open spaces", "Cluster housing creates common open spaces by clustering units, preserving natural features.", 2),
                    make_q("If a plot of 1000 sq.m has FAR of 2.0 and ground coverage of 50%, the maximum number of floors possible is:", ["4", "2", "3", "5"], "4", "Built-up area = 1000 × 2.0 = 2000 sq.m. Ground coverage = 500 sq.m. Floors = 2000/500 = 4.", 2),
                ],
            },
        ],
    },
]

# ─── SECTION 7: Services and Infrastructure ───

INFRA_TOPICS = [
    {
        "name": "Water Supply & Drainage Systems",
        "desc": "Water treatment, supply, drainage, harvesting systems",
        "concepts": [
            {
                "name": "Water Supply & Treatment",
                "explanation": "Water treatment processes, distribution systems, water demand calculations, rainwater harvesting.",
                "key_points": ["Per capita demand", "Water treatment steps", "Distribution networks", "Rainwater harvesting"],
                "questions": [
                    make_q("The per capita water supply standard for Indian cities (as per CPHEEO) is:", ["135 liters per day", "70 liters per day", "200 liters per day", "50 liters per day"], "135 liters per day", "CPHEEO recommends 135 lpcd for cities with full flushing systems.", 2),
                    make_q("The correct sequence of water treatment is:", ["Screening → Sedimentation → Filtration → Disinfection", "Filtration → Sedimentation → Screening → Disinfection", "Disinfection → Filtration → Sedimentation → Screening", "Sedimentation → Disinfection → Screening → Filtration"], "Screening → Sedimentation → Filtration → Disinfection", "Water passes through these stages from coarse to fine treatment.", 1),
                    make_q("A dead-end (tree) distribution system is suitable for:", ["Small towns with irregular development", "Large cities with grid layout", "High-rise buildings", "Industrial areas only"], "Small towns with irregular development", "Dead-end systems are economical for small towns but have stagnation issues.", 2),
                    make_q("Rainwater harvesting can be done by:", ["Both rooftop collection and surface runoff harvesting", "Only rooftop collection", "Only groundwater recharge", "Only surface water storage"], "Both rooftop collection and surface runoff harvesting", "RWH includes both rooftop collection (storage/recharge) and surface runoff harvesting.", 1),
                    make_q("Chlorination of water supply is done to:", ["Kill pathogenic bacteria", "Remove hardness", "Remove color", "Reduce turbidity"], "Kill pathogenic bacteria", "Chlorine is the most common disinfectant for killing disease-causing organisms in water.", 1),
                    make_q("The minimum residual pressure at consumer tap should be:", ["7 meters (0.7 bar)", "1 meter", "20 meters", "0.1 meter"], "7 meters (0.7 bar)", "Minimum 7m residual pressure ensures adequate flow at consumer taps.", 2),
                ],
            },
        ],
    },
    {
        "name": "Solid Waste & Fire Safety",
        "desc": "Solid waste management, fire safety systems, building management",
        "concepts": [
            {
                "name": "Solid Waste Management",
                "explanation": "Collection, transportation, treatment, and disposal methods for municipal solid waste.",
                "key_points": ["Waste hierarchy (3R)", "Composting", "Landfill design", "SWM Rules 2016"],
                "questions": [
                    make_q("The waste hierarchy in order of preference is:", ["Reduce → Reuse → Recycle → Recover → Dispose", "Dispose → Recover → Recycle → Reuse → Reduce", "Recycle → Reduce → Reuse → Dispose → Recover", "Collect → Transport → Process → Dispose → Monitor"], "Reduce → Reuse → Recycle → Recover → Dispose", "The waste hierarchy prioritizes prevention over disposal.", 1),
                    make_q("Sanitary landfill differs from open dumping by:", ["Engineered containment with liner, leachate collection, gas management", "Simply covering waste with soil", "Location outside city only", "Burning waste before burial"], "Engineered containment with liner, leachate collection, gas management", "Sanitary landfills have engineered systems to prevent groundwater contamination.", 2),
                    make_q("Source segregation of waste means:", ["Separating waste at the point of generation into dry and wet", "Sorting waste at the landfill", "Transporting different wastes separately", "Mixing all waste for easy collection"], "Separating waste at the point of generation into dry and wet", "SWM Rules 2016 mandate source segregation into biodegradable, non-biodegradable, and hazardous.", 1),
                    make_q("Composting is suitable for:", ["Biodegradable/organic waste", "Plastic waste", "Construction debris", "E-waste"], "Biodegradable/organic waste", "Composting converts organic waste into useful soil amendment through biological decomposition.", 1),
                    make_q("Per capita solid waste generation in Indian cities is approximately:", ["300-600 grams per day", "50-100 grams per day", "1-2 kg per day", "5-10 kg per day"], "300-600 grams per day", "Indian cities generate 300-600 g/capita/day of municipal solid waste.", 2),
                    make_q("Waste-to-energy (WtE) plants are most suitable for waste with:", ["High calorific value (≥1500 kcal/kg)", "High moisture content", "High biodegradable fraction", "Low volume"], "High calorific value (≥1500 kcal/kg)", "WtE needs waste with sufficient calorific value to sustain combustion.", 3),
                ],
            },
            {
                "name": "Fire Safety & Building Services",
                "explanation": "Fire protection systems, detection, suppression, escape routes, building management systems.",
                "key_points": ["Fire detection systems", "Sprinkler systems", "Fire escape design", "NBC fire safety norms"],
                "questions": [
                    make_q("The maximum travel distance to the nearest fire exit in a high-rise building should not exceed:", ["30 meters", "60 meters", "100 meters", "15 meters"], "30 meters", "NBC specifies maximum 30m travel distance to nearest exit in high-rise buildings.", 2),
                    make_q("Wet riser system in fire fighting:", ["Keeps water in the pipe at all times, ready for immediate use", "Uses dry pipes that fill only when needed", "Uses chemical foam only", "Is an external fire hydrant system"], "Keeps water in the pipe at all times, ready for immediate use", "Wet risers maintain pressurized water for immediate use — standard in buildings >15m height.", 2),
                    make_q("The minimum width of a fire escape staircase should be:", ["1.0 meter", "0.6 meter", "1.5 meters", "2.0 meters"], "1.0 meter", "NBC mandates minimum 1.0m clear width for fire escape stairs.", 2),
                    make_q("Smoke detectors work on the principle of:", ["Detecting change in light/ionization caused by smoke particles", "Measuring temperature only", "Detecting carbon monoxide only", "Detecting flame wavelength only"], "Detecting change in light/ionization caused by smoke particles", "Photoelectric and ionization detectors sense smoke particles disrupting light beams or ionized air.", 2),
                    make_q("Refuge area in high-rise buildings is provided at every:", ["Floor or at intervals not exceeding 15m height", "Alternate floor", "Ground floor only", "Top floor only"], "Floor or at intervals not exceeding 15m height", "NBC requires refuge areas at intervals for safe waiting during evacuation.", 2),
                    make_q("Automatic sprinkler systems are activated by:", ["Heat (fusible element or glass bulb)", "Smoke detection", "Manual activation only", "Motion sensors"], "Heat (fusible element or glass bulb)", "Sprinklers activate when heat melts fusible links or breaks glass bulbs at set temperatures.", 1),
                    make_q("The minimum fire resistance rating for structural elements in a high-rise building is:", ["2 hours", "30 minutes", "4 hours", "15 minutes"], "2 hours", "NBC requires minimum 2-hour fire resistance for structural elements in high-rise buildings.", 2),
                ],
            },
        ],
    },
    {
        "name": "Transportation Planning",
        "desc": "Road design, traffic engineering, mass transit, parking",
        "concepts": [
            {
                "name": "Transportation & Traffic Engineering",
                "explanation": "Road hierarchy, Level of Service, traffic analysis, mass transit systems, parking standards.",
                "key_points": ["Road hierarchy", "Level of Service (LOS)", "Parking norms", "Mass transit modes"],
                "questions": [
                    make_q("The hierarchy of urban roads from highest to lowest capacity is:", ["Expressway → Arterial → Sub-arterial → Collector → Local", "Local → Collector → Arterial → Expressway", "Highway → Street → Lane → Path", "Arterial → Expressway → Local → Collector"], "Expressway → Arterial → Sub-arterial → Collector → Local", "Road hierarchy moves from high-speed/capacity (expressway) to low-speed access (local).", 1),
                    make_q("Level of Service (LOS) 'A' represents:", ["Free flow conditions with maximum comfort", "Forced flow/breakdown", "Stable flow with some delay", "Near capacity unstable flow"], "Free flow conditions with maximum comfort", "LOS A = free flow, LOS F = forced flow/breakdown.", 1),
                    make_q("Equivalent Car Space (ECS) for a bus is typically:", ["3.0", "1.0", "5.0", "0.5"], "3.0", "A bus occupies approximately 3 times the road space of a car (ECS = 3.0).", 2),
                    make_q("PCU (Passenger Car Unit) for a two-wheeler is:", ["0.5", "1.0", "2.0", "0.25"], "0.5", "A two-wheeler has PCU of 0.5, meaning it occupies half the road capacity of a car.", 2),
                    make_q("BRTS stands for:", ["Bus Rapid Transit System", "Basic Road Transport Service", "Building Response Tracking System", "Bridge and Road Testing System"], "Bus Rapid Transit System", "BRTS provides dedicated bus lanes for fast, reliable, high-capacity urban transit.", 1),
                    make_q("The recommended parking space size for a car is:", ["2.5m × 5.0m", "1.5m × 3.0m", "3.5m × 7.0m", "4.0m × 8.0m"], "2.5m × 5.0m", "Standard parking space dimensions are 2.5m wide × 5.0m long.", 2),
                    make_q("Multi-modal transport integration means:", ["Seamless connection between different transport modes", "Using only one mode of transport", "Separate planning for each transport mode", "Replacing all modes with metro"], "Seamless connection between different transport modes", "Multi-modal integration connects bus, metro, rail, cycling, walking for seamless travel.", 1),
                    make_q("The 4-stage transportation planning model includes:", ["Trip Generation → Trip Distribution → Modal Split → Trip Assignment", "Survey → Analysis → Design → Construction", "Planning → Design → Build → Operate", "Demand → Supply → Price → Equilibrium"], "Trip Generation → Trip Distribution → Modal Split → Trip Assignment", "The classic 4-stage model is the foundation of transport demand forecasting.", 2),
                ],
            },
        ],
    },
]

# ─── Part B1: Architecture ───

ARCH_B1_TOPICS = [
    {
        "name": "History of Architecture",
        "desc": "World and Indian architecture history — Egyptian, Greek, Roman, Gothic, Renaissance, Modern",
        "concepts": [
            {
                "name": "Classical & Medieval Architecture",
                "explanation": "Egyptian, Greek, Roman, Byzantine, Gothic architecture — key features, structures, and innovations.",
                "key_points": ["Greek orders (Doric, Ionic, Corinthian)", "Roman arches and domes", "Gothic pointed arches and flying buttresses", "Byzantine pendentives"],
                "questions": [
                    make_q("The three classical Greek orders are:", ["Doric, Ionic, Corinthian", "Tuscan, Doric, Composite", "Roman, Greek, Egyptian", "Gothic, Romanesque, Byzantine"], "Doric, Ionic, Corinthian", "The three Greek orders differ in column proportions and capital decoration.", 1),
                    make_q("The Parthenon in Athens uses which order?", ["Doric", "Ionic", "Corinthian", "Composite"], "Doric", "The Parthenon (447-432 BCE) is the most iconic example of the Doric order.", 1),
                    make_q("The pendentive was a structural innovation of:", ["Byzantine architecture", "Gothic architecture", "Egyptian architecture", "Greek architecture"], "Byzantine architecture", "Pendentives enable circular domes to sit atop square bases, perfected in Hagia Sophia.", 2),
                    make_q("Flying buttresses are characteristic of:", ["Gothic architecture", "Renaissance architecture", "Roman architecture", "Art Deco architecture"], "Gothic architecture", "Flying buttresses transfer lateral thrust from high walls to external piers in Gothic cathedrals.", 1),
                    make_q("The Pantheon in Rome is notable for its:", ["Unreinforced concrete dome with an oculus", "Timber truss roof", "Steel frame structure", "Stone post-and-lintel system"], "Unreinforced concrete dome with an oculus", "The Pantheon's dome (43.3m diameter) remains the world's largest unreinforced concrete dome.", 2),
                    make_q("Ribbed vaulting was introduced during:", ["Gothic period", "Egyptian period", "Classical Greek period", "Art Nouveau period"], "Gothic period", "Ribbed vaults distributed weight along stone ribs, allowing larger windows in Gothic cathedrals.", 2),
                    make_q("The Pyramids of Giza were built during:", ["Ancient Egyptian civilization (~2560 BCE)", "Roman Empire", "Mesopotamian civilization", "Indus Valley civilization"], "Ancient Egyptian civilization (~2560 BCE)", "The Great Pyramid of Giza was built as a tomb for Pharaoh Khufu around 2560 BCE.", 1),
                ],
            },
            {
                "name": "Modern Architecture Movements",
                "explanation": "Art Nouveau, Art Deco, International Style, Brutalism, Post-Modernism, Deconstructivism.",
                "key_points": ["International Style (Mies, Gropius)", "Brutalism (Le Corbusier)", "Post-Modernism (Venturi)", "Deconstructivism (Gehry, Hadid)"],
                "questions": [
                    make_q("'Less is more' is attributed to:", ["Mies van der Rohe", "Le Corbusier", "Frank Lloyd Wright", "Robert Venturi"], "Mies van der Rohe", "Mies van der Rohe's famous dictum embodies minimalist International Style architecture.", 1),
                    make_q("The Bauhaus school was founded by:", ["Walter Gropius", "Le Corbusier", "Mies van der Rohe", "Frank Lloyd Wright"], "Walter Gropius", "Gropius founded the Bauhaus in Weimar, Germany in 1919.", 1),
                    make_q("Brutalism is characterized by:", ["Raw exposed concrete (béton brut), massive forms", "Glass and steel minimalism", "Ornamental facades", "Organic curved forms"], "Raw exposed concrete (béton brut), massive forms", "Brutalism celebrates raw concrete and bold geometric forms — from French béton brut.", 2),
                    make_q("Robert Venturi's book 'Complexity and Contradiction in Architecture' was a manifesto for:", ["Post-Modernism", "Modernism", "Deconstructivism", "Art Deco"], "Post-Modernism", "Venturi challenged modernist simplicity with 'Less is a bore' — launching Post-Modernism.", 2),
                    make_q("Frank Gehry's Guggenheim Museum Bilbao represents:", ["Deconstructivism", "Classical Revival", "Art Deco", "Brutalism"], "Deconstructivism", "The Bilbao Guggenheim (1997) is the most famous example of Deconstructivist architecture.", 2),
                    make_q("Le Corbusier's 'Five Points of Architecture' include:", ["Pilotis, free plan, free facade, ribbon windows, roof garden", "Symmetry, proportion, order, hierarchy, rhythm", "Form, function, material, structure, space", "Column, beam, arch, dome, vault"], "Pilotis, free plan, free facade, ribbon windows, roof garden", "Le Corbusier's 1926 manifesto defined the principles of modern architecture.", 2),
                    make_q("The International Style exhibition was held at:", ["MoMA, New York (1932)", "Crystal Palace, London (1851)", "Centre Pompidou, Paris (1977)", "Venice Biennale (1980)"], "MoMA, New York (1932)", "The 1932 MoMA exhibition curated by Hitchcock and Johnson named the International Style.", 3),
                    make_q("Zaha Hadid is known for:", ["Fluid, dynamic forms in Parametric/Deconstructivist style", "Classical Greek revival buildings", "Minimalist glass boxes", "Traditional brick construction"], "Fluid, dynamic forms in Parametric/Deconstructivist style", "Hadid pioneered flowing, sculptural architecture using parametric design tools.", 1),
                ],
            },
        ],
    },
    {
        "name": "Building Construction & Structural Systems",
        "desc": "Construction techniques, structural systems, materials, pre-stressing",
        "concepts": [
            {
                "name": "Structural Systems & Materials",
                "explanation": "Load-bearing vs framed structures, pre-stressed concrete, high-rise systems, long-span structures.",
                "key_points": ["Framed vs load-bearing", "Pre-stressed concrete", "Lateral load systems", "Space frames"],
                "questions": [
                    make_q("Load-bearing structures transfer loads through:", ["Walls directly to the foundation", "Beams and columns", "Trusses and cables", "Membrane action"], "Walls directly to the foundation", "In load-bearing construction, walls carry both their own weight and floor/roof loads.", 1),
                    make_q("Pre-stressed concrete achieves its strength by:", ["Applying compressive stress to counteract tensile forces", "Using thicker reinforcement bars", "Adding more cement", "Curing at higher temperature"], "Applying compressive stress to counteract tensile forces", "Pre-stressing introduces compressive forces that counteract tensile stresses under load.", 2),
                    make_q("A shear wall in high-rise buildings primarily resists:", ["Lateral forces (wind and earthquake)", "Vertical gravity loads only", "Temperature stresses", "Foundation settlement"], "Lateral forces (wind and earthquake)", "Shear walls are rigid planar elements that resist lateral forces in high-rise buildings.", 1),
                    make_q("A space frame is a:", ["Three-dimensional truss system for large-span roofs", "Two-dimensional portal frame", "Load-bearing wall system", "Cable-stayed structure"], "Three-dimensional truss system for large-span roofs", "Space frames distribute loads three-dimensionally, ideal for large-span roof structures.", 2),
                    make_q("Modular coordination in building aims to:", ["Standardize dimensions to reduce waste and improve efficiency", "Create unique designs for each building", "Maximize building height", "Minimize structural cost only"], "Standardize dimensions to reduce waste and improve efficiency", "Modular coordination uses a basic module (100mm) to standardize building components.", 2),
                    make_q("The outrigger system in tall buildings:", ["Connects core to perimeter columns to reduce drift", "Is an exterior diagonal bracing system", "Is used only in steel buildings", "Reduces gravity loads"], "Connects core to perimeter columns to reduce drift", "Outriggers extend from the central core to engage perimeter columns in resisting lateral loads.", 3),
                    make_q("Ferrocement uses:", ["Thin cement mortar reinforced with wire mesh layers", "Thick precast concrete panels", "Steel plates with concrete filling", "Timber with concrete overlay"], "Thin cement mortar reinforced with wire mesh layers", "Ferrocement uses closely-spaced wire mesh with cement mortar for thin, strong elements.", 2),
                ],
            },
        ],
    },
]


def seed_expanded():
    db = SessionLocal()
    try:
        order_idx = 11  # Start after existing 10 topics
        total_topics = 0
        total_concepts = 0
        total_questions = 0

        all_topic_groups = ENV_TOPICS + URBAN_TOPICS + PLANNING_TOPICS + INFRA_TOPICS + ARCH_B1_TOPICS

        for topic_def in all_topic_groups:
            # Check if topic already exists
            existing = db.query(Topic).filter(
                Topic.subject_id == ARCH_SUBJECT_ID,
                Topic.name == topic_def["name"]
            ).first()
            if existing:
                print(f"  ⏩ Topic '{topic_def['name']}' already exists, skipping")
                order_idx += 1
                continue

            topic = Topic(
                id=str(uuid.uuid4()),
                name=topic_def["name"],
                description=topic_def["desc"],
                order_index=order_idx,
                subject_id=ARCH_SUBJECT_ID,
            )
            db.add(topic)
            db.flush()
            order_idx += 1
            total_topics += 1
            print(f"✅ Topic: {topic_def['name']}")

            for ci, concept_def in enumerate(topic_def["concepts"]):
                concept = Concept(
                    id=str(uuid.uuid4()),
                    name=concept_def["name"],
                    explanation=concept_def["explanation"],
                    key_points=concept_def["key_points"],
                    order_index=ci + 1,
                    topic_id=topic.id,
                )
                db.add(concept)
                db.flush()
                total_concepts += 1

                for q_def in concept_def["questions"]:
                    question = Question(
                        id=q_def["id"],
                        question_text=q_def["question_text"],
                        question_type=q_def["question_type"],
                        options=q_def["options"],
                        correct_answer=q_def["correct_answer"],
                        explanation=q_def["explanation"],
                        difficulty=q_def["difficulty"],
                        time_estimate_seconds=q_def["time_estimate_seconds"],
                    )
                    db.add(question)
                    db.flush()

                    qc = QuestionConcept(
                        question_id=question.id,
                        concept_id=concept.id,
                    )
                    db.add(qc)
                    total_questions += 1

                print(f"   📝 {concept_def['name']}: {len(concept_def['questions'])} questions")

        db.commit()
        print(f"\n🎉 Seeded {total_topics} topics, {total_concepts} concepts, {total_questions} questions")
        print(f"   (Skipped topics that already existed)")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_expanded()
