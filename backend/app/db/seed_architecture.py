"""
Seed database with Architecture & Planning content — GATE AR Sections 1 & 2.
Section 1: Architecture, Planning and Design
Section 2: Construction and Management
"""
import uuid
from app.db.session import SessionLocal
from app.models.subject import Subject, Topic
from app.models.concept import Concept
from app.models.question import Question, QuestionConcept


def _id():
    return str(uuid.uuid4())


def _mcq(text, opts, correct, explanation, difficulty=1, time_est=30):
    return {
        "id": _id(), "question_text": text, "question_type": "mcq",
        "options": opts, "correct_answer": correct, "explanation": explanation,
        "difficulty": difficulty, "time_estimate_seconds": time_est,
    }


def _tf(text, correct, explanation, difficulty=1):
    return {
        "id": _id(), "question_text": text, "question_type": "true_false",
        "options": ["True", "False"], "correct_answer": correct,
        "explanation": explanation, "difficulty": difficulty, "time_estimate_seconds": 20,
    }


def seed_architecture():
    db = SessionLocal()
    try:
        # Check if Architecture subject already exists
        existing = db.query(Subject).filter(Subject.name.like("%Architecture%")).first()
        if existing:
            print("Architecture subject already exists — skipping.")
            return

        # ─── Subject ───
        subj_id = _id()
        db.add(Subject(
            id=subj_id,
            name="Architecture & Planning",
            description="GATE AR syllabus — Architecture, Planning and Design, Construction Management, and more.",
            icon="🏛️", color="#8b5cf6", order_index=1,
            target_degrees="B.Arch,M.Arch",
        ))

        # ─── Topics ───
        topics_data = [
            (_id(), "Architectural Graphics & Visual Composition", "Architectural drawing, visual composition in 2D/3D, computer applications in architecture.", "📐", 0),
            (_id(), "Anthropometrics & Space Standards", "Human body dimensions, space standards, universal design, and ergonomics.", "📏", 1),
            (_id(), "Organization of Space & Circulation", "Spatial organization principles, horizontal & vertical circulation, building planning.", "🏗️", 2),
            (_id(), "Building Byelaws & Codes", "Building regulations, codes, standards, NBC of India, FAR, setbacks.", "📋", 3),
            (_id(), "Project Management Techniques", "PERT, CPM, bar charts, resource allocation, project scheduling.", "📊", 4),
            (_id(), "Estimation & Specification", "Quantity surveying, estimation methods, specifications for construction.", "📝", 5),
            (_id(), "Professional Practice & Ethics", "Architectural practice, COA regulations, professional ethics, contracts.", "⚖️", 6),
            (_id(), "Form & Structure", "Structural systems, form-structure relationship, load paths.", "🏛️", 7),
            (_id(), "Disaster Resistant Structures", "Earthquake, wind, and flood resistant design principles.", "🌊", 8),
            (_id(), "Temporary Structures & Rehabilitation", "Emergency shelters, temporary housing, post-disaster rehabilitation.", "⛺", 9),
        ]
        topic_ids = {}
        for tid, name, desc, icon, order in topics_data:
            db.add(Topic(id=tid, subject_id=subj_id, name=name, description=desc, icon=icon, order_index=order))
            topic_ids[order] = tid

        all_questions = []

        def add_concept(topic_order, name, explanation, key_points, order_idx, questions):
            cid = _id()
            db.add(Concept(id=cid, topic_id=topic_ids[topic_order], name=name,
                           explanation=explanation, key_points=key_points, order_index=order_idx))
            db.flush()
            for q in questions:
                qid = q["id"]
                db.add(Question(**q))
                db.flush()
                db.add(QuestionConcept(question_id=qid, concept_id=cid))

        # ═══════════════════════════════════════════════════
        # TOPIC 0: Architectural Graphics & Visual Composition
        # ═══════════════════════════════════════════════════

        add_concept(0, "Architectural Drawing Types",
            "Architectural drawings communicate design intent through standardized conventions. Key types include **plans** (horizontal cuts), **sections** (vertical cuts), **elevations** (external views), and **isometric/axonometric** projections. Each has specific line weights, hatching patterns, and annotation standards per IS codes.",
            [
                "Plan: horizontal cut at ~1.2m above floor level",
                "Section: vertical cut showing internal structure",
                "Elevation: orthographic view of exterior face",
                "Isometric: 3D representation at 30° axes",
                "Working drawings include dimensions, materials, and construction details",
            ], 0, [
            _mcq("A **floor plan** is created by taking a horizontal section at what typical height above floor level?",
                 ["0.5m", "1.0m", "1.2m", "2.0m"], "1.2m",
                 "A floor plan is a horizontal section typically cut at **1.2 meters** above the floor level to capture windows, doors, and openings."),
            _mcq("Which type of architectural drawing shows the external face of a building in true shape and proportion?",
                 ["Plan", "Section", "Elevation", "Perspective"], "Elevation",
                 "An **elevation** is an orthographic projection of the exterior face of a building, showing it in true shape without perspective distortion."),
            _mcq("In architectural drawings, which projection type uses **30° angles** from the horizontal for both axes?",
                 ["Perspective", "Isometric", "Oblique", "Orthographic"], "Isometric",
                 "**Isometric projection** uses 30° angles from the horizontal for both receding axes, creating a 3D representation without vanishing points.", 2),
            _tf("A section drawing reveals the internal structure of a building by cutting vertically through it.",
                "True", "A **section** is a vertical cut through a building that reveals internal structure, materials, floor-to-floor heights, and construction details."),
            _mcq("Which line type is used to show elements **above the cutting plane** in a floor plan?",
                 ["Solid thick line", "Dashed line", "Center line", "Hidden line"], "Dashed line",
                 "Elements above the cutting plane (like overhead beams, lofts) are shown with **dashed lines** in floor plans.", 2),
        ])

        add_concept(0, "Visual Composition Principles",
            "Visual composition in architecture involves organizing elements to create visually coherent designs. Key principles include **balance** (symmetrical/asymmetrical), **rhythm** (repetition/alternation), **proportion** (golden ratio, modular systems), **harmony**, **contrast**, and **unity**. These apply to both 2D drawings and 3D spatial design.",
            [
                "Balance: symmetrical (formal) or asymmetrical (informal)",
                "Rhythm: repetition, alternation, or progression of elements",
                "Proportion: golden ratio (1:1.618), Le Corbusier's Modulor",
                "Hierarchy: visual dominance through size, color, or position",
                "Unity: coherence of all elements working together",
            ], 1, [
            _mcq("The **Golden Ratio** used in architectural proportion is approximately:",
                 ["1:1.414", "1:1.618", "1:2.000", "1:1.500"], "1:1.618",
                 "The Golden Ratio (φ) is approximately **1:1.618**. It appears in classical architecture (Parthenon) and is considered naturally pleasing to the eye.", 2),
            _mcq("**Le Corbusier's Modulor** is a proportioning system based on:",
                 ["Fibonacci series only", "Human body proportions and golden ratio", "Classical orders", "Metric grid system"],
                 "Human body proportions and golden ratio",
                 "The **Modulor** combines human body proportions (a 6-foot man with raised arm) with the golden ratio and Fibonacci series to create a universal proportioning system.", 2),
            _mcq("Which type of balance uses **equal visual weight on both sides** of an axis?",
                 ["Asymmetrical", "Symmetrical", "Radial", "Informal"], "Symmetrical",
                 "**Symmetrical balance** distributes equal visual weight on both sides of an axis, creating formal, stable compositions. The Taj Mahal is a classic example."),
            _tf("Rhythm in architecture can only be achieved through repetition of identical elements.",
                "False",
                "Rhythm can be achieved through **repetition** (identical elements), **alternation** (two elements alternating), or **progression** (gradual change in size, color, or spacing)."),
            _mcq("In visual hierarchy, which element tends to draw the eye first?",
                 ["Smallest element", "Lightest colored element", "Largest or most contrasting element", "Most centered element"],
                 "Largest or most contrasting element",
                 "**Visual hierarchy** is established through size, contrast, color, and isolation. The largest or most contrasting element typically draws attention first."),
        ])

        add_concept(0, "Computer Applications in Architecture",
            "Computer-Aided Design (CAD) and Building Information Modeling (BIM) have transformed architectural practice. **CAD** handles 2D/3D drafting, **BIM** manages building data through the entire lifecycle. Key software includes AutoCAD, Revit, SketchUp, Rhino, and Grasshopper for parametric design.",
            [
                "CAD: Computer-Aided Design for 2D/3D drafting (AutoCAD)",
                "BIM: Building Information Modeling — 3D model + data (Revit)",
                "GIS: Geographic Information System for site analysis",
                "Parametric design: algorithm-driven form generation (Grasshopper)",
                "BIM levels: 0 (2D CAD) → 4 (time/cost integration)",
            ], 2, [
            _mcq("**BIM** differs from traditional CAD primarily because it:",
                 ["Uses 3D instead of 2D", "Contains building data and information beyond geometry",
                  "Is faster for drafting", "Requires more powerful hardware"],
                 "Contains building data and information beyond geometry",
                 "BIM goes beyond CAD's geometric representation by embedding **material properties, cost data, scheduling, and lifecycle information** into the model.", 2),
            _mcq("Which BIM level includes **4D scheduling** (time) and **5D costing**?",
                 ["Level 1", "Level 2", "Level 3", "Level 4"], "Level 4",
                 "**BIM Level 4** (and above) integrates time (4D), cost (5D), sustainability (6D), and facility management (7D) into the building model.", 3),
            _tf("AutoCAD is classified as a BIM software.",
                "False",
                "AutoCAD is a **CAD** (Computer-Aided Design) tool primarily for 2D/3D drafting. **Revit** is Autodesk's BIM software that includes data-rich modeling."),
            _mcq("Parametric design in architecture uses:",
                 ["Fixed geometric shapes", "Algorithms and parameters to generate form",
                  "Only circular geometries", "Pre-designed templates"],
                 "Algorithms and parameters to generate form",
                 "**Parametric design** uses algorithms and variable parameters to generate complex, adaptive forms. Grasshopper (for Rhino) is a popular visual programming tool for this.", 2),
        ])

        # ═══════════════════════════════════════════════════
        # TOPIC 1: Anthropometrics & Space Standards
        # ═══════════════════════════════════════════════════

        add_concept(1, "Human Body Dimensions",
            "Anthropometrics is the study of human body measurements for design. Key dimensions include **standing height** (avg 1.7m male), **eye level** (1.5m), **reach** (shoulder height ~1.4m), and **wheelchair dimensions** (750mm width). Design must accommodate the **5th to 95th percentile** range.",
            [
                "Average male height: ~1700mm, female: ~1600mm",
                "Eye level (standing): ~1500mm from floor",
                "Standard door height: 2100mm (7 feet)",
                "Wheelchair width: 750mm, turning radius: 1500mm",
                "Design for 5th-95th percentile range",
            ], 0, [
            _mcq("The minimum clear width required for a **wheelchair** to pass through a doorway is:",
                 ["600mm", "750mm", "900mm", "1200mm"], "900mm",
                 "While a wheelchair is ~750mm wide, the minimum **clear door opening** for wheelchair access is **900mm** (as per NBC and accessibility standards) to allow for hand clearance.", 2),
            _mcq("In ergonomic design, the standard **kitchen counter height** is approximately:",
                 ["750mm", "850mm", "900mm", "1000mm"], "850mm",
                 "Standard kitchen counter height is **850mm** (roughly 34 inches), designed for comfortable standing work for the average adult."),
            _mcq("The **turning radius** for a standard wheelchair is:",
                 ["900mm", "1200mm", "1500mm", "1800mm"], "1500mm",
                 "A standard wheelchair requires a **1500mm (1.5m) turning circle** for a full 360° turn. This is critical for accessible bathroom and corridor design.", 2),
            _tf("Anthropometric data for design should accommodate 100% of the population.",
                "False",
                "Design typically accommodates the **5th to 95th percentile** range. Designing for 100% would make spaces impractical. Extreme outliers are handled through adjustable features."),
        ])

        add_concept(1, "Space Standards & NBC",
            "The **National Building Code of India (NBC 2016)** prescribes minimum space standards. Key standards include room sizes, ventilation requirements, staircase dimensions, and corridor widths. These ensure **health, safety, and livability** in buildings.",
            [
                "Habitable room: minimum 9.5 sqm area, 2.4m height",
                "Kitchen: minimum 5.0 sqm with 1.8m width",
                "Bathroom: minimum 1.8 sqm",
                "Staircase width: minimum 1.0m for residential",
                "Corridor width: minimum 1.0m residential, 1.8m public",
            ], 1, [
            _mcq("As per NBC 2016, the minimum **floor area** of a habitable room is:",
                 ["7.5 sqm", "9.5 sqm", "12.0 sqm", "15.0 sqm"], "9.5 sqm",
                 "NBC 2016 specifies a minimum **9.5 sqm** floor area for a habitable room with a minimum width of 2.4m."),
            _mcq("The minimum **ceiling height** for a habitable room as per NBC is:",
                 ["2.1m", "2.4m", "2.7m", "3.0m"], "2.7m",
                 "NBC prescribes a minimum **2.7m** clear ceiling height for habitable rooms to ensure adequate ventilation and comfort. (Note: some state byelaws allow 2.4m for specific cases.)", 2),
            _mcq("The minimum width of a **residential staircase** as per NBC is:",
                 ["750mm", "900mm", "1000mm", "1200mm"], "1000mm",
                 "NBC specifies minimum **1000mm (1.0m)** width for residential staircases. For public buildings, it increases to 1.5m or more.", 2),
            _tf("The minimum riser height for a residential staircase as per NBC is 150mm.",
                "False",
                "NBC specifies maximum riser height of **190mm** for residential and **150mm** for public buildings. There is no prescribed minimum — the maximum ensures comfortable climbing."),
            _mcq("What is the minimum ventilation opening area as a percentage of floor area for habitable rooms per NBC?",
                 ["1/6th", "1/8th", "1/10th", "1/12th"], "1/6th",
                 "NBC requires ventilation openings of at least **1/6th (approximately 16.7%)** of the floor area for habitable rooms.", 3),
        ])

        add_concept(1, "Universal Design Principles",
            "Universal Design ensures environments are usable by **all people**, regardless of age, ability, or status. The 7 principles (by Ron Mace) include equitable use, flexibility, simple/intuitive use, perceptible information, tolerance for error, low physical effort, and appropriate size/space.",
            [
                "7 principles by Ron Mace (1997)",
                "Equitable Use: design useful for people with diverse abilities",
                "Flexibility in Use: accommodates a wide range of preferences",
                "Ramps: maximum gradient 1:12 for wheelchair access",
                "Tactile guiding blocks (TGBs) for visually impaired navigation",
            ], 2, [
            _mcq("The maximum **gradient for a wheelchair ramp** as per universal design standards is:",
                 ["1:8", "1:10", "1:12", "1:15"], "1:12",
                 "The maximum gradient for wheelchair ramps is **1:12** (one unit rise for every 12 units of run). For every 750mm rise, a landing is required."),
            _mcq("How many principles of **Universal Design** were defined by Ron Mace?",
                 ["5", "6", "7", "8"], "7",
                 "Ron Mace defined **7 principles** of Universal Design in 1997: Equitable Use, Flexibility, Simple/Intuitive, Perceptible Information, Tolerance for Error, Low Physical Effort, and Size & Space."),
            _mcq("**Tactile Guiding Blocks** (TGBs) are primarily designed for:",
                 ["Wheelchair users", "Visually impaired persons", "Elderly people", "Children"],
                 "Visually impaired persons",
                 "TGBs are textured ground surface indicators that help **visually impaired persons** navigate. They come in two types: directional (bars) and warning (dots)."),
            _tf("Universal Design benefits only people with disabilities.",
                "False",
                "Universal Design benefits **everyone** — elderly, children, pregnant women, people carrying heavy loads, and those with temporary injuries. Example: automatic doors benefit wheelchair users AND parents with strollers."),
        ])

        # ═══════════════════════════════════════════════════
        # TOPIC 2: Organization of Space & Circulation
        # ═══════════════════════════════════════════════════

        add_concept(2, "Spatial Organization Patterns",
            "Francis D.K. Ching identifies key spatial organization types: **linear** (arranged along a path), **centralized** (around a dominant central space), **radial** (extending from center), **grid** (regular pattern), and **clustered** (grouped by proximity). Choice depends on function, site, and design intent.",
            [
                "Linear: spaces along an axis (corridors, row houses)",
                "Centralized: dominant space with secondary around it (churches, domes)",
                "Radial: arms extending from center (star forts, airports)",
                "Grid: regular modular pattern (Manhattan, office floors)",
                "Clustered: grouped by proximity/function (organic villages)",
            ], 0, [
            _mcq("A **centralized organization** of space typically features:",
                 ["Spaces arranged along a line", "A dominant central space with secondary spaces around it",
                  "Irregular clustering", "A regular grid pattern"],
                 "A dominant central space with secondary spaces around it",
                 "Centralized organization has a **dominant central space** (often a gathering or focal space) with secondary spaces arranged around it. Examples: Pantheon, Florence Cathedral."),
            _mcq("The spatial organization of most **airports** with a central hub and terminal arms is:",
                 ["Linear", "Centralized", "Radial", "Grid"], "Radial",
                 "Airports typically use **radial organization** with arms (concourses) extending from a central hub, allowing efficient movement and clear wayfinding.", 2),
            _mcq("Which spatial organization type characterizes **traditional organic villages**?",
                 ["Grid", "Linear", "Radial", "Clustered"], "Clustered",
                 "Traditional organic villages develop through **clustered organization** — spaces grouped by proximity, function, or social relationships without a strict geometric order.", 2),
            _tf("A grid organization is always the most efficient for all building types.",
                "False",
                "Grid organization works well for offices and residential blocks but is **not universally efficient**. Hospitals benefit from radial/centralized plans, and museums often use linear sequences."),
        ])

        add_concept(2, "Horizontal Circulation",
            "Horizontal circulation includes **corridors, lobbies, galleries, and ramps** that connect spaces on the same level. Effective circulation minimizes travel distance, avoids dead-ends, and provides clear wayfinding. Corridor widths depend on building type and occupancy.",
            [
                "Single-loaded corridor: rooms on one side only",
                "Double-loaded corridor: rooms on both sides (more efficient)",
                "Minimum corridor width: 1.0m residential, 1.8m public",
                "Dead-end corridors should not exceed 6m (fire safety)",
                "Gallery: corridor overlooking a lower space",
            ], 1, [
            _mcq("A **double-loaded corridor** has rooms on:",
                 ["One side only", "Both sides", "The corridor is outdoors", "No rooms — it's a passageway"],
                 "Both sides",
                 "A double-loaded corridor has rooms on **both sides**, making it more space-efficient than single-loaded (rooms on one side only). Common in apartments and hotels."),
            _mcq("As per fire safety codes, the maximum length of a **dead-end corridor** is typically:",
                 ["3m", "6m", "10m", "15m"], "6m",
                 "Dead-end corridors are limited to approximately **6m** (varies by code) to ensure safe evacuation. They create bottlenecks during emergencies.", 2),
            _mcq("Which corridor type provides **better natural ventilation and light**?",
                 ["Double-loaded", "Single-loaded", "Internal corridor", "Basement corridor"], "Single-loaded",
                 "**Single-loaded corridors** (rooms on one side only) allow natural light and ventilation from the open side, though they use more building area."),
            _tf("A ramp can serve as both horizontal and vertical circulation.",
                "True",
                "A ramp transitions between levels gradually, serving as **both horizontal movement and vertical level change**. It's essential for wheelchair accessibility."),
        ])

        add_concept(2, "Vertical Circulation",
            "Vertical circulation connects different levels: **stairs, ramps, elevators, and escalators**. Stair design follows the **2R + T = 600–640mm** rule (riser + tread formula). Elevators are essential above 4 stories. Fire escape stairs must be enclosed with fire-rated doors.",
            [
                "Staircase formula: 2R + T = 600–640mm",
                "Maximum riser: 190mm residential, 150mm public",
                "Minimum tread: 250mm residential, 300mm public",
                "Elevators required: above 4 stories (15m height)",
                "Fire escape: enclosed, self-closing doors, pressurized stairwell",
            ], 2, [
            _mcq("The standard formula for comfortable stair design is **2R + T =**",
                 ["500–540mm", "600–640mm", "700–740mm", "550–590mm"], "600–640mm",
                 "The **2R + T = 600–640mm** formula (where R = riser height, T = tread depth) ensures comfortable stride length. For residential: 2(150) + 300 = 600mm.", 2),
            _mcq("Elevators are mandatory in buildings exceeding how many stories (as per NBC)?",
                 ["2 stories", "3 stories", "4 stories", "5 stories"], "4 stories",
                 "NBC mandates elevators in buildings exceeding **4 stories** (approximately 15m height) for accessibility and convenience.", 2),
            _mcq("The minimum **tread depth** for a public building staircase is:",
                 ["200mm", "250mm", "300mm", "350mm"], "300mm",
                 "For public buildings, NBC specifies a minimum tread depth of **300mm** for safe and comfortable use. Residential buildings allow 250mm."),
            _mcq("A **scissor staircase** is used primarily for:",
                 ["Decorative purposes", "Space efficiency — two stairs in the space of one",
                  "Emergency use only", "Connecting more than 5 floors"],
                 "Space efficiency — two stairs in the space of one",
                 "A scissor staircase interleaves **two separate flights** within the footprint of a single staircase, providing two independent means of egress efficiently.", 3),
            _tf("A fire escape staircase should be an open staircase for better ventilation.",
                "False",
                "Fire escape staircases must be **enclosed** with fire-rated walls and self-closing doors. Open stairs would allow smoke and fire spread. Pressurized stairwells push smoke out."),
        ])

        # ═══════════════════════════════════════════════════
        # TOPIC 3: Building Byelaws & Codes
        # ═══════════════════════════════════════════════════

        add_concept(3, "Floor Area Ratio (FAR)",
            "**FAR** (Floor Area Ratio) = Total built-up area / Plot area. It controls building density. Higher FAR allows taller/larger buildings. FAR excludes certain areas like parking, lift rooms, and services. Different cities have different FAR norms based on land use zones.",
            [
                "FAR = Total built-up area ÷ Plot area",
                "Higher FAR = more dense development",
                "Excludes: parking, staircase, lift shaft, service areas (varies by city)",
                "Premium FAR available in some cities for extra charges",
                "FAR varies by land use zone: residential, commercial, industrial",
            ], 0, [
            _mcq("A plot of **1000 sqm** with a permissible FAR of **2.0** allows a maximum built-up area of:",
                 ["1000 sqm", "1500 sqm", "2000 sqm", "2500 sqm"], "2000 sqm",
                 "FAR = Total built-up area / Plot area. So **2.0 × 1000 = 2000 sqm** maximum built-up area, which can be distributed across multiple floors."),
            _mcq("Which of the following is typically **excluded** from FAR calculation?",
                 ["Living room", "Bedroom", "Parking area", "Kitchen"], "Parking area",
                 "Most byelaws **exclude parking, lift rooms, staircases, and service areas** from FAR calculation to incentivize these essential facilities.", 2),
            _mcq("If FAR is 1.5 on a **2000 sqm** plot with 50% ground coverage, what is the maximum number of floors?",
                 ["2 floors", "3 floors", "4 floors", "5 floors"], "3 floors",
                 "Total built-up = 1.5 × 2000 = 3000 sqm. Ground coverage = 50% × 2000 = 1000 sqm per floor. Floors = 3000/1000 = **3 floors**.", 3),
            _tf("FAR regulations are uniform across all cities in India.",
                "False",
                "FAR norms **vary significantly** across cities and even within zones of the same city. Delhi, Mumbai, and Bangalore all have different FAR regulations based on local planning requirements."),
        ])

        add_concept(3, "Setbacks & Ground Coverage",
            "**Setbacks** are mandatory distances from plot boundaries. **Ground coverage** is the percentage of plot covered by building footprint. Both control building mass, ensure light/ventilation, fire safety, and privacy between buildings.",
            [
                "Front setback: distance from road boundary",
                "Side and rear setbacks: from adjacent plot boundaries",
                "Ground coverage = Building footprint area / Plot area × 100",
                "Higher building height requires larger setbacks",
                "Setbacks ensure light, ventilation, fire access, and privacy",
            ], 1, [
            _mcq("**Ground coverage** of 60% on a 500 sqm plot means the maximum building footprint is:",
                 ["200 sqm", "250 sqm", "300 sqm", "400 sqm"], "300 sqm",
                 "Ground coverage = Building footprint / Plot area × 100. So **60% × 500 = 300 sqm** maximum footprint.", 2),
            _mcq("As building **height increases**, what typically happens to setback requirements?",
                 ["They decrease", "They remain the same", "They increase", "They are eliminated"],
                 "They increase",
                 "Higher buildings require **larger setbacks** to ensure adequate daylight, ventilation, and fire access for adjacent buildings. Many codes use a height-to-setback ratio.", 2),
            _tf("Setbacks are measured from the center line of the road to the building.",
                "False",
                "Setbacks are measured from the **plot boundary** (not road center line) to the nearest point of the building. Road widening may affect the plot boundary position."),
            _mcq("The primary purpose of **setback regulations** is:",
                 ["Aesthetic uniformity", "Light, ventilation, fire safety, and privacy",
                  "Maximizing built-up area", "Reducing construction cost"],
                 "Light, ventilation, fire safety, and privacy",
                 "Setbacks serve multiple critical functions: ensuring **natural light and ventilation**, providing **fire access**, maintaining **privacy** between buildings, and creating open spaces."),
        ])

        # ═══════════════════════════════════════════════════
        # TOPIC 4: Project Management Techniques
        # ═══════════════════════════════════════════════════

        add_concept(4, "PERT and CPM",
            "**PERT** (Program Evaluation and Review Technique) uses probabilistic time estimates (optimistic, most likely, pessimistic). **CPM** (Critical Path Method) uses deterministic single time estimates. Both identify the **critical path** — the longest sequence determining minimum project duration.",
            [
                "PERT: three time estimates (O + 4M + P)/6",
                "CPM: single deterministic time estimate",
                "Critical Path: longest path = minimum project duration",
                "Float/Slack: delay possible without affecting project end",
                "Activities on critical path have zero float",
            ], 0, [
            _mcq("The **PERT expected time** formula using optimistic (O), most likely (M), and pessimistic (P) is:",
                 ["(O + M + P)/3", "(O + 4M + P)/6", "(O + 2M + P)/4", "(O + 6M + P)/8"],
                 "(O + 4M + P)/6",
                 "PERT uses a **weighted average**: te = (O + 4M + P)/6, giving most weight to the most likely estimate. This follows a beta distribution.", 2),
            _mcq("Activities on the **critical path** have a total float of:",
                 ["Maximum", "Variable", "Zero", "Negative"], "Zero",
                 "Critical path activities have **zero float** — any delay in these activities directly delays the entire project. They determine the minimum project duration.", 2),
            _mcq("**CPM** differs from **PERT** primarily in that CPM:",
                 ["Uses three time estimates", "Uses probabilistic analysis",
                  "Uses single deterministic time estimates", "Cannot identify critical path"],
                 "Uses single deterministic time estimates",
                 "CPM uses **single, deterministic time estimates** based on experience, while PERT uses three estimates (optimistic, most likely, pessimistic) for probabilistic analysis."),
            _mcq("If an activity has **optimistic=4, most likely=6, pessimistic=14 days**, the PERT expected time is:",
                 ["6 days", "7 days", "8 days", "9 days"], "7 days",
                 "te = (O + 4M + P)/6 = (4 + 4×6 + 14)/6 = (4 + 24 + 14)/6 = **42/6 = 7 days**.", 3),
            _tf("In PERT, the variance of activity duration is [(P - O)/6]².",
                "True",
                "PERT variance = **[(P - O)/6]²**. This measures uncertainty in the time estimate. Higher difference between pessimistic and optimistic = higher variance.", 3),
        ])

        add_concept(4, "Bar Charts & Resource Planning",
            "**Bar charts** (Gantt charts) visually display project schedule with activities as horizontal bars against a time axis. They show start/end dates, duration, and can indicate progress. **Resource leveling** optimizes resource usage to avoid over-allocation.",
            [
                "Gantt chart: activities as bars along time axis",
                "Shows dependencies, milestones, and progress",
                "Easy to read but doesn't show critical path clearly",
                "Resource leveling: smoothing peaks in resource demand",
                "Resource histogram: bar chart showing resource usage over time",
            ], 1, [
            _mcq("A **Gantt chart** primarily displays:",
                 ["Cost breakdown", "Activities against a time scale",
                  "Resource allocation only", "Material quantities"],
                 "Activities against a time scale",
                 "A Gantt chart shows project **activities as horizontal bars** plotted against a time scale, making it easy to see durations, start/end dates, and overlaps."),
            _mcq("The main limitation of a **Gantt chart** compared to CPM/PERT is:",
                 ["Cannot show duration", "Cannot show start dates",
                  "Does not clearly show the critical path", "Cannot handle many activities"],
                 "Does not clearly show the critical path",
                 "While Gantt charts are visually intuitive, they **don't explicitly show dependencies and critical path** like network diagrams (CPM/PERT). Modern tools add dependency lines to address this.", 2),
            _tf("Resource leveling may extend the project duration.",
                "True",
                "Resource leveling smooths peaks in resource demand, which may require **delaying non-critical activities**. If non-critical activities use up all float, the project duration may extend.", 2),
        ])

        # ═══════════════════════════════════════════════════
        # TOPIC 5: Estimation & Specification
        # ═══════════════════════════════════════════════════

        add_concept(5, "Methods of Estimation",
            "Estimation determines the probable cost of a project. Key methods: **detailed estimate** (item-wise quantities × rates), **abstract/approximate estimate** (cost per unit area/volume), **plinth area method**, and **cube rate method**. Detailed estimates are most accurate but time-consuming.",
            [
                "Detailed estimate: most accurate, item-wise measurement",
                "Plinth area method: cost per sqm of plinth area",
                "Cube rate method: cost per cubic meter of building volume",
                "Abstract estimate: quick approximate using benchmarks",
                "Contingencies: 3-5% of estimated cost for unforeseen items",
            ], 0, [
            _mcq("The most accurate method of estimation is:",
                 ["Plinth area method", "Cube rate method", "Detailed estimate", "Abstract estimate"],
                 "Detailed estimate",
                 "A **detailed estimate** measures each item of work individually and applies current rates, making it the most accurate but also the most time-consuming method."),
            _mcq("The **plinth area method** estimates cost based on:",
                 ["Volume of building", "Length of walls",
                  "Built-up area at plinth level", "Number of rooms"],
                 "Built-up area at plinth level",
                 "The plinth area method multiplies the **built-up area at plinth level** by a standard rate per sqm. It's quick but approximate, suitable for preliminary estimates."),
            _mcq("**Contingencies** in an estimate typically range from:",
                 ["1-2%", "3-5%", "10-15%", "20-25%"], "3-5%",
                 "Contingencies of **3-5%** are added to cover unforeseen items, price fluctuations, and minor changes during construction. Higher percentages may apply for renovation work.", 2),
            _tf("The cube rate method considers both area and height of a building for estimation.",
                "True",
                "The cube rate method calculates building **volume** (length × width × height) and multiplies by a rate per cubic meter, accounting for **both area and height** variations."),
        ])

        add_concept(5, "Specifications in Construction",
            "Specifications describe **quality, materials, and workmanship** for construction. **General specifications** cover common requirements; **detailed specifications** describe each item precisely. They supplement drawings and form part of the contract document.",
            [
                "General specs: broad requirements for entire project",
                "Detailed specs: item-wise material and workmanship standards",
                "IS codes: Indian Standards for materials and methods",
                "Specs complement drawings — drawings show 'what', specs describe 'how'",
                "Part of contract documents along with BOQ and drawings",
            ], 1, [
            _mcq("**Specifications** in construction primarily describe:",
                 ["Dimensions of elements", "Quality of materials and workmanship",
                  "Cost of items", "Timeline of construction"],
                 "Quality of materials and workmanship",
                 "Specifications define **quality standards, materials, and methods of workmanship**. They complement drawings which show dimensions and geometry."),
            _mcq("A **Bill of Quantities (BOQ)** contains:",
                 ["Only material costs", "Itemized list of work with quantities and rates",
                  "Labor schedules only", "Equipment specifications"],
                 "Itemized list of work with quantities and rates",
                 "A BOQ is a detailed document listing all items of work with their **measured quantities and rates**, forming the basis for cost estimation and tendering.", 2),
            _tf("Detailed specifications are needed only for large projects.",
                "False",
                "**All projects** benefit from detailed specifications to ensure quality control and avoid disputes. Even small projects need clarity on materials, finishes, and workmanship standards."),
        ])

        # ═══════════════════════════════════════════════════
        # TOPIC 6: Professional Practice & Ethics
        # ═══════════════════════════════════════════════════

        add_concept(6, "Architectural Practice in India",
            "Architecture practice in India is regulated by the **Council of Architecture (COA)**, established under the Architects Act 1972. Only COA-registered architects can use the title 'Architect'. The COA prescribes conditions of engagement, scale of fees, and professional conduct.",
            [
                "COA: Council of Architecture (Architects Act 1972)",
                "Only registered architects can use the title 'Architect'",
                "Minimum qualification: B.Arch (5 years) from recognized institution",
                "COA prescribes minimum scale of professional fees",
                "Professional indemnity insurance is recommended",
            ], 0, [
            _mcq("The **Council of Architecture (COA)** was established under:",
                 ["Architects Act 1952", "Architects Act 1972", "Indian Constitution", "Building Code 1985"],
                 "Architects Act 1972",
                 "The COA was established under the **Architects Act 1972** to regulate architecture education and practice in India."),
            _mcq("The minimum educational qualification to register as an architect in India is:",
                 ["Diploma in Architecture", "B.Arch (5 years)", "M.Arch", "Any engineering degree"],
                 "B.Arch (5 years)",
                 "A **5-year Bachelor of Architecture (B.Arch)** from a COA-recognized institution is the minimum qualification to register as an architect in India."),
            _tf("Any civil engineer can legally use the title 'Architect' in India.",
                "False",
                "Only persons **registered with the Council of Architecture** can legally use the title 'Architect' in India, as per the Architects Act 1972. Civil engineers cannot use this title."),
            _mcq("The professional fee for architectural services as per COA guidelines is typically a percentage of:",
                 ["Material cost", "Labor cost", "Total project cost", "Land cost"],
                 "Total project cost",
                 "COA prescribes professional fees as a **percentage of the total project cost** (construction cost), typically ranging from 5-10% depending on project size and complexity.", 2),
        ])

        add_concept(6, "Types of Contracts",
            "Construction contracts define the relationship between owner and contractor. Key types: **lump sum** (fixed price), **item rate** (payment per measured item), **cost plus** (actual cost + fee), and **turnkey** (single entity handles design + construction).",
            [
                "Lump sum: fixed total price, contractor bears risk",
                "Item rate: payment based on measured quantities",
                "Cost plus: actual cost + percentage or fixed fee",
                "Turnkey/Design-build: single entity for design + construction",
                "BOQ-based contracts: most common in India",
            ], 1, [
            _mcq("In a **lump sum contract**, the financial risk primarily falls on:",
                 ["Owner", "Contractor", "Architect", "Both equally"], "Contractor",
                 "In lump sum contracts, the **contractor** bears the financial risk since they agree to complete work for a fixed price regardless of actual costs. Changes require formal variation orders.", 2),
            _mcq("An **item rate contract** is best suited for projects where:",
                 ["Scope is fully defined", "Scope may vary during execution",
                  "Timeline is critical", "Quality is the only concern"],
                 "Scope may vary during execution",
                 "Item rate contracts are ideal when **scope may change** during execution, as payment is based on actual measured quantities at agreed rates. Common for government projects in India.", 2),
            _mcq("A **turnkey contract** combines:",
                 ["Design and supervision", "Design and construction under one entity",
                  "Multiple contractors", "Only material supply"],
                 "Design and construction under one entity",
                 "A turnkey (design-build) contract gives **one entity responsibility for both design and construction**, providing single-point accountability and often faster delivery."),
            _tf("In a cost-plus contract, the owner bears more financial risk than the contractor.",
                "True",
                "In cost-plus contracts, the **owner pays actual costs plus a fee**, so the owner bears the risk of cost overruns. The contractor has less incentive to minimize costs unless the fee structure includes incentives.", 2),
        ])

        # ═══════════════════════════════════════════════════
        # TOPIC 7: Form & Structure
        # ═══════════════════════════════════════════════════

        add_concept(7, "Structural Systems",
            "Buildings use various structural systems to resist gravity and lateral loads. **Load-bearing walls** (masonry), **framed structures** (RCC/steel columns and beams), **shell structures** (curved thin surfaces), and **space frames** (3D trusses). The choice depends on span, height, loads, and aesthetics.",
            [
                "Load-bearing: walls carry loads (limited height ~4 stories)",
                "Framed: columns + beams transfer loads (most common for multi-story)",
                "Shell: thin curved surfaces (domes, vaults)",
                "Space frame: 3D truss systems for large spans",
                "Tensile: cables and membranes (stadiums, canopies)",
            ], 0, [
            _mcq("A **load-bearing structural system** is most suitable for buildings up to:",
                 ["2 stories", "4 stories", "8 stories", "12 stories"], "4 stories",
                 "Load-bearing masonry walls are economical and practical for buildings up to **approximately 4 stories**. Beyond this, the wall thickness becomes impractical and framed structures are preferred."),
            _mcq("Which structural system is most commonly used for **multi-story buildings** in India?",
                 ["Load-bearing masonry", "RCC framed structure", "Steel space frame", "Timber frame"],
                 "RCC framed structure",
                 "**RCC (Reinforced Cement Concrete) framed structures** with columns and beams are the most common for multi-story buildings in India, offering flexibility in layout and good seismic resistance."),
            _mcq("A **shell structure** achieves strength through:",
                 ["Thick heavy sections", "Its curved geometry and thinness",
                  "Multiple columns", "Post-tensioning cables"],
                 "Its curved geometry and thinness",
                 "Shell structures like domes and vaults achieve strength through their **curved geometry**, distributing loads efficiently through membrane action. They can be remarkably thin relative to their span.", 2),
            _mcq("The **Sydney Opera House** is an example of which structural type?",
                 ["Framed structure", "Shell structure", "Space frame", "Load-bearing walls"],
                 "Shell structure",
                 "The Sydney Opera House uses precast concrete **shell** roof segments, making it one of the most iconic shell structures in modern architecture.", 2),
            _tf("Space frames are 2D planar truss structures.",
                "False",
                "Space frames are **3D truss systems** extending in three dimensions. This 3D configuration gives them excellent spanning capability for large areas like airport terminals and exhibition halls."),
        ])

        add_concept(7, "Load Paths & Force Flow",
            "Every building must transfer loads from point of application to the foundation. The **load path** traces how forces flow: live/dead loads → slab → beam → column → footing → soil. Understanding load paths is essential for structural integrity.",
            [
                "Load path: slab → beam → column → footing → soil",
                "Dead loads: permanent (self-weight, finishes)",
                "Live loads: variable (occupants, furniture)",
                "Lateral loads: wind, earthquake",
                "Continuous load path essential for structural stability",
            ], 1, [
            _mcq("The correct **load path** in a framed building is:",
                 ["Column → Beam → Slab → Foundation", "Slab → Beam → Column → Foundation",
                  "Beam → Slab → Column → Foundation", "Foundation → Column → Beam → Slab"],
                 "Slab → Beam → Column → Foundation",
                 "Loads are applied on the slab, transferred to **beams, then columns, then footings**, and finally to the soil. This is the standard gravity load path in framed structures."),
            _mcq("**Dead load** of a building includes:",
                 ["Occupants and furniture", "Wind forces", "Self-weight of structure and permanent fixtures",
                  "Earthquake forces"],
                 "Self-weight of structure and permanent fixtures",
                 "Dead loads are **permanent, constant loads** including the self-weight of structure, walls, floors, finishes, and fixed equipment. They do not change during the building's life."),
            _tf("A discontinuity in the load path can cause structural failure.",
                "True",
                "A **continuous, uninterrupted load path** from roof to foundation is essential. Any discontinuity (like a transfer floor without proper design) creates a weak point that can cause structural failure, especially during earthquakes.", 2),
        ])

        # ═══════════════════════════════════════════════════
        # TOPIC 8: Disaster Resistant Structures
        # ═══════════════════════════════════════════════════

        add_concept(8, "Earthquake Resistant Design",
            "Earthquake resistant design follows IS 1893 and IS 13920. Key principles: **ductility** (ability to deform without collapse), **regularity** (avoid soft stories and plan irregularities), **adequate reinforcement** (at beam-column joints), and **base isolation** (decoupling building from ground motion).",
            [
                "IS 1893: seismic zoning and design criteria",
                "India: 4 seismic zones (II, III, IV, V)",
                "Ductile detailing: IS 13920 for RCC structures",
                "Soft story: avoid open ground floor without infill/bracing",
                "Base isolation: rubber bearings decouple building from ground",
            ], 0, [
            _mcq("India is divided into how many **seismic zones**?",
                 ["3", "4", "5", "6"], "4",
                 "India is divided into **4 seismic zones** (II, III, IV, V) as per IS 1893. Zone V (highest risk) includes NE India, J&K, and Kutch. Zone I was merged into Zone II in the 2002 revision."),
            _mcq("A **soft story** in a building is dangerous during earthquakes because:",
                 ["It's too heavy", "It has less stiffness than adjacent stories",
                  "It has too many windows", "It's always the topmost floor"],
                 "It has less stiffness than adjacent stories",
                 "A soft story (often open ground floor for parking) has **significantly less stiffness** than floors above, causing stress concentration and potential pancake collapse during earthquakes.", 2),
            _mcq("**Base isolation** in earthquake resistant design works by:",
                 ["Making the building heavier", "Fixing the building rigidly to the ground",
                  "Decoupling the building from ground motion", "Adding more floors"],
                 "Decoupling the building from ground motion",
                 "Base isolation uses flexible bearings (rubber/lead) between foundation and superstructure to **decouple the building from ground shaking**, reducing seismic forces transmitted to the structure.", 3),
            _tf("All buildings in India must be designed for earthquake resistance.",
                "True",
                "As per IS 1893, **all buildings in India** (even in the lowest seismic zone II) must be designed for earthquake forces. The design intensity varies by zone."),
            _mcq("Which IS code provides guidelines for **ductile detailing** of RCC structures?",
                 ["IS 456", "IS 875", "IS 1893", "IS 13920"], "IS 13920",
                 "**IS 13920** provides guidelines for ductile detailing of RCC structures in seismic zones, covering beam-column joints, confinement reinforcement, and shear wall design.", 3),
        ])

        add_concept(8, "Wind & Flood Resistant Design",
            "Wind resistant design follows IS 875 Part 3. Tall and lightweight buildings are most vulnerable. Key measures: **aerodynamic form**, **adequate bracing**, **secured cladding**. Flood resistant design includes **raised plinths**, **stilts**, **water-resistant materials**, and **proper drainage**.",
            [
                "IS 875 Part 3: wind load calculations",
                "Wind pressure increases with height",
                "Aerodynamic shapes reduce wind loads",
                "Flood: raise plinth above High Flood Level (HFL)",
                "Stilts: elevate living spaces above flood level",
            ], 1, [
            _mcq("Wind pressure on a building **increases with**:",
                 ["Decrease in height", "Increase in height", "Number of rooms", "Wall thickness"],
                 "Increase in height",
                 "Wind speed and pressure **increase with height** due to reduced friction from the ground. IS 875 Part 3 provides height-dependent coefficients for wind load calculation."),
            _mcq("The most effective flood-resistant strategy for residential buildings in flood-prone areas is:",
                 ["Using waterproof paint", "Raising the plinth above the High Flood Level",
                  "Making walls thicker", "Using more cement"],
                 "Raising the plinth above the High Flood Level",
                 "**Raising the plinth** above the High Flood Level (HFL) is the most fundamental strategy, keeping living spaces above expected flood waters. Combined with stilts for severe flood zones.", 2),
            _tf("Aerodynamic building shapes can reduce wind forces on a structure.",
                "True",
                "**Rounded, tapered, or setback forms** reduce wind forces by allowing air to flow around the building smoothly rather than creating large drag forces. The Taipei 101's tapered form is an example."),
        ])

        # ═══════════════════════════════════════════════════
        # TOPIC 9: Temporary Structures & Rehabilitation
        # ═══════════════════════════════════════════════════

        add_concept(9, "Emergency Shelters",
            "Emergency shelters provide immediate post-disaster housing. Types include **tents**, **prefabricated units**, **container homes**, and **transitional shelters**. Key requirements: rapid deployment, weather protection, minimum 3.5 sqm per person, adequate ventilation, and cultural appropriateness.",
            [
                "Minimum space: 3.5 sqm per person (Sphere standards)",
                "Rapid deployment: setup within hours/days",
                "Materials: canvas, tarpaulin, bamboo, light steel",
                "Transitional: bridge between emergency and permanent housing",
                "Must consider local climate and cultural norms",
            ], 0, [
            _mcq("As per **Sphere humanitarian standards**, the minimum covered living space per person in emergency shelters is:",
                 ["2.0 sqm", "3.5 sqm", "5.0 sqm", "7.5 sqm"], "3.5 sqm",
                 "The Sphere standards prescribe **3.5 sqm per person** as minimum covered living space in emergency shelters. This excludes cooking and sanitation facilities.", 2),
            _mcq("**Transitional shelters** serve the purpose of:",
                 ["Permanent housing", "Bridging emergency shelters and permanent reconstruction",
                  "Commercial use", "Storage only"],
                 "Bridging emergency shelters and permanent reconstruction",
                 "Transitional shelters provide **dignified interim housing** between the emergency phase (tents) and permanent reconstruction, which may take years. They can often be upgraded or relocated."),
            _tf("Emergency shelter design should ignore local cultural preferences to prioritize speed.",
                "False",
                "While speed is critical, shelters should **respect local cultural norms** (privacy, cooking arrangements, gender segregation) to be accepted and effectively used by displaced populations."),
            _mcq("Which material is most commonly used for **rapid emergency shelter** construction?",
                 ["Reinforced concrete", "Steel and glass", "Tarpaulin and bamboo/timber", "Brick masonry"],
                 "Tarpaulin and bamboo/timber",
                 "**Tarpaulin sheets with bamboo or timber frames** are most common for rapid emergency shelters due to availability, low cost, and ease of construction without skilled labor."),
        ])

        add_concept(9, "Post-Disaster Rehabilitation",
            "Rehabilitation involves restoring communities after disasters through **housing reconstruction, infrastructure repair, livelihood restoration**, and community rebuilding. It follows the principles of **'Build Back Better'** — reconstructing stronger and more resilient than before.",
            [
                "Build Back Better: improve resilience in reconstruction",
                "Owner-driven reconstruction: empowers communities",
                "Phases: relief → rehabilitation → reconstruction → development",
                "Gujarat model (2001): successful owner-driven approach",
                "Must address physical, social, and economic recovery",
            ], 1, [
            _mcq("The **'Build Back Better'** principle in post-disaster rehabilitation means:",
                 ["Build exactly the same as before", "Build larger structures",
                  "Reconstruct with improved resilience and standards", "Use only imported materials"],
                 "Reconstruct with improved resilience and standards",
                 "'Build Back Better' means using the reconstruction opportunity to **improve building standards, disaster resilience, and community infrastructure** beyond pre-disaster levels."),
            _mcq("The **Gujarat earthquake (2001)** rehabilitation is considered successful primarily because of:",
                 ["Government-built housing for all", "Owner-driven reconstruction approach",
                  "International aid only", "Complete relocation of affected villages"],
                 "Owner-driven reconstruction approach",
                 "Gujarat's **owner-driven reconstruction** gave financial assistance directly to homeowners with technical guidance, resulting in culturally appropriate, well-maintained housing with strong community ownership.", 2),
            _tf("Post-disaster rehabilitation should focus only on housing reconstruction.",
                "False",
                "Rehabilitation must address **housing, infrastructure, livelihoods, education, health, and psychosocial recovery**. Focusing only on housing ignores the broader needs of disaster-affected communities."),
        ])

        db.commit()
        print(f"✅ Architecture & Planning seeded: 10 topics, {20} concepts")
        # Count questions
        from sqlalchemy import func as sqla_func
        q_count = db.query(sqla_func.count(Question.id)).scalar()
        print(f"   Total questions in database: {q_count}")
    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_architecture()
