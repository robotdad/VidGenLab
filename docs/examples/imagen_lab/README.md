# Imagen Lab - Image Generation and Analysis

**Purpose**: Generate images from text prompts and analyze existing images to extract descriptive prompts using Google's Imagen 3 API.

## Commands

### `imagen_lab generate` - Generate Images

Generate images from text descriptions:

```bash
# Test with dry-run first (no API costs)
uv run imagen_lab generate "Portrait of a cyberpunk character with neon lighting" --dry

# Basic image generation
uv run imagen_lab generate "Portrait of a cyberpunk character with neon lighting"

# With custom model
uv run imagen_lab generate "Futuristic cityscape at night" --model imagen-3.0-generate-001

# Custom output location  
uv run imagen_lab generate "Digital art landscape" --output my_images/landscape --name custom_landscape
```

### `imagen_lab analyze` - Extract Prompts from Images

Analyze existing images to generate descriptive prompts:

```bash
# Analyze any image file
uv run imagen_lab analyze path/to/your/image.jpg

# With custom vision model
uv run imagen_lab analyze image.png --model gemini-2.0-flash-exp

# Custom output location
uv run imagen_lab analyze photo.jpg --output analysis/photo_analysis
```

### Dry Run Mode

Test commands and validate configuration without consuming API quota:

```bash
# Test generation setup
uv run imagen_lab generate "cyberpunk character portrait" --dry

# Test with custom model and output
uv run imagen_lab generate "landscape scene" --model imagen-3.0-fast-generate-001 --output test/location --name test_image --dry

# Test with environment variable
IMAGEN_MODEL=custom-model uv run imagen_lab generate "test prompt" --dry
```

Dry-run shows exactly what would be generated without making API calls - perfect for:
- Validating prompts and file paths
- Testing environment variable configuration  
- Debugging CLI arguments
- Scripting and automation workflows

## Input Formats

**Text Prompts**: Descriptive text for image generation
- Style descriptions: "cyberpunk", "minimalist", "photorealistic"  
- Composition: "close-up portrait", "wide landscape", "medium shot"
- Lighting: "dramatic lighting", "soft natural light", "neon highlights"
- Mood: "mysterious", "serene", "intense"

**Image Files**: JPG, PNG, or other common image formats for analysis

## Examples

### Character Reference Generation

Generate consistent character references for video generation:

```bash
# Generate character from detailed prompt
uv run imagen_lab generate "Close-up portrait of a stoic, handsome Black man with short hair and stubble. He wears dark, futuristic sunglasses. He is wearing a black leather hooded jacket with subtle geometric patterns and neon blue highlights along the seams. Cyberpunk style, dramatic cool and warm lighting, smooth gradient background. Mood: intense, futuristic." --output examples/characters/generated/neon_occultist --name neon_occultist
```

### Style Transfer Workflow

Extract style from existing images and create variations:

```bash
# 1. Analyze an existing image to understand its style
uv run imagen_lab analyze reference_artwork.jpg

# 2. Use the generated prompt to create variations
# (Copy the generated prompt from the analysis output)
uv run imagen_lab generate "Studio portrait of a young woman with the same dramatic lighting and composition as the reference, but with different clothing and pose"
```

### Batch Character Generation

Create multiple character references from text prompts:

```bash
# Generate all character types for a project
for character in cyber_witch digital_monk hooded_cybermancer neon_occultist; do
    uv run imagen_lab generate "$(cat examples/characters/${character}.txt)" --output examples/characters/generated/${character} --name ${character}
done
```

## Output Structure

Each generation creates a timestamped directory:

```
out/2025-01-18/153045_imagen_portrait_cyberpunk_character/
├── portrait_cyberpunk_character.jpg  # Generated image
├── metadata.json                     # Generation metadata  
└── prompt.txt                        # Original text prompt
```

**Custom output** (using `--output` flag):
```
examples/characters/generated/cyber_witch/
├── cyber_witch.jpg       # Generated image
├── metadata.json         # Generation metadata
└── prompt.txt           # Original text prompt
```

## Integration with Video Generation

Use generated images as references for video generation:

```bash
# 1. Generate character reference
uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch

# 2. Use in video generation
uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/

# 3. Or single video with reference
uv run -m veo_lab.simple --prompt "Witch casting spells" --ref-image examples/characters/generated/cyber_witch/cyber_witch.jpg
```

## Use Cases

**Character Development**:
- Generate consistent character references for video projects
- Create character variations and design iterations
- Build character libraries for different projects

**Style Exploration**:
- Analyze reference artwork to understand visual styles
- Generate style variations and interpretations
- Create mood boards and visual references

**Reference Creation**:
- Replace binary image files with reproducible text prompts
- Generate references on-demand for video generation
- Create consistent visual assets across projects

**Creative Workflow**:
- Text → Image → Video complete pipeline
- Rapid prototyping of visual concepts
- Style transfer and variation generation

## Tips

**For Better Generation Results**:
- Be specific with style descriptions ("cyberpunk", "photorealistic", etc.)
- Include composition details ("close-up portrait", "medium shot")  
- Specify lighting ("dramatic", "soft", "neon highlights")
- Add mood descriptors ("mysterious", "serene", "intense")

**For Character References**:
- Use consistent lighting descriptions across character sets
- Include pose and expression details
- Specify background type ("gradient", "textured", "solid")
- Consider compatibility with your video scenes

**For Analysis**:
- Use clear, well-lit source images for better prompt extraction
- Analyze images similar to your target style
- Use generated prompts as starting points for variations

## Models

**Image Generation**: `imagen-3.0-generate-001` (default)
**Image Analysis**: `gemini-2.0-flash-exp` (default)

Check current models:
```bash
# List available models (through veo_lab for now)
uv run -m veo_lab.simple --list-models
```