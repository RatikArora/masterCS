# Part 10: PERT/CPM + Bar Charts
questions_part10 = [
  {
    "concept_id": "253e1b1d",
    "question_text": "In CPM (Critical Path Method), the critical path is defined as:",
    "options": [
      "The longest path through the network determining the minimum project duration",
      "The shortest path through the network",
      "The path with the fewest activities",
      "Any path from start to finish"
    ],
    "difficulty": "medium",
    "explanation": "The critical path is the longest sequence of dependent activities from project start to finish, determining the minimum total project duration. Activities on the critical path have zero total float — any delay directly delays the project completion. There may be multiple critical paths in a project network."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "Total Float of an activity is calculated as:",
    "options": [
      "Late Start - Early Start (or Late Finish - Early Finish)",
      "Early Start - Late Start",
      "Duration × Safety Factor",
      "Early Finish + Late Start"
    ],
    "difficulty": "medium",
    "explanation": "Total Float = LS - ES = LF - EF. It represents the maximum time an activity can be delayed without delaying the project. Critical path activities have zero total float. Float is calculated through forward pass (ES, EF) and backward pass (LF, LS). Positive float indicates scheduling flexibility; negative float indicates a schedule overrun."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "In PERT, the expected time (te) is calculated using three estimates:",
    "options": [
      "te = (to + 4tm + tp) / 6",
      "te = (to + tm + tp) / 3",
      "te = (to + tp) / 2",
      "te = to × tm × tp"
    ],
    "difficulty": "medium",
    "explanation": "PERT uses three time estimates: optimistic (to), most likely (tm), and pessimistic (tp). The expected time te = (to + 4tm + tp)/6 approximates a Beta distribution. The variance σ² = [(tp - to)/6]². PERT accounts for uncertainty, unlike CPM which uses single deterministic durations for each activity."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "If an activity has optimistic time = 4 days, most likely = 7 days, and pessimistic = 16 days, the expected time is:",
    "options": [
      "8 days",
      "7 days",
      "9 days",
      "10 days"
    ],
    "difficulty": "medium",
    "explanation": "te = (to + 4tm + tp)/6 = (4 + 4×7 + 16)/6 = (4 + 28 + 16)/6 = 48/6 = 8 days. The variance σ² = [(tp - to)/6]² = [(16-4)/6]² = [12/6]² = 4. Standard deviation = 2 days. This expected time is used in the network for determining the critical path and project duration."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "Free Float of an activity is:",
    "options": [
      "The delay possible without affecting the Early Start of any successor activity",
      "The maximum delay without delaying the project",
      "Always equal to Total Float",
      "Always greater than Total Float"
    ],
    "difficulty": "medium",
    "explanation": "Free Float = ES(successor) - EF(current activity). It measures the delay an activity can have without affecting any immediate successor's earliest start. Free Float ≤ Total Float always. Activities on the critical path have zero free float. Free float indicates scheduling flexibility without impacting downstream activities."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "A project has three paths: A-B-C (18 days), A-D-E (22 days), A-F-G (20 days). The project duration is:",
    "options": [
      "22 days",
      "20 days",
      "18 days",
      "60 days"
    ],
    "difficulty": "medium",
    "explanation": "The critical path is A-D-E at 22 days — the longest path determines minimum project duration. Total float of A-B-C = 22-18 = 4 days; A-F-G = 22-20 = 2 days. Shortening the project requires reducing activities on the critical path. Reducing non-critical activities does not change project duration."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "A dummy activity in network diagrams:",
    "options": [
      "Has zero duration and is used to maintain logical dependencies between activities",
      "Is a critical activity with the longest duration",
      "Represents a physical task that takes time",
      "Can be removed without affecting the network"
    ],
    "difficulty": "medium",
    "explanation": "Dummy activities (shown as dashed arrows in ADM/AOA networks) have zero time and zero cost. They are used to: (1) show logical dependencies that cannot be represented by actual activities, (2) ensure unique identification of activities (no two activities share the same start and end events). Not needed in PDM (precedence diagram method)."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "The probability that a project will be completed within a specified time T is found using:",
    "options": [
      "Z = (T - Te) / σ, where Te is expected completion time and σ is standard deviation of the critical path",
      "Simple addition of all activity durations",
      "Division of project budget by time",
      "Random simulation only"
    ],
    "difficulty": "hard",
    "explanation": "PERT assumes project duration follows a normal distribution. Z = (T - Te)/σ where Te = sum of expected times on critical path, σ = √(sum of variances on critical path). Using normal distribution tables, Z gives the probability. For example, Z=0 means 50% probability, Z=1 means 84.13%, Z=2 means 97.72%."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "If the critical path has expected duration 30 days and standard deviation 3 days, the probability of completing the project in 33 days is approximately:",
    "options": [
      "84.13%",
      "50%",
      "97.72%",
      "68.27%"
    ],
    "difficulty": "hard",
    "explanation": "Z = (T - Te)/σ = (33 - 30)/3 = 1.0. From standard normal distribution table, P(Z ≤ 1.0) = 0.8413 = 84.13%. This means there is an 84.13% probability of completing the project within 33 days. For 100% confidence, one would need a much larger buffer (practically Z ≥ 3, i.e., 39 days)."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "Crashing in CPM refers to:",
    "options": [
      "Reducing the duration of critical activities by adding resources at additional cost",
      "Stopping the project midway",
      "Delaying non-critical activities",
      "Adding more activities to the network"
    ],
    "difficulty": "medium",
    "explanation": "Crashing reduces activity durations by applying additional resources (overtime labor, more equipment, premium materials) at extra cost. Only critical activities are crashed. The cost slope = (Crash Cost - Normal Cost)/(Normal Duration - Crash Duration). Activities with the lowest cost slope are crashed first for most economical time reduction."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "An activity has normal duration 10 days (cost ₹50,000) and crash duration 7 days (cost ₹80,000). The cost slope is:",
    "options": [
      "₹10,000 per day",
      "₹30,000 per day",
      "₹8,000 per day",
      "₹15,000 per day"
    ],
    "difficulty": "medium",
    "explanation": "Cost slope = (Crash Cost - Normal Cost)/(Normal Duration - Crash Duration) = (80,000 - 50,000)/(10 - 7) = 30,000/3 = ₹10,000 per day. This means each day of duration reduction costs ₹10,000 extra. Activities with lower cost slopes are crashed first when reducing project duration to minimize total cost increase."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "In Precedence Diagram Method (PDM), activities are represented on:",
    "options": [
      "Nodes (boxes), with arrows showing dependencies between them",
      "Arrows, with nodes representing events",
      "A bar chart with time on X-axis",
      "A circular diagram"
    ],
    "difficulty": "medium",
    "explanation": "PDM (Activity-on-Node) places activities in boxes/nodes and uses arrows to show dependencies. It supports all four dependency types: Finish-to-Start (most common), Start-to-Start, Finish-to-Finish, and Start-to-Finish. PDM eliminates the need for dummy activities required in ADM (Activity-on-Arrow) networks. Modern software uses PDM."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "The variance of the critical path duration in PERT is:",
    "options": [
      "Sum of variances of all activities on the critical path",
      "Variance of the longest activity only",
      "Average variance of all project activities",
      "Product of all activity variances"
    ],
    "difficulty": "hard",
    "explanation": "Project duration variance = Σ(σᵢ²) for all activities i on the critical path, assuming activities are independent. Since σᵢ = (tp - to)/6, variance = [(tp - to)/6]². The project standard deviation = √(project variance). This enables probability calculations for project completion time using normal distribution."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "Resource leveling in project scheduling aims to:",
    "options": [
      "Smooth resource demand over time to avoid peaks and valleys while respecting schedule constraints",
      "Add more resources to complete the project faster",
      "Remove resources from non-critical activities",
      "Use resources only on the critical path"
    ],
    "difficulty": "medium",
    "explanation": "Resource leveling adjusts activity schedules (within float limits) to create a more uniform resource demand profile. It reduces peak resource needs (hiring/firing costs) and improves efficiency. Activities with float are shifted to periods of lower demand. This may extend the project if float is insufficient, requiring tradeoff analysis."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "The Finish-to-Start (FS) relationship in PDM means:",
    "options": [
      "The successor activity cannot start until the predecessor finishes",
      "Both activities must finish at the same time",
      "Both activities must start at the same time",
      "The successor must finish before the predecessor starts"
    ],
    "difficulty": "medium",
    "explanation": "FS is the most common dependency: Activity B cannot start until Activity A finishes. With lag: FS+3 means B starts 3 days after A finishes. Other relationships: SS (start together), FF (finish together), SF (B finishes after A starts). Understanding these four relationship types is essential for realistic construction scheduling."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "A project network has activities with the following durations: A(3), B(5), C(2), D(4), E(6). Dependencies: A→C, A→D, B→D, C→E, D→E. The critical path is:",
    "options": [
      "B → D → E (15 days)",
      "A → C → E (11 days)",
      "A → D → E (13 days)",
      "B → D → E (15 days) and all other paths"
    ],
    "difficulty": "hard",
    "explanation": "Path analysis: A→C→E = 3+2+6 = 11 days. A→D→E = 3+4+6 = 13 days. B→D→E = 5+4+6 = 15 days. The critical path is B→D→E at 15 days (longest path). Total float of A→C→E = 15-11 = 4 days. Total float of A→D→E = 15-13 = 2 days. Project duration = 15 days."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "Interfering Float is defined as:",
    "options": [
      "Total Float minus Free Float, representing delay that affects successors but not project completion",
      "The same as Total Float",
      "Float of activities not on the critical path",
      "Negative float indicating schedule overrun"
    ],
    "difficulty": "hard",
    "explanation": "Interfering Float = Total Float - Free Float. If an activity has Total Float = 5 days and Free Float = 2 days, the Interfering Float = 3 days. Using more than 2 days of float will delay successor activities (interfering) even though it won't delay the project until all 5 days are consumed. Understanding this helps optimize scheduling."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "PERT is more suitable than CPM for:",
    "options": [
      "Research and development projects where activity durations are uncertain",
      "Routine construction projects with well-known durations",
      "Manufacturing processes with fixed cycle times",
      "Repetitive maintenance operations"
    ],
    "difficulty": "medium",
    "explanation": "PERT handles uncertainty through three-time estimates and probabilistic analysis, ideal for R&D, new product development, and unique projects. CPM uses single deterministic durations, suited for routine construction where durations are well-established from experience. In practice, hybrid approaches combining both are common."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "An event in an Activity-on-Arrow (AOA) network represents:",
    "options": [
      "A point in time marking the start or finish of one or more activities",
      "A task requiring time and resources",
      "A resource assignment",
      "A cost estimate"
    ],
    "difficulty": "medium",
    "explanation": "Events (nodes/circles) in AOA networks are instantaneous points in time — they consume no time or resources. They mark the beginning and/or completion of activities. Each event has an earliest event time (forward pass) and latest event time (backward pass). The difference gives event slack. Events are numbered for unique activity identification (i-j notation)."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "If an activity can start immediately without waiting for any predecessor, its Early Start (ES) is:",
    "options": [
      "Zero (or the project start time)",
      "Equal to its duration",
      "Equal to the project completion time",
      "Negative one"
    ],
    "difficulty": "medium",
    "explanation": "Activities with no predecessors have ES = 0 (project start). For other activities, ES = maximum EF of all predecessors (forward pass). Early Finish (EF) = ES + Duration. The forward pass calculates ES and EF for all activities, while the backward pass calculates LS and LF. Together they determine float for each activity."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "The main difference between PERT and CPM is:",
    "options": [
      "PERT is probabilistic (three time estimates) while CPM is deterministic (single time estimate)",
      "PERT is used for construction, CPM for research",
      "PERT uses nodes, CPM uses arrows",
      "There is no difference between PERT and CPM"
    ],
    "difficulty": "medium",
    "explanation": "PERT (Program Evaluation and Review Technique) uses three time estimates per activity and calculates probabilities of project completion. CPM (Critical Path Method) uses single deterministic durations and focuses on time-cost tradeoffs through crashing. Both use network diagrams and identify critical paths. Modern software often combines both approaches."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "In a network, if Activity X has ES=5, EF=12, LS=8, LF=15, the Total Float is:",
    "options": [
      "3 days",
      "7 days",
      "5 days",
      "0 days"
    ],
    "difficulty": "medium",
    "explanation": "Total Float = LS - ES = 8 - 5 = 3 days, or equivalently LF - EF = 15 - 12 = 3 days. This activity can be delayed by up to 3 days without affecting the project completion date. Its duration is EF - ES = 12 - 5 = 7 days. Activity X is not on the critical path since its float is positive."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "Earned Value Management (EVM) integrates:",
    "options": [
      "Scope, schedule, and cost performance measurement for project control",
      "Only cost tracking",
      "Only time tracking",
      "Resource allocation only"
    ],
    "difficulty": "hard",
    "explanation": "EVM measures project performance using: Planned Value (PV, budgeted cost of scheduled work), Earned Value (EV, budgeted cost of completed work), and Actual Cost (AC). Key metrics: CPI = EV/AC (cost performance), SPI = EV/PV (schedule performance). CPI<1 indicates over-budget; SPI<1 indicates behind schedule."
  },
  {
    "concept_id": "253e1b1d",
    "question_text": "Lead and Lag in project scheduling mean:",
    "options": [
      "Lead allows successor to start before predecessor finishes; Lag requires waiting after predecessor",
      "Lead means extra time, Lag means less time",
      "They are the same concept",
      "Lead applies to cost, Lag applies to time"
    ],
    "difficulty": "hard",
    "explanation": "Lead (negative lag) allows overlapping: FS-2 means successor starts 2 days before predecessor finishes (fast-tracking). Lag (positive) adds waiting: FS+3 means successor starts 3 days after predecessor finishes (e.g., concrete curing time). Both modify the basic dependency relationship to model real construction sequences accurately."
  },
  {
    "concept_id": "530d8def",
    "question_text": "A Gantt chart (bar chart) displays:",
    "options": [
      "Activities as horizontal bars plotted against a time scale, showing start, duration, and finish",
      "Only the cost of each activity",
      "Statistical frequency distribution",
      "Organizational hierarchy"
    ],
    "difficulty": "medium",
    "explanation": "Henry Gantt (1910s) developed the bar chart showing each activity as a horizontal bar whose length represents duration, positioned along a time axis. It provides an intuitive visual of the project schedule, making it easy to identify activity timing, overlaps, and progress. However, it does not clearly show dependencies between activities."
  },
  {
    "concept_id": "530d8def",
    "question_text": "The main limitation of a traditional bar chart compared to a network diagram is:",
    "options": [
      "It does not clearly show logical dependencies (relationships) between activities",
      "It cannot show activity durations",
      "It is always less accurate",
      "It requires computer software"
    ],
    "difficulty": "medium",
    "explanation": "Bar charts show timing but not logic — you can see when activities happen but not why. Network diagrams (CPM/PERT) explicitly show predecessor-successor relationships. A delay in one activity's impact on others is obvious in a network but not in a bar chart. Linked bar charts partially address this by adding dependency arrows."
  },
  {
    "concept_id": "530d8def",
    "question_text": "Milestones in project scheduling represent:",
    "options": [
      "Key events or achievements with zero duration marking significant project progress points",
      "The longest activities in the project",
      "Activities requiring the most resources",
      "Daily tasks assigned to workers"
    ],
    "difficulty": "medium",
    "explanation": "Milestones are zero-duration markers signifying important project events: project start, design completion, permit approval, structural completion, handover. Shown as diamonds (◆) on Gantt charts. They serve as progress checkpoints, client communication points, and contractual obligations. Typically 10-15 milestones for a medium construction project."
  },
  {
    "concept_id": "530d8def",
    "question_text": "A linked bar chart improves upon a standard bar chart by:",
    "options": [
      "Adding dependency arrows between activity bars to show logical relationships",
      "Using different colors for each activity",
      "Showing resource allocation",
      "Adding cost information to each bar"
    ],
    "difficulty": "medium",
    "explanation": "Linked (logic-linked) bar charts add arrows connecting related activity bars, showing predecessor-successor relationships. This combines the visual clarity of bar charts with the logical structure of network diagrams. Delays in predecessor activities visually cascade through linked successors, making schedule impact analysis more intuitive."
  },
  {
    "concept_id": "530d8def",
    "question_text": "Progress monitoring on a bar chart is typically shown by:",
    "options": [
      "Shading or filling the activity bar proportional to the percentage of work completed",
      "Changing the bar color",
      "Adding a separate chart below",
      "Writing notes above each bar"
    ],
    "difficulty": "medium",
    "explanation": "Progress is shown by filling/shading each bar proportionally: a 60% complete activity shows 60% of the bar filled. A vertical 'today' line indicates the data date. Bars filled to the left of today are behind schedule; bars filled beyond today are ahead. This provides immediate visual progress assessment for project monitoring."
  },
  {
    "concept_id": "530d8def",
    "question_text": "A time-chainage diagram (time-distance diagram) is most useful for:",
    "options": [
      "Linear projects like roads, pipelines, and railways where progress varies along the route length",
      "Building construction with vertical progression",
      "Software development projects",
      "Organizational restructuring projects"
    ],
    "difficulty": "medium",
    "explanation": "Time-chainage diagrams plot distance (chainage, y-axis) against time (x-axis), showing how work progresses along a linear route. Different activities (earthwork, paving, utilities) appear as bands. Their slope indicates production rate. Overlaps and interfaces between activities are clearly visible. Essential for highway, railway, and pipeline construction management."
  },
  {
    "concept_id": "530d8def",
    "question_text": "Resource histogram is a:",
    "options": [
      "Bar chart showing resource demand (workforce, equipment) against time periods",
      "Pie chart of project costs",
      "Network diagram with resources",
      "Table of resource prices"
    ],
    "difficulty": "medium",
    "explanation": "Resource histograms display resource requirements over time as vertical bars for each period. Peaks indicate high demand periods requiring overtime or additional hiring. Valleys indicate underutilization. Resource leveling adjusts the schedule to smooth the histogram, reducing peak demand and improving efficiency."
  },
  {
    "concept_id": "530d8def",
    "question_text": "The S-curve in project management represents:",
    "options": [
      "Cumulative progress or expenditure plotted against time, forming an S-shaped curve",
      "The critical path in a network",
      "Structural stability analysis",
      "Soil strength vs depth relationship"
    ],
    "difficulty": "medium",
    "explanation": "S-curves show cumulative quantities (cost, progress, manhours) vs time. The S-shape reflects: slow start (mobilization), rapid middle phase (peak production), and tapering end (finishing works). Comparing planned vs actual S-curves reveals schedule and cost performance. Early divergence warns of potential problems."
  },
  {
    "concept_id": "530d8def",
    "question_text": "In a bar chart, the term 'float' or 'slack' for non-critical activities is typically shown as:",
    "options": [
      "A thin line or lighter bar extending from the end of the activity bar to its latest finish date",
      "A separate bar below the activity",
      "A circular symbol",
      "Not shown at all in bar charts"
    ],
    "difficulty": "medium",
    "explanation": "Float is displayed as a dotted or thin line extending from the activity bar's end to the Latest Finish time. This visually shows available scheduling flexibility. The solid bar represents the planned duration from ES to EF, while the extension to LF shows the float. Activities with no extension (float = 0) are critical."
  },
  {
    "concept_id": "530d8def",
    "question_text": "Fast-tracking in project scheduling means:",
    "options": [
      "Performing sequential activities in parallel or with overlap to compress the schedule",
      "Adding more resources to critical activities",
      "Removing activities from the schedule",
      "Delaying the project start date"
    ],
    "difficulty": "medium",
    "explanation": "Fast-tracking overlaps activities that would normally be sequential — e.g., starting foundation work before design is 100% complete. It compresses the schedule without additional cost but increases risk (rework if early work changes). Differs from crashing (adding resources at extra cost). Both are schedule compression techniques."
  },
  {
    "concept_id": "530d8def",
    "question_text": "The line of balance (LOB) technique is used for:",
    "options": [
      "Scheduling repetitive projects like multi-story buildings or housing developments",
      "Single unique construction projects",
      "Research and development projects",
      "Software development projects"
    ],
    "difficulty": "hard",
    "explanation": "Line of Balance plots cumulative units completed for each activity against time, showing the required production rate (slope of the line). For repetitive projects (identical floors, houses), it ensures balanced resource flow between activities. Steeper slopes indicate faster production. Activities must be balanced to avoid interference and idle time."
  },
  {
    "concept_id": "530d8def",
    "question_text": "A construction schedule baseline is:",
    "options": [
      "The approved original schedule against which actual progress is measured and compared",
      "The fastest possible schedule",
      "A daily activity list",
      "A budget estimate"
    ],
    "difficulty": "medium",
    "explanation": "The baseline schedule is the approved reference plan established at project commencement. Actual progress is compared against the baseline to measure performance (ahead/behind schedule, over/under budget). Baselines should not be changed without formal approval. Multiple baselines may exist if the project is re-baselined due to major scope changes."
  },
  {
    "concept_id": "530d8def",
    "question_text": "Look-ahead schedules (rolling wave planning) typically cover:",
    "options": [
      "3-6 weeks ahead, providing detailed short-term scheduling for coordination",
      "The entire project duration",
      "Only the first day",
      "Only the final month"
    ],
    "difficulty": "medium",
    "explanation": "Look-ahead schedules detail activities for the next 3-6 weeks, derived from the master schedule. They enable weekly coordination meetings, identify upcoming constraints (permits, material deliveries, subcontractor availability), and provide actionable work plans. Updated weekly, they bridge the gap between the master schedule and daily work assignments."
  },
  {
    "concept_id": "530d8def",
    "question_text": "A Work Breakdown Structure (WBS) is:",
    "options": [
      "A hierarchical decomposition of the total project scope into manageable work packages",
      "A list of workers assigned to the project",
      "A structural engineering calculation",
      "A financial balance sheet"
    ],
    "difficulty": "medium",
    "explanation": "WBS decomposes the project into levels: project → phases → deliverables → work packages. Each work package is a manageable unit that can be scheduled, budgeted, and assigned. WBS is the foundation for scheduling (each work package becomes an activity), cost estimation, and progress tracking. 100% rule: WBS must capture the entire scope."
  },
  {
    "concept_id": "530d8def",
    "question_text": "A procurement schedule tracks:",
    "options": [
      "Material ordering, fabrication, delivery, and inspection timelines for construction materials",
      "Worker attendance and leave",
      "Weather forecasts for construction",
      "Design revision history"
    ],
    "difficulty": "medium",
    "explanation": "Procurement schedules track long-lead items: specification → vendor selection → purchase order → fabrication → shipping → delivery → inspection → installation. Steel, elevators, curtain wall, and mechanical equipment require 8-16 weeks lead time. Late procurement can delay the critical path. Procurement is linked to the construction schedule through milestone dates."
  },
  {
    "concept_id": "530d8def",
    "question_text": "In construction scheduling, the term 'lag' between two activities refers to:",
    "options": [
      "A mandatory waiting period between activities (e.g., concrete curing time)",
      "An activity that is behind schedule",
      "A mistake in the schedule",
      "The difference between two project budgets"
    ],
    "difficulty": "medium",
    "explanation": "Lag is a mandatory delay between activities, often representing physical processes: concrete curing (28 days lag before loading), paint drying (1 day lag before second coat), soil stabilization. Lag differs from float — lag is a technical requirement that cannot be reduced, while float is scheduling flexibility that can be used."
  },
  {
    "concept_id": "530d8def",
    "question_text": "The critical difference between a Master Schedule and a Detailed Schedule is:",
    "options": [
      "Master shows major phases and milestones; Detailed shows all individual activities with resources",
      "There is no difference",
      "Master is for small projects, Detailed for large",
      "Master uses bar charts, Detailed uses networks only"
    ],
    "difficulty": "medium",
    "explanation": "Master (summary) schedules show major project phases, key milestones, and critical path at a high level — suitable for management and client communication. Detailed (working) schedules decompose each phase into individual activities with durations, dependencies, resources, and costs — used by construction teams for daily planning and coordination."
  },
  {
    "concept_id": "530d8def",
    "question_text": "A construction schedule showing activities on a calendar format with daily/weekly view is called:",
    "options": [
      "A calendar schedule or production calendar",
      "A network diagram",
      "A cost estimate",
      "A quality control plan"
    ],
    "difficulty": "medium",
    "explanation": "Calendar schedules map activities onto calendar dates, accounting for non-working days (weekends, holidays, monsoon breaks). This transforms the abstract network/bar chart into actionable dates. Activities are placed considering working day calendars, resource availability, and seasonal constraints. Most scheduling software provides calendar view output."
  },
  {
    "concept_id": "530d8def",
    "question_text": "The purpose of schedule risk analysis is:",
    "options": [
      "To identify and quantify the probability and impact of schedule uncertainties on project completion",
      "To eliminate all risks from the project",
      "To extend the project deadline",
      "To assign blame for delays"
    ],
    "difficulty": "hard",
    "explanation": "Schedule risk analysis (often using Monte Carlo simulation) assigns probability distributions to activity durations, running thousands of simulations to determine: probability of completing by a target date, confidence levels for different completion dates, and activities most likely to cause delay. This quantitative approach provides realistic completion forecasts."
  },
  {
    "concept_id": "530d8def",
    "question_text": "Progress can be measured by all EXCEPT:",
    "options": [
      "Color of the building facade",
      "Physical percentage complete (quantity-based)",
      "Cost-based percentage (earned value)",
      "Milestones achieved"
    ],
    "difficulty": "medium",
    "explanation": "Progress measurement methods include: physical quantity (e.g., 500 of 1000 m³ concrete placed = 50%), cost-based (earned value vs planned), milestones (binary: achieved or not), and weighted milestones (distributed percentages at key stages). Building facade color has no relationship to construction progress measurement."
  },
  {
    "concept_id": "530d8def",
    "question_text": "A Time-Impact Analysis (TIA) is used to:",
    "options": [
      "Determine the schedule impact of a delay event by inserting it into the project network and recalculating",
      "Analyze the aesthetic impact of a building on its surroundings",
      "Study the environmental impact of construction",
      "Calculate the financial impact of inflation"
    ],
    "difficulty": "hard",
    "explanation": "TIA inserts the delay event (with its actual duration and dependencies) into the as-planned or updated schedule and recalculates the critical path. The difference between the pre-delay and post-delay project completion date quantifies the delay impact. TIA is the preferred method for delay analysis in construction claims and dispute resolution."
  },
  {
    "concept_id": "530d8def",
    "question_text": "The 4D scheduling technique adds which dimension to 3D building models?",
    "options": [
      "Time — linking schedule activities to 3D model components for visual construction simulation",
      "Cost as the fourth dimension",
      "Resource allocation",
      "Risk assessment"
    ],
    "difficulty": "hard",
    "explanation": "4D BIM links construction schedule activities to 3D model elements, creating time-lapse visual simulations of the construction sequence. This helps identify spatial conflicts, optimize sequencing, communicate plans to stakeholders, and verify constructability. The visual format is particularly effective for complex projects with multiple trades and phased occupation."
  },
  {
    "concept_id": "530d8def",
    "question_text": "The difference between a target schedule and an as-built schedule is:",
    "options": [
      "Target shows planned dates; as-built records actual dates when activities were performed",
      "They are identical documents",
      "Target is used only for payment",
      "As-built is prepared before construction"
    ],
    "difficulty": "medium",
    "explanation": "Target (planned/baseline) schedule shows intended start and finish dates. As-built schedule records actual dates activities started and finished during construction. Comparing them reveals: activities completed early or late, actual vs planned durations, and critical path changes. As-built records are essential for delay claims, disputes, and lessons learned."
  }
]
