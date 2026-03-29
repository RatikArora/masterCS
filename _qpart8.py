# Part 8: GIS Components + Remote Sensing
questions_part8 = [
  {
    "concept_id": "91aadeeb",
    "question_text": "The fundamental difference between raster and vector data models is:",
    "options": [
      "Raster uses a grid of cells (pixels) while vector uses points, lines, and polygons",
      "Raster is 3D while vector is 2D only",
      "Raster is more accurate than vector for all applications",
      "Vector cannot represent continuous data"
    ],
    "difficulty": "medium",
    "explanation": "Raster data divides space into regular grid cells, each storing a value (elevation, temperature, land cover). Vector data represents features as discrete geometric objects: points (wells), lines (roads), polygons (land parcels). Raster suits continuous phenomena; vector suits discrete features with precise boundaries."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Topology in GIS defines:",
    "options": [
      "Spatial relationships such as adjacency, connectivity, and containment between features",
      "The color scheme used in maps",
      "The scale of the map",
      "The coordinate system used"
    ],
    "difficulty": "medium",
    "explanation": "Topology describes spatial relationships between features: adjacency (which polygons share boundaries), connectivity (which lines connect at nodes), and containment (which features are inside others). Topological data models prevent errors like gaps and overlaps between adjacent polygons and enable spatial queries like route finding."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "The WGS84 datum is:",
    "options": [
      "The global geodetic reference system used by GPS, based on an ellipsoid model of the Earth",
      "A map projection specific to India",
      "A type of remote sensing satellite",
      "A software for digital mapping"
    ],
    "difficulty": "medium",
    "explanation": "World Geodetic System 1984 (WGS84) is the reference coordinate system used by GPS globally. It defines an ellipsoid (semi-major axis 6,378,137m, flattening 1/298.257) approximating Earth's shape. In India, the older Everest spheroid (1830) was used historically; transitioning to WGS84 ensures compatibility with GPS and global datasets."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "A large-scale map (e.g., 1:1,000) shows:",
    "options": [
      "A small area with great detail",
      "A large area with little detail",
      "Only administrative boundaries",
      "Only elevation data"
    ],
    "difficulty": "medium",
    "explanation": "Large-scale maps (1:1,000 to 1:10,000) cover small areas with high detail — individual buildings, property boundaries, utility lines. Small-scale maps (1:1,000,000+) cover large areas with less detail — state/national boundaries, major cities. Scale = Map distance / Ground distance. Larger denominator = smaller scale."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "On a map with scale 1:50,000, a distance of 3 cm on the map represents what ground distance?",
    "options": [
      "1.5 km",
      "3.0 km",
      "0.5 km",
      "15 km"
    ],
    "difficulty": "medium",
    "explanation": "Map distance / Ground distance = 1/50,000. Ground distance = 3 cm × 50,000 = 150,000 cm = 1,500 m = 1.5 km. Scale calculations are fundamental in GIS and cartography. A 1:50,000 toposheet is the standard Survey of India map scale, where 1 cm = 500 m on ground."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Georeferencing in GIS involves:",
    "options": [
      "Assigning real-world coordinates to a raster image using ground control points",
      "Adding text labels to a map",
      "Changing the color of map features",
      "Creating a new database table"
    ],
    "difficulty": "medium",
    "explanation": "Georeferencing transforms a scanned map or satellite image to a known coordinate system by identifying Ground Control Points (GCPs) — points with known real-world coordinates. Affine, polynomial, or spline transformations are applied. RMS error measures accuracy. This is essential for overlaying multiple data layers in GIS analysis."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "The difference between a geoid and an ellipsoid is:",
    "options": [
      "Geoid represents Earth's actual gravitational surface while ellipsoid is a mathematical approximation",
      "They are identical concepts",
      "Ellipsoid is more accurate than geoid",
      "Geoid is used only for maps, not GPS"
    ],
    "difficulty": "hard",
    "explanation": "The geoid is the equipotential gravitational surface of Earth (approximately mean sea level) — irregular due to varying mass distribution. The ellipsoid is a smooth mathematical surface approximating Earth's shape. The difference (geoid undulation) varies by ±100m globally. GPS measures height above ellipsoid; engineering uses geoid (orthometric) heights."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "TIN (Triangulated Irregular Network) is used in GIS for:",
    "options": [
      "Modeling terrain surfaces from irregularly spaced elevation points",
      "Storing attribute data in tables",
      "Network analysis of transportation routes",
      "Satellite image classification"
    ],
    "difficulty": "medium",
    "explanation": "TIN creates a surface model by connecting irregularly spaced elevation points into non-overlapping triangles (Delaunay triangulation). Unlike regular-grid DEMs, TINs concentrate detail where terrain varies most (ridges, valleys) and use fewer points in flat areas. TINs efficiently represent terrain for slope, aspect, visibility, and volume calculations."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Spatial queries in GIS include:",
    "options": [
      "Point-in-polygon, proximity analysis, and selection by attribute or location",
      "Only text search in databases",
      "Internet keyword searches",
      "Audio file searching"
    ],
    "difficulty": "medium",
    "explanation": "Spatial queries exploit geographic relationships: point-in-polygon (which district contains this point?), proximity (what is within 5km?), intersection (which roads cross this river?), and selection by attribute (all zones with population >10,000). SQL extensions (PostGIS, SpatiaLite) enable spatial queries in relational databases."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Digitization errors in GIS include all EXCEPT:",
    "options": [
      "Atmospheric distortion",
      "Overshoots (lines extending beyond intended endpoint)",
      "Undershoots (lines not reaching intended endpoint)",
      "Slivers (thin polygons from overlay of slightly different boundaries)"
    ],
    "difficulty": "medium",
    "explanation": "Common digitization errors: overshoots (line extends past intersection), undershoots (line stops short of intersection), slivers (thin artifact polygons from imprecise overlay), and dangling nodes. Atmospheric distortion is a remote sensing issue, not a digitization error. Topology rules and cleaning tools detect and correct these errors."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "The Mercator projection preserves:",
    "options": [
      "Shape and angles (conformal) but distorts area, especially near poles",
      "Area accurately at all latitudes",
      "Distance from center point",
      "Direction from two points"
    ],
    "difficulty": "medium",
    "explanation": "Mercator (1569) is a conformal cylindrical projection preserving local shapes and angles — essential for navigation (rhumb lines appear straight). However, it severely distorts area at high latitudes: Greenland appears as large as Africa (actually 14× smaller). Not suitable for thematic maps showing area-dependent data."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Equal-area projections are preferred for:",
    "options": [
      "Thematic maps showing density, distribution, or comparative area measurements",
      "Navigation and maritime charts",
      "Topographic mapping of small areas",
      "Cadastral surveys"
    ],
    "difficulty": "medium",
    "explanation": "Equal-area (equivalent) projections preserve relative area at the expense of shape distortion. They are essential for maps showing population density, crop distribution, climate zones, or any phenomenon where accurate area representation matters. Mollweide and Albers Equal-Area Conic are common examples used for continental and national thematic maps."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Nominal data in GIS attribute classification represents:",
    "options": [
      "Categories without inherent order (e.g., land use types: residential, commercial, industrial)",
      "Temperature values on a continuous scale",
      "Ranked data like soil fertility classes",
      "Ratio data with a true zero"
    ],
    "difficulty": "medium",
    "explanation": "Data measurement scales: Nominal — unordered categories (land use, soil type, road class); Ordinal — ordered categories (low/medium/high risk); Interval — equal intervals without true zero (temperature °C); Ratio — equal intervals with true zero (height, distance, population). Each scale determines appropriate analytical methods."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "NSDI (National Spatial Data Infrastructure) in India aims to:",
    "options": [
      "Facilitate sharing and access to spatial data across government agencies through standards and metadata",
      "Restrict all spatial data to military use",
      "Create a single national GIS software",
      "Replace all paper maps with digital versions"
    ],
    "difficulty": "hard",
    "explanation": "NSDI is India's framework for spatial data sharing: metadata standards, clearinghouse mechanisms, data exchange protocols, and institutional arrangements. It promotes interoperability among ISRO, SOI, Census, NRSC, and state agencies. Metadata catalogs enable discovery and access to spatial datasets for planning, disaster management, and governance."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "An affine transformation in georeferencing involves:",
    "options": [
      "Translation, rotation, scaling, and skewing of the image to fit control points",
      "Only changing the image color",
      "Converting raster to vector",
      "Adding elevation data to a flat image"
    ],
    "difficulty": "hard",
    "explanation": "Affine transformation uses 6 parameters to transform image coordinates: 2 translations (x,y shift), 2 scales, 1 rotation, and 1 skew. It preserves parallelism and straightness of lines. Minimum 3 GCPs are needed. Higher-order polynomial transformations handle more complex distortions but require more GCPs and may introduce errors."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "A geodatabase in GIS is:",
    "options": [
      "A structured database for storing, querying, and managing spatial data with topological relationships",
      "A simple spreadsheet of geographic names",
      "A collection of paper maps",
      "A GPS receiver database"
    ],
    "difficulty": "medium",
    "explanation": "Geodatabases (Esri's model) store geographic features with geometry, attributes, topology rules, and behavior in a relational database. Types: personal (Access-based), file (file system), and enterprise (Oracle/SQL Server). They support domains (valid values), subtypes, relationship classes, and geometric networks for sophisticated spatial data management."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Spatial data quality is assessed by:",
    "options": [
      "Accuracy, precision, completeness, consistency, and currency (how up-to-date)",
      "Only visual appearance of the map",
      "File size of the dataset",
      "Number of layers in the GIS project"
    ],
    "difficulty": "medium",
    "explanation": "Spatial data quality dimensions: positional accuracy (how close features are to true locations), attribute accuracy (correctness of properties), completeness (coverage of features), logical consistency (topological validity), temporal currency (how recent), and lineage (data source and processing history). Quality metadata should accompany all spatial datasets."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "UTM Zone 44N covers which region of India?",
    "options": [
      "Western India (approximately 78°E to 84°E)",
      "Eastern India (approximately 90°E to 96°E)",
      "Southern India (approximately 72°E to 78°E)",
      "Northern India only"
    ],
    "difficulty": "hard",
    "explanation": "UTM divides Earth into 60 zones, each 6° wide. Zone 44N covers 78°E-84°E (central India including parts of MP, UP, Rajasthan, Maharashtra). India spans UTM zones 42N (66°-72°E) through 47N (96°-102°E). Each zone uses Transverse Mercator projection with scale factor 0.9996 at central meridian. Coordinates are in meters."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "A relational database model in GIS stores data in:",
    "options": [
      "Tables with rows (records) and columns (fields) linked by key fields",
      "A single continuous data stream",
      "Hierarchical tree structures only",
      "Unstructured text files"
    ],
    "difficulty": "medium",
    "explanation": "Relational databases (RDBMS) organize data in tables where rows represent spatial features and columns store attributes. Tables are linked through primary and foreign keys enabling JOIN operations. SQL is used for querying. Spatial extensions (PostGIS, SpatiaLite) add geometry columns and spatial functions to standard RDBMS."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "The representative fraction (RF) of a map where 1 cm represents 2.5 km on ground is:",
    "options": [
      "1:250,000",
      "1:25,000",
      "1:2,500",
      "1:2,500,000"
    ],
    "difficulty": "medium",
    "explanation": "RF = Map distance / Ground distance = 1 cm / 2.5 km = 1 cm / 250,000 cm = 1:250,000. Converting: 2.5 km = 2,500 m = 250,000 cm. RF is dimensionless (no units) making it universally understood. Verbal scale ('1 cm = 2.5 km') and bar scale provide alternative representations."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Heads-up digitizing refers to:",
    "options": [
      "Digitizing features on-screen by tracing over a displayed image or scanned map",
      "Digitizing using a digitizing tablet with a puck",
      "Automatic feature extraction by software",
      "Digitizing in the field using GPS"
    ],
    "difficulty": "hard",
    "explanation": "Heads-up digitizing traces features on a computer screen over a georeferenced backdrop (scanned map, satellite image, or aerial photo). It replaced manual tablet digitizing as monitors and pointing devices improved. The operator creates points, lines, and polygons by clicking on visible features, with real-time coordinate capture."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "A cylindrical map projection is created by projecting the globe onto:",
    "options": [
      "A cylinder tangent or secant to the globe, then unrolling it",
      "A cone placed over the globe",
      "A flat plane tangent to the globe",
      "A sphere of larger diameter"
    ],
    "difficulty": "medium",
    "explanation": "Cylindrical projections wrap a cylinder around the globe (tangent along the equator or secant at two standard parallels), then unroll it. Mercator is the most famous cylindrical projection. Distortion increases away from the line(s) of tangency. Cylindrical projections produce rectangular maps suitable for world maps and equatorial regions."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "The Everest spheroid, historically used in India for mapping, was defined in:",
    "options": [
      "1830 by George Everest",
      "1900 by Survey of India",
      "1950 by United Nations",
      "1984 by US Department of Defense"
    ],
    "difficulty": "hard",
    "explanation": "Colonel George Everest determined the parameters of the Everest spheroid in 1830 for the Great Trigonometrical Survey of India. It was locally best-fitting for the Indian subcontinent. Semi-major axis: 6,377,276.345m. India is transitioning to WGS84 (1984) for GPS compatibility while maintaining legacy data in Everest datum."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Conical projections are best suited for mapping:",
    "options": [
      "Mid-latitude regions with east-west extent",
      "Polar regions",
      "Equatorial regions",
      "The entire globe"
    ],
    "difficulty": "medium",
    "explanation": "Conical projections place a cone over the globe, tangent or secant at one or two standard parallels. Distortion is minimized along these parallels, making conical projections ideal for mid-latitude regions with east-west extent (e.g., continental USA, Europe, India). Lambert Conformal Conic is widely used for aeronautical charts and state-level mapping."
  },
  {
    "concept_id": "91aadeeb",
    "question_text": "Metadata in GIS provides:",
    "options": [
      "Information about the data itself — source, accuracy, date, projection, and processing history",
      "The actual geographic coordinates of features",
      "Only the color scheme of the map",
      "Nothing useful for data users"
    ],
    "difficulty": "medium",
    "explanation": "Metadata is 'data about data': who created it, when, what area it covers, projection/datum, accuracy, resolution, processing methods, and access restrictions. ISO 19115 is the international metadata standard. Metadata enables data discovery (finding relevant datasets), assessment (fitness for purpose), and proper use (understanding limitations)."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "The visible portion of the electromagnetic spectrum ranges from:",
    "options": [
      "0.4 to 0.7 micrometers",
      "0.1 to 0.3 micrometers",
      "0.7 to 1.3 micrometers",
      "1.0 to 3.0 micrometers"
    ],
    "difficulty": "medium",
    "explanation": "Visible light spans 0.4μm (violet) to 0.7μm (red). Blue: 0.4-0.5μm, Green: 0.5-0.6μm, Red: 0.6-0.7μm. Near-infrared (NIR): 0.7-1.3μm, Short-wave infrared (SWIR): 1.3-3.0μm, Thermal IR: 3-14μm, Microwave: 1mm-1m. Different wavelengths interact differently with surface materials."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Healthy vegetation has high reflectance in which spectral band?",
    "options": [
      "Near-Infrared (NIR) band (0.7-1.3 μm)",
      "Blue band (0.4-0.5 μm)",
      "Thermal infrared (8-14 μm)",
      "Microwave band"
    ],
    "difficulty": "medium",
    "explanation": "Healthy vegetation strongly reflects NIR radiation (due to internal leaf cell structure) while absorbing red and blue light (for photosynthesis). This NIR 'vegetation red edge' is the basis for NDVI and other vegetation indices. Stressed or dying vegetation shows reduced NIR reflectance — a key indicator for crop health monitoring."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "NDVI (Normalized Difference Vegetation Index) is calculated as:",
    "options": [
      "(NIR - Red) / (NIR + Red)",
      "(Red - NIR) / (Red + NIR)",
      "(Green - Red) / (Green + Red)",
      "(NIR - Green) / (NIR + Green)"
    ],
    "difficulty": "medium",
    "explanation": "NDVI = (NIR - Red)/(NIR + Red) ranges from -1 to +1. Dense vegetation: 0.6-0.9 (high NIR, low red). Bare soil: 0.1-0.2. Water: negative values (low NIR, higher visible reflectance). NDVI is the most widely used vegetation index for monitoring crop health, deforestation, desertification, and seasonal phenological changes."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "If NIR reflectance is 0.50 and Red reflectance is 0.08, the NDVI value is:",
    "options": [
      "0.72",
      "0.42",
      "0.58",
      "0.84"
    ],
    "difficulty": "medium",
    "explanation": "NDVI = (NIR - Red)/(NIR + Red) = (0.50 - 0.08)/(0.50 + 0.08) = 0.42/0.58 = 0.724 ≈ 0.72. This high NDVI value indicates dense, healthy vegetation. Values above 0.6 typically represent dense forest or healthy crops. This numerical calculation is commonly tested in GATE remote sensing questions."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Spatial resolution of a satellite sensor refers to:",
    "options": [
      "The smallest area on the ground that can be distinguished as a separate unit (pixel size)",
      "The number of spectral bands the sensor records",
      "How often the satellite revisits the same area",
      "The number of brightness levels the sensor can record"
    ],
    "difficulty": "medium",
    "explanation": "Spatial resolution = ground dimension of one pixel. Landsat: 30m (multispectral), SPOT-6/7: 1.5m (panchromatic), WorldView-3: 0.31m, IRS LISS-IV: 5.8m. Higher spatial resolution reveals finer detail but covers smaller areas and generates larger datasets. Resolution selection depends on application requirements."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Supervised classification in image processing requires:",
    "options": [
      "Training samples (ground truth data) to teach the algorithm to classify pixels",
      "No prior knowledge of the study area",
      "Only unsupervised clustering as a first step",
      "Manual visual interpretation pixel by pixel"
    ],
    "difficulty": "medium",
    "explanation": "Supervised classification uses analyst-defined training samples (representative pixels for each land cover class verified by field data). Algorithms (Maximum Likelihood, SVM, Random Forest) learn spectral patterns from training data and classify all pixels. Accuracy depends on quality and representativeness of training samples. Accuracy assessment uses confusion matrix."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Landsat satellites provide imagery with a temporal resolution (revisit time) of:",
    "options": [
      "16 days",
      "1 day",
      "5 days",
      "30 days"
    ],
    "difficulty": "medium",
    "explanation": "Landsat satellites (currently Landsat 8 and 9) have a 16-day revisit period at any given location. Combined, Landsat 8+9 provide 8-day coverage. Landsat has provided continuous Earth observation since 1972 (Landsat 1), creating the longest continuous satellite imagery archive — invaluable for change detection and environmental monitoring."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Rayleigh scattering affects which wavelengths most?",
    "options": [
      "Shorter wavelengths (blue light) — making the sky appear blue",
      "Longer wavelengths (red and infrared)",
      "Microwave wavelengths only",
      "All wavelengths equally"
    ],
    "difficulty": "medium",
    "explanation": "Rayleigh scattering occurs when particles are much smaller than the wavelength (air molecules). It is inversely proportional to the 4th power of wavelength (λ⁻⁴), affecting shorter wavelengths most. Blue light (0.45μm) is scattered ~5.5× more than red (0.65μm), making the sky blue and degrading blue-band satellite imagery most."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Active remote sensing differs from passive remote sensing in that active sensors:",
    "options": [
      "Emit their own energy and record the returned signal (e.g., radar, LiDAR)",
      "Only record naturally available energy (sunlight, thermal emission)",
      "Work only during daytime",
      "Cannot penetrate clouds"
    ],
    "difficulty": "medium",
    "explanation": "Active sensors (SAR radar, LiDAR) emit electromagnetic energy and measure the backscattered return — working day/night and through clouds (microwave). Passive sensors (optical, thermal) detect naturally reflected sunlight or emitted thermal energy, limited by cloud cover and daylight (optical). Active sensing enables all-weather monitoring."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Radiometric resolution of a sensor refers to:",
    "options": [
      "The number of brightness levels (bit depth) the sensor can distinguish",
      "The size of each pixel on the ground",
      "The number of spectral bands",
      "The orbital altitude of the satellite"
    ],
    "difficulty": "medium",
    "explanation": "Radiometric resolution = number of discrete brightness levels = 2^n where n is bit depth. 8-bit = 256 levels, 11-bit = 2048 levels, 16-bit = 65536 levels. Higher radiometric resolution distinguishes subtle differences in reflected/emitted energy, important for water quality studies, shadow detail, and precise land cover classification."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "SAR (Synthetic Aperture Radar) imaging can operate:",
    "options": [
      "Day and night, in all weather conditions including through clouds",
      "Only during clear daytime conditions",
      "Only at night",
      "Only during specific seasons"
    ],
    "difficulty": "medium",
    "explanation": "SAR uses microwave radar (typically C-band 5.6cm or L-band 23cm wavelength) which penetrates clouds, rain, and operates independently of solar illumination. This makes SAR invaluable for monitoring flood extent, deformation mapping (InSAR), ship detection, and land cover classification in persistently cloudy tropical regions."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "The IRS (Indian Remote Sensing) satellite system includes:",
    "options": [
      "Resourcesat, Cartosat, and Oceansat series operated by ISRO/NRSC",
      "Only the Landsat series",
      "Only military reconnaissance satellites",
      "GPS navigation satellites"
    ],
    "difficulty": "medium",
    "explanation": "India's IRS program (since IRS-1A, 1988) includes: Resourcesat (LISS-III/IV multispectral, 5.8-23m), Cartosat (2.5m stereo for topographic mapping), Oceansat (ocean color monitoring), RISAT (SAR for all-weather observation), and several others. NRSC (Hyderabad) distributes data. India has one of the world's largest civilian Earth observation fleets."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Atmospheric windows in remote sensing are:",
    "options": [
      "Wavelength ranges where the atmosphere is relatively transparent to electromagnetic radiation",
      "Physical openings in the atmosphere",
      "Windows on satellite platforms for camera mounting",
      "Time windows when satellites pass overhead"
    ],
    "difficulty": "medium",
    "explanation": "Atmospheric windows are spectral bands with high transmittance: visible (0.4-0.7μm), NIR (0.7-1.3μm), SWIR windows (1.5-1.8, 2.0-2.5μm), thermal windows (3-5, 8-14μm), and microwave (>1mm). Water vapor, CO₂, and ozone absorb strongly in intervening bands. Sensors are designed to operate within these windows for clear surface observation."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "In aerial photography, the standard forward overlap between successive photographs is:",
    "options": [
      "60%",
      "30%",
      "80%",
      "40%"
    ],
    "difficulty": "medium",
    "explanation": "Standard aerial photography uses 60% forward (along-track) overlap and 30% lateral (cross-track/sidelap) overlap. The 60% forward overlap ensures stereoscopic coverage — each ground point appears in at least two photos, enabling 3D viewing and height measurement through parallax. Higher overlaps provide redundancy and better stereo geometry."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Parallax in photogrammetry is:",
    "options": [
      "The apparent shift of an object's position when viewed from different camera positions, proportional to its height",
      "The resolution of the aerial photograph",
      "The flight height of the aircraft",
      "The lens focal length"
    ],
    "difficulty": "hard",
    "explanation": "Parallax is the apparent displacement of objects between overlapping photos taken from different positions. Objects closer to the camera (higher elevation) show greater parallax. Height difference = (Δp × H) / (B + Δp), where Δp is differential parallax, H is flying height, B is air base. This enables terrain height measurement from stereo pairs."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "K-means clustering is an example of:",
    "options": [
      "Unsupervised classification algorithm",
      "Supervised classification algorithm",
      "Image enhancement technique",
      "Geometric correction method"
    ],
    "difficulty": "medium",
    "explanation": "K-means is an unsupervised classification algorithm that partitions pixels into K clusters based on spectral similarity without prior training data. The analyst specifies the number of clusters (K), and the algorithm iteratively assigns pixels to the nearest cluster center. The analyst then identifies each cluster's land cover class using field data."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "The spectral signature of water is characterized by:",
    "options": [
      "Low reflectance across all bands, with near-zero reflectance in NIR and SWIR",
      "High reflectance in NIR bands",
      "Uniform high reflectance across all wavelengths",
      "Highest reflectance in thermal infrared"
    ],
    "difficulty": "medium",
    "explanation": "Water absorbs strongly in NIR and SWIR (near-zero reflectance), reflecting weakly in visible bands (blue-green). Clear water reflects more blue; turbid water reflects more in green/red. This distinctive spectral signature enables water body mapping using band ratios (NDWI) and classification algorithms. Depth and turbidity affect the spectral profile."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Change detection in remote sensing involves:",
    "options": [
      "Comparing multi-temporal images to identify changes in land cover or land use over time",
      "Detecting changes in satellite orbit",
      "Changing the projection of an image",
      "Modifying pixel values for enhancement"
    ],
    "difficulty": "medium",
    "explanation": "Change detection compares images of the same area from different dates to identify differences: urban growth, deforestation, flood extent, coastal erosion. Methods include image differencing, post-classification comparison, PCA, and object-based change detection. Radiometric normalization and geometric co-registration are prerequisites for accurate change detection."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "LiDAR (Light Detection and Ranging) measures:",
    "options": [
      "Distance to targets by illuminating them with laser pulses and analyzing the reflected returns",
      "Thermal radiation emitted by objects",
      "Magnetic field variations of the Earth",
      "Gravity anomalies"
    ],
    "difficulty": "medium",
    "explanation": "LiDAR emits laser pulses (typically 1064nm NIR) and measures the time for return from targets. With aircraft position (GPS) and orientation (INS), precise 3D coordinates of ground and above-ground features are calculated. LiDAR generates dense point clouds for DEM creation, building modeling, forestry inventory, and flood modeling."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "PCA (Principal Component Analysis) in digital image processing is used for:",
    "options": [
      "Data reduction by transforming correlated bands into uncorrelated principal components",
      "Increasing the number of spectral bands",
      "Correcting geometric distortions",
      "Adding color to grayscale images"
    ],
    "difficulty": "hard",
    "explanation": "PCA transforms correlated multispectral bands into uncorrelated principal components, concentrating most information into fewer bands (PC1 contains most variance). This reduces data dimensionality while preserving key information. PCA is used for change detection (multi-date PCA), band selection, noise reduction, and feature enhancement."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "The scale of an aerial photograph with focal length 150mm taken from a flying height of 3000m AGL is:",
    "options": [
      "1:20,000",
      "1:10,000",
      "1:30,000",
      "1:5,000"
    ],
    "difficulty": "hard",
    "explanation": "Photo scale = focal length / flying height = 150mm / 3,000,000mm = 1/20,000. Scale = f/H where f is focal length and H is height above ground level (AGL). For areas with varying terrain, scale varies across the photo. Scale at any point = f/(H-h) where h is ground elevation. Flat terrain gives uniform scale."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Sentinel-2 satellite provides imagery with a spatial resolution of:",
    "options": [
      "10 meters (for visible and NIR bands)",
      "30 meters",
      "1 meter",
      "250 meters"
    ],
    "difficulty": "hard",
    "explanation": "ESA's Sentinel-2 (A and B) provides: 10m (blue, green, red, NIR), 20m (red edge, SWIR), 60m (atmospheric bands). With 5-day revisit (combined A+B), it provides free, open-access multispectral data ideal for agriculture, forestry, and land cover monitoring. It complements Landsat (30m, 16-day) with finer resolution and higher temporal frequency."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Urban heat island mapping primarily uses:",
    "options": [
      "Thermal infrared remote sensing to measure land surface temperature",
      "Visible band imagery only",
      "Microwave radar data",
      "UV radiation measurement"
    ],
    "difficulty": "medium",
    "explanation": "Thermal infrared sensors (Landsat TIRS bands 10-11, ASTER TIR) measure land surface temperature (LST). Urban areas show 2-8°C higher LST than surrounding rural areas due to impervious surfaces, waste heat, and reduced vegetation. LST mapping using thermal RS helps urban planners identify heat islands and plan mitigation (green infrastructure, cool roofs)."
  },
  {
    "concept_id": "0f373c78",
    "question_text": "Mie scattering occurs when:",
    "options": [
      "Atmospheric particles are approximately the same size as the wavelength of radiation",
      "Particles are much smaller than the wavelength",
      "Particles are much larger than the wavelength",
      "There are no particles in the atmosphere"
    ],
    "difficulty": "hard",
    "explanation": "Mie scattering occurs when particle diameter approximates the wavelength — dust, pollen, smoke, and water droplets scatter visible and NIR wavelengths. Unlike Rayleigh (λ⁻⁴ dependence), Mie scattering affects wavelengths more uniformly, explaining why clouds (water droplets) and haze (dust) appear white. It affects lower atmosphere more than Rayleigh."
  }
]
