# Character Pack - Character-Focused Testing

**Purpose**: Test the same scene with multiple character reference images to compare results.

## Quick Start

**Generate character references first:**
```bash
# Generate all character references (from text prompts)
uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch
uv run imagen_lab generate "$(cat examples/characters/digital_monk.txt)" --output examples/characters/generated/digital_monk --name digital_monk  
uv run imagen_lab generate "$(cat examples/characters/hooded_cybermancer.txt)" --output examples/characters/generated/hooded_cybermancer --name hooded_cybermancer
uv run imagen_lab generate "$(cat examples/characters/neon_occultist.txt)" --output examples/characters/generated/neon_occultist --name neon_occultist
```

**Then create videos:**
```bash
# Use generated character references
uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
```

## Usage

```bash
uv run -m veo_lab.character_pack --scene "Scene description" --ref-dir path/to/character/images

# Or use scene from file  
uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
```

## Character Reference Setup

The modern approach uses generated character references from text prompts:

```
examples/characters/
├── cyber_witch.txt              # Text prompts for generation
├── digital_monk.txt
├── hooded_cybermancer.txt  
├── neon_occultist.txt
└── generated/                   # Generated references
    ├── cyber_witch/
    │   ├── cyber_witch.jpg
    │   ├── metadata.json
    │   └── prompt.txt
    ├── digital_monk/
    │   └── ...
    └── ...
```

**Benefits of generated references:**
- **Reproducible**: Anyone can regenerate from text prompts
- **Version controlled**: Text prompts instead of binary files
- **Customizable**: Easy to modify and iterate on character designs
- **Consistent**: Generated with same models and settings

## Input Format

**Scene**: Standard prompt text (same as `simple` script)
**Reference Directory**: Folder containing character images (JPG/PNG)

## Examples

**Fantasy character test**:
```bash
# Scene description
echo "Subject: heroic character stands atop mountain peak
Action: raises weapon toward stormy sky
Style: epic fantasy, dramatic clouds
Camera: low angle, heroic framing
Ambience: wind-swept, lightning flashes
Audio: thunder, cape flapping" > fantasy_scene.txt

# Run with character references
uv run -m veo_lab.character_pack --scene "$(cat fantasy_scene.txt)" --ref-dir fantasy_characters/
```

**Commercial character test**:
```bash
# Test same commercial scene with different models
uv run -m veo_lab.character_pack --scene "Subject: confident person walks through modern office
Action: turns to camera with smile
Style: bright commercial lighting
Camera: tracking shot, professional" --ref-dir model_headshots/
```

## Output

- One video per reference image in the directory
- Videos named: `char_{image_name}_{prompt_snippet}_{model}.mp4`
- All organized in single session directory
- Metadata tracks which reference image was used for each video

## Use Cases

- **Character casting**: See how different character types work in same scene
- **Consistency testing**: Check if character references work reliably
- **Style matching**: Find characters that match your visual style
- **Reference validation**: Test if your reference images are effective

## Complete Workflow Example

```bash
# 1. Create custom character prompts
echo "Portrait of a medieval knight in shining armor, dramatic lighting, heroic pose" > my_characters/knight.txt
echo "Close-up of a wise wizard with long beard, mystical robes, glowing eyes" > my_characters/wizard.txt

# 2. Generate character references  
uv run imagen_lab generate "$(cat my_characters/knight.txt)" --output my_characters/generated/knight --name knight
uv run imagen_lab generate "$(cat my_characters/wizard.txt)" --output my_characters/generated/wizard --name wizard

# 3. Create scene prompt
echo "Subject: character stands atop mountain peak
Action: raises weapon toward stormy sky  
Style: epic fantasy, dramatic clouds
Camera: low angle, heroic framing" > fantasy_scene.txt

# 4. Generate videos with each character
uv run -m veo_lab.character_pack --scene "$(cat fantasy_scene.txt)" --ref-dir my_characters/generated/
```

## Tips

**Character Generation**:
- Use consistent lighting descriptions across character sets
- Include pose and expression details that match your scenes
- Specify background type (gradient, solid color) for clean references
- Consider the visual style compatibility with your video scenes

**Reference Organization**:
- Keep character prompts in version control as `.txt` files
- Use descriptive names for character types
- Generate references on-demand rather than storing images
- Test character references work well before batch generation

**Scene Compatibility**:
- Ensure character lighting matches scene lighting
- Consider pose compatibility (standing characters for action scenes)
- Match visual style (realistic characters for realistic scenes)
- Test with 2-3 references before generating larger batches