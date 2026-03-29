# Part 9: GPS + GIS Analysis
questions_part9 = [
  {
    "concept_id": "ddca910f",
    "question_text": "The GPS space segment consists of:",
    "options": [
      "A constellation of 24+ satellites in 6 orbital planes at approximately 20,200 km altitude",
      "Ground-based transmitter stations only",
      "A single geostationary satellite",
      "12 satellites in 2 orbital planes"
    ],
    "difficulty": "medium",
    "explanation": "GPS space segment has 24+ operational satellites (currently 31) in 6 orbital planes inclined 55° to the equator at ~20,200 km altitude. Each satellite orbits every 11 hours 58 minutes (nearly 12-hour period). This configuration ensures at least 4 satellites are visible from any point on Earth at any time for position fixing."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "The minimum number of GPS satellites needed for a 3D position fix is:",
    "options": [
      "4 satellites",
      "3 satellites",
      "2 satellites",
      "6 satellites"
    ],
    "difficulty": "medium",
    "explanation": "Four satellites are needed: 3 for trilateration (determining x, y, z position from intersection of three spheres) plus 1 to solve for receiver clock error. Each satellite transmits its position and precise time; the receiver calculates pseudorange from signal travel time. With known satellite positions, four equations solve four unknowns (x, y, z, clock bias)."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "DGPS (Differential GPS) improves accuracy by:",
    "options": [
      "Using a base station at a known location to calculate and broadcast correction signals to nearby receivers",
      "Using more satellites in the constellation",
      "Increasing the power of GPS signals",
      "Using laser instead of radio signals"
    ],
    "difficulty": "medium",
    "explanation": "DGPS places a reference station at a precisely surveyed location. It compares its known position with GPS-calculated position, determining errors from atmospheric delays, orbit inaccuracies, and clock drift. These corrections are broadcast to nearby users in real-time. DGPS achieves sub-meter accuracy compared to standard GPS (3-5m accuracy)."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "NavIC (IRNSS — Indian Regional Navigation Satellite System) consists of:",
    "options": [
      "7 satellites providing coverage over India and surrounding region (1,500 km beyond borders)",
      "24 satellites providing global coverage",
      "3 satellites for India only",
      "12 satellites covering Asia-Pacific"
    ],
    "difficulty": "medium",
    "explanation": "NavIC (Navigation with Indian Constellation) has 7 satellites: 3 in geostationary orbit (GEO) and 4 in geosynchronous inclined orbit (GSO) at 36° inclination. It provides position accuracy of better than 20m over India and 1,500 km beyond borders. Dual frequency (L5 and S band) signals provide civilian and restricted services."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "The UTM (Universal Transverse Mercator) projection divides the world into:",
    "options": [
      "60 zones, each 6 degrees of longitude wide",
      "36 zones, each 10 degrees wide",
      "24 zones, each 15 degrees wide",
      "12 zones, each 30 degrees wide"
    ],
    "difficulty": "medium",
    "explanation": "UTM creates 60 zones, each 6° wide, from 80°S to 84°N. Each zone uses a Transverse Mercator projection with scale factor 0.9996 at the central meridian. Coordinates are in meters: easting (500,000m at central meridian) and northing (0 at equator in Northern Hemisphere). UTM minimizes distortion within each zone for large-scale mapping."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "Survey of India (SOI) topographic maps at 1:50,000 scale are identified using:",
    "options": [
      "An alphanumeric grid referencing system based on 1° latitude × 1° longitude sheets",
      "Only latitude and longitude coordinates",
      "Random serial numbers",
      "City names and dates"
    ],
    "difficulty": "medium",
    "explanation": "SOI toposheets follow a hierarchical numbering: India/degree sheets (1:250,000), each divided into 16 sheets at 1:50,000 (15' × 15'), further into 4 sheets at 1:25,000. Each sheet is numbered like 45D/7, where 45 is the degree sheet, D is the quarter, and 7 is the specific 1:50,000 sheet."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "A 6-figure grid reference on a SOI toposheet provides location accuracy of:",
    "options": [
      "100 meters",
      "1 kilometer",
      "10 meters",
      "1 meter"
    ],
    "difficulty": "hard",
    "explanation": "Grid references: 4-figure (e.g., 2347) identifies a 1km × 1km grid square; 6-figure (e.g., 234478) identifies a 100m × 100m square by subdividing each 1km square into tenths. The first three digits are easting, last three are northing. For GATE problems, reading eastings first (left) then northings (up) is the convention."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "On a 1:50,000 toposheet, the contour interval is typically:",
    "options": [
      "20 meters",
      "5 meters",
      "50 meters",
      "100 meters"
    ],
    "difficulty": "medium",
    "explanation": "SOI toposheets at 1:50,000 use 20m contour interval with index contours (thicker lines) at every 100m (5th contour). At 1:25,000 scale, contour interval is 10m. Contours show terrain shape: closely spaced = steep slope, widely spaced = gentle slope, V-shaped pointing upstream = valley, V-shaped pointing downstream = ridge."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "If two points on a 1:50,000 map are 4.5 cm apart and the contour difference between them is 60m, the average gradient is:",
    "options": [
      "1 in 37.5 (approximately 2.67%)",
      "1 in 75 (approximately 1.33%)",
      "1 in 15 (approximately 6.67%)",
      "1 in 100 (approximately 1%)"
    ],
    "difficulty": "hard",
    "explanation": "Ground distance = 4.5 × 50,000 = 225,000 cm = 2,250 m. Gradient = rise/run = 60/2250 = 1/37.5 or 2.67%. This gradient calculation from toposheets is essential for road alignment, pipeline routing, and drainage design. Slopes >5% require special consideration for road design; >15% generally unsuitable for development."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "Tissot's indicatrix is used to show:",
    "options": [
      "Map projection distortion patterns — how circles on the globe are transformed to ellipses on the map",
      "The location of GPS satellites",
      "Contour patterns on toposheets",
      "Color coding standards for maps"
    ],
    "difficulty": "hard",
    "explanation": "Tissot's indicatrix represents infinitesimally small circles on the globe as ellipses on the projected map, showing: shape distortion (circle → ellipse), area distortion (ellipse area ≠ original), and angular distortion. On conformal maps, indicatrices are circles of varying size; on equal-area maps, varying shapes but equal areas."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "GPS errors include all EXCEPT:",
    "options": [
      "Magnetic declination error",
      "Ionospheric delay",
      "Multipath error",
      "Satellite clock error"
    ],
    "difficulty": "medium",
    "explanation": "GPS errors include: ionospheric delay (50-150m), tropospheric delay (2-25m), satellite clock errors (corrected by control segment), ephemeris errors (satellite position), multipath (signal reflection off surfaces), receiver noise, and GDOP (poor satellite geometry). Magnetic declination affects compass bearings, not GPS positioning."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "GDOP (Geometric Dilution of Precision) in GPS is affected by:",
    "options": [
      "The geometric arrangement of satellites relative to the receiver",
      "The number of ground control stations",
      "The receiver's battery level",
      "The time of day"
    ],
    "difficulty": "hard",
    "explanation": "GDOP measures how satellite geometry affects position accuracy. Low GDOP (good geometry) occurs when satellites are well-distributed across the sky. High GDOP (poor geometry, e.g., satellites clustered together) amplifies ranging errors. GDOP < 3 is excellent, 3-6 is good, >6 is poor. Types include HDOP (horizontal), VDOP (vertical), PDOP (position)."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "A Total Station instrument combines:",
    "options": [
      "Electronic Distance Measurement (EDM) and electronic theodolite in a single unit",
      "GPS receiver and compass",
      "Level and chain",
      "Planimeter and pantograph"
    ],
    "difficulty": "medium",
    "explanation": "A Total Station integrates EDM (infrared/laser distance measurement) with an electronic theodolite (angle measurement) and onboard computer. It measures distances (±2-3mm + 2ppm) and angles (±1-5 arc seconds), calculating 3D coordinates in real-time. Data is stored digitally for direct transfer to CAD/GIS software. Essential for modern surveying."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "The Indian Polyconic projection is used for:",
    "options": [
      "Survey of India topographical maps covering the Indian subcontinent",
      "World navigation charts",
      "Polar region mapping",
      "Ocean floor mapping"
    ],
    "difficulty": "medium",
    "explanation": "The modified Polyconic projection was adopted by Survey of India for toposheets. It uses multiple cone surfaces tangent at each latitude, reducing distortion across India's large latitudinal extent (8°N-37°N). At 1:50,000 and 1:250,000 scales, the distortion is negligible within each sheet. India is transitioning to UTM for GPS compatibility."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "GLONASS is the satellite navigation system of:",
    "options": [
      "Russia",
      "European Union",
      "China",
      "India"
    ],
    "difficulty": "medium",
    "explanation": "GLONASS (Global Navigation Satellite System) is Russia's counterpart to GPS, with 24 satellites in 3 orbital planes at 19,100 km altitude. Other GNSS systems: GPS (USA), Galileo (EU, 30 satellites), BeiDou (China, 35 satellites), NavIC/IRNSS (India, 7 satellites, regional). Modern receivers use multiple GNSS for improved accuracy and reliability."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "Chain surveying is suitable for:",
    "options": [
      "Small areas with simple details on relatively flat terrain",
      "Large-scale topographic mapping",
      "Underwater surveys",
      "Aerial triangulation"
    ],
    "difficulty": "medium",
    "explanation": "Chain surveying uses only linear measurements (chain/tape) to survey small areas by triangulation — dividing the area into well-conditioned triangles. No angular measurements are taken. Suitable for small flat areas with simple details. Limitations: unsuitable for hilly terrain, large areas, or areas requiring high accuracy. Cross-staff and offsets locate details."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "The Lambert Conformal Conic projection is:",
    "options": [
      "A conformal projection preserving shapes and angles, suitable for mid-latitude regions",
      "An equal-area projection for world maps",
      "A cylindrical projection for equatorial regions",
      "A perspective projection from the center of Earth"
    ],
    "difficulty": "medium",
    "explanation": "Lambert Conformal Conic uses a cone intersecting the globe at two standard parallels where scale is exact. Between these parallels, scale is slightly compressed; outside, slightly expanded. It preserves local shapes and angles (conformal), making it ideal for aeronautical charts, state-level mapping, and regions with east-west extent."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "Leveling in surveying is used to determine:",
    "options": [
      "Differences in elevation between points",
      "Horizontal distances between points",
      "Angles between survey lines",
      "Magnetic bearing of survey lines"
    ],
    "difficulty": "medium",
    "explanation": "Leveling establishes elevation differences using a level instrument (auto-level, dumpy level, or digital level) and graduated staff. The instrument provides a horizontal line of sight; staff readings at different points give height differences. Reduced levels (RL) are calculated using Height of Instrument or Rise and Fall methods. Benchmark = known elevation reference."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "Compass surveying measures:",
    "options": [
      "Magnetic bearings of survey lines using a prismatic or surveyor's compass",
      "Distances using electromagnetic waves",
      "Elevations using barometric pressure",
      "Underground features using radar"
    ],
    "difficulty": "medium",
    "explanation": "Compass surveying determines the magnetic bearing (angle from magnetic north) of survey lines. Prismatic compass reads whole circle bearings (0-360°); surveyor's compass reads quadrantal bearings (N/S 0-90° E/W). Magnetic declination (angle between true and magnetic north) must be applied. Not suitable where magnetic interference exists."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "Plane table surveying is unique because:",
    "options": [
      "Plotting is done in the field simultaneously with observation, requiring no office work",
      "It provides the highest accuracy of all survey methods",
      "It can only be used at night",
      "It requires satellite signals"
    ],
    "difficulty": "medium",
    "explanation": "Plane table surveying plots the survey directly on paper mounted on a drawing board in the field. The alidade (sighting rule) is placed on the plotted position and aimed at target; the direction is drawn immediately. Methods: radiation, intersection, resection (three-point problem). Advantages: no recording errors; limitations: heavy equipment, weather-dependent."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "The scale factor at the central meridian of a UTM zone is:",
    "options": [
      "0.9996 (slightly less than 1, meaning distances are slightly compressed)",
      "1.0000 (true scale)",
      "1.0004 (slightly enlarged)",
      "0.9900"
    ],
    "difficulty": "hard",
    "explanation": "UTM uses scale factor 0.9996 at the central meridian, meaning mapped distances are 0.04% shorter than ground distances there. This ensures the scale factor equals 1.0 at two lines parallel to the central meridian (approximately 180km east and west), reducing maximum distortion across the 6° zone. This balances positive and negative distortion."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "The three segments of GNSS systems are:",
    "options": [
      "Space segment (satellites), Control segment (ground stations), User segment (receivers)",
      "Transmit, Receive, and Process segments",
      "Land, Sea, and Air segments",
      "Hardware, Software, and Data segments"
    ],
    "difficulty": "medium",
    "explanation": "All GNSS systems have three segments: Space (satellite constellation transmitting navigation signals), Control (ground stations that track satellites, update orbits, and synchronize clocks — GPS has a Master Control Station in Colorado), and User (receivers that compute position from satellite signals). Understanding this architecture is fundamental to GPS applications."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "Trilateration in GPS positioning uses:",
    "options": [
      "Distance measurements from multiple satellites to determine receiver position at the intersection of spheres",
      "Angle measurements between satellites",
      "Star observations for celestial navigation",
      "Magnetic field measurements"
    ],
    "difficulty": "medium",
    "explanation": "GPS trilateration measures pseudoranges (distances derived from signal travel time × speed of light) from each visible satellite. Each range defines a sphere around the satellite. The intersection of 3 spheres gives 2 possible positions (one eliminated as unreasonable). A 4th satellite resolves receiver clock error, giving precise 3D position."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "On a 1:25,000 toposheet, 1 cm on the map represents:",
    "options": [
      "250 meters on the ground",
      "25 meters on the ground",
      "2.5 km on the ground",
      "25 km on the ground"
    ],
    "difficulty": "medium",
    "explanation": "At 1:25,000 scale: 1 cm on map = 25,000 cm on ground = 250 m. This is double the detail of 1:50,000 (where 1 cm = 500 m). SOI 1:25,000 sheets cover 7.5' × 7.5' areas with 10m contour interval. These larger-scale maps are used for detailed planning, engineering projects, and cadastral purposes."
  },
  {
    "concept_id": "ddca910f",
    "question_text": "Fast-static GPS surveying typically requires occupation time of:",
    "options": [
      "15-30 minutes per point for baseline lengths up to 20 km",
      "1-2 minutes per point",
      "2-4 hours per point",
      "24 hours continuous observation"
    ],
    "difficulty": "hard",
    "explanation": "Fast-static GPS requires 15-30 minutes per point (depending on satellite geometry and baseline length) to resolve carrier phase ambiguities. It achieves centimeter-level accuracy for baselines up to 20 km. Compared to static (1-2 hours), it is faster but requires dual-frequency receivers and good satellite visibility. Used for control surveys and GIS control networks."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Overlay analysis in GIS combines two or more spatial layers to:",
    "options": [
      "Create new features based on the spatial intersection of input layers",
      "Change the color of map features",
      "Convert raster to vector data",
      "Project data to a different coordinate system"
    ],
    "difficulty": "medium",
    "explanation": "Overlay analysis combines geometries and attributes of multiple layers: Union (all features from both layers), Intersect (only overlapping areas), Identity (input features split by overlay), Erase (input minus overlay). Raster overlay uses map algebra. Overlay is fundamental for suitability analysis, environmental impact assessment, and land use planning."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Buffer analysis creates:",
    "options": [
      "Zones of specified distance around point, line, or polygon features",
      "Elevation profiles along a line",
      "Statistical summaries of attribute data",
      "Network routing solutions"
    ],
    "difficulty": "medium",
    "explanation": "Buffers generate polygon zones at specified distances around features: fixed-distance (e.g., 100m around all schools), variable (distance based on attribute, e.g., noise zone based on road class), dissolved (merged overlapping buffers) or undissolved (individual buffers). Applications: impact zones, service areas, setback regulations, environmental protection zones."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Dijkstra's algorithm in GIS network analysis is used for:",
    "options": [
      "Finding the shortest path between two points in a network",
      "Classifying satellite imagery",
      "Interpolating elevation data",
      "Creating buffer zones"
    ],
    "difficulty": "medium",
    "explanation": "Dijkstra's algorithm (1959) finds the shortest (or least-cost) path between nodes in a weighted network graph. In GIS, it routes vehicles on road networks considering distance, travel time, or cost. The algorithm explores nodes systematically, always expanding the nearest unvisited node, guaranteeing the optimal solution."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "A DEM (Digital Elevation Model) represents:",
    "options": [
      "A continuous surface of ground elevation values, typically as a regular grid",
      "Building heights only",
      "Population density distribution",
      "Land ownership boundaries"
    ],
    "difficulty": "medium",
    "explanation": "A DEM is a bare-earth elevation model (excluding buildings/vegetation) stored as a regular grid of elevation values. Sources: contour digitization, photogrammetry, LiDAR, radar (SRTM 30m, ASTER GDEM 30m, CARTOSAT 10m). DEMs enable slope, aspect, watershed, viewshed, and flood modeling. DSM (Digital Surface Model) includes surface features."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Slope in terrain analysis is calculated as:",
    "options": [
      "Maximum rate of change in elevation between a cell and its neighbors (rise/run)",
      "The total elevation of a point above sea level",
      "The direction a slope faces (north, south, etc.)",
      "The curvature of the terrain surface"
    ],
    "difficulty": "medium",
    "explanation": "Slope = maximum rate of elevation change = rise/run, expressed in degrees (0-90°) or percent (0-∞%). In GIS, slope is calculated using a 3×3 moving window on the DEM, finding the steepest descent direction. Slope maps are essential for: buildability assessment, erosion modeling, agricultural suitability, and landslide hazard mapping."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Aspect in terrain analysis represents:",
    "options": [
      "The compass direction (azimuth) that a slope faces",
      "The steepness of the slope",
      "The elevation of the terrain",
      "The curvature of the surface"
    ],
    "difficulty": "medium",
    "explanation": "Aspect is the downslope direction measured clockwise from north (0/360° = north, 90° = east, 180° = south, 270° = west). Flat areas have no aspect. Aspect affects solar radiation, temperature, moisture, and vegetation patterns. South-facing slopes (in Northern Hemisphere) receive more sunlight, important for building orientation and crop planning."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "IDW (Inverse Distance Weighting) interpolation assumes:",
    "options": [
      "Nearer sample points have greater influence on predicted values than distant ones",
      "All sample points contribute equally regardless of distance",
      "Only the nearest single point determines the value",
      "The surface follows a mathematical trend"
    ],
    "difficulty": "medium",
    "explanation": "IDW estimates unknown values as a weighted average of nearby known values, with weights inversely proportional to distance raised to a power (typically 2). Closer points contribute more. IDW is intuitive and fast but can create 'bull's eye' patterns around sample points and cannot extrapolate beyond the data range. Suitable for dense, evenly distributed data."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Kriging differs from IDW interpolation in that kriging:",
    "options": [
      "Uses a statistical model (variogram) to account for spatial autocorrelation and provides error estimates",
      "Simply averages nearby points equally",
      "Cannot handle irregularly spaced data",
      "Is always faster than IDW"
    ],
    "difficulty": "hard",
    "explanation": "Kriging is a geostatistical method that uses a variogram (model of spatial autocorrelation) to determine optimal weights. Unlike IDW, it considers the spatial pattern of data, provides prediction error estimates (standard error surface), and can handle clustered data without bias. It is the Best Linear Unbiased Estimator (BLUE) for spatial data."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Watershed delineation using DEM involves:",
    "options": [
      "Determining flow direction, flow accumulation, and identifying drainage basins from elevation data",
      "Mapping water bodies from satellite imagery",
      "Measuring water quality at sampling points",
      "Calculating water demand for urban areas"
    ],
    "difficulty": "medium",
    "explanation": "GIS watershed delineation: (1) Fill DEM sinks (remove artificial pits), (2) Calculate flow direction (D8 — each cell flows to steepest neighbor), (3) Calculate flow accumulation (count upstream cells), (4) Define streams (threshold accumulation), (5) Delineate basins from pour points. This automated process replaces manual contour-based watershed mapping."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Strahler stream ordering assigns:",
    "options": [
      "Order 1 to headwater streams, increasing order when two streams of equal order join",
      "Higher orders to smaller streams",
      "Numbers based on stream length only",
      "Random orders for identification"
    ],
    "difficulty": "hard",
    "explanation": "Strahler ordering: headwater streams = Order 1. When two streams of equal order n join, the resulting stream is order n+1. When streams of different orders join, the higher order continues. This hierarchical system helps characterize drainage networks. Bifurcation ratio (number of order n / number of order n+1) indicates basin shape and flood potential."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Viewshed analysis determines:",
    "options": [
      "All areas visible from a specified observer point based on terrain elevation",
      "The best route between two locations",
      "Population density distribution",
      "Soil type classification"
    ],
    "difficulty": "medium",
    "explanation": "Viewshed analysis uses a DEM to determine which cells are visible from one or more observer points by checking line-of-sight along all directions. Applications: telecommunications tower placement (signal coverage), military (defensive positions), landscape planning (visual impact assessment), real estate (view analysis), and conservation (scenic corridor protection)."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Suitability analysis using weighted overlay involves:",
    "options": [
      "Assigning weights to different criteria layers and combining them to identify the most suitable locations",
      "Simple visual comparison of maps",
      "Statistical regression analysis",
      "Random sampling of locations"
    ],
    "difficulty": "medium",
    "explanation": "Weighted overlay combines multiple reclassified raster layers (slope, soil, land use, proximity to roads, water availability) using assigned weights reflecting relative importance. Each layer is rated (1-10 suitability scale), multiplied by its weight, and summed. AHP (Analytical Hierarchy Process) provides systematic weight determination. Used for site selection and land use planning."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Thiessen (Voronoi) polygons are used for:",
    "options": [
      "Assigning areas of influence around discrete points based on nearest-neighbor proximity",
      "Creating contour maps from elevation data",
      "Network routing and shortest path analysis",
      "Image classification and pattern recognition"
    ],
    "difficulty": "medium",
    "explanation": "Thiessen polygons divide space so every location within a polygon is closer to its generating point than to any other point. Applications: rainfall estimation (assigning each rain gauge an area of influence), service area delineation, market area analysis, and spatial sampling design. They approximate Christaller's hexagonal market areas with real-world data."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Map algebra in raster analysis includes which types of operations?",
    "options": [
      "Local (cell-by-cell), focal (neighborhood), zonal (region), and global (entire grid)",
      "Only addition and subtraction of layers",
      "Vector-only operations",
      "Database query operations"
    ],
    "difficulty": "hard",
    "explanation": "Map algebra (Tomlin, 1990): Local operations compute output from corresponding cells in input layers (NDVI = (NIR-Red)/(NIR+Red)). Focal operations use neighborhood windows (mean filter, slope). Zonal operations summarize values within zones (mean elevation per district). Global operations use the entire grid (flow direction, cost distance). This framework structures all raster analysis."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Hot spot analysis (Getis-Ord Gi*) in spatial statistics identifies:",
    "options": [
      "Statistically significant clusters of high or low values",
      "The geographic center of a point distribution",
      "Linear patterns in point data",
      "Temporal trends in spatial data"
    ],
    "difficulty": "hard",
    "explanation": "Getis-Ord Gi* statistic identifies statistically significant spatial clusters: hot spots (clusters of high values) and cold spots (clusters of low values). It compares local averages to global averages considering spatial proximity. Used for crime analysis, disease surveillance, poverty mapping, and identifying development priority areas."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Cost distance analysis in GIS:",
    "options": [
      "Finds the least-cost path across a surface where movement cost varies by location",
      "Measures straight-line (Euclidean) distance between points",
      "Calculates the monetary cost of GPS equipment",
      "Determines the distance between two cities by road"
    ],
    "difficulty": "medium",
    "explanation": "Cost distance analysis creates a surface where each cell's value represents the minimum accumulated cost to reach a source location. The cost surface reflects factors like slope, land cover, and barriers. Least-cost path traces the route through the cost surface with minimum total cost. Used for wildlife corridor design, pipeline routing, and evacuation planning."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Moran's I statistic measures:",
    "options": [
      "Spatial autocorrelation — the degree to which nearby features have similar values",
      "The mean value of a dataset",
      "Standard deviation of spatial data",
      "Linear regression coefficient"
    ],
    "difficulty": "hard",
    "explanation": "Moran's I ranges from -1 (perfect dispersion) through 0 (random) to +1 (perfect clustering). Positive values indicate nearby features are similar (clustered), negative values indicate nearby features are dissimilar (dispersed). It provides a global measure of spatial pattern. Local Moran's I (LISA) identifies individual locations contributing to the overall pattern."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Kernel density estimation creates:",
    "options": [
      "A smooth continuous surface showing the density of point features per unit area",
      "A classification map of land cover types",
      "A network of connected features",
      "A 3D building model"
    ],
    "difficulty": "medium",
    "explanation": "Kernel density estimation (KDE) calculates the density of point features (crimes, disease cases, accidents) within a specified search radius, producing a smooth surface. The kernel function weights nearer points more heavily. Output cell values represent estimated density (events per unit area). Used for crime mapping, epidemiology, and market analysis."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Cut-fill analysis using a DEM calculates:",
    "options": [
      "Volume of earth to be cut (excavated) and filled to transform existing terrain to a proposed grade",
      "The cost of land acquisition",
      "Building floor area ratios",
      "Population density changes"
    ],
    "difficulty": "medium",
    "explanation": "Cut-fill compares existing terrain DEM with proposed grade surface: where existing is higher, material must be cut (excavated); where lower, fill is needed. Volume = Σ(height difference × cell area). This analysis is essential for earthwork estimation in road construction, site grading, reservoir capacity, and mining operations."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Network analysis in GIS can solve all of the following EXCEPT:",
    "options": [
      "Soil type classification",
      "Shortest path routing",
      "Service area calculation",
      "Closest facility identification"
    ],
    "difficulty": "medium",
    "explanation": "GIS network analysis solves: shortest/fastest path (Dijkstra), service area (isochrones), closest facility (emergency services), vehicle routing (optimized delivery routes), and location-allocation (optimal facility placement). Soil classification is done through remote sensing, field surveys, and interpolation — not network analysis, which operates on connected linear features."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "AHP (Analytical Hierarchy Process) in GIS suitability analysis is used to:",
    "options": [
      "Systematically determine weights for criteria through pairwise comparison",
      "Automatically classify satellite imagery",
      "Create Digital Elevation Models",
      "Perform GPS coordinate transformations"
    ],
    "difficulty": "hard",
    "explanation": "AHP (Saaty, 1980) structures complex decisions: criteria are compared in pairs on a 1-9 scale. A comparison matrix is created, eigenvector gives weights, and consistency ratio (CR < 0.10) validates judgments. In GIS suitability analysis, AHP determines relative importance of factors like slope, proximity to roads, soil type, and water availability."
  },
  {
    "concept_id": "3a03dab2",
    "question_text": "Geocoding in GIS is the process of:",
    "options": [
      "Converting textual addresses into geographic coordinates (latitude/longitude)",
      "Encoding satellite data into image formats",
      "Encrypting geographic data for security",
      "Coding survey data into questionnaire format"
    ],
    "difficulty": "medium",
    "explanation": "Geocoding matches textual descriptions (addresses, place names, postal codes) to geographic coordinates. A reference dataset with address ranges and geometry is needed. Geocoding enables spatial analysis of address-based data: customer locations, crime incidents, disease cases. Accuracy varies from rooftop-level to interpolated street segment positions."
  }
]
