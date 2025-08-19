# SCP-093 Themed Examples Planning

_Planning document for reworking VidGenLab examples around SCP-093 "Red Sea Object" themes_

## SCP-093 Core Elements

**The Object**: Ancient red stone disc that must remain on mirrors, acts as portal to alternate dimensions

**The Anomaly**: Transforms mirrors into gateways to dead/apocalyptic worlds when activated

**Key Themes**:
- Dimensional portal exploration through mirrors
- Sterile Foundation containment vs desolate otherworlds
- Ancient mystical object with technological monitoring
- Documentation of expeditions into hostile dimensions
- Color-changing properties indicating different destinations
- Massive otherworldly creatures glimpsed through portals

## Current Example Structure Analysis

### Character Files (examples/characters/)
- **Current**: cyber_witch.txt, digital_monk.txt, hooded_cybermancer.txt, neon_occultist.txt
- **Theme**: Cyberpunk-occult mystics performing tech rituals
- **Need**: Foundation personnel and expedition team archetypes

### Scene File (examples/basic_prompt.txt)
- **Current**: "hooded figure studies glowing sigils on server racks"  
- **Theme**: Cyberpunk occult tech manipulation
- **Need**: Portal activation, dimensional exploration, or containment scenarios

### Template Files
- **matrix_demo.yml**: Template variations system
- **storyboard_demo.json**: Multi-shot narrative structure  
- **chain_demo.yml**: Sequential shot progression
- **base_template.j2**: Jinja2 template for systematic variations

## Prompt Requirements Breakdown

### 1. Character Archetypes (4 files to replace current characters)

**Foundation Personnel Types**:
- Research scientist/project lead
- Security/containment specialist  
- Technical operator/monitor
- Field expedition member

**Visual Requirements**:
- Professional/clinical appearance
- Foundation uniform elements (lab coats, tactical gear, ID badges)
- Sterile institutional environments
- Serious, focused demeanor

### 2. Scene Prompts (replace basic_prompt.txt and others)

**Foundation Side Scenes**:
- Mirror containment chamber monitoring
- Portal activation procedures
- Pre-expedition briefings
- Technical analysis of the disc

**Otherworld Side Scenes**:
- Stepping through mirror portals
- Exploring desolate landscapes
- Documenting strange phenomena
- Encountering massive entities

**Visual Requirements**:
- Clinical Foundation aesthetics (white/gray/sterile)
- Mirror/portal visual effects
- Wasteland/apocalyptic otherworld environments  
- Documentary/surveillance camera feel

### 3. Template Adaptations

**Matrix Variables** (for systematic testing):
- Personnel types (researcher, security, technical, field)
- Scenarios (containment, activation, exploration, encounter)
- Otherworld environments (desert, urban ruins, toxic landscape, void)
- Disc colors (red, blue, green, violet - different dimensions)

**Storyboard Sequences**:
- Complete expedition: briefing → activation → exploration → return
- Containment breach: disc escape → pursuit → recapture
- Discovery: finding → initial testing → first portal → exploration

## Mood and Aesthetic Shifts

### From Cyberpunk-Occult to Foundation-Anomalous

**Visual Style Changes**:
- Neon/dark → Clinical/sterile lighting
- Mystical symbols → Scientific equipment  
- Server racks → Mirror chambers
- Hooded figures → Uniformed personnel
- Glowing energy → Portal distortions

**Atmospheric Changes**:
- Mysterious/mystical → Professional/clinical
- Underground/shadowy → Institutional/observed
- Magical ritual → Scientific procedure
- Tech-magic fusion → Science meets anomalous

## Implementation Plan

### Phase 1: Character Development
Replace current character files with Foundation personnel archetypes

### Phase 2: Scene Adaptation  
Rework basic scene prompt and create portal/otherworld variants

### Phase 3: Template Updates
Adapt matrix and storyboard examples for Foundation scenarios

### Phase 4: Testing & Refinement
Generate test images/videos and refine prompts based on results

## Considerations

**Avoid Explicit SCP References**: Use themes and mood without mentioning SCP Foundation directly

**Maintain Clinical Tone**: Professional, documented, institutional feel rather than mystical

**Balance Sides**: Both sterile Foundation environments and desolate otherworlds

**Video Generation Focus**: Prompts optimized for 8-second clips with clear action/movement

**Reference Image Pipeline**: Characters designed to work with scene variations through the character_pack workflow

---

# IMPLEMENTATION PROPOSAL

## Current Examples Structure (13 files)
```
examples/
├── basic_prompt.txt (1)
├── characters/ (4 character .txt files)  
├── references/ (4 style reference descriptions)
├── matrix_demo.yml (1)
├── chain_demo.yml (1) 
├── storyboard_demo.json (1)
└── base_template.j2 (1)
```

## Our SCP-093 Content (17+ items)
- **5 scene prompts** (basic + 4 atmospheric)
- **4 character archetypes** (multiple D-Class + Foundation personnel)
- **4 location-based style references**  
- **2 sequences** (tunnel + city observation)
- **1 matrix template** + **1 jinja template**

---

## PROPOSED STRUCTURE

### CORE EXAMPLES (Direct Replacements - 13 files)

**Essential Files for `examples/`:**

#### 1. Basic Scene Prompt
- **basic_prompt.txt** → **Red Sea Object Teaser** (most iconic SCP-093 moment)

#### 2. Character References (4 files in `characters/`)
- **d_class_20384.txt** → Blue Test male D-Class (tunnel explorer)
- **d_class_54493.txt** → Green Test female D-Class (farmhouse observer) 
- **security_officer.txt** → Professional reconnaissance/documentation
- **research_supervisor.txt** → Clinical authority managing experiments

#### 3. Style References (4 files in `references/`)
- **containment_facility.txt** → "Sterile containment chamber with mirror array, clinical white lighting, video surveillance equipment"
- **concrete_tunnel.txt** → "Underground concrete tunnel with failing ceiling lights, institutional corridors, metal debris"
- **abandoned_cityscape.txt** → "Modern downtown district with raised expressways, urban decay, dead city atmosphere"
- **green_farmland.txt** → "Rural desolation with green color tinge, rotted scarecrow, barren tilled fields where nothing grows"

#### 4. Templates & Sequences
- **matrix_demo.yml** → Updated with SCP-093 variables
- **chain_demo.yml** → City horror sequence (security observation)  
- **storyboard_demo.json** → Tunnel discovery sequence
- **base_template.j2** → Keep existing (universal)

### EXTRAS (Additional Content - 5+ items)

**Additional Content for `user_prompts/scp_093_extras/` or similar:**

#### Extra Scene Prompts
- **farmhouse_crawler.txt** → D-54493 farmhouse sighting
- **control_room_discovery.txt** → Cylindrical room with disc array
- **upper_city_view.txt** → Security observation of Unclean entities

#### Extra Templates  
- **tunnel_storyboard_extended.json** → More detailed tunnel sequence
- **matrix_extended.yml** → Full variable matrix with all locations/personnel

---

## RATIONALE FOR CORE VS EXTRAS

### CORE Selection Criteria:
1. **Most Iconic**: Red Sea Object activation (the central SCP-093 element)
2. **Essential Workflows**: Character pack + reference lab workflows represented
3. **Story Diversity**: Different test colors (Blue, Green), different personnel types
4. **Technical Coverage**: All major VidGenLab features demonstrated

### EXTRAS Reasoning:
- **Farmhouse/Control Room**: Atmospheric but not essential for learning the system
- **Extended Templates**: Valuable for advanced users but overwhelming for newcomers
- **Multiple D-Class**: Important for story accuracy but can be added later

### Benefits:
- **Core examples** remain manageable and teachable
- **Essential SCP-093 atmosphere** captured without overwhelming users
- **Advanced content** available for exploration
- **Maintains parity** with current file count

---

## Actual SCP-093 Story Moments (Selected)

### Single 8-Second Atmospheric Clips

**1. Red Sea Object Teaser (basic_prompt.txt replacement)**
```
Subject: red stone disc carved from cinnabar-like material, 7.62 cm diameter, with circular engravings and unknown symbols carved 0.5 cm deep, resting inert on mirror surface
Action: slow camera push-in on the carved disc, hand reaches to pick it up, disc begins changing color from red to blue upon contact
Style: clinical documentation with building tension, sterile lighting
Camera: extreme close-up push-in on disc details, ending as hand lifts color-changing disc
Ambience: sterile containment chamber with video surveillance equipment visible
Audio: subtle electronic monitoring beeps, silence broken by disc activation hum
```

**2. Tunnel Emergence (Blue Test - D-20384)** 
```
Subject: D-20384, 34-year-old male D-Class in orange jumpsuit, walking through concrete tunnel with partially functional ceiling light fixtures, past six side doors toward final blocked door
Action: emerges from dark concrete tunnel into over-bright room with filthy walls covered in melted plastic-like brown material
Style: institutional underground with stark lighting contrast, unsettling discovery
Camera: following shot from behind through concrete tunnel, revealing the harshly lit room with multiple doorways
Ambience: concrete enclosure with 3/4 functional ceiling lights, transition to over-illuminated chamber
Audio: footsteps echoing on concrete, electrical humming from failing lights, distant mechanical sounds
```

**3. Upper Floor City View - Security Observation (The Unclean)**
```
Subject: security personnel in tactical gear observing from upper floor window at modern downtown district with raised expressways encircling the city
Action: documents and reports as they realize the massive moving objects on the highways are 50-foot tall faceless torsos dragging themselves with elongated elastic arms, brown gel dripping as they crawl
Style: professional security documentation with horrific scale realization, clinical observation perspective
Camera: over-shoulder view through window of security officer, then closer on expressway showing massive torso creatures with no legs or faces
Ambience: abandoned modern cityscape with raised highway system, enormous torso creatures slowly crawling in circles
Audio: radio communications, distant bellowing sounds from creatures, wind through broken windows, professional reporting
```

**4. Farmhouse Crawler Sighting (Green Test - D-54493)**
```
Subject: D-54493, 23-year-old female D-Class in orange jumpsuit, viewing from large two-story farmhouse across green-tinged farmland with rotted scarecrow, toward two massive humanoid beings crawling 700m distant
Action: enormous featureless torso entities with arms that stretch and contract drag themselves across barren tilled field where nothing grows
Style: rural desolation with green color tinge, scale-defying horror entities, single subject documentation
Camera: wide shot from farmhouse emphasizing vast scale, 700m distance, and wrongness of entities
Ambience: abandoned farmland heavily tinged in green, barren tilled land, entities taking 10 minutes to cross field of vision
Audio: distant scraping sounds as arms stretch across ground, wind through empty farmland, unnatural silence, subject's breathing
```

**5. Cylindrical Control Room Discovery (Red Test - Individual D-Class)**
```
Subject: individual D-Class subject in orange jumpsuit enters large cylindrical room with rotating pillar 1.8m wide, walls lined with countless copies of SCP-093 discs
Action: discovers rotating pillar with random holes emitting white light beams connected to disc array, some wall sections missing their SCP-093 copies
Style: institutional cylindrical chamber with central rotating mechanism, clinical lighting from white beams
Camera: wide shot revealing full cylindrical scope with rotating pillar, then close-ups of missing disc positions on walls
Ambience: sterile cylindrical control environment with mechanical rotation sounds, white light beams periodically emerging
Audio: mechanical clicking and rotation of central pillar, electrical humming, single subject's breathing, realization of missing array elements
```

## Character Archetypes (Based on Story Roles)

### 1. D-Class Personnel (replaces cyber_witch.txt)
```
Portrait of a D-Class test subject in standard orange jumpsuit, middle-aged person with weathered features showing stress and resignation. They wear the basic institutional clothing with visible ID number. Their expression shows wariness mixed with forced compliance - someone who knows they're expendable. They hold basic exploration equipment - flashlight, radio, documentation materials. The background is a sterile preparation area with security monitoring. Harsh institutional lighting emphasizes their vulnerable position in the system.
```

### 2. Research Supervisor (replaces digital_monk.txt)  
```
Portrait of a research project supervisor in professional attire - white lab coat over business clothes, laminated security badge visible. They have an authoritative but clinical demeanor, holding a tablet with expedition data and monitoring information. Their expression is focused and detached - professional distance from human test subjects. The background shows a control room with mirror monitoring stations and data screens. Professional lighting emphasizes their position of clinical authority over the experiments.
```

### 3. Security Officer (replaces hooded_cybermancer.txt)
```
Portrait of a containment security officer in tactical gear with radio equipment and monitoring devices. They wear professional security uniform with utility equipment for managing D-Class personnel and containment protocols. Their stance is alert and ready, positioned to respond to containment issues. Their expression shows professional vigilance mixed with unease about the anomalous nature of their assignment. The background is a containment corridor with reinforced security measures.
```

### 4. Site Technician (replaces neon_occultist.txt)
```
Portrait of a site technical specialist responsible for mirror array maintenance and monitoring equipment. They wear practical work clothes under a lab coat, with various technical tools and diagnostic equipment. Their expression shows technical competence mixed with nervous awareness of what they're monitoring. They're positioned near control panels and monitoring stations. The background features the technical infrastructure supporting the mirror containment and portal monitoring systems.
```

## Template Adaptations

### Matrix Variables (matrix_demo.yml replacement)
```yaml
matrix:
  personnel:
    - D-Class test subject with exploration equipment
    - research supervisor monitoring expedition data
    - security officer managing containment protocols
    - site technician maintaining mirror array systems
  location:
    - sterile mirror containment chamber
    - unlit tunnel leading to lit room with doors
    - upper floor overlooking dead city with moving torsos
    - farmhouse with view of massive crawler entity
    - control room with multiple disc array positions
  scenario:
    - red sea object activation sequence
    - D-Class tunnel emergence into lit chamber
    - city observation revealing torso movement horror
    - massive crawler entity sighting from farmhouse
    - control room discovery of missing disc positions
  disc_state:
    - dormant red carved stone on mirror surface
    - color-changing when touched by test subject
    - multiple discs in control room array
    - empty positions where discs should be
  atmosphere:
    - clinical institutional documentation style
    - building tension and dread discovery
    - scale-defying horror realization  
    - institutional control with missing elements
    - rural desolation with impossible entities
```

### Storyboard Sequence - Tunnel Discovery (storyboard_demo.json replacement)
```json
{
  "title": "Blue Test - Tunnel to Lit Room Discovery",
  "shots": [
    {
      "id": "tunnel_01",
      "prompt": "Subject: D-Class personnel walking through concrete tunnel with partially functional ceiling light fixtures, past multiple side doors\nAction: moves cautiously forward through concrete enclosure, 3/4 of ceiling lights working, six side doors visible along walls\nStyle: institutional underground with failing electrical systems, building tension\nCamera: following shot from behind through concrete tunnel, flickering ceiling lights casting uneven illumination\nAmbience: concrete tunnel enclosure with metal shelving debris, distant bright light ahead\nAudio: echoing footsteps on concrete, electrical humming from failing ceiling fixtures, distant mechanical sounds",
      "negative": "outdoor scenes, natural lighting, clean environments"
    },
    {
      "id": "emergence_02", 
      "prompt": "Subject: D-Class approaches final door blocked by rusted metal shelving debris, bright over-lit room beyond\nAction: hesitates at threshold of harshly illuminated chamber with filthy walls\nStyle: stark lighting contrast from concrete tunnel to over-bright institutional space\nCamera: medium shot showing subject silhouetted against brilliant room lighting, metal debris visible\nAmbience: dark concrete tunnel opening to over-illuminated chamber with melted plastic-like brown material on walls\nAudio: footsteps slowing on concrete, mechanical hum growing louder, metal debris shifting",
      "carry_last_frame": true
    },
    {
      "id": "revelation_03",
      "prompt": "Subject: D-Class emerges into bare room with filthy walls covered in melted plastic-like brown material, makeshift cot and wooden crates visible\nAction: turns to survey the bizarre chamber with crumbling newspaper clippings, aged blankets, dried water bottles\nStyle: clinical institutional over-lighting contrasting with filthy decaying contents\nCamera: wide shot revealing full scope of lit room with makeshift living arrangements and wall deterioration\nAmbience: over-bright institutional space with makeshift cot, wooden crates with old cereal boxes, closed book\nAudio: mechanical systems humming, subject's breathing, realization of human habitation in wrong place",
      "carry_last_frame": true
    }
  ]
}
```

### Chain Demo - City Horror Sequence (chain_demo.yml replacement)
```yaml
# Each shot uses the last frame of the previous as a starting point
prompts:
  - |
    Subject: security personnel in tactical gear exploring upper floors of abandoned building in modern downtown district
    Action: moves through empty rooms with dust-covered furniture toward windows for reconnaissance of city below
    Style: professional security documentation, abandoned modern cityscape surveillance
    Camera: following shot through empty interior spaces with 1950s-style furniture, tactical movement
    Ambience: abandoned building interior with raised expressway system visible through windows
    Audio: radio equipment static, footsteps on debris, wind through broken windows, distant urban sounds
  - |
    Subject: security officer approaches window and sets up observation equipment to survey raised expressways encircling the city
    Action: establishes surveillance position, notices large moving objects on elevated highway system
    Style: professional reconnaissance perspective, dead city with raised transportation infrastructure
    Camera: over-shoulder view through window of security officer with equipment, focusing on cityscape with expressways
    Ambience: modern downtown district with raised expressway system, something massive moving on highways
    Audio: radio communications, equipment adjustment, wind through broken windows, distant mechanical sounds from city
  - |
    Subject: security officer realizes through binoculars that moving objects are 50-foot tall faceless torsos
    Action: professional documentation and reporting as the Unclean entities drag themselves with elongated arms, brown gel dripping
    Style: clinical security documentation showing scale of massive torso creatures without legs or faces
    Camera: alternating between security officer's reaction and closer view of raised expressway showing enormous torso entities crawling in circles
    Ambience: abandoned cityscape with massive faceless humanoid torsos slowly dragging themselves on highways
    Audio: urgent radio reporting, distant bellowing sounds from creatures, scraping of elongated arms on pavement
```