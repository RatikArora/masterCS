# Part 1: Water Supply + Solid Waste Management
questions_part1 = [
  {
    "concept_id": "e3aa2ab1",
    "question_text": "As per IS 1172, the per capita water supply for a city with population above 1 lakh and having full flushing system is recommended as:",
    "options": [
      "150 lpcd",
      "100 lpcd",
      "200 lpcd",
      "135 lpcd"
    ],
    "difficulty": "medium",
    "explanation": "IS 1172 recommends 150 litres per capita per day (lpcd) for cities with population above 1 lakh having full flushing systems. This includes domestic, commercial, industrial, and public uses. For smaller towns, 135 lpcd is recommended, while 200 lpcd applies to metropolitan cities with higher standards."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The maximum daily demand of water is generally taken as what factor of the average daily demand?",
    "options": [
      "1.8",
      "1.5",
      "2.0",
      "1.2"
    ],
    "difficulty": "medium",
    "explanation": "The maximum daily demand is conventionally taken as 1.8 times the average daily demand to account for seasonal variations and peak usage during hot months. The maximum hourly demand is additionally multiplied by 1.5 times the maximum daily demand, resulting in a peak factor of 2.7 times average demand."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "A city has a population of 2,00,000 with per capita demand of 150 lpcd. What is the total water demand in MLD (Million Litres per Day)?",
    "options": [
      "30 MLD",
      "20 MLD",
      "15 MLD",
      "45 MLD"
    ],
    "difficulty": "medium",
    "explanation": "Total water demand = Population × Per capita demand = 2,00,000 × 150 litres/day = 30,000,000 litres/day = 30 MLD. This calculation is fundamental in water supply engineering for designing treatment plants, storage reservoirs, and distribution networks to meet the city's water requirements."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "In a rapid sand filter, the rate of filtration is typically in the range of:",
    "options": [
      "3000-6000 litres/m²/hour",
      "100-200 litres/m²/hour",
      "8000-12000 litres/m²/hour",
      "500-1000 litres/m²/hour"
    ],
    "difficulty": "medium",
    "explanation": "Rapid sand filters operate at 3000-6000 litres/m²/hour (about 40-50 times faster than slow sand filters). They use coarser sand (effective size 0.45-0.7mm) and rely on coagulation pre-treatment. Backwashing is required for cleaning, unlike slow sand filters which use scraping."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The slow sand filter operates at a filtration rate of approximately:",
    "options": [
      "100-200 litres/m²/hour",
      "3000-6000 litres/m²/hour",
      "500-1000 litres/m²/hour",
      "50-75 litres/m²/hour"
    ],
    "difficulty": "medium",
    "explanation": "Slow sand filters operate at 100-200 litres/m²/hour using fine sand (effective size 0.2-0.4mm). They form a biological layer called 'schmutzdecke' on top which provides biological treatment. They are suitable for small communities and do not require coagulation pre-treatment, making them cost-effective."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Breakpoint chlorination is the point at which:",
    "options": [
      "Free residual chlorine begins to appear after chloramines are destroyed",
      "All bacteria in water are killed",
      "Chlorine demand equals chlorine dose",
      "Combined residual chlorine is maximum"
    ],
    "difficulty": "medium",
    "explanation": "Breakpoint chlorination occurs when sufficient chlorine has been added to oxidize all ammonia nitrogen and destroy chloramines (combined residual chlorine). Beyond this point, free residual chlorine appears in direct proportion to additional chlorine added. This ensures effective disinfection with free chlorine."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Which distribution system is most suitable for a city with well-planned roads in a grid pattern?",
    "options": [
      "Grid iron system",
      "Dead end system",
      "Ring system",
      "Radial system"
    ],
    "difficulty": "medium",
    "explanation": "The grid iron (or interlaced) system is ideal for cities with rectangular road layouts. Water can reach any point from multiple directions, ensuring reliability. Dead-end systems cause stagnation, ring systems suit circular layouts, and radial systems distribute from a central source outward."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The detention time for plain sedimentation tank is typically:",
    "options": [
      "4-8 hours",
      "1-2 hours",
      "30-40 minutes",
      "12-24 hours"
    ],
    "difficulty": "medium",
    "explanation": "Plain sedimentation tanks (without coagulation) require 4-8 hours detention time to allow suspended particles to settle by gravity. With coagulation (flocculated sedimentation), the detention time reduces to 2-3 hours due to formation of larger, heavier flocs that settle faster."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The fire demand of a city with population of 1,00,000 as per Kuichling's formula (Q = 3182√P, where P is in thousands) is approximately:",
    "options": [
      "31,820 litres/min",
      "10,060 litres/min",
      "3,182 litres/min",
      "50,000 litres/min"
    ],
    "difficulty": "hard",
    "explanation": "Using Kuichling's formula: Q = 3182√P where P is population in thousands. P = 100, so Q = 3182 × √100 = 3182 × 10 = 31,820 litres/minute. This formula is widely used in India for estimating fire fighting water requirements in urban water supply design."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Hardy Cross method is used for:",
    "options": [
      "Analysis of flow in pipe networks with loops",
      "Design of open channel flow",
      "Estimation of water demand",
      "Design of water treatment plants"
    ],
    "difficulty": "medium",
    "explanation": "The Hardy Cross method is an iterative technique for analyzing flow distribution in closed-loop pipe networks. It uses continuity and energy equations to balance flows by applying corrections until convergence. Each loop must satisfy the condition that the algebraic sum of head losses equals zero."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The Hazen-Williams coefficient 'C' for new cast iron pipes is approximately:",
    "options": [
      "130",
      "100",
      "80",
      "150"
    ],
    "difficulty": "medium",
    "explanation": "The Hazen-Williams coefficient C for new cast iron pipes is approximately 130. This coefficient decreases with age due to corrosion and deposits (old CI pipes: C=80-100). The formula V = 0.849 × C × R^0.63 × S^0.54 is used extensively for pipe flow calculations in water distribution design."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The storage capacity of a service reservoir is typically designed as what fraction of maximum daily demand?",
    "options": [
      "One-third to one-half",
      "One-fourth to one-third",
      "One-half to full",
      "Equal to average daily demand"
    ],
    "difficulty": "medium",
    "explanation": "Service reservoirs are designed with a capacity of one-third to one-half of the maximum daily demand. This accounts for hourly variations in demand, provides emergency storage, and maintains adequate pressure. The reservoir acts as a buffer between the treatment plant output and variable consumer demand patterns."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The process of adding alum (Al₂(SO₄)₃) to raw water for water treatment is called:",
    "options": [
      "Coagulation",
      "Flocculation",
      "Sedimentation",
      "Disinfection"
    ],
    "difficulty": "medium",
    "explanation": "Coagulation involves adding chemical coagulants like alum (aluminium sulphate) to neutralize the charges on colloidal particles, allowing them to aggregate. Flocculation is the subsequent gentle mixing that promotes formation of larger floc particles. Together they prepare water for efficient sedimentation."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "What is the residual chlorine required in the distribution system at the consumer end as per Indian standards?",
    "options": [
      "0.2 mg/L",
      "0.5 mg/L",
      "1.0 mg/L",
      "0.05 mg/L"
    ],
    "difficulty": "medium",
    "explanation": "As per IS 10500 and CPHEEO guidelines, a minimum free residual chlorine of 0.2 mg/L must be maintained at the farthest point in the distribution system. At the treatment plant exit, 0.5 mg/L is maintained. This ensures continued disinfection and prevents bacterial regrowth during distribution."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The contact period for chlorination of water should be at least:",
    "options": [
      "30 minutes",
      "10 minutes",
      "60 minutes",
      "5 minutes"
    ],
    "difficulty": "medium",
    "explanation": "A minimum contact time of 30 minutes is required for effective chlorine disinfection of water. The CT value (concentration × time) is the key parameter determining disinfection effectiveness. Higher temperatures and lower pH improve chlorination efficiency, while higher turbidity reduces it."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "In water treatment, the flocculation chamber typically has a detention time of:",
    "options": [
      "20-30 minutes",
      "4-8 hours",
      "5-10 minutes",
      "60-90 minutes"
    ],
    "difficulty": "medium",
    "explanation": "Flocculation chambers provide gentle mixing for 20-30 minutes with gradually decreasing velocity gradient (G value from 60 to 10 s⁻¹). This allows coagulated particles to form larger flocs through contact. The slow mixing prevents breakup of delicate floc structures while promoting growth."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "A water treatment plant receives raw water with turbidity of 200 NTU. Which treatment sequence is most appropriate?",
    "options": [
      "Coagulation → Flocculation → Sedimentation → Filtration → Disinfection",
      "Disinfection → Filtration → Sedimentation → Coagulation",
      "Filtration → Sedimentation → Coagulation → Disinfection",
      "Sedimentation → Filtration → Disinfection only"
    ],
    "difficulty": "medium",
    "explanation": "For high turbidity water (200 NTU), the standard treatment sequence is: coagulation (chemical addition and rapid mix), flocculation (slow mixing), sedimentation (gravity settling of flocs), filtration (removal of remaining particles), and disinfection (chlorination). This sequence progressively removes impurities."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The permissible limit of pH for drinking water as per IS 10500 is:",
    "options": [
      "6.5 to 8.5",
      "5.0 to 7.0",
      "7.0 to 9.0",
      "6.0 to 7.5"
    ],
    "difficulty": "medium",
    "explanation": "IS 10500 specifies the acceptable pH range for drinking water as 6.5 to 8.5. Water outside this range can cause corrosion of pipes (low pH) or scale formation (high pH). The pH also affects the efficiency of chlorine disinfection, with free chlorine being more effective at lower pH values."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The desirable limit of Total Dissolved Solids (TDS) in drinking water as per IS 10500 is:",
    "options": [
      "500 mg/L",
      "1000 mg/L",
      "1500 mg/L",
      "200 mg/L"
    ],
    "difficulty": "medium",
    "explanation": "IS 10500 specifies the desirable TDS limit as 500 mg/L and the maximum permissible limit as 2000 mg/L (in absence of alternative source). High TDS causes taste issues, scaling, and health concerns. TDS is measured using conductivity or by evaporating a filtered sample and weighing the residue."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Calculate the horsepower of a pump required to lift 500 litres/minute of water to a height of 30 meters (assume pump efficiency 75%).",
    "options": [
      "4.0 HP approximately",
      "2.5 HP approximately",
      "6.0 HP approximately",
      "8.0 HP approximately"
    ],
    "difficulty": "hard",
    "explanation": "Water HP = (Q × H × γ)/(75 × 60) where Q=500 L/min, H=30m, γ=1 kg/L. Water HP = (500 × 30)/(75 × 60) = 15000/4500 = 3.33 HP. Actual HP = Water HP/Efficiency = 3.33/0.75 = 4.44 HP ≈ 4.0 HP. This pump sizing calculation is essential for water supply system design."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "In a dead-end distribution system, the main disadvantage is:",
    "options": [
      "Stagnation of water at dead ends causing quality deterioration",
      "High construction cost",
      "Complex design calculations",
      "Inability to maintain pressure"
    ],
    "difficulty": "medium",
    "explanation": "Dead-end (tree) distribution systems cause water stagnation at terminal points because water reaches consumers from only one direction. This leads to bacterial growth, taste/odor issues, and sediment accumulation. For fire fighting, it provides inadequate supply since water comes from one direction only."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The MPN (Most Probable Number) test for coliform count in treated drinking water should show:",
    "options": [
      "Less than 1 per 100 mL",
      "Less than 10 per 100 mL",
      "Less than 100 per 100 mL",
      "Zero per 100 mL at all times"
    ],
    "difficulty": "hard",
    "explanation": "As per IS 10500, treated drinking water should have coliform count less than 1 per 100 mL (ideally zero). MPN test uses multiple dilution tubes to statistically estimate bacterial concentration. The presence of coliforms indicates potential fecal contamination and inadequate treatment or post-treatment contamination."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Which type of valve is used to prevent backflow in water distribution systems?",
    "options": [
      "Non-return valve (check valve)",
      "Gate valve",
      "Butterfly valve",
      "Pressure relief valve"
    ],
    "difficulty": "medium",
    "explanation": "Non-return valves (check valves) allow water flow in one direction only and automatically close when flow reverses. They prevent contamination from backflow (back-siphonage) in water supply systems. Gate valves are for isolation, butterfly valves for throttling, and pressure relief valves for overpressure protection."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Rainwater harvesting through rooftop collection — if a roof area is 200 m² and annual rainfall is 800 mm with runoff coefficient 0.85, the annual rainwater potential is:",
    "options": [
      "136,000 litres",
      "160,000 litres",
      "100,000 litres",
      "200,000 litres"
    ],
    "difficulty": "hard",
    "explanation": "Annual rainwater potential = Roof area × Rainfall × Runoff coefficient = 200 × 0.8 × 0.85 = 136 m³ = 136,000 litres. The runoff coefficient (0.85 for RCC roof) accounts for losses due to evaporation and first-flush diversion. This calculation is critical for designing rainwater harvesting systems."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The minimum velocity of flow in water distribution pipes should be maintained at:",
    "options": [
      "0.6 m/s",
      "0.3 m/s",
      "1.0 m/s",
      "2.0 m/s"
    ],
    "difficulty": "medium",
    "explanation": "A minimum velocity of 0.6 m/s (self-cleansing velocity) prevents sediment deposition in water distribution mains. The maximum velocity is limited to 3.0 m/s to prevent erosion and water hammer. Optimal velocity range of 0.6-1.5 m/s balances between sediment prevention and pipe longevity."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "BOD (Biochemical Oxygen Demand) of raw domestic sewage is typically in the range of:",
    "options": [
      "200-300 mg/L",
      "50-100 mg/L",
      "500-800 mg/L",
      "20-50 mg/L"
    ],
    "difficulty": "medium",
    "explanation": "Raw domestic sewage has BOD typically in the range of 200-300 mg/L, indicating the amount of dissolved oxygen needed by microorganisms to decompose organic matter. Treated water should have BOD less than 30 mg/L for discharge into inland water bodies as per CPCB standards."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The National Board of Fire Underwriters formula for fire demand is Q = 4637√P(1-0.01√P). For a population of 40,000, the fire demand is approximately:",
    "options": [
      "23,455 litres/min",
      "29,312 litres/min",
      "18,548 litres/min",
      "32,000 litres/min"
    ],
    "difficulty": "hard",
    "explanation": "Q = 4637√P(1 - 0.01√P) where P = population in thousands = 40. Q = 4637 × √40 × (1 - 0.01 × √40) = 4637 × 6.32 × (1 - 0.0632) = 4637 × 6.32 × 0.9368 = 29,313 × 0.80 ≈ 23,455 L/min. This formula accounts for reduced rate of increase for larger populations."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Zeolite process in water treatment is used for:",
    "options": [
      "Removal of hardness (water softening)",
      "Removal of turbidity",
      "Disinfection",
      "Removal of color and odor"
    ],
    "difficulty": "medium",
    "explanation": "Zeolite (base exchange) process removes hardness by exchanging calcium and magnesium ions with sodium ions in the zeolite bed. When exhausted, zeolite is regenerated with brine (NaCl) solution. It is effective for removing both temporary and permanent hardness but does not remove turbidity or bacteria."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Aeration in water treatment is primarily done to remove:",
    "options": [
      "Dissolved gases like CO₂ and H₂S, and to add oxygen",
      "Suspended solids",
      "Bacteria and viruses",
      "Heavy metals"
    ],
    "difficulty": "medium",
    "explanation": "Aeration removes dissolved gases (CO₂, H₂S, methane) that cause taste and odor issues, and adds dissolved oxygen which helps in oxidation of iron and manganese. Types include cascade aerators, spray aerators, and diffused air systems. Aeration is typically the first step in water treatment."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "In the radial distribution system, water flows:",
    "options": [
      "From center outwards towards the periphery",
      "Along a ring main in a circular path",
      "From periphery towards the center",
      "In a branching tree pattern"
    ],
    "difficulty": "medium",
    "explanation": "In radial distribution, water is pumped from a centrally located source/reservoir and flows radially outward through mains to the peripheral areas. This system provides high pressure near the center and is suitable for cities with a central water source. Each zone can have independent control."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The effective size (D₁₀) of sand used in a rapid sand filter is in the range of:",
    "options": [
      "0.45 to 0.70 mm",
      "0.15 to 0.30 mm",
      "1.0 to 2.0 mm",
      "0.05 to 0.10 mm"
    ],
    "difficulty": "medium",
    "explanation": "Rapid sand filters use coarser sand with effective size D₁₀ of 0.45 to 0.70 mm and uniformity coefficient of 1.2-1.7. Coarser sand allows higher filtration rates but requires coagulation pre-treatment. Slow sand filters use finer sand (D₁₀ = 0.2-0.4mm) allowing biological treatment without chemicals."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The supernatant water depth above the sand bed in a slow sand filter is maintained at:",
    "options": [
      "1.0 to 1.5 m",
      "0.3 to 0.5 m",
      "2.0 to 3.0 m",
      "3.0 to 5.0 m"
    ],
    "difficulty": "hard",
    "explanation": "In slow sand filters, supernatant water depth of 1.0-1.5 m is maintained above the sand bed. This provides the necessary head for filtration through the fine sand bed (0.6-1.0m thick). The sand bed sits on gravel support of 0.3-0.6m depth. An underdrainage system collects filtered water below."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Which chemical is used as a coagulant aid to improve floc formation in water treatment?",
    "options": [
      "Polyelectrolytes (activated silica or polymers)",
      "Calcium hypochlorite",
      "Potassium permanganate",
      "Copper sulphate"
    ],
    "difficulty": "hard",
    "explanation": "Polyelectrolytes (organic polymers) and activated silica serve as coagulant aids, strengthening floc and accelerating sedimentation. They bridge between particles, creating larger and denser flocs. Calcium hypochlorite is a disinfectant, KMnO₄ removes iron/manganese, and CuSO₄ controls algae growth in reservoirs."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "A water supply system operates on an intermittent supply basis. The recommended storage capacity at consumer level is:",
    "options": [
      "Equal to one day's requirement",
      "Half of daily requirement",
      "Three days' requirement",
      "One week's requirement"
    ],
    "difficulty": "hard",
    "explanation": "For intermittent water supply systems (common in Indian cities), consumer-level storage equal to one full day's requirement is recommended. This ensures water availability during non-supply hours. At community level, overhead tanks are designed for the peak supply period. Continuous supply systems need less storage."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "The velocity of flow in water supply mains should not exceed:",
    "options": [
      "3.0 m/s",
      "1.5 m/s",
      "5.0 m/s",
      "0.6 m/s"
    ],
    "difficulty": "hard",
    "explanation": "Maximum velocity in water mains is limited to 3.0 m/s to prevent pipe erosion, excessive head loss, and water hammer effects. Minimum velocity of 0.6 m/s is needed for self-cleansing. For gravity mains, economical velocity is 0.9-1.5 m/s. Higher velocities increase friction losses proportional to V² (Darcy-Weisbach equation)."
  },
  {
    "concept_id": "e3aa2ab1",
    "question_text": "Which is NOT a type of water distribution system layout?",
    "options": [
      "Parallel system",
      "Dead-end system",
      "Grid iron system",
      "Ring system"
    ],
    "difficulty": "hard",
    "explanation": "The four recognized types of water distribution system layouts are: dead-end (tree), grid iron (interlaced), ring (circular), and radial. 'Parallel system' is not a standard classification. Each layout has specific advantages regarding reliability, cost, and water quality maintenance depending on city morphology."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "As per SWM Rules 2016, the responsibility of segregation of waste at source lies with:",
    "options": [
      "Waste generator (household/establishment)",
      "Municipal corporation only",
      "Rag pickers and informal sector",
      "State Pollution Control Board"
    ],
    "difficulty": "medium",
    "explanation": "SWM Rules 2016 mandate that every waste generator shall segregate waste into wet (biodegradable), dry (recyclable), and domestic hazardous categories at source before handing over to authorized collectors. This is a paradigm shift from the earlier approach where municipalities handled unsegregated waste."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "The per capita solid waste generation rate in Indian metropolitan cities is approximately:",
    "options": [
      "0.3 to 0.6 kg/capita/day",
      "0.1 to 0.2 kg/capita/day",
      "1.0 to 1.5 kg/capita/day",
      "2.0 to 3.0 kg/capita/day"
    ],
    "difficulty": "medium",
    "explanation": "Indian metropolitan cities generate 0.3-0.6 kg of solid waste per capita per day, significantly lower than developed countries (USA: 2.0 kg/capita/day). The composition is predominantly organic (40-60%), with increasing recyclable content. Higher income areas generate more waste with higher recyclable fraction."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "The correct order of the waste management hierarchy (most preferred to least preferred) is:",
    "options": [
      "Prevention → Reduction → Reuse → Recycle → Recovery → Disposal",
      "Disposal → Recovery → Recycle → Reuse → Reduction → Prevention",
      "Recycle → Reuse → Recovery → Reduction → Prevention → Disposal",
      "Collection → Transport → Processing → Disposal → Monitoring"
    ],
    "difficulty": "medium",
    "explanation": "The waste hierarchy prioritizes: Prevention (avoid waste generation), Reduction (minimize waste), Reuse (use items again), Recycle (material recovery), Recovery (energy recovery), and Disposal (landfilling as last resort). This hierarchy guides policy and practice in sustainable waste management worldwide."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "In biomedical waste management, the yellow colored container/bag is used for:",
    "options": [
      "Incinerable waste like human anatomical waste, animal waste, and soiled waste",
      "Recyclable contaminated waste like tubing and catheters",
      "Sharp waste like needles and blades",
      "Glassware and metallic implants"
    ],
    "difficulty": "medium",
    "explanation": "BMW Rules 2016 specify color-coded segregation: Yellow for anatomical waste, soiled waste, expired medicines (for incineration/deep burial); Red for contaminated recyclable waste; White/translucent for sharps; Blue for glassware and metallic body implants. This prevents cross-contamination and ensures appropriate treatment."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Sanitary landfill differs from open dumping primarily because sanitary landfill has:",
    "options": [
      "Engineered liner system, daily cover, leachate collection, and gas management",
      "Larger area and deeper pits",
      "Location in remote areas only",
      "No restrictions on type of waste accepted"
    ],
    "difficulty": "medium",
    "explanation": "Sanitary landfills are engineered facilities with compacted clay or HDPE liner systems to prevent groundwater contamination, daily soil cover to minimize odor and vermin, leachate collection and treatment systems, and landfill gas management. Open dumps lack these environmental safeguards."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "As per SWM Rules 2016, bulk generators are defined as establishments generating waste more than:",
    "options": [
      "100 kg per day",
      "50 kg per day",
      "200 kg per day",
      "500 kg per day"
    ],
    "difficulty": "medium",
    "explanation": "SWM Rules 2016 define bulk generators as establishments generating more than 100 kg of waste per day. They must segregate waste, process biodegradable waste on-site through composting or biomethanation, and pay user fees as specified by local authorities. Hotels, malls, and institutional campuses typically qualify."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Vermicomposting uses which organism to convert organic waste into compost?",
    "options": [
      "Earthworms (Eisenia fetida)",
      "Bacteria (Bacillus subtilis)",
      "Fungi (Aspergillus niger)",
      "Protozoa"
    ],
    "difficulty": "medium",
    "explanation": "Vermicomposting uses earthworms, primarily Eisenia fetida (red wigglers), to decompose organic waste into nutrient-rich vermicompost. The process operates at ambient temperatures (20-30°C), takes 45-60 days, and produces humus-like material rich in NPK. It is suitable for decentralized processing of biodegradable waste."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "The C:N ratio ideal for composting organic waste is:",
    "options": [
      "25:1 to 30:1",
      "10:1 to 15:1",
      "50:1 to 60:1",
      "5:1 to 8:1"
    ],
    "difficulty": "medium",
    "explanation": "Optimal C:N ratio for composting is 25:1 to 30:1. Too much carbon (high ratio) slows decomposition; too much nitrogen (low ratio) causes ammonia release and odor. Kitchen waste (C:N ~15:1) is mixed with dry leaves or paper (C:N ~50:1) to achieve the ideal ratio for aerobic composting."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Windrow composting involves:",
    "options": [
      "Arranging organic waste in long rows (windrows) with periodic turning for aeration",
      "Composting in enclosed vessels with forced aeration",
      "Underground pit composting without aeration",
      "Composting using only earthworms in shallow beds"
    ],
    "difficulty": "medium",
    "explanation": "Windrow composting arranges organic waste in elongated piles (windrows) 1.5-2m high and 3-4m wide. Regular turning (every 3-7 days) provides aeration for aerobic decomposition. Temperature rises to 55-70°C during thermophilic phase, killing pathogens. The process takes 3-6 months for complete stabilization."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "EPR (Extended Producer Responsibility) in the context of solid waste management means:",
    "options": [
      "Producers are responsible for the entire lifecycle of their products including post-consumer disposal",
      "Producers must extend their production capacity to meet demand",
      "Government extends responsibility to local bodies for waste management",
      "Consumers are responsible for product repair and maintenance"
    ],
    "difficulty": "medium",
    "explanation": "EPR mandates that producers take responsibility for collection, recycling, and environmentally sound disposal of their products at end-of-life. Applied in India under E-waste Rules 2016, Plastic Waste Rules 2016, and Battery Waste Rules. It shifts financial and management burden from municipalities to manufacturers."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "The minimum buffer zone around a sanitary landfill site from habitation should be:",
    "options": [
      "500 meters",
      "100 meters",
      "1 kilometer",
      "200 meters"
    ],
    "difficulty": "medium",
    "explanation": "SWM Rules 2016 and CPCB guidelines require a minimum 500-meter buffer zone between sanitary landfill boundaries and the nearest habitation. This buffer reduces health impacts from landfill gas emissions, odor, vector breeding, and leachate contamination. The zone should have tree plantation as a green belt."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "HDPE liner used in sanitary landfills has a typical thickness of:",
    "options": [
      "1.5 mm to 2.0 mm",
      "0.5 mm to 0.8 mm",
      "5.0 mm to 8.0 mm",
      "0.1 mm to 0.3 mm"
    ],
    "difficulty": "hard",
    "explanation": "HDPE (High Density Polyethylene) liners used in sanitary landfill construction are typically 1.5-2.0 mm thick. They are used as part of composite liner systems (clay + HDPE) to prevent leachate migration to groundwater. Seams are welded using hot wedge or extrusion welding and integrity-tested before use."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Leachate from a landfill is best described as:",
    "options": [
      "Liquid that percolates through waste and carries dissolved and suspended contaminants",
      "Gas generated from anaerobic decomposition of waste",
      "Surface runoff collected around the landfill",
      "Treated effluent from waste processing"
    ],
    "difficulty": "medium",
    "explanation": "Leachate is liquid formed when water percolates through solid waste, dissolving organic and inorganic contaminants. It contains high BOD, COD, ammonia, heavy metals, and toxic compounds. Leachate collection systems (drainage layers + pipes) are essential in sanitary landfills to prevent groundwater pollution."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "E-Waste Rules 2016 in India are based on the principle of:",
    "options": [
      "Extended Producer Responsibility (EPR)",
      "Polluter Pays Principle",
      "Precautionary Principle",
      "Common but Differentiated Responsibility"
    ],
    "difficulty": "medium",
    "explanation": "E-Waste (Management) Rules 2016 are founded on EPR, making producers responsible for collection and channelizing e-waste to authorized dismantlers/recyclers. Producers must set up collection centers or take-back systems. The rules cover 21 categories of electrical and electronic equipment (Schedule I)."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "RDF (Refuse Derived Fuel) is produced by:",
    "options": [
      "Processing and pelletizing the combustible fraction of MSW after removing non-combustibles",
      "Direct incineration of mixed municipal solid waste",
      "Composting followed by drying",
      "Anaerobic digestion of organic waste"
    ],
    "difficulty": "medium",
    "explanation": "RDF is produced by mechanically processing MSW to remove non-combustibles (metals, glass, moisture), shredding, and pelletizing the combustible fraction (paper, plastic, textiles, wood). RDF has higher calorific value (3000-4000 kcal/kg) than raw MSW, making it suitable as fuel in cement kilns and power plants."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "The calorific value of Indian municipal solid waste is typically in the range of:",
    "options": [
      "800-1200 kcal/kg",
      "2500-3500 kcal/kg",
      "4000-5000 kcal/kg",
      "200-400 kcal/kg"
    ],
    "difficulty": "hard",
    "explanation": "Indian MSW has low calorific value (800-1200 kcal/kg) due to high moisture (40-60%) and organic content, compared to Western MSW (2500-3500 kcal/kg). This makes direct incineration challenging without supplementary fuel. Waste-to-energy viability requires minimum 1200 kcal/kg, necessitating pre-processing and drying."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Pyrolysis of solid waste involves:",
    "options": [
      "Thermal decomposition of waste in the absence of oxygen at 400-900°C",
      "Burning waste in excess oxygen at high temperatures",
      "Partial oxidation with limited oxygen supply",
      "Biological decomposition at elevated temperatures"
    ],
    "difficulty": "medium",
    "explanation": "Pyrolysis thermally decomposes organic material at 400-900°C without oxygen, producing syngas, bio-oil, and char. Unlike incineration (excess oxygen) or gasification (limited oxygen), pyrolysis operates in oxygen-free environment. It handles mixed waste including plastics and produces fewer air pollutants than incineration."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Construction and Demolition (C&D) waste management rules require that waste exceeding what quantity must be submitted with a waste management plan?",
    "options": [
      "20 tonnes or more",
      "5 tonnes or more",
      "50 tonnes or more",
      "100 tonnes or more"
    ],
    "difficulty": "hard",
    "explanation": "C&D Waste Management Rules 2016 mandate that any project generating 20 tonnes or more of C&D waste must prepare a waste management plan and get it approved by the local authority. The plan should include reuse/recycling targets. At least 80% of C&D waste should be recycled or reused."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Which of the following is NOT a component of a typical sanitary landfill?",
    "options": [
      "Activated sludge treatment unit",
      "Bottom liner system",
      "Leachate collection pipes",
      "Gas collection wells"
    ],
    "difficulty": "medium",
    "explanation": "A sanitary landfill comprises bottom liner (clay + HDPE), leachate collection system, gas collection wells, daily/intermediate/final cover, and stormwater drainage. Activated sludge is a wastewater treatment process, not a landfill component. Leachate may be treated in a separate treatment plant, but this is distinct from the landfill itself."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Biomethanation of organic waste produces primarily:",
    "options": [
      "Methane (CH₄) and carbon dioxide (CO₂)",
      "Hydrogen and nitrogen",
      "Ethanol and acetic acid",
      "Oxygen and water vapor"
    ],
    "difficulty": "medium",
    "explanation": "Biomethanation (anaerobic digestion) converts organic waste into biogas containing 55-65% methane (CH₄) and 35-45% CO₂, along with digestate. Methane has calorific value of ~8500 kcal/m³ and can be used for power generation or cooking. One tonne of organic waste yields approximately 100-150 m³ of biogas."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "The Plastic Waste Management Rules 2016 ban plastic carry bags below a thickness of:",
    "options": [
      "75 microns (amended to 75 from original 50)",
      "40 microns",
      "100 microns",
      "25 microns"
    ],
    "difficulty": "hard",
    "explanation": "PWM Rules were originally set at 50 microns and later amended to ban plastic carry bags below 75 microns thickness. The increased thickness ensures bags are reusable and recyclable. Single-use plastics (cups, plates, straws, stirrers) were banned from July 2022. This applies to manufacturers, sellers, and users."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "A Material Recovery Facility (MRF) is used for:",
    "options": [
      "Sorting, cleaning, and processing recyclable materials from mixed waste",
      "Biological treatment of organic waste",
      "Thermal treatment of hazardous waste",
      "Storage of treated waste before landfilling"
    ],
    "difficulty": "medium",
    "explanation": "MRFs mechanically and manually sort commingled recyclables into categories (paper, plastic types, metals, glass) for marketing to recyclers. Modern MRFs use screens, magnets, eddy current separators, and optical sorters. They are essential infrastructure for maximizing material recovery and reducing landfill dependence."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "TSDF in hazardous waste management stands for:",
    "options": [
      "Treatment, Storage, and Disposal Facility",
      "Technical Standard and Design Framework",
      "Testing, Sampling, and Documentation Framework",
      "Toxic Substance Disposal Facility"
    ],
    "difficulty": "medium",
    "explanation": "TSDF (Treatment, Storage, and Disposal Facility) is an integrated common facility for managing hazardous waste from multiple generators. It includes treatment units (physical, chemical, biological, thermal), secured storage areas, and engineered landfills with double liner systems. TSDFs require authorization under HW Rules."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "The 7R principle in waste management includes all EXCEPT:",
    "options": [
      "Relocate",
      "Refuse",
      "Reduce",
      "Repurpose"
    ],
    "difficulty": "hard",
    "explanation": "The 7R principle includes: Refuse, Reduce, Reuse, Repurpose, Repair, Recycle, and Rot (compost). 'Relocate' is not part of this framework. The 7Rs expand the traditional 3R concept to provide a more comprehensive approach to waste minimization, encouraging behavioral change before material recovery."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "In the SWM Rules 2016, waste is required to be segregated into:",
    "options": [
      "Wet (biodegradable), Dry (recyclable), and Domestic hazardous waste",
      "Only biodegradable and non-biodegradable",
      "Organic, inorganic, and medical waste",
      "Combustible and non-combustible waste"
    ],
    "difficulty": "medium",
    "explanation": "SWM Rules 2016 mandate three-way segregation at source: wet/biodegradable (kitchen waste, garden waste), dry/recyclable (paper, plastic, metal, glass), and domestic hazardous (batteries, CFL bulbs, expired medicines, paint). This enables appropriate processing - composting for wet, recycling for dry, safe disposal for hazardous."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Incineration of municipal solid waste requires a minimum calorific value of approximately:",
    "options": [
      "1200 kcal/kg for self-sustaining combustion",
      "800 kcal/kg for self-sustaining combustion",
      "2000 kcal/kg for self-sustaining combustion",
      "500 kcal/kg for self-sustaining combustion"
    ],
    "difficulty": "hard",
    "explanation": "Self-sustaining incineration without auxiliary fuel requires a minimum calorific value of approximately 1200 kcal/kg (some sources cite 1000 kcal/kg). Indian MSW (800-1200 kcal/kg) is often marginal, requiring pre-processing to remove moisture and non-combustibles. Flue gas treatment is mandatory to control dioxins and furans."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "The concept of 'Circular Economy' in waste management emphasizes:",
    "options": [
      "Keeping products and materials in use for as long as possible through continuous cycles",
      "Disposing waste in circular landfill designs",
      "Transporting waste in circular routes for efficiency",
      "Recycling only circular-shaped waste items"
    ],
    "difficulty": "medium",
    "explanation": "Circular economy aims to eliminate waste by designing products for durability, reuse, remanufacturing, and recycling. Unlike the linear 'take-make-dispose' model, it creates closed loops where waste becomes resource. Key strategies include product-as-service models, industrial symbiosis, and cradle-to-cradle design."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Door-to-door collection of municipal solid waste is preferred over community bin system because:",
    "options": [
      "It ensures better source segregation and reduces littering around bins",
      "It is cheaper than community bin system",
      "It requires fewer collection vehicles",
      "It does not need any worker involvement"
    ],
    "difficulty": "medium",
    "explanation": "Door-to-door collection improves source segregation rates (since collectors can reject improperly sorted waste), eliminates open waste bins that attract animals and vectors, reduces littering, and maintains cleaner public spaces. Though operationally costlier, it results in better waste quality for processing and recycling."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Landfill gas is typically composed of approximately:",
    "options": [
      "50-60% methane and 40-50% carbon dioxide",
      "90% nitrogen and 10% oxygen",
      "70% hydrogen and 30% carbon dioxide",
      "80% carbon monoxide and 20% methane"
    ],
    "difficulty": "hard",
    "explanation": "Mature landfill gas contains approximately 50-60% methane (CH₄) and 40-50% CO₂ with traces of H₂S, NH₃, and volatile organics. Methane generation begins 6-12 months after waste placement and can continue for 20-30 years. Landfill gas recovery can generate electricity (1 MW per ~1 million tonnes of waste)."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Plasma arc gasification of waste operates at temperatures of:",
    "options": [
      "3000-10,000°C",
      "500-800°C",
      "100-200°C",
      "1000-1500°C"
    ],
    "difficulty": "hard",
    "explanation": "Plasma arc gasification uses electrically generated plasma at 3000-10,000°C to convert waste into syngas (CO + H₂) and vitrified slag. The extreme temperature breaks down all organic molecules including hazardous compounds. The vitrified slag is non-leachable and can be used as construction aggregate."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "As per BMW Rules 2016, the maximum time for storage of biomedical waste at the generation site before treatment is:",
    "options": [
      "48 hours",
      "24 hours",
      "72 hours",
      "7 days"
    ],
    "difficulty": "hard",
    "explanation": "Biomedical Waste Management Rules 2016 mandate that untreated biomedical waste shall not be stored beyond 48 hours at the point of generation. If stored beyond this period, permission from the prescribed authority is required. This prevents infection spread and ensures timely treatment through incineration, autoclaving, or chemical treatment."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "The ISWM (Integrated Solid Waste Management) approach involves:",
    "options": [
      "Combining waste reduction, recycling, composting, incineration, and landfilling in an optimized hierarchy",
      "Using only landfilling for all waste disposal",
      "Processing all waste through a single technology",
      "Focusing exclusively on waste collection and transportation"
    ],
    "difficulty": "medium",
    "explanation": "ISWM integrates multiple waste management strategies - source reduction, recycling, composting, waste-to-energy, and landfilling - in a complementary hierarchy. It considers environmental, economic, and social factors to optimize the waste management system. No single technology can address all waste types effectively."
  },
  {
    "concept_id": "fac31b54",
    "question_text": "Under SWM Rules 2016, which authority is the nodal agency for enforcement?",
    "options": [
      "Urban Local Body (Municipal Corporation/Municipality/Nagar Panchayat)",
      "Central Pollution Control Board",
      "State Urban Development Department",
      "Ministry of Environment, Forest and Climate Change"
    ],
    "difficulty": "medium",
    "explanation": "SWM Rules 2016 designate Urban Local Bodies (ULBs) as the primary authority responsible for implementation and enforcement. ULBs must prepare SWM plans, ensure door-to-door collection, set up processing facilities, and manage landfills. CPCB provides technical standards, while state boards monitor compliance."
  }
]
