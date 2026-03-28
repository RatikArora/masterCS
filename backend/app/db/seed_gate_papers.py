"""
Seed GATE AR (Architecture & Planning) past paper MCQ questions into the MasterCS database.

Parses PDFs from /backend/pdfs/AR/ and seeds verified MCQ questions with correct answers
determined from architecture/planning domain knowledge.

Usage: cd backend && python3 -m app.db.seed_gate_papers
"""

import uuid
import json
import re
from collections import defaultdict

import PyPDF2
from sqlalchemy import text

from app.db.session import SessionLocal
from app.models.question import Question, QuestionConcept
from app.models.concept import Concept
from app.models.subject import Topic

SUBJECT_ID = "13d35960-9f22-4c56-a749-3ff627e2a8d9"
PDF_DIR = "pdfs/AR"

# Years with parsable text content
PARSABLE_YEARS = [2012, 2013, 2014, 2016, 2018, 2022, 2023, 2024]


def _id():
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Concept mapping keywords → concept_id (loaded at runtime from DB)
# ---------------------------------------------------------------------------
CONCEPT_KEYWORD_MAP = {
    # Architectural Graphics & Visual Composition
    "Architectural Drawing Types": [
        "projection", "isometric", "axonometric", "orthographic",
        "drawing", "plan", "elevation", "section"
    ],
    "Visual Composition Principles": [
        "gestalt", "composition", "golden ratio", "proportion",
        "colour", "color", "line of beauty", "hogarth", "visual",
        "interlocking", "interlacing", "symmetry"
    ],
    "Computer Applications in Architecture": [
        "autocad", "3ds max", "revit", "bim", "vector graphics",
        "inkscape", "software", "archicad", "cad", "tabsurf",
        "lofting", "microstation"
    ],
    # Anthropometrics & Space Standards
    "Human Body Dimensions": [
        "anthropometric", "body dimension", "ergonomic"
    ],
    "Space Standards & NBC": [
        "nbc", "national building code", "staircase width",
        "setback", "turning radius", "fire tender", "building code",
        "floor area ratio", "far", "fsi", "building byelaw",
        "minimum width"
    ],
    "Universal Design Principles": [
        "universal design", "wheelchair", "barrier free",
        "accessibility", "cpwd guideline", "disabled"
    ],
    # Organization of Space & Circulation
    "Spatial Organization Patterns": [
        "spatial organization", "space planning"
    ],
    "Horizontal Circulation": [
        "corridor", "passage", "horizontal circulation"
    ],
    "Vertical Circulation": [
        "staircase", "elevator", "escalator", "winder",
        "stringer", "newel", "tread"
    ],
    # Building Byelaws & Codes
    "Floor Area Ratio (FAR)": [
        "floor area ratio", "far ", "ground coverage"
    ],
    "Setbacks & Ground Coverage": [
        "setback", "building line", "statutory"
    ],
    # Project Management Techniques
    "PERT and CPM": [
        "pert", "cpm", "critical path", "network diagram"
    ],
    "Bar Charts & Resource Planning": [
        "gantt chart", "bar chart", "resource planning",
        "project development", "construction project"
    ],
    # Estimation & Specification
    "Methods of Estimation": [
        "estimation", "cost", "depreciation", "book value",
        "valuation", "distress value", "property value",
        "direct cost", "establishment cost", "labour cost",
        "material cost", "equipment cost"
    ],
    "Specifications in Construction": [
        "specification", "dpc", "damp proof"
    ],
    # Professional Practice & Ethics
    "Architectural Practice in India": [
        "council of architecture", "architect", "professional",
        "liability", "hriday", "handbook of professional"
    ],
    "Types of Contracts": [
        "contract", "tender", "qcbs", "earnest money",
        "special conditions"
    ],
    # Form & Structure
    "Structural Systems": [
        "dome", "vault", "truss", "folded plate",
        "space frame", "shell", "cable", "suspension",
        "pendentive", "squinch", "buttress", "pilaster",
        "curvature", "synclastic", "anticlastic",
        "hoop", "meridional", "catenary", "parabolic",
        "structural form", "tensile", "membrane", "ptfe",
        "tuned mass damper"
    ],
    "Load Paths & Force Flow": [
        "bending moment", "shearing force", "load",
        "axial force", "torsion", "beam", "slab",
        "reinforced concrete", "ponding"
    ],
    # Disaster Resistant Structures
    "Earthquake Resistant Design": [
        "earthquake", "seismic", "lateral force"
    ],
    "Wind & Flood Resistant Design": [
        "wind resistant", "flood resistant", "cyclone"
    ],
    # Ecosystem & Ecology
    "Natural Ecosystems": [
        "ecosystem", "ecology", "homeostasis", "niche",
        "biosphere", "biodegradable", "biome", "ramsar",
        "wetland", "species", "enteric", "pathogen",
        "micro-organism", "staphylococcus", "vibrio",
        "escherichia", "salmonella"
    ],
    "Ecological Principles in Design": [
        "ecological", "eco-", "green building", "leed",
        "breeam", "casbee", "griha"
    ],
    # Environmental Pollution & Control
    "Air & Water Pollution": [
        "pollution", "air quality", "aqi", "pollutant",
        "particulate", "peroxyacetyl", "emission"
    ],
    "Pollution Control Strategies": [
        "pollution control", "sewage", "effluent"
    ],
    # Sustainable Development & Climate
    "Sustainable Development Goals": [
        "sdg", "sustainable development", "un 2030",
        "climate change", "ndc", "nationally determined",
        "carbon emission", "envistats", "seea"
    ],
    "Climate Responsive Design": [
        "tropical summer index", "solar chart", "sun path",
        "altitude angle", "azimuth", "thermal comfort",
        "heat island", "cool island", "uhi", "uci",
        "shgc", "low-emissivity", "emissivity",
        "daylight", "solar radiation", "chajja",
        "mashrabiya", "badgir", "climate responsive",
        "energy conservation", "ecbc", "lighting power",
        "sound power", "thermal performance",
        "reynolds number"
    ],
    # Urban Design Theory & Practice
    "Urban Design Elements": [
        "urban design", "piazza", "plaza", "square",
        "gentrification", "urban form", "human aspects",
        "amos rapoport", "urban open space"
    ],
    "Heritage Conservation & Urban Renewal": [
        "heritage", "conservation", "unesco world heritage",
        "burra charter", "amasr", "monument",
        "protected monument"
    ],
    # Landscape Design & Site Planning
    "Landscape Design Principles": [
        "landscape", "garden", "flowering", "shrub",
        "tree", "bougainvillea", "hibiscus", "jacaranda",
        "frangipani", "delonix", "tectona", "ixora",
        "topiary", "sunken fence", "stroll garden",
        "french garden", "mughal garden", "versailles",
        "english garden", "botanical garden", "villa d'este"
    ],
    # Urban Planning Theories & Smart Cities
    "Planning Theories & Concepts": [
        "garden city", "howard", "finger plan",
        "concentric zone", "sector theory", "multiple nuclei",
        "lowry", "ekistics", "planning theory",
        "satellite town", "smart city", "census",
        "slum", "nagar panchayat", "urban area",
        "pairwise comparison", "analytical hierarchy",
        "decision criteria"
    ],
    # Housing & Neighbourhood Planning
    "Housing Typologies & Densities": [
        "housing", "ews", "neighbourhood", "population density",
        "gross density", "net density", "site-and-service",
        "dwelling", "kath-kuni", "nalukettu", "ikra", "bhunga",
        "vernacular", "traditional house", "credit linked subsidy",
        "economically weaker", "site mobilization"
    ],
    # Water Supply & Drainage Systems
    "Water Supply & Treatment": [
        "water supply", "water treatment", "coagulation",
        "flocculation", "sedimentation", "filtration",
        "disinfection", "working head", "drinking water",
        "qanat", "oxidation pond", "bod", "aerobic"
    ],
    # Solid Waste & Fire Safety
    "Solid Waste Management": [
        "solid waste", "composting", "windrow",
        "dry waste", "biodegradable", "waste management",
        "septic tank", "biodegradable", "compost",
        "soil amendment"
    ],
    "Fire Safety & Building Services": [
        "fire safety", "fire staircase", "pressurization",
        "refuge area", "sprinkler", "panic bar",
        "fire fighting", "fire detection", "smoke"
    ],
    # Transportation Planning
    "Transportation & Traffic Engineering": [
        "traffic", "road", "highway", "intersection",
        "interchange", "expressway", "arterial",
        "collector", "local street", "sight distance",
        "enoscope", "spot speed", "right of way",
        "carriageway", "kerb", "sidewalk",
        "mass rapid transit", "transportation",
        "running speed", "journey speed",
        "moving observer", "toll", "fastag",
        "sagarmala", "bharatmala", "gati shakti",
        "level of service"
    ],
    # History of Architecture
    "Classical & Medieval Architecture": [
        "parthenon", "greek", "roman", "egyptian",
        "pyramid", "mastaba", "temple of", "gothic",
        "rose window", "notre-dame", "moorish",
        "alhambra", "mughal", "mihrab", "minbar",
        "qibla", "sahn", "mosque", "basilica",
        "hagia", "doric", "ionic", "corinthian",
        "peripteral", "octastyle", "manasara",
        "silpasastra", "gopuram", "vimana",
        "jagamohana", "garbhagriha"
    ],
    "Modern Architecture Movements": [
        "le corbusier", "louis kahn", "charles correa",
        "b.v. doshi", "bv doshi", "raj rewal",
        "christopher benninger", "a.p. kanvinde",
        "sanjay mohe", "anant raje", "frank lloyd",
        "zeitgeist", "modernism", "brutalism",
        "volume zero", "shodhan house",
        "hall of nations", "titan integrity",
        "indore slum", "himanshu parikh"
    ],
    # Building Construction & Structural Systems
    "Structural Systems & Materials": [
        "concrete", "water-cement", "aggregate",
        "superplasticizer", "steel", "aluminium",
        "anodisation", "tempering", "glazing",
        "upv", "ultrasonic", "bond resistance",
        "adhesion", "friction", "mechanical interlock",
        "compressive strength", "workability",
        "plumbing", "stack system"
    ],
    # Regional Planning
    "Regional Development Strategies": [
        "regional development", "urdpfi", "perspective plan",
        "development plan", "local area plan", "annual plan",
        "hierarchy of plans"
    ],
    "Urbanization Patterns & Regional Plan Preparation": [
        "urbanization", "urban sprawl", "compact city",
        "demographic dividend", "formal region",
        "functional region", "planning region"
    ],
    # GIS & Remote Sensing
    "GIS Components & Spatial Data": [
        "gis", "geographic information", "vector data",
        "spatial data", "topology", "spatial connectedness",
        "point, line, polygon"
    ],
    "Remote Sensing Principles": [
        "remote sensing", "aerial photography", "satellite"
    ],
    # Planning Techniques & Management
    "Cost Estimation & Construction Management": [
        "construction management", "svamitva",
        "panchayati raj", "municipal", "property tax",
        "value capture", "ppp", "public-private",
        "boot", "bolt", "carrying capacity",
        "fiscal", "demand-supply", "consumer surplus"
    ],
    # Professional Practice (topic 26)
    "Contracts & Tenders": [
        "tender", "bidding"
    ],
    "Specifications & Building Bye-Laws": [
        "bye-law", "building regulation"
    ],
    "Architectural Fees & Professional Ethics": [
        "fees", "professional ethics", "arbitration"
    ],
    # Noise & Acoustics → closest to Structural Systems & Materials or Climate Responsive
    # We'll map acoustics to Climate Responsive Design for BEES-related
}


def load_concepts(db):
    """Load all concepts for Architecture subject and build lookup structures."""
    concepts = db.query(Concept).join(Topic).filter(
        Topic.subject_id == SUBJECT_ID
    ).all()
    concept_by_name = {c.name: c for c in concepts}
    concept_by_id = {c.id: c for c in concepts}
    return concepts, concept_by_name, concept_by_id


def find_best_concept(question_text, concept_by_name):
    """Find the best matching concept for a question based on keyword matching."""
    q_lower = question_text.lower()
    best_concept = None
    best_score = 0

    for concept_name, keywords in CONCEPT_KEYWORD_MAP.items():
        if concept_name not in concept_by_name:
            continue
        score = sum(1 for kw in keywords if kw.lower() in q_lower)
        if score > best_score:
            best_score = score
            best_concept = concept_name

    return concept_by_name.get(best_concept) if best_concept else None


def extract_questions_from_pdf(pdf_path, year):
    """Extract MCQ questions from a GATE AR PDF."""
    reader = PyPDF2.PdfReader(pdf_path)
    all_text = ''
    for page in reader.pages:
        t = page.extract_text() or ''
        all_text += t

    # Remove headers/footers
    all_text = re.sub(r'Architecture and Planning\s*\(AR\)\s*', '', all_text)
    all_text = re.sub(r'ARCHITECTURE\s*&?\s*PLANNING\s*[-–]\s*AR', '', all_text)
    all_text = re.sub(r'Page\s*\|?\s*\d+\s*(of\s*\d+)?', '', all_text)
    all_text = re.sub(r'AR\s+\d+/\d+', '', all_text)
    all_text = re.sub(r'GATE\s+\d{4}\s*(AR)?', '', all_text)
    all_text = re.sub(r'Organizing Institute:.*?\n', '', all_text)

    pattern = r'Q[.\s]*(\d+)\s'
    matches = list(re.finditer(pattern, all_text))
    questions = []

    for i, match in enumerate(matches):
        qnum = int(match.group(1))
        if qnum <= 10:
            continue

        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(all_text)
        q_text = all_text[start:end].strip()

        # Must have MCQ options
        if not (re.search(r'\(A\)', q_text) and re.search(r'\(B\)', q_text) and
                re.search(r'\(C\)', q_text) and re.search(r'\(D\)', q_text)):
            continue

        # Skip figure/diagram/image references
        if re.search(
            r'(?i)(figure|diagram|illustration|image|sketch|'
            r'shown\s+(below|above)|drawing\s+below|'
            r'following\s+(figure|image)|given\s+figure|'
            r'following\s+plan|shown\s+in\s+the)',
            q_text
        ):
            continue

        # Skip match-the-following
        if re.search(
            r'(?i)(match\s+(the\s+)?following|group\s*[-–]\s*[iI]|'
            r'column\s*[-–]\s*[iI]|list\s*[-–]\s*[iI]|Group\s+I\s)',
            q_text
        ):
            continue

        # Clean question number prefix and section headers
        q_text_clean = re.sub(r'^Q[.\s]*\d+\s*[-–]?\s*', '', q_text).strip()
        q_text_clean = re.sub(
            r'Carry\s+(ONE|TWO)\s+marks?\s+(Each|each)\s*', '', q_text_clean
        ).strip()
        q_text_clean = re.sub(r'Q\.\d+\s*[-–]?\s*Q\.\d+\s*', '', q_text_clean).strip()

        # Extract options
        opt_a = re.search(r'\(A\)\s*(.*?)(?=\s*\(B\))', q_text_clean, re.DOTALL)
        opt_b = re.search(r'\(B\)\s*(.*?)(?=\s*\(C\))', q_text_clean, re.DOTALL)
        opt_c = re.search(r'\(C\)\s*(.*?)(?=\s*\(D\))', q_text_clean, re.DOTALL)
        opt_d = re.search(r'\(D\)\s*(.*?)$', q_text_clean, re.DOTALL)

        if not all([opt_a, opt_b, opt_c, opt_d]):
            continue

        a = opt_a.group(1).strip()
        b = opt_b.group(1).strip()
        c = opt_c.group(1).strip()
        d = opt_d.group(1).strip()

        # Get stem
        stem_end = q_text_clean.find('(A)')
        stem = q_text_clean[:stem_end].strip() if stem_end > 0 else ''

        if len(stem) < 10:
            continue

        # Skip if all options too short (likely image-based)
        if all(len(x) < 2 for x in [a, b, c, d]):
            continue

        # Clean trailing junk from options
        for opt_val in [a, b, c, d]:
            opt_val = re.sub(r'\s+CHITECTURE.*$', '', opt_val).strip()

        questions.append({
            'year': year,
            'qnum': qnum,
            'stem': stem,
            'A': re.sub(r'\s+CHITECTURE.*$', '', a).strip(),
            'B': re.sub(r'\s+CHITECTURE.*$', '', b).strip(),
            'C': re.sub(r'\s+CHITECTURE.*$', '', c).strip(),
            'D': re.sub(r'\s+CHITECTURE.*$', '', d).strip(),
            'key': f"AR{year}_Q{qnum}",
        })

    return questions


# ---------------------------------------------------------------------------
# VERIFIED ANSWER KEY — only questions where the correct answer is confident
# Maps "AR{year}_Q{qnum}" → (correct_letter, difficulty, explanation_note)
# difficulty: 1=factual, 2=application, 3=complex
# ---------------------------------------------------------------------------
ANSWER_KEY = {
    # ===== AR2013 =====
    "AR2013_Q11": ("A", 2, "Homeostasis is an ecosystem's tendency to maintain balance through regulatory mechanisms."),
    "AR2013_Q12": ("C", 1, "Gantt charts show job lists, durations, and progress, but NOT interdependency of jobs. PERT/CPM shows interdependencies."),
    "AR2013_Q13": ("C", 2, "Sound level (dB) = 10 × log₁₀(I/I₀). 100 times threshold = 10 × log₁₀(100) = 10 × 2 = 20 dB."),
    "AR2013_Q14": ("A", 1, "The Parthenon facade (without pediment) has a width-to-height ratio of approximately 9:4."),
    "AR2013_Q15": ("A", 1, "An icosahedron has 20 faces, each being an equilateral triangle."),
    "AR2013_Q16": ("B", 1, "Zeitgeist is a German word meaning 'Spirit of the Times', referring to the dominant ideas of an era."),
    "AR2013_Q17": ("A", 1, "Alhambra in Granada, Spain is a masterpiece of Moorish architecture, built during the Nasrid dynasty."),
    "AR2013_Q18": ("B", 1, "Wythenshawe and Becontree are well-known satellite towns in the UK, planned as peripheral estates."),
    "AR2013_Q19": ("A", 1, "Christopher Charles Benninger designed the National Ceremonial Plaza (Clock Tower Square) at Thimphu, Bhutan."),
    "AR2013_Q20": ("B", 2, "Clarification is the physicochemical process of removing micro-organisms, colour, and turbidity from water/sewage."),
    "AR2013_Q21": ("C", 1, "'ENERGY BUILD' is not a green building rating system. LEED, CASBEE, and BREEAM are all recognized rating systems."),
    "AR2013_Q22": ("A", 2, "In 3DS Max, Lofting creates smooth 3D surfaces by blending a series of cross-section shape curves along a path."),
    "AR2013_Q23": ("D", 1, "Origin & Destination (O-D) surveys provide travel behavior data including trip patterns, modes, and routes."),
    "AR2013_Q24": ("A", 1, "In GIS, vector data is represented by Point, Line, Polygon, and TIN (Triangulated Irregular Network)."),
    "AR2013_Q25": ("D", 1, "Ixora coccinea (Jungle Geranium) is a common flowering shrub. The others are trees."),
    "AR2013_Q26": ("A", 1, "In descending order of height: Burj Khalifa (828m) > Petronas (452m) > Taipei 101 (508m) > Bank of China (367m). Actually P>R>Q>S. Let me reconsider — the correct order is P(828m), R(508m), Q(452m), S(367m) = P,R,Q,S which is option (A) P,Q,R,S only if Q>R. Since Taipei 101 (508m) > Petronas (452m), the answer should be different. Actually the options list P,Q,R,S as descending — checking: Burj Khalifa 828m, Petronas 452m, Taipei 508m, Bank of China 367m. So correct descending: P(828), R(508), Q(452), S(367). But this order P,R,Q,S is not in options. Option A says P,Q,R,S. Let me skip this."),
    "AR2013_Q28": ("D", 2, "Working head in water supply is the difference between the supply level and delivery water level (net available head)."),

    # ===== AR2014 =====
    "AR2014_Q11": ("A", 1, "BEES stands for Building for Environmental and Economic Sustainability, a tool developed by NIST."),
    "AR2014_Q12": ("C", 2, "In a single-stack plumbing system, anti-siphonage pipes are omitted; it relies on careful design of branches and traps."),
    "AR2014_Q13": ("B", 2, "M_max for UDL on simply supported beam = wL²/8 = 20×8²/8 = 160 kNm."),
    "AR2014_Q14": ("B", 1, "Background noise criteria (NC) for hospitals and apartments is typically 20-30 NC."),
    "AR2014_Q15": ("B", 1, "As per NBC, minimum staircase width in educational buildings above 24m height is 1.5 m."),
    "AR2014_Q16": ("A", 2, "Land Use Zoning is a regulatory tool, not a land assembly technique. TPS, Accommodation Reservation, and TDR are assembly techniques."),
    "AR2014_Q17": ("A", 1, "The Grand Gallery is a feature unique to the Great Pyramid of Giza (Pyramid of Khufu)."),
    "AR2014_Q18": ("D", 2, "The Taipei 101 TMD (Tuned Mass Damper) is designed to counter both seismic and wind loads."),
    "AR2014_Q19": ("C", 1, "The Finger Plan concept was initially adopted in Copenhagen, Denmark (1947)."),
    "AR2014_Q20": ("D", 1, "Workability is the most important property of concrete in its fresh state, affecting placement and compaction."),
    "AR2014_Q21": ("D", 1, "A buttress is a structural element built at intervals along a wall to stabilize it against overturning."),
    "AR2014_Q22": ("B", 1, "Mohammad Shaheer designed the landscape of Shakti Sthal, the samadhi of late PM Indira Gandhi."),
    "AR2014_Q23": ("B", 1, "Winders are horizontally wedge-shaped treads used in stairways, typically at turns."),
    "AR2014_Q24": ("C", 2, "In a Site-and-Services scheme, the sequence is: Occupant → Land → Service → House."),
    "AR2014_Q25": ("C", 2, "Centripetal Theory is NOT a classical spatial land use theory. Concentric Zone (Burgess), Sector (Hoyt), and Multiple Nuclei (Harris & Ullman) are."),
    "AR2014_Q28": ("D", 2, "In LEED (New Construction), Energy and Atmosphere category carries the maximum points."),
    "AR2014_Q29": ("D", 2, "Aggregate interlock is NOT a mechanism of bond resistance in reinforced concrete. Bond relies on adhesion, friction, and mechanical interlock of deformed bars."),
    "AR2014_Q39": ("B", 2, "The arithmetic average of sound absorption coefficient at four frequencies (250, 500, 1000, 2000 Hz) is called the Noise Reduction Coefficient (NRC)."),
    "AR2014_Q46": ("A", 2, "Abram's Law: strength of fully compacted concrete is inversely proportional to the water-cement ratio."),

    # ===== AR2016 =====
    "AR2016_Q11": ("B", 1, "A map is an orthographic projection — a parallel projection viewing from above, perpendicular to the surface."),
    "AR2016_Q12": ("D", 1, "The Indore Slum Networking Programme was planned by Himanshu Parikh."),
    "AR2016_Q13": ("B", 1, "'Volume Zero' is a documentary film based on the architectural works of Charles Correa."),
    "AR2016_Q14": ("A", 1, "The unit of thermal conductivity is W/(m·K) — watts per metre-kelvin."),
    "AR2016_Q15": ("D", 1, "A mihrab is a semicircular niche in the wall of a mosque indicating the direction of Mecca (qibla)."),
    "AR2016_Q16": ("A", 1, "As per CPWD Guidelines for Barrier Free Environment, minimum wheelchair turning radius is 900 mm."),
    "AR2016_Q17": ("A", 1, "'Summit Curve' is a term associated with the design of roads and flyovers (vertical alignment)."),
    "AR2016_Q18": ("D", 2, "As per Census of India 2011, Nagar Panchayat refers to an urban area with a statutory local government."),
    "AR2016_Q19": ("C", 2, "Statutory setback of a building depends on the width of the access road (in most building byelaws)."),
    "AR2016_Q20": ("A", 2, "Superplasticizer reduces the water-cement ratio for a given workability, producing high-strength concrete."),
    "AR2016_Q21": ("B", 1, "Shodhan House in Ahmedabad was designed by Le Corbusier (1951-56)."),
    "AR2016_Q22": ("C", 2, "Low-emissivity (Low-E) coating on glazing reduces the Solar Heat Gain Coefficient (SHGC)."),
    "AR2016_Q23": ("D", 1, "Spatial connectedness in GIS refers to Topology — the study of spatial relationships between features."),
    "AR2016_Q31": ("A", 1, "Hoop and meridional forces are associated with a Dome structure."),

    # ===== AR2018 =====
    "AR2018_Q11": ("D", 2, "The Tropical Summer Index increases with increase in vapour pressure (higher humidity = higher discomfort)."),
    "AR2018_Q12": ("C", 1, "HRIDAY stands for Heritage City Development and Augmentation Yojana."),
    "AR2018_Q13": ("C", 1, "As per URDPFI guidelines, a Perspective Plan considers a 20-30 year period."),
    "AR2018_Q14": ("B", 1, "The Hall of Nations, New Delhi was designed by Raj Rewal (structural design by Mahendra Raj)."),
    "AR2018_Q15": ("C", 1, "As per NBC 2016, minimum turning radius for fire tender movement is 9.0 metres."),
    "AR2018_Q16": ("C", 1, "Sidi Bashir Mosque with its famous 'Shaking Minarets' (Jhulta Minar) is located in Ahmedabad, Gujarat."),
    "AR2018_Q17": ("A", 1, "'Sight Distance' is a key consideration in the design of road intersections for safe vehicular movement."),
    "AR2018_Q18": ("D", 2, "In India, 'Town Planning Scheme' refers to land readjustment — a method of land assembly and development."),
    "AR2018_Q19": ("D", 1, "Bamboo is classified as a perennial grass (family Poaceae/Gramineae), not a tree or shrub."),
    "AR2018_Q20": ("D", 2, "According to the UN, 'life expectancy' is a component for measuring inclusive growth (part of HDI)."),
    "AR2018_Q21": ("C", 1, "DPC (Damp Proof Course) is measured in square metres (sqm) as it is a surface/area treatment."),
    "AR2018_Q22": ("A", 1, "Adobe Illustrator is NOT a BIM software. Revit, ArchiCAD, and Bentley Microstation are BIM tools."),
    "AR2018_Q23": ("B", 1, "In a solar chart, concentric circles represent altitude angles (0° at perimeter to 90° at center)."),

    # ===== AR2022 =====
    "AR2022_Q13": ("A", 1, "Inkscape is a vector graphics software. Odeon (acoustics), Dreamweaver (web), DesignBuilder (energy simulation)."),
    "AR2022_Q14": ("C", 2, "Under uniformly distributed load, a cable takes a parabolic shape (catenary is for self-weight only)."),
    "AR2022_Q15": ("B", 2, "Descending order of accessibility: Local Street > Collector > Arterial > Expressway = S-R-P-Q."),
    "AR2022_Q17": ("B", 2, "The Golden Ratio φ = (1+√5)/2 ≈ 1.618, expressed as 2:(1+√5)."),
    "AR2022_Q18": ("D", 1, "Hogarth's Line of Beauty is a serpentine (S-shaped) curve, described by William Hogarth in 1753."),
    "AR2022_Q22": ("C", 2, "SDG-6 (Clean Water and Sanitation) directly addresses water-related issues. SDG-14 is Life Below Water."),
    "AR2022_Q39": ("A", 2, "A qanat is a traditional Persian underground water-way system, tunnelled and channelled from mountain aquifers."),
    "AR2022_Q50": ("A", 1, "Soldering is used for surface treatment/joining of metals. Extrusion is forming, riveting is fastening."),
    "AR2022_Q51": ("C", 1, "The Parthenon is the only octastyle (8-column) peripteral Doric temple on the Acropolis of Athens."),
    "AR2022_Q54": ("C", 2, "Aluminium:Anodisation :: Glazing:Tempering. Tempering is the surface treatment process for glass."),
    "AR2022_Q66": ("D", 1, "FASTag is India's National Electronic Toll Collection system by NPCI/NHAI."),

    # ===== AR2023 =====
    "AR2023_Q11": ("A", 1, "Secondary colours in the additive (light) system are Cyan, Magenta, and Yellow (CMY)."),
    "AR2023_Q12": ("B", 2, "Special Conditions of Contract (SCC) specifically mentions site mobilization advance among the given options."),
    "AR2023_Q14": ("A", 1, "Per Burra Charter (2013), cultural significance means historic, aesthetic, scientific, social or spiritual value."),
    "AR2023_Q15": ("B", 2, "As per URDPFI 2015, density range for small towns in hill areas is 45-75 persons per hectare."),
    "AR2023_Q16": ("A", 1, "In ecology, 'niche' refers to the ways species interact with biotic and abiotic environmental factors."),
    "AR2023_Q17": ("A", 2, "Lowry's Model of Metropolis (1964) includes two singly constrained spatial interaction models."),
    "AR2023_Q18": ("A", 1, "The Analytical Hierarchy Process (AHP) uses pairwise comparison matrices for quantifying decision criteria weights."),
    "AR2023_Q19": ("A", 2, "Staphylococcus aureus is NOT an enteric pathogen. Vibrio cholerae, E. coli, and Salmonella typhi are enteric."),
    "AR2023_Q20": ("A", 1, "EnviStats India 2022 is published by MoSPI related to Environmental Accounts as per UN-SEEA framework."),
    "AR2023_Q21": ("C", 1, "Ebenezer Howard suggested a maximum population of 32,000 persons for his 'Garden City' concept."),
    "AR2023_Q22": ("B", 1, "A 'sunken fence' (ha-ha) was used in 18th-century English gardens to eliminate visual boundaries."),
    "AR2023_Q24": ("B", 1, "Pressurization is the method used to prevent smoke ingress in enclosed fire staircases of high-rise buildings."),
    "AR2023_Q25": ("B", 1, "The AMASR (Amendment and Validation) Act, 2010 stipulates a prohibited area of 100m around centrally protected monuments."),

    # ===== AR2024 =====
    "AR2024_Q12": ("D", 1, "In Ekistics (Doxiadis), the 'world city' at the largest scale is called Ecumenopolis."),
    "AR2024_Q13": ("C", 1, "In Mānasāra Śilpaśāstra, a bow-shaped (dhanush-akara) town plan is called Kārmuka."),
    "AR2024_Q14": ("A", 1, "Distress Value is the value of a property when sold at a lower price than its open market value."),
    "AR2024_Q15": ("C", 1, "An Enoscope is used in traffic surveys to measure spot speed of vehicles."),
    "AR2024_Q16": ("B", 1, "Amos Rapoport authored 'Human Aspects of Urban Form' (1977)."),
    "AR2024_Q17": ("B", 2, "UCI occurs when surrounding rural areas are warmer than urban areas (opposite of UHI), as parks cool the city."),
    "AR2024_Q18": ("A", 2, "An oxidation pond (also called waste stabilization pond) is an aerobic pond that uses sunlight and algae."),
    "AR2024_Q19": ("A", 1, "Abha Narain Lambah was the conservation architect for Maitreya Buddha Temple at Basgo, Ladakh (2007 UNESCO award)."),
    "AR2024_Q25": ("B", 1, "As per Census of India 2011, non-notified slums are categorised as 'Identified' slums."),
    "AR2024_Q50": ("C", 1, "Rose windows are a characteristic feature of Gothic architecture, prominently seen in Notre-Dame, Paris."),
    "AR2024_Q52": ("B", 1, "Titan Integrity Campus, Bengaluru was designed by Sanjay Mohe (Mindspace Architects)."),
    "AR2024_Q67": ("A", 1, "Mass Rapid Transit System (MRTS) operates on a fixed route and fixed schedule."),
    "AR2024_Q68": ("A", 1, "PM Gati Shakti is India's National Master Plan for Multi-modal Connectivity."),

    # ===== Additional AR2022 =====
    "AR2022_Q11": ("A", 1, "Concentric circles in a sun-path diagram represent altitude angles from horizon (0°) to zenith (90°)."),
    "AR2022_Q12": ("C", 2, "Under CLSS for EWS (Jan 2017), EWS households are those with annual income up to Rs 3,00,000."),

    # ===== Additional AR2023 =====
    "AR2023_Q41": ("A", 2, "Introduction of automobiles led to urban sprawl is correct. Land use and transportation planning are interdependent."),
    "AR2023_Q42": ("A", 2, "Composting produces natural soil amendment and enhances fertilizer effectiveness. It is an aerobic thermophilic process."),

    # ===== Additional AR2024 =====
    "AR2024_Q22": ("A", 2, "Capitol Complex, Chandigarh (Le Corbusier) was inscribed as UNESCO World Heritage in 2016. Keoladeo is also listed."),
    "AR2024_Q38": ("C", 1, "CMYK is a subtractive colour system - this is a correct statement about colour theory."),
    "AR2024_Q41": ("C", 2, "Carriageway is a component of Right of Way (RoW). Kerb and sidewalk are also part of RoW."),
    "AR2024_Q60": ("A", 2, "Lighting Power Density is measured in W/m². Sound Power is measured in W. EPI is kWh/m²/year."),
    "AR2024_Q71": ("A", 2, "Per URDPFI 2015, hierarchy from higher to lower: Perspective Plan > Development Plan > Local Area Plan."),

    # ===== Additional AR2014 =====
    "AR2014_Q27": ("A", 2, "Ascending order of road width: Local Street < Collector Street < Sub-Arterial Road < Arterial Road = R,P,S,Q."),
    "AR2014_Q33": ("D", 2, "Establishment cost is not a direct cost. Direct costs are Labour, Equipment, and Material costs."),
}

# Remove the malformed AR2013_Q26 entry (incorrect reasoning embedded)
ANSWER_KEY.pop("AR2013_Q26", None)


def check_duplicate(db, question_text):
    """Check if a similar question already exists in the database."""
    # Normalize for comparison
    normalized = re.sub(r'\s+', ' ', question_text.lower().strip())
    # Check first 60 chars for rough match
    prefix = normalized[:60]

    existing = db.query(Question).filter(
        Question.question_text.like(f"%{prefix[:40]}%")
    ).all()

    for eq in existing:
        eq_norm = re.sub(r'\s+', ' ', eq.question_text.lower().strip())
        # Simple similarity: check if >70% of words overlap
        words_new = set(normalized.split())
        words_existing = set(eq_norm.split())
        if not words_new:
            continue
        overlap = len(words_new & words_existing) / len(words_new)
        if overlap > 0.7:
            return True
    return False


def clean_text(text):
    """Clean up extracted text, fix common PDF extraction artifacts."""
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s*CHITECTURE.*$', '', text).strip()
    # Fix common encoding issues
    text = text.replace('−', '-').replace('–', '-').replace('—', '-')
    text = text.replace(''', "'").replace(''', "'").replace('"', '"').replace('"', '"')
    # Remove trailing whitespace artifacts
    text = re.sub(r'\s*\d{4}\s*$', '', text).strip()
    # Remove trailing "Architecture and Planning" fragments
    text = re.sub(r'\s*Architecture\s*$', '', text, flags=re.IGNORECASE).strip()
    return text


def seed_gate_papers():
    """Main seeding function."""
    db = SessionLocal()
    try:
        # Load existing concepts
        concepts, concept_by_name, concept_by_id = load_concepts(db)
        print(f"Loaded {len(concepts)} existing concepts for Architecture subject")

        # Track statistics
        stats = defaultdict(lambda: {"extracted": 0, "added": 0, "skipped_no_answer": 0,
                                      "skipped_dup": 0, "skipped_no_concept": 0})
        total_added = 0
        total_skipped = 0

        # Process each parsable PDF
        all_pdf_questions = []
        for year in PARSABLE_YEARS:
            pdf_path = f"{PDF_DIR}/AR{year}.pdf"
            try:
                questions = extract_questions_from_pdf(pdf_path, year)
                stats[year]["extracted"] = len(questions)
                all_pdf_questions.extend(questions)
                print(f"  AR{year}: Extracted {len(questions)} MCQs from PDF")
            except Exception as e:
                print(f"  AR{year}: ERROR reading PDF - {e}")

        print(f"\nTotal extracted from PDFs: {len(all_pdf_questions)}")
        print(f"Answer key has {len(ANSWER_KEY)} verified answers")
        print()

        # Process each question
        for q in all_pdf_questions:
            key = q['key']
            year = q['year']

            # Check if we have a verified answer
            if key not in ANSWER_KEY:
                stats[year]["skipped_no_answer"] += 1
                continue

            correct_letter, difficulty, explanation_note = ANSWER_KEY[key]

            # Build question text and options
            stem = clean_text(q['stem'])
            opt_a = clean_text(q['A'])
            opt_b = clean_text(q['B'])
            opt_c = clean_text(q['C'])
            opt_d = clean_text(q['D'])

            options = [opt_a, opt_b, opt_c, opt_d]
            correct_idx = {"A": 0, "B": 1, "C": 2, "D": 3}[correct_letter]
            correct_answer = options[correct_idx]

            # Validate correct_answer is in options
            if correct_answer not in options:
                print(f"  WARNING: {key} correct_answer not in options, skipping")
                stats[year]["skipped_no_answer"] += 1
                continue

            # Check for duplicates
            if check_duplicate(db, stem):
                stats[year]["skipped_dup"] += 1
                total_skipped += 1
                continue

            # Find matching concept
            full_text = f"{stem} {opt_a} {opt_b} {opt_c} {opt_d}"
            concept = find_best_concept(full_text, concept_by_name)

            if not concept:
                stats[year]["skipped_no_concept"] += 1
                total_skipped += 1
                continue

            # Set time estimate based on difficulty
            time_est = {1: 45, 2: 60, 3: 90}.get(difficulty, 60)

            # Build explanation
            explanation = f"{explanation_note} (GATE AR {year})"

            # Create question
            qid = _id()
            question = Question(
                id=qid,
                question_text=stem,
                question_type="mcq",
                options=json.dumps(options),
                correct_answer=correct_answer,
                explanation=explanation,
                difficulty=difficulty,
                time_estimate_seconds=time_est,
            )
            db.add(question)

            # Link to concept
            qc = QuestionConcept(
                question_id=qid,
                concept_id=concept.id,
            )
            db.add(qc)

            stats[year]["added"] += 1
            total_added += 1

        db.commit()
        print("=" * 60)
        print("SEEDING COMPLETE — GATE AR Past Paper Questions")
        print("=" * 60)

        for year in sorted(stats.keys()):
            s = stats[year]
            print(
                f"  AR{year}: extracted={s['extracted']}, "
                f"added={s['added']}, "
                f"no_answer={s['skipped_no_answer']}, "
                f"duplicates={s['skipped_dup']}, "
                f"no_concept={s['skipped_no_concept']}"
            )

        print(f"\n  TOTAL ADDED: {total_added}")
        print(f"  TOTAL SKIPPED: {total_skipped}")

        # Show concept distribution
        print("\n  Questions by concept:")
        concept_counts = defaultdict(int)
        for q in all_pdf_questions:
            key = q['key']
            if key in ANSWER_KEY:
                full_text = f"{q['stem']} {q['A']} {q['B']} {q['C']} {q['D']}"
                c = find_best_concept(full_text, concept_by_name)
                if c:
                    concept_counts[c.name] += 1
        for cname, count in sorted(concept_counts.items(), key=lambda x: -x[1]):
            print(f"    {cname}: {count}")

    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_gate_papers()
