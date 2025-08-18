# Ref Image Lab - Reference Image Experiments

**Purpose**: Test multiple reference images with the same scene to compare their influence on generation.

## Usage

```bash
uv run -m veo_lab.ref_image_lab --ref-dir path/to/reference/images --scene path/to/scene.txt

# Or inline scene
uv run -m veo_lab.ref_image_lab --ref-dir references/ --scene "Your scene description here"
```

## Setup Required

Create directory with diverse reference images:

```
references/
├── moody_lighting.jpg     # Dark, atmospheric
├── bright_daylight.jpg    # Sunny, high-key
├── neon_cyberpunk.jpg     # Colorful, futuristic  
├── vintage_film.jpg       # Grainy, retro
└── minimalist_white.jpg   # Clean, simple
```

## Input Format

**Scene File**: Standard prompt text
**Reference Directory**: Images to test as starting references

## Examples

**Lighting study**:
```bash
# Create scene focused on lighting
echo "Subject: elegant dancer in flowing dress
Action: graceful spin with fabric flowing
Style: high fashion photography
Camera: medium shot, slight slow motion
Ambience: studio setting, dramatic mood
Audio: classical music, fabric rustle" > dancer_scene.txt

# Test with different lighting references
uv run -m veo_lab.ref_image_lab --ref-dir lighting_references/ --scene dancer_scene.txt
```

**Environment study**:
```bash
# Test how different environments influence same action
echo "Subject: person walks confidently forward
Action: determined stride toward camera
Style: cinematic, hero shot
Camera: low angle tracking
Ambience: epic, inspiring
Audio: rising orchestral score" > hero_walk.txt

# Test with various environment references
uv run -m veo_lab.ref_image_lab --ref-dir environments/ --scene hero_walk.txt  
```

## Output

- One video per reference image
- Videos named: `ref_{image_name}_{prompt_snippet}_{model}.mp4`
- All videos use same scene text but different reference images
- Metadata shows which reference influenced each video

## Use Cases

- **Reference testing**: See how different images affect your scene
- **Style exploration**: Find references that give desired aesthetic
- **Consistency checking**: Test if references work reliably with your prompts
- **Visual development**: Explore different moods/styles for same concept
- **Client options**: Show how different reference styles affect output

## Reference Image Tips

**Good References**:
- Clear composition and lighting
- Similar subject matter or mood to your scene
- High quality, not blurry or low-res
- Distinctive visual characteristics

**Reference Categories to Test**:
- **Lighting**: golden hour, studio, natural, dramatic
- **Color palettes**: warm, cool, monochrome, saturated
- **Composition**: wide shots, close-ups, angles
- **Styles**: vintage, modern, artistic, commercial
- **Moods**: energetic, calm, mysterious, upbeat

## Analysis

After generation, compare outputs to understand:
- Which references work best with your scene types
- How strongly references influence the final result  
- Whether certain reference styles are more reliable
- Which combinations create unexpected but good results