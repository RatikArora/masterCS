"""
Seed database with Architecture & Planning Part B2 content.
Topics: Regional Planning, GIS & Remote Sensing, Planning Techniques & Management, Professional Practice.
120+ GATE-level questions with proper explanations.
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


# ═══════════════════════════════════════════════════════════════════
# TOPIC 1: Regional Planning
# ═══════════════════════════════════════════════════════════════════

REGIONAL_PLANNING_TOPICS = [
    {
        "name": "Regional Planning",
        "desc": "Regional development strategies, growth pole theory, central place theory, regional disparities, urbanization patterns, and regional plan preparation.",
        "concepts": [
            {
                "name": "Regional Development Strategies",
                "explanation": "Regional planning aims to reduce disparities between regions through balanced development. Strategies include growth poles, spread-backwash effects, and top-down vs bottom-up approaches.",
                "key_points": [
                    "Balanced vs unbalanced growth theories",
                    "Core-periphery model by Friedmann",
                    "Spread and backwash effects (Myrdal)",
                    "Regional imbalances and corrective strategies",
                ],
                "questions": [
                    make_q("The core-periphery model of regional development was proposed by:", ["John Friedmann", "Walter Christaller", "August Lösch", "François Perroux"], "John Friedmann", "John Friedmann proposed the core-periphery model describing how development spreads from core urban regions to peripheral areas.", 1),
                    make_q("Gunnar Myrdal's concept of 'backwash effect' refers to:", ["Movement of resources from poor to rich regions, widening disparities", "Government subsidies to backward regions", "Spread of development to surrounding areas", "Decline in birth rates in developed regions"], "Movement of resources from poor to rich regions, widening disparities", "Backwash effect describes how developed regions attract capital, skilled labor, and trade away from poorer regions, worsening inequality.", 2),
                    make_q("The 'spread effect' in regional economics means:", ["Positive spillover of growth from developed to less-developed areas", "Deliberate government-funded dispersal of population", "Spreading of industrial pollution across regions", "Equal distribution of population density"], "Positive spillover of growth from developed to less-developed areas", "Spread effect is the counterbalancing force where growth in core regions benefits peripheral areas through increased demand and diffusion.", 2),
                    make_q("Which of the following is an example of a top-down regional planning approach?", ["Central government designating Special Economic Zones", "Village-level participatory planning", "Community-driven watershed management", "Gram Sabha decision making"], "Central government designating Special Economic Zones", "Top-down approaches involve central authority decisions imposed on regions, like SEZ designations.", 1),
                    make_q("Albert Hirschman's theory of unbalanced growth suggests:", ["Strategic investment in key sectors will trigger development in linked sectors", "All sectors should receive equal investment simultaneously", "Agricultural development should precede industrial development", "Free markets naturally eliminate regional disparities"], "Strategic investment in key sectors will trigger development in linked sectors", "Hirschman argued that deliberate imbalance creates linkage effects that stimulate broader economic development.", 2),
                    make_q("In India, the backward region grant fund (BRGF) primarily targets:", ["Districts identified as backward based on composite index", "All metropolitan cities", "State capitals only", "Coastal districts"], "Districts identified as backward based on composite index", "BRGF targets 250 identified backward districts to bridge regional development gaps.", 1),
                    make_q("The 'trickle-down' hypothesis in regional planning assumes that:", ["Growth in leading sectors/regions will eventually benefit poorer areas", "Government must directly redistribute income", "Rural areas develop faster than urban areas", "Regional disparities are permanent"], "Growth in leading sectors/regions will eventually benefit poorer areas", "Trickle-down theory suggests economic benefits flow from top to bottom, though evidence is mixed.", 3),
                ],
            },
            {
                "name": "Growth Pole Theory",
                "explanation": "François Perroux proposed that growth does not occur uniformly but concentrates at 'poles' — dynamic industries or urban centers that drive surrounding development through linkages.",
                "key_points": [
                    "Propulsive industries drive growth",
                    "Forward and backward linkages",
                    "Perroux's original abstract economic space",
                    "Boudeville adapted it to geographic space",
                ],
                "questions": [
                    make_q("Growth Pole Theory was originally proposed by:", ["François Perroux", "Walter Christaller", "John Friedmann", "Gunnar Myrdal"], "François Perroux", "François Perroux introduced Growth Pole Theory in 1955, arguing growth concentrates around propulsive industries.", 1),
                    make_q("In Growth Pole Theory, a 'propulsive industry' is one that:", ["Has strong linkages and generates growth in related sectors", "Is located at a geographical pole", "Produces only consumer goods", "Has the largest number of employees"], "Has strong linkages and generates growth in related sectors", "Propulsive industries are large, innovative firms with strong inter-industry linkages that stimulate surrounding economic activity.", 2),
                    make_q("Who adapted Perroux's growth pole concept from abstract economic space to geographical space?", ["Boudeville", "Myrdal", "Rostow", "Christaller"], "Boudeville", "J.R. Boudeville translated Perroux's abstract concept into a geographical framework, making it applicable to regional planning.", 2),
                    make_q("A key criticism of Growth Pole Theory is that:", ["Benefits may not spread to hinterlands and can increase regional inequality", "It focuses too much on agriculture", "It cannot be applied to developing countries", "It requires zero government intervention"], "Benefits may not spread to hinterlands and can increase regional inequality", "Growth poles can become enclaves, concentrating resources without trickling benefits to surrounding areas.", 3),
                    make_q("Backward linkages in the context of growth poles refer to:", ["Demand created for inputs/raw materials from supplying industries", "Migration of workers back to rural areas", "Decline in industrial production", "Reduction in transport connectivity"], "Demand created for inputs/raw materials from supplying industries", "Backward linkages occur when a propulsive industry demands inputs, stimulating growth in supplier industries.", 2),
                    make_q("Forward linkages from a growth pole industry involve:", ["Output of the industry becoming input for downstream industries", "Exporting products to foreign countries", "Government subsidies to new industries", "Training programs for rural workers"], "Output of the industry becoming input for downstream industries", "Forward linkages happen when the output of a propulsive industry serves as raw material for other industries.", 2),
                ],
            },
            {
                "name": "Central Place Theory",
                "explanation": "Walter Christaller's theory explains the spatial distribution of settlements based on market areas. Settlements form a hierarchy from small villages to large cities, each serving a hexagonal market area.",
                "key_points": [
                    "Hexagonal market areas minimize unserved space",
                    "K=3 (marketing), K=4 (transport), K=7 (administrative) systems",
                    "Range and threshold concepts",
                    "Settlement hierarchy",
                ],
                "questions": [
                    make_q("Central Place Theory was proposed by:", ["Walter Christaller", "François Perroux", "August Lösch", "Von Thünen"], "Walter Christaller", "Walter Christaller proposed Central Place Theory in 1933 to explain the size, number, and distribution of settlements.", 1),
                    make_q("In Central Place Theory, the 'threshold' refers to:", ["Minimum population needed to support a service", "Maximum distance consumers will travel", "Height limit for buildings", "Population density requirement for urbanization"], "Minimum population needed to support a service", "Threshold is the minimum market size (population × purchasing power) required for a service to be economically viable.", 2),
                    make_q("The 'range' in Central Place Theory is:", ["Maximum distance consumers are willing to travel for a service", "Physical extent of the settlement", "Number of services a central place offers", "Distance between two adjacent central places"], "Maximum distance consumers are willing to travel for a service", "Range defines the outer limit of the market area beyond which consumers will go to a nearer central place.", 2),
                    make_q("In Christaller's K=3 system (marketing principle), each higher-order center serves how many lower-order centers?", ["3 (including itself and portions of 6 neighbors)", "4", "7", "2"], "3 (including itself and portions of 6 neighbors)", "Under the K=3 marketing principle, the market area of a higher-order place is 3 times that of the next lower order.", 3),
                    make_q("Why did Christaller choose hexagonal market areas instead of circular ones?", ["Hexagons tessellate without gaps or overlaps", "Hexagons have the largest area", "Circles cannot be drawn on maps", "Hexagons look more aesthetic on plans"], "Hexagons tessellate without gaps or overlaps", "Hexagons provide complete coverage of the plane without overlap or unserved areas, unlike circles.", 1),
                    make_q("The K=4 system in Central Place Theory is based on the:", ["Transport principle — settlements align along transport routes", "Marketing principle — maximizing market areas", "Administrative principle — complete control of lower-order places", "Ecological principle — settlement near water sources"], "Transport principle — settlements align along transport routes", "K=4 optimizes transport connectivity, with settlements located on routes between higher-order centers.", 2),
                    make_q("The K=7 system in Central Place Theory represents the:", ["Administrative principle — lower-order centers fall entirely within one higher-order market area", "Maximum number of services at each level", "Seven hierarchical levels of settlements", "Optimal ratio of rural to urban population"], "Administrative principle — lower-order centers fall entirely within one higher-order market area", "Under K=7, each higher-order center has complete administrative control over 6 surrounding lower-order centers.", 3),
                    make_q("August Lösch modified Central Place Theory by:", ["Allowing variable K-values across different goods and relaxing rigid hierarchy", "Adding time as a fourth dimension", "Replacing hexagons with squares", "Eliminating the concept of threshold"], "Allowing variable K-values across different goods and relaxing rigid hierarchy", "Lösch created a more flexible landscape allowing different K-values for different goods, generating 'city-rich' and 'city-poor' sectors.", 3),
                ],
            },
            {
                "name": "Urbanization Patterns & Regional Plan Preparation",
                "explanation": "Urbanization is the increasing concentration of population in urban areas. Regional plans coordinate land use, infrastructure, and development across multiple local jurisdictions.",
                "key_points": [
                    "Levels of urbanization in India",
                    "Urban-rural continuum",
                    "Regional plan components and preparation",
                    "Counter-urbanization and satellite towns",
                ],
                "questions": [
                    make_q("India's urbanization level as per Census 2011 was approximately:", ["31.2%", "45.5%", "22.8%", "55.3%"], "31.2%", "Census 2011 recorded India's urban population at 31.16%, indicating a steadily urbanizing but still predominantly rural nation.", 1),
                    make_q("A 'million-plus city' in India refers to urban agglomerations with population exceeding:", ["1 million (10 lakh)", "10 million (1 crore)", "100,000 (1 lakh)", "500,000 (5 lakh)"], "1 million (10 lakh)", "Census classification uses 'million-plus cities' for urban agglomerations with population above 10 lakh.", 1),
                    make_q("Counter-urbanization is the process of:", ["Population movement from large cities to smaller towns and rural areas", "Rapid urbanization of villages", "Increasing density in city centers", "Building new capital cities"], "Population movement from large cities to smaller towns and rural areas", "Counter-urbanization reverses the urbanization trend as people move away from congested cities to smaller settlements.", 1),
                    make_q("A satellite town is:", ["A planned self-contained settlement near a large city to decongest it", "A town with satellite communication facilities", "Any suburb of a metropolis", "A town located at a national border"], "A planned self-contained settlement near a large city to decongest it", "Satellite towns are planned near metropolitan areas to divert growth pressure, providing employment and amenities locally.", 2),
                    make_q("The Urban and Regional Development Plans Formulation and Implementation (URDPFI) guidelines are issued by:", ["Ministry of Urban Development, Government of India", "NITI Aayog", "Reserve Bank of India", "Ministry of Rural Development"], "Ministry of Urban Development, Government of India", "URDPFI guidelines by MoUD provide a framework for preparing development plans at regional, metropolitan, and local levels.", 2),
                    make_q("Which of the following is NOT a component of a regional plan?", ["Individual building floor plans", "Land use zoning", "Transportation network", "Environmental conservation zones"], "Individual building floor plans", "Regional plans deal with macro-level spatial strategies, not individual building designs.", 1),
                    make_q("The concept of 'urban primacy' refers to:", ["Dominance of one large city over all others in a country's urban system", "The first city to be established in a region", "Highest literacy rate in a city", "City with the best infrastructure"], "Dominance of one large city over all others in a country's urban system", "Urban primacy occurs when the largest city is disproportionately larger than the second city (e.g., Bangkok in Thailand).", 2),
                    make_q("Rank-size rule states that the population of the nth largest city is:", ["Population of largest city divided by n", "Population of largest city multiplied by n", "Equal to the national average", "Population of smallest city multiplied by n"], "Population of largest city divided by n", "Zipf's rank-size rule: Pn = P1/n, where Pn is population of nth city and P1 is population of the largest city.", 3),
                    make_q("If the largest city in a country has a population of 10 million, the 5th largest city's population according to the rank-size rule would be:", ["2 million", "5 million", "50 million", "1 million"], "2 million", "Rank-size rule: P5 = P1/5 = 10,000,000/5 = 2,000,000 = 2 million.", 2),
                    make_q("In India, the authority responsible for preparing a regional plan is typically the:", ["State Town and Country Planning Department or Regional Development Authority", "Municipal Corporation", "Gram Panchayat", "District Collector's Office"], "State Town and Country Planning Department or Regional Development Authority", "Regional plans in India are prepared by state-level town planning departments or special development authorities.", 1),
                ],
            },
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════
# TOPIC 2: GIS & Remote Sensing
# ═══════════════════════════════════════════════════════════════════

GIS_REMOTE_SENSING_TOPICS = [
    {
        "name": "GIS & Remote Sensing",
        "desc": "GIS components, spatial data types (raster/vector), remote sensing principles, satellite imagery, GPS, overlay analysis, buffer analysis, map projections.",
        "concepts": [
            {
                "name": "GIS Components & Spatial Data",
                "explanation": "A Geographic Information System (GIS) integrates hardware, software, data, and people to capture, store, analyze, and display spatial information. Data exists as vector (points, lines, polygons) or raster (grid cells).",
                "key_points": [
                    "Five components: hardware, software, data, people, methods",
                    "Vector data: points, lines, polygons",
                    "Raster data: grid of cells with attribute values",
                    "Topology defines spatial relationships in vector data",
                ],
                "questions": [
                    make_q("Which of the following is NOT a component of GIS?", ["Chemical analysis equipment", "Hardware", "Software", "Spatial data"], "Chemical analysis equipment", "GIS comprises hardware, software, data, people, and methods — chemical analysis equipment is not a GIS component.", 1),
                    make_q("In GIS, vector data represents spatial features as:", ["Points, lines, and polygons", "Grid cells with values", "Satellite images", "Contour lines only"], "Points, lines, and polygons", "Vector data uses discrete geometric primitives: points (wells, trees), lines (roads, rivers), and polygons (land parcels, lakes).", 1),
                    make_q("Raster data in GIS stores information as:", ["A grid of cells where each cell holds an attribute value", "Connected line segments forming boundaries", "Coordinate pairs defining vertices", "Text-based address records"], "A grid of cells where each cell holds an attribute value", "Raster data divides space into regular grid cells (pixels), each containing a single value representing an attribute.", 1),
                    make_q("Which spatial data model is better for representing continuous phenomena like elevation?", ["Raster", "Vector", "TIN only", "Tabular"], "Raster", "Raster models excel at representing continuous surfaces like elevation, temperature, and rainfall.", 2),
                    make_q("Topology in GIS refers to:", ["Spatial relationships such as adjacency, connectivity, and containment", "The physical shape of the Earth", "Map color schemes", "Height of terrain features"], "Spatial relationships such as adjacency, connectivity, and containment", "Topology defines how spatial features relate — which polygons are adjacent, which lines connect, which points are within polygons.", 3),
                    make_q("A raster cell size of 30m × 30m means:", ["Each pixel represents a 30m × 30m area on the ground", "The map is 30m wide", "There are 30 rows of pixels", "The satellite is 30m above ground"], "Each pixel represents a 30m × 30m area on the ground", "Cell size (spatial resolution) defines the ground area represented by each pixel. Landsat typically uses 30m resolution.", 1),
                    make_q("Which is an advantage of vector data over raster data?", ["More precise boundary representation and smaller file size for discrete features", "Better for continuous surface modeling", "Simpler data structure", "Faster overlay operations"], "More precise boundary representation and smaller file size for discrete features", "Vector data provides precise coordinates for boundaries and is more storage-efficient for discrete features like parcels.", 2),
                    make_q("In a GIS database, a shapefile (.shp) stores:", ["Vector data geometry", "Raster image pixels", "3D building models", "Audio recordings of field surveys"], "Vector data geometry", "Shapefiles are a popular vector format storing geometry (points, lines, polygons) along with attribute data.", 1),
                ],
            },
            {
                "name": "Remote Sensing Principles",
                "explanation": "Remote sensing acquires information about objects from a distance, typically using electromagnetic radiation. Sensors on satellites or aircraft detect reflected/emitted energy from Earth's surface.",
                "key_points": [
                    "Electromagnetic spectrum bands used in RS",
                    "Active vs passive sensors",
                    "Spectral, spatial, temporal, radiometric resolution",
                    "NDVI for vegetation analysis",
                ],
                "questions": [
                    make_q("Remote sensing is defined as:", ["Acquiring information about objects without physical contact", "Measuring distances with a tape", "Conducting field surveys on foot", "Analyzing soil samples in a laboratory"], "Acquiring information about objects without physical contact", "Remote sensing gathers data about Earth's surface from a distance, usually using electromagnetic radiation sensors.", 1),
                    make_q("An active remote sensing system:", ["Provides its own source of electromagnetic energy (e.g., RADAR)", "Relies solely on reflected sunlight", "Only works during daytime", "Measures gravitational fields"], "Provides its own source of electromagnetic energy (e.g., RADAR)", "Active sensors emit their own energy and measure the return signal. Examples: RADAR, LiDAR.", 2),
                    make_q("Which type of sensor depends on sunlight reflected from Earth's surface?", ["Passive sensor", "Active sensor", "Radar sensor", "Sonar sensor"], "Passive sensor", "Passive sensors detect naturally reflected or emitted energy (sunlight, thermal emission). They cannot operate at night in visible bands.", 1),
                    make_q("Spatial resolution in remote sensing refers to:", ["Size of the smallest feature that can be detected", "Number of spectral bands captured", "Frequency of satellite revisit", "Sensitivity to differences in energy levels"], "Size of the smallest feature that can be detected", "Spatial resolution is determined by pixel size — smaller pixels detect smaller features (e.g., 1m vs 30m).", 2),
                    make_q("NDVI (Normalized Difference Vegetation Index) is calculated using:", ["Near-Infrared and Red bands: (NIR − Red)/(NIR + Red)", "Blue and Green bands", "Thermal and microwave bands", "Ultraviolet and visible bands"], "Near-Infrared and Red bands: (NIR − Red)/(NIR + Red)", "NDVI = (NIR − Red)/(NIR + Red). Healthy vegetation strongly reflects NIR and absorbs Red, giving high NDVI values.", 2),
                    make_q("If NIR reflectance = 0.5 and Red reflectance = 0.1, the NDVI value is:", ["0.67", "0.40", "0.50", "0.80"], "0.67", "NDVI = (0.5 − 0.1)/(0.5 + 0.1) = 0.4/0.6 = 0.667 ≈ 0.67.", 2),
                    make_q("Temporal resolution in satellite remote sensing refers to:", ["Revisit time — how frequently the satellite images the same area", "Number of pixels in an image", "Wavelength range of the sensor", "Orbital altitude of the satellite"], "Revisit time — how frequently the satellite images the same area", "Temporal resolution is the time between consecutive observations of the same location (e.g., Landsat: 16 days).", 3),
                    make_q("Which satellite series provides 30m resolution multispectral imagery since 1972?", ["Landsat", "IKONOS", "SPOT", "CARTOSAT"], "Landsat", "NASA's Landsat program has provided continuous 30m multispectral imagery since Landsat 1 launched in 1972.", 1),
                    make_q("LiDAR is an example of:", ["Active remote sensing using laser pulses", "Passive remote sensing using sunlight", "Ground-based survey using total station", "Acoustic sensing using sound waves"], "Active remote sensing using laser pulses", "LiDAR (Light Detection and Ranging) emits laser pulses and measures return time to create precise 3D point clouds.", 2),
                ],
            },
            {
                "name": "GPS & Map Projections",
                "explanation": "GPS (Global Positioning System) uses satellite constellations to determine location. Map projections transform the 3D Earth surface onto 2D maps, inevitably introducing distortions.",
                "key_points": [
                    "GPS needs minimum 4 satellites for 3D fix",
                    "Types of projections: cylindrical, conical, azimuthal",
                    "Properties: conformal, equal-area, equidistant",
                    "UTM and geographic coordinate systems",
                ],
                "questions": [
                    make_q("The minimum number of GPS satellites needed for a 3D position fix is:", ["4", "3", "2", "6"], "4", "Four satellites are needed: three for trilateration (x, y, z) and one to correct for receiver clock error.", 1),
                    make_q("GPS operates using satellites in which orbital system?", ["Medium Earth Orbit (approximately 20,200 km altitude)", "Geostationary orbit (36,000 km)", "Low Earth Orbit (200 km)", "Polar orbit (800 km)"], "Medium Earth Orbit (approximately 20,200 km altitude)", "GPS satellites orbit at ~20,200 km altitude in 6 orbital planes with ~12-hour orbital periods.", 2),
                    make_q("The Mercator projection is classified as:", ["Cylindrical conformal projection", "Conical equal-area projection", "Azimuthal equidistant projection", "Polyconic projection"], "Cylindrical conformal projection", "Mercator is a cylindrical projection that preserves angles (conformal) but greatly distorts areas near the poles.", 2),
                    make_q("An equal-area map projection preserves:", ["Relative sizes of areas on the map", "Shapes of features", "Directions from a central point", "Distances along all meridians"], "Relative sizes of areas on the map", "Equal-area (equivalent) projections maintain proportional areas, though shapes may be distorted.", 1),
                    make_q("The UTM system divides the Earth into how many zones?", ["60", "24", "36", "180"], "60", "UTM (Universal Transverse Mercator) divides Earth into 60 zones, each 6° of longitude wide, numbered 1-60.", 2),
                    make_q("A conformal map projection preserves:", ["Local shapes and angles", "Areas of all features", "Distances from all points", "Cardinal directions only"], "Local shapes and angles", "Conformal projections maintain angular relationships and local shapes, important for navigation charts.", 2),
                    make_q("India falls within UTM zones:", ["42 to 47", "1 to 6", "30 to 35", "55 to 60"], "42 to 47", "India extends from approximately 68°E to 97°E, falling within UTM zones 42 through 47.", 3),
                    make_q("DGPS (Differential GPS) improves accuracy by:", ["Using a base station at a known location to compute and broadcast correction signals", "Adding more satellites to the constellation", "Using longer antennas on the receiver", "Increasing the signal frequency"], "Using a base station at a known location to compute and broadcast correction signals", "DGPS uses a reference station to calculate errors and broadcast corrections, achieving sub-meter accuracy.", 3),
                ],
            },
            {
                "name": "GIS Analysis Techniques",
                "explanation": "GIS provides powerful analytical tools including overlay analysis, buffer analysis, network analysis, and spatial interpolation for urban planning and decision support.",
                "key_points": [
                    "Overlay: union, intersect, clip operations",
                    "Buffer analysis for proximity zones",
                    "Network analysis for routing and allocation",
                    "Spatial interpolation methods (IDW, Kriging)",
                ],
                "questions": [
                    make_q("Buffer analysis in GIS creates:", ["Zones of specified distance around features", "Color-coded maps of population", "3D models of terrain", "Statistical summaries of attribute data"], "Zones of specified distance around features", "Buffer analysis generates polygon zones at specified distances around point, line, or polygon features for proximity analysis.", 1),
                    make_q("If a 500m buffer is created around a school point in GIS, the result is:", ["A circle with 500m radius centered on the school", "A square with 500m sides", "A line 500m long from the school", "The school point moved 500m"], "A circle with 500m radius centered on the school", "A buffer around a point creates a circular polygon with the specified distance as the radius.", 1),
                    make_q("Overlay analysis in GIS combines:", ["Two or more spatial layers to create new derived information", "Multiple satellite images from different dates", "Text documents and spreadsheets", "Audio and video files"], "Two or more spatial layers to create new derived information", "Overlay analysis combines multiple layers (e.g., land use + soil type) to derive new spatial information for decision making.", 2),
                    make_q("In GIS, the 'intersect' overlay operation:", ["Returns only areas common to both input layers", "Returns all areas from both layers", "Subtracts one layer from another", "Merges all features without regard to overlap"], "Returns only areas common to both input layers", "Intersect preserves only the geometric area where both input layers overlap, retaining attributes from both.", 2),
                    make_q("Network analysis in GIS is used for:", ["Shortest path routing, service area delineation, and facility allocation", "Satellite orbit calculation", "Weather prediction", "Image classification"], "Shortest path routing, service area delineation, and facility allocation", "Network analysis operates on line datasets (roads, utilities) for routing, closest facility, and service area problems.", 3),
                    make_q("IDW (Inverse Distance Weighting) interpolation assigns values based on:", ["Nearby known points weighted inversely proportional to distance", "Equal weights to all sample points", "Random selection of data points", "Atmospheric pressure readings"], "Nearby known points weighted inversely proportional to distance", "IDW assumes closer points have more influence — weights decrease with distance from the prediction location.", 3),
                    make_q("A suitability analysis using GIS overlay might combine which layers?", ["Slope, land use, soil type, and proximity to roads", "Only satellite images", "Architectural floor plans", "Building elevation drawings"], "Slope, land use, soil type, and proximity to roads", "Multi-criteria suitability analysis overlays multiple environmental and infrastructure layers to find optimal locations.", 2),
                    make_q("Georeferencing in GIS means:", ["Assigning real-world coordinates to a raster image or map", "Creating a geographic dictionary", "Measuring distances on a map", "Drawing contour lines"], "Assigning real-world coordinates to a raster image or map", "Georeferencing aligns raster data (scanned maps, aerial photos) to a known coordinate system using control points.", 1),
                ],
            },
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════
# TOPIC 3: Planning Techniques & Management
# ═══════════════════════════════════════════════════════════════════

PLANNING_TECHNIQUES_TOPICS = [
    {
        "name": "Planning Techniques & Management",
        "desc": "PERT/CPM, project planning, construction management, cost estimation, scheduling, bar charts, network diagrams, and resource allocation.",
        "concepts": [
            {
                "name": "PERT & CPM Fundamentals",
                "explanation": "PERT (Program Evaluation and Review Technique) uses probabilistic time estimates, while CPM (Critical Path Method) uses deterministic durations. Both use network diagrams to plan and control projects.",
                "key_points": [
                    "PERT uses three time estimates (optimistic, most likely, pessimistic)",
                    "CPM uses single deterministic time estimate",
                    "Critical path = longest path through the network",
                    "Expected time (Te) = (to + 4tm + tp) / 6",
                ],
                "questions": [
                    make_q("PERT stands for:", ["Program Evaluation and Review Technique", "Project Estimation and Resource Tracking", "Planning Execution and Review Technique", "Performance Evaluation Rating Tool"], "Program Evaluation and Review Technique", "PERT was developed by the US Navy in 1958 for the Polaris missile project to manage uncertain activity durations.", 1),
                    make_q("CPM uses which type of time estimate?", ["Single deterministic duration", "Three probabilistic estimates", "No time estimates", "Variable random durations"], "Single deterministic duration", "CPM (Critical Path Method) assumes activity durations are known with certainty, using single time estimates.", 1),
                    make_q("In PERT, if optimistic time = 4 days, most likely = 6 days, and pessimistic = 14 days, the expected time is:", ["7 days", "8 days", "6 days", "10 days"], "7 days", "Te = (to + 4tm + tp)/6 = (4 + 4×6 + 14)/6 = (4 + 24 + 14)/6 = 42/6 = 7 days.", 2),
                    make_q("The critical path in a project network is:", ["The longest path determining minimum project duration", "The shortest path through the network", "The most expensive sequence of activities", "The path with the most resources"], "The longest path determining minimum project duration", "The critical path is the longest sequence of dependent activities — it determines the earliest possible project completion.", 1),
                    make_q("Activities on the critical path have:", ["Zero total float", "Maximum float", "Negative float", "Float equal to project duration"], "Zero total float", "Critical activities have zero float — any delay in a critical activity directly delays the entire project.", 2),
                    make_q("If activity A→B has ES=5, EF=12, LS=8, LF=15, the total float is:", ["3 days", "7 days", "5 days", "0 days"], "3 days", "Total Float = LS − ES = 8 − 5 = 3 days (or LF − EF = 15 − 12 = 3 days).", 2),
                    make_q("In PERT, the variance of an activity with optimistic=2, pessimistic=14 is:", ["4", "2", "6", "12"], "4", "Variance = ((tp − to)/6)² = ((14 − 2)/6)² = (12/6)² = 2² = 4.", 3),
                    make_q("Free float of an activity is:", ["Delay possible without affecting the earliest start of any successor activity", "Delay possible without delaying the project", "Total duration minus activity duration", "Always greater than total float"], "Delay possible without affecting the earliest start of any successor activity", "Free float is the amount an activity can be delayed without affecting the ES of immediately following activities.", 3),
                    make_q("A dummy activity in a network diagram:", ["Has zero duration and represents logical dependency only", "Is the longest activity", "Requires the most resources", "Can be eliminated from the critical path"], "Has zero duration and represents logical dependency only", "Dummy activities (shown as dashed arrows) maintain logical relationships without consuming time or resources.", 1),
                ],
            },
            {
                "name": "Bar Charts & Scheduling",
                "explanation": "Bar charts (Gantt charts) are visual tools showing activity start/finish times on a time scale. They are simple to understand but limited in showing dependencies between activities.",
                "key_points": [
                    "Gantt chart: horizontal bars on time axis",
                    "Easy to read but poor at showing dependencies",
                    "Milestone charts mark key events",
                    "Resource leveling adjusts schedule to optimize resource use",
                ],
                "questions": [
                    make_q("A Gantt chart is also known as:", ["Bar chart", "Network diagram", "Histogram", "Pie chart"], "Bar chart", "Henry Gantt developed the bar chart format showing activities as horizontal bars plotted against a time axis.", 1),
                    make_q("The main limitation of a Gantt chart is:", ["It does not clearly show dependencies between activities", "It cannot display time information", "It is too complex to understand", "It cannot show more than 10 activities"], "It does not clearly show dependencies between activities", "While easy to read, Gantt charts poorly represent logical dependencies and interdependencies between activities.", 2),
                    make_q("A milestone in project scheduling represents:", ["A significant event or checkpoint with zero duration", "The longest activity in the project", "A resource-intensive phase", "A budget approval point only"], "A significant event or checkpoint with zero duration", "Milestones mark key achievements or decision points (e.g., design approval, foundation completion) with zero duration.", 1),
                    make_q("Resource leveling aims to:", ["Smooth out resource demand to avoid peaks and valleys", "Increase project duration", "Add more workers to the project", "Eliminate the critical path"], "Smooth out resource demand to avoid peaks and valleys", "Resource leveling adjusts activity timing (using float) to reduce resource demand fluctuations without extending the project.", 3),
                    make_q("Crashing a project means:", ["Reducing activity duration by adding resources at extra cost", "Allowing the project to fail", "Removing activities from the schedule", "Starting a new project"], "Reducing activity duration by adding resources at extra cost", "Crashing involves shortening critical path activities by allocating additional resources, increasing direct costs.", 3),
                    make_q("Lead time in scheduling refers to:", ["Starting a successor activity before the predecessor finishes", "Time taken to deliver materials", "Duration of the longest activity", "Delay between project phases"], "Starting a successor activity before the predecessor finishes", "Lead is a negative lag — allowing an overlap where a successor begins before its predecessor completes (e.g., FS-2 days).", 2),
                    make_q("The S-curve in project management shows:", ["Cumulative progress or expenditure over time", "Structural deflection of beams", "Soil bearing capacity variation", "Population growth rate"], "Cumulative progress or expenditure over time", "S-curves plot cumulative cost, labor hours, or progress against time, typically showing slow start, rapid middle, and tapering end.", 1),
                    make_q("In a project with 10 activities, if the critical path duration is 45 days and a non-critical activity with 5 days of float is delayed by 3 days, the project duration becomes:", ["45 days (unchanged)", "48 days", "42 days", "50 days"], "45 days (unchanged)", "A 3-day delay on an activity with 5 days float does not affect project duration since delay < available float.", 2),
                ],
            },
            {
                "name": "Cost Estimation & Construction Management",
                "explanation": "Cost estimation determines the financial resources required for construction. Methods range from rough preliminary estimates to detailed item-wise estimates based on quantities and rates.",
                "key_points": [
                    "Preliminary, detailed, and revised estimates",
                    "Plinth area rate and cubic rate methods",
                    "Rate analysis components: materials, labor, overhead",
                    "Contingencies typically 3-5% of estimated cost",
                ],
                "questions": [
                    make_q("A plinth area estimate is calculated by:", ["Multiplying plinth area by a per-unit rate based on building type", "Counting every brick and steel bar individually", "Dividing total budget by number of floors", "Using satellite imagery analysis"], "Multiplying plinth area by a per-unit rate based on building type", "Plinth area method provides a quick approximate estimate using the built-up area at plinth level × rate per sq.m. for similar buildings.", 1),
                    make_q("In a detailed estimate, the quantity of each item is calculated from:", ["Drawings and specifications", "Previous project photos", "Contractor's verbal quotation", "Random assumptions"], "Drawings and specifications", "Detailed estimates use architectural/structural drawings and specifications to measure exact quantities of each work item.", 1),
                    make_q("Contingency allowance in an estimate typically is:", ["3-5% of estimated cost", "25-30% of estimated cost", "50% of estimated cost", "0% — no contingency needed"], "3-5% of estimated cost", "Contingencies cover unforeseen items, price variations, and minor changes — typically 3-5% for government projects.", 2),
                    make_q("Rate analysis for a construction item includes:", ["Material cost, labor cost, and overhead/profit", "Only material cost", "Only labor cost", "Only contractor's profit margin"], "Material cost, labor cost, and overhead/profit", "Rate analysis breaks down unit cost into materials, labor, equipment, contractor overhead (typically 10%), and profit.", 2),
                    make_q("The cubic content method of estimation measures:", ["Volume of building from plinth to roof and multiplies by rate per cubic meter", "Area of the roof only", "Length of all walls", "Number of rooms in the building"], "Volume of building from plinth to roof and multiplies by rate per cubic meter", "Cubic rate method uses total volume (length × breadth × height) multiplied by a rate per cubic meter.", 1),
                    make_q("In construction, work-breakdown structure (WBS) is used to:", ["Decompose the project into manageable work packages", "Calculate structural loads", "Design building aesthetics", "Determine soil bearing capacity"], "Decompose the project into manageable work packages", "WBS hierarchically breaks down total project scope into smaller, manageable deliverables and work packages.", 2),
                    make_q("Earned Value Management (EVM) integrates which three dimensions?", ["Scope, schedule, and cost performance", "Length, width, and height", "Time, temperature, and pressure", "Materials, labor, and equipment only"], "Scope, schedule, and cost performance", "EVM combines scope (planned work), schedule (time), and cost to provide objective measures of project performance.", 2),
                    make_q("If a project has Budgeted Cost of Work Performed (BCWP) = ₹80 lakh and Actual Cost of Work Performed (ACWP) = ₹100 lakh, the Cost Performance Index (CPI) is:", ["0.8", "1.25", "1.0", "0.6"], "0.8", "CPI = BCWP/ACWP = 80/100 = 0.8, indicating cost overrun (the project is over budget).", 3),
                    make_q("A Budgeted Cost of Work Scheduled (BCWS) = ₹60 lakh and BCWP = ₹45 lakh gives a Schedule Performance Index (SPI) of:", ["0.75", "1.33", "1.0", "0.50"], "0.75", "SPI = BCWP/BCWS = 45/60 = 0.75, indicating the project is behind schedule (only 75% of planned work completed).", 2),
                ],
            },
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════
# TOPIC 4: Professional Practice
# ═══════════════════════════════════════════════════════════════════

PROFESSIONAL_PRACTICE_TOPICS = [
    {
        "name": "Professional Practice",
        "desc": "Contracts, tenders, specifications, building bye-laws, NBC codes, architectural fees, professional ethics, arbitration, and legal framework for architectural practice.",
        "concepts": [
            {
                "name": "Contracts & Tenders",
                "explanation": "Construction contracts define the legal relationship between client and contractor. Tender is the process of inviting bids for executing work. Common contract types include lump sum, item rate, and cost-plus.",
                "key_points": [
                    "Open tender vs limited/invited tender",
                    "Lump sum, item rate, cost-plus contracts",
                    "Earnest money deposit (EMD) and security deposit",
                    "Notice Inviting Tender (NIT) components",
                ],
                "questions": [
                    make_q("In an open tender system:", ["Any eligible contractor can submit a bid", "Only pre-selected contractors can bid", "The contractor is directly appointed", "No bidding process is followed"], "Any eligible contractor can submit a bid", "Open tender (advertised) invites all eligible contractors to bid, ensuring maximum competition and transparency.", 1),
                    make_q("An item rate contract means:", ["The contractor is paid for actual quantities executed at agreed rates per item", "A fixed lump sum is paid regardless of quantities", "The contractor is paid cost plus a fixed fee", "Payment is made only upon project completion"], "The contractor is paid for actual quantities executed at agreed rates per item", "Item rate contracts pay based on measured quantities of each work item at pre-agreed unit rates. Most common in government works.", 2),
                    make_q("Earnest Money Deposit (EMD) in tendering is:", ["A refundable deposit submitted with the bid to show serious intent", "Final payment to the contractor", "Architect's professional fee", "Insurance premium for the project"], "A refundable deposit submitted with the bid to show serious intent", "EMD (typically 2-5% of estimated cost) demonstrates the bidder's commitment. It is returned to unsuccessful bidders.", 1),
                    make_q("A cost-plus contract is most suitable when:", ["Project scope is uncertain and cannot be fully defined at the start", "Exact quantities and specifications are fully known", "The lowest bid must be accepted", "No architect supervision is required"], "Project scope is uncertain and cannot be fully defined at the start", "Cost-plus contracts suit uncertain-scope projects where the client pays actual costs plus an agreed fee/percentage for contractor profit.", 2),
                    make_q("Security deposit in a construction contract is typically:", ["5-10% of contract value, retained as guarantee for work quality", "100% of contract value", "Paid to the architect", "0% for government projects"], "5-10% of contract value, retained as guarantee for work quality", "Security deposit (5-10%) is retained from running bills to ensure the contractor completes the work satisfactorily.", 3),
                    make_q("A negotiated tender is appropriate when:", ["Work is of specialized nature or during emergency", "Large number of contractors are available", "Maximum competition is desired", "The project has a very large budget"], "Work is of specialized nature or during emergency", "Negotiated tenders are used for specialized works, emergencies, or when only one qualified contractor is available.", 2),
                    make_q("The defect liability period in a typical construction contract is:", ["6-12 months after completion", "5-10 years after completion", "Only during construction", "1 month before completion"], "6-12 months after completion", "Defect liability period (typically 6-12 months) requires the contractor to repair any defects discovered after completion.", 1),
                    make_q("Liquidated damages in a construction contract are:", ["Pre-agreed compensation for delay, deducted from contractor's payments", "Additional payments for early completion", "Insurance claims for accidents", "Taxes paid to the government"], "Pre-agreed compensation for delay, deducted from contractor's payments", "Liquidated damages are pre-determined penalties (typically 0.5-1% per week of delay) levied for late completion.", 2),
                ],
            },
            {
                "name": "Specifications & Building Bye-Laws",
                "explanation": "Specifications describe quality of materials and workmanship. Building bye-laws regulate construction to ensure safety, hygiene, and orderly development. NBC (National Building Code) provides comprehensive construction guidelines.",
                "key_points": [
                    "General vs detailed specifications",
                    "NBC 2016 provisions",
                    "FAR/FSI, ground coverage, setbacks",
                    "Fire safety and structural safety codes",
                ],
                "questions": [
                    make_q("General specifications describe:", ["Overall quality standards and methods applicable to all items of work", "Detailed measurements of each work item", "Only the material brand names to be used", "Contractor selection criteria"], "Overall quality standards and methods applicable to all items of work", "General specifications outline broad standards for materials, workmanship, and methods applicable across the entire project.", 1),
                    make_q("Detailed specifications differ from general specifications in that they:", ["Describe exact materials, proportions, and methods for each specific work item", "Are shorter and less descriptive", "Are only verbal instructions", "Apply to all projects universally"], "Describe exact materials, proportions, and methods for each specific work item", "Detailed specifications provide item-wise precise requirements: material grades, mix proportions, surface finish, testing requirements.", 3),
                    make_q("FAR (Floor Area Ratio) is calculated as:", ["Total built-up area of all floors divided by plot area", "Plot area divided by number of floors", "Height of building divided by road width", "Ground coverage multiplied by setback distance"], "Total built-up area of all floors divided by plot area", "FAR = Total floor area / Plot area. If FAR is 2.0 on a 500 sq.m plot, maximum built-up area is 1000 sq.m.", 1),
                    make_q("If a plot is 1000 sq.m and permissible FAR is 1.5, the maximum total floor area allowed is:", ["1500 sq.m", "1000 sq.m", "2000 sq.m", "667 sq.m"], "1500 sq.m", "Maximum floor area = FAR × Plot area = 1.5 × 1000 = 1500 sq.m distributed across floors.", 1),
                    make_q("Building setback refers to:", ["Mandatory open space between building and plot boundary", "Distance between two buildings on the same plot", "Height of the parapet wall", "Depth of the foundation"], "Mandatory open space between building and plot boundary", "Setbacks ensure light, ventilation, fire safety, and privacy. Front, rear, and side setbacks are prescribed by bye-laws.", 1),
                    make_q("The National Building Code of India (NBC) is published by:", ["Bureau of Indian Standards (BIS)", "CPWD", "Ministry of Housing", "Council of Architecture"], "Bureau of Indian Standards (BIS)", "NBC is published by BIS as IS:SP7, providing comprehensive guidelines for construction across India.", 2),
                    make_q("Ground coverage is defined as:", ["Percentage of plot area covered by the building at ground level", "Total area of all floors", "Area of the foundation only", "Area of the roof including overhangs"], "Percentage of plot area covered by the building at ground level", "Ground coverage = (Building footprint area / Plot area) × 100. Bye-laws limit it to ensure open spaces.", 2),
                    make_q("As per NBC, the minimum width of a residential staircase should be:", ["1.0 m", "0.5 m", "2.0 m", "0.75 m"], "1.0 m", "NBC specifies minimum 1.0 m clear width for residential staircases to ensure safe egress and accessibility.", 2),
                    make_q("Fire escape staircases as per NBC should be:", ["Enclosed with fire-resistant walls and have direct access to ground level", "Open to the sky only", "Made of timber with steel railings", "Located inside the building core without separation"], "Enclosed with fire-resistant walls and have direct access to ground level", "NBC mandates fire escape stairs be enclosed in fire-rated construction with direct ground-level exit.", 2),
                ],
            },
            {
                "name": "Architectural Fees & Professional Ethics",
                "explanation": "Architects' fees are governed by the Council of Architecture (COA) regulations. Professional ethics require architects to maintain integrity, serve public interest, and uphold professional standards.",
                "key_points": [
                    "COA fee structure based on project cost",
                    "Conditions of Engagement (COE)",
                    "Architect's duties and liabilities",
                    "Code of professional conduct",
                ],
                "questions": [
                    make_q("In India, the minimum architectural fees are regulated by:", ["Council of Architecture (COA)", "Institute of Engineers India", "Ministry of Finance", "RERA"], "Council of Architecture (COA)", "COA, established under the Architects Act 1972, prescribes minimum conditions of engagement and fee scales.", 1),
                    make_q("According to COA, an architect's services typically include:", ["Preliminary design, working drawings, specifications, and site supervision", "Only drawing the floor plan", "Only structural design", "Only interior decoration"], "Preliminary design, working drawings, specifications, and site supervision", "Full architectural services span from inception through design development, documentation, tendering assistance, and construction supervision.", 2),
                    make_q("The Architects Act in India was enacted in:", ["1972", "1947", "2000", "1956"], "1972", "The Architects Act 1972 established the Council of Architecture to regulate the profession and architectural education.", 1),
                    make_q("An architect can be held liable for:", ["Professional negligence causing structural failure or safety issues", "Client's inability to secure a bank loan", "Changes in government regulations after design approval", "Contractor's personal financial problems"], "Professional negligence causing structural failure or safety issues", "Architects have professional liability for design deficiencies, specification errors, or negligent supervision causing damage.", 3),
                    make_q("Professional indemnity insurance for architects covers:", ["Claims arising from professional negligence or errors in design", "Fire damage to the building under construction", "Worker injuries on site", "Theft of construction materials"], "Claims arising from professional negligence or errors in design", "Professional indemnity insurance protects architects against claims of negligence, errors, or omissions in professional services.", 2),
                    make_q("According to professional ethics, an architect should NOT:", ["Simultaneously work for competing clients on the same project without disclosure", "Charge fees as per COA scale", "Maintain client confidentiality", "Continue professional development"], "Simultaneously work for competing clients on the same project without disclosure", "Conflict of interest must be avoided — architects cannot serve competing interests without transparent disclosure and consent.", 1),
                    make_q("The minimum qualification to register as an architect with COA is:", ["Recognized degree in architecture (B.Arch)", "Diploma in civil engineering", "Master's degree in architecture only", "10 years of construction experience"], "Recognized degree in architecture (B.Arch)", "Section 14 of the Architects Act requires a recognized B.Arch degree (5-year program) for COA registration.", 1),
                ],
            },
            {
                "name": "Arbitration & Dispute Resolution",
                "explanation": "Construction disputes are resolved through negotiation, mediation, arbitration, or litigation. The Arbitration and Conciliation Act 1996 governs arbitration proceedings in India.",
                "key_points": [
                    "Arbitration as alternative to litigation",
                    "Arbitration clause in contracts",
                    "Arbitrator appointment and proceedings",
                    "Arbitral award enforcement",
                ],
                "questions": [
                    make_q("Arbitration in construction disputes is:", ["An alternative dispute resolution method where a neutral third party gives a binding decision", "A court trial with a judge", "Informal discussion between contractor and architect", "A method of selecting the lowest bidder"], "An alternative dispute resolution method where a neutral third party gives a binding decision", "Arbitration provides faster, less formal resolution than courts. The arbitrator's award is legally binding.", 1),
                    make_q("The Arbitration and Conciliation Act in India was enacted in:", ["1996", "1872", "2016", "1947"], "1996", "The Arbitration and Conciliation Act 1996 (amended 2015, 2019) governs domestic and international arbitration in India.", 2),
                    make_q("An arbitration clause in a construction contract:", ["Specifies that disputes will be resolved through arbitration rather than courts", "Determines the project completion date", "Defines the contractor's profit margin", "Lists the materials to be used"], "Specifies that disputes will be resolved through arbitration rather than courts", "The arbitration clause is a pre-agreed provision directing parties to resolve disputes through arbitration.", 1),
                    make_q("Mediation differs from arbitration in that:", ["The mediator facilitates agreement but cannot impose a binding decision", "The mediator's decision is legally binding", "Mediation is always conducted in court", "Mediation requires a panel of three judges"], "The mediator facilitates agreement but cannot impose a binding decision", "Mediation is a facilitative process — the mediator helps parties reach mutual agreement but has no authority to impose a decision.", 3),
                    make_q("In a construction dispute, the order of preference for dispute resolution is typically:", ["Negotiation → Mediation → Arbitration → Litigation", "Litigation → Arbitration → Mediation → Negotiation", "Arbitration only", "Litigation only"], "Negotiation → Mediation → Arbitration → Litigation", "Dispute resolution escalates from informal (negotiation) to formal (litigation), preferring less costly methods first.", 2),
                    make_q("An arbitral award can be challenged in court under the 1996 Act on grounds of:", ["Public policy violation, fraud, or procedural irregularities", "Any reason the losing party disagrees with", "Insufficient profit for the contractor", "The project took too long"], "Public policy violation, fraud, or procedural irregularities", "Section 34 allows challenge only on limited grounds: incapacity, invalid agreement, procedural errors, or public policy violation.", 3),
                    make_q("Conciliation as per the Arbitration Act differs from arbitration because:", ["It is non-binding unless parties reach a settlement agreement", "It is always binding", "It is more formal than arbitration", "It can only be done by a court-appointed officer"], "It is non-binding unless parties reach a settlement agreement", "Conciliation is voluntary and non-binding. Only when parties sign a settlement agreement does it become enforceable as an arbitral award.", 3),
                ],
            },
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════
# SEEDING FUNCTION
# ═══════════════════════════════════════════════════════════════════

def seed_part_b2():
    db = SessionLocal()
    try:
        order_idx = 23  # Start after existing 22 topics
        total_topics = 0
        total_concepts = 0
        total_questions = 0

        all_topic_groups = (
            REGIONAL_PLANNING_TOPICS
            + GIS_REMOTE_SENSING_TOPICS
            + PLANNING_TECHNIQUES_TOPICS
            + PROFESSIONAL_PRACTICE_TOPICS
        )

        for topic_def in all_topic_groups:
            # Skip if topic already exists
            existing = db.query(Topic).filter(
                Topic.subject_id == ARCH_SUBJECT_ID,
                Topic.name == topic_def["name"],
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

        # Print difficulty distribution
        easy = sum(
            1 for tg in all_topic_groups
            for c in tg["concepts"]
            for q in c["questions"]
            if q["difficulty"] == 1
        )
        medium = sum(
            1 for tg in all_topic_groups
            for c in tg["concepts"]
            for q in c["questions"]
            if q["difficulty"] == 2
        )
        hard = sum(
            1 for tg in all_topic_groups
            for c in tg["concepts"]
            for q in c["questions"]
            if q["difficulty"] == 3
        )
        total = easy + medium + hard
        print(f"\n📊 Difficulty Distribution:")
        print(f"   Easy (1):   {easy} ({100*easy//total}%)")
        print(f"   Medium (2): {medium} ({100*medium//total}%)")
        print(f"   Hard (3):   {hard} ({100*hard//total}%)")
        print(f"   Total:      {total}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_part_b2()
