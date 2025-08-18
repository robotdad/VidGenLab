# VidGenLab Examples

Quick-start examples for both image generation and video generation.

## Getting Started

### Image Generation First

1. **Generate your first image**:

   ```bash
   uv run imagen_lab generate "Portrait of a cyberpunk character with neon lighting, dramatic atmosphere"
   ```

2. **Test with dry-run first** (no API costs):

   ```bash
   uv run imagen_lab generate "Portrait of a cyberpunk character with neon lighting, dramatic atmosphere" --dry
   ```

3. **Create character references from prompts**:

   ```bash
   uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch
   ```

### Video Generation

1. **Try inline prompts** (simplest):

   ```bash
   uv run -m veo_lab.simple --prompt "Cloaked figure traces glowing symbols, cyberpunk occult atmosphere"
   ```

2. **Use prompt files** for longer/reusable prompts:

   ```bash
   uv run -m veo_lab.simple --prompt-file examples/basic_prompt.txt
   ```

3. **Complete pipeline** (image → video):

   ```bash
   # Generate reference, then create video using it
   uv run imagen_lab generate "$(cat examples/characters/digital_monk.txt)" --output examples/characters/generated/digital_monk --name digital_monk
   uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
   ```

> **Tip**: Instead of `export GEMINI_API_KEY=...`, you can copy `.env.example` to `.env` and set your API key there.

4. **Explore advanced features** - See [docs/examples/](../docs/examples/) for comprehensive guides

## Image Generation Examples

### Basic Image Generation

```bash
# Simple generation
uv run imagen_lab generate "Digital art of a futuristic cityscape at night, neon lights, cyberpunk style"

# With custom output location
uv run imagen_lab generate "Portrait of a wise wizard" --output my_images/wizard --name wizard_portrait

# Different models (check available models with veo_lab for now)
uv run imagen_lab generate "Landscape painting" --model imagen-3.0-generate-001
```

### Image Analysis

```bash
# Analyze any image to get a descriptive prompt
uv run imagen_lab analyze path/to/your/image.jpg

# Use generated prompt to create variations
uv run imagen_lab generate "$(cat out/YYYY-MM-DD/HHMMSS_analyze_*/prompt.txt)"
```

#### Character Reference Workflow

Generate character references from text prompts, then test them with the same scene:

```bash
# First, test with dry-run to validate prompts
uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch --dry

# Generate all provided character references
uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch
uv run imagen_lab generate "$(cat examples/characters/digital_monk.txt)" --output examples/characters/generated/digital_monk --name digital_monk
uv run imagen_lab generate "$(cat examples/characters/hooded_cybermancer.txt)" --output examples/characters/generated/hooded_cybermancer --name hooded_cybermancer
uv run imagen_lab generate "$(cat examples/characters/neon_occultist.txt)" --output examples/characters/generated/neon_occultist --name neon_occultist

# Then use them in video generation
uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
```

### Style Reference Workflow

Generate style references for different atmospheric approaches, then test them with the same scene:

```bash
# Generate style reference images
uv run imagen_lab generate "Bright neon-lit cyberpunk server room with glowing data streams" --output examples/references/generated/neon_server --name neon_server_room
uv run imagen_lab generate "Dark occult ritual space with candles and mystical symbols" --output examples/references/generated/occult_space --name occult_ritual_space
uv run imagen_lab generate "Digital corruption glitch art aesthetic, distorted reality" --output examples/references/generated/digital_glitch --name digital_corruption
uv run imagen_lab generate "Ethereal otherworldly glow, soft mystical lighting, dreamy ambiance" --output examples/references/generated/ethereal_light --name ethereal_glow

# Test with generated style references
uv run -m veo_lab.ref_image_lab --ref-dir examples/references/generated/ --scene examples/basic_prompt.txt
```

## Video Generation Examples

### Basic Usage

```bash
# Inline prompt (quickest way to test)
uv run -m veo_lab.simple --prompt "Subject: cyber-witch casting holographic spells, Style: neon-lit gothic atmosphere, Action: mystical energy flows"

# From file (better for complex prompts)
uv run -m veo_lab.simple --prompt-file examples/basic_prompt.txt

# With negative prompt
uv run -m veo_lab.simple -f examples/basic_prompt.txt -n "bright lighting, cheerful atmosphere"

# Image-to-video (requires reference image)
uv run -m veo_lab.simple -f examples/basic_prompt.txt -i path/to/reference.jpg

# Specify model (default is veo-2.0-generate-001)
uv run -m veo_lab.simple -f examples/basic_prompt.txt --model veo-3.0-generate-preview
uv run -m veo_lab.simple -f examples/basic_prompt.txt --model veo-3.0-fast-generate-preview

# List available models
uv run -m veo_lab.simple --list-models
```

### Video Chain (`shot_chain`)

```bash
uv run -m veo_lab.shot_chain --file examples/chain_demo.yml
```

### Storyboard (`storyboard`)

```bash
# Generate shots
uv run -m veo_lab.storyboard --storyboard examples/storyboard_demo.json

# Generate and concatenate into final video
uv run -m veo_lab.storyboard --storyboard examples/storyboard_demo.json --concat final_seance.mp4
```

### Template Matrix (`prompt_matrix`)

```bash
uv run -m veo_lab.prompt_matrix --template examples/base_template.j2 --config examples/matrix_demo.yml
```

## Model Selection

All scripts support the `--model` option to choose between Veo versions:

- **`veo-2.0-generate-001`** (default) - Reliable, good rate limits
- **`veo-3.0-generate-preview`** - Best quality, very limited rate limits
- **`veo-3.0-fast-generate-preview`** - Faster Veo 3, still limited rate limits

You can also set a default in `.env`: `VEO_MODEL=veo-2.0-generate-001`

**Note**: Veo 3 has much lower rate limits. See [Rate Limits Documentation](https://ai.google.dev/gemini-api/docs/rate-limits).

## File Organization

Both images and videos are organized in `out/` with consistent naming:

```
out/
├── 2025-01-15/
│   ├── 143022_imagen_cyberpunk_character/    # Image generation
│   │   ├── cyberpunk_character.jpg
│   │   ├── metadata.json
│   │   └── prompt.txt
│   └── 143045_simple_sailboat_in_fog/        # Video generation
│       ├── sailboat_in_fog_veo3.mp4
│       ├── metadata.json
│       └── prompt.txt
└── latest -> 2025-01-15/143045_simple_sailboat_in_fog/
```

**Custom output locations** (using `--output` flag):
```
examples/characters/generated/
├── cyber_witch/
│   ├── cyber_witch.jpg
│   ├── metadata.json
│   └── prompt.txt
└── digital_monk/
    ├── digital_monk.jpg
    ├── metadata.json
    └── prompt.txt
```

## Next Steps

- **Learn more**: Browse [docs/examples/](../docs/examples/) for detailed guides on each script
- **Validate setup**: Follow the validation guide in [ai_working/VALIDATION_GUIDE.md](../ai_working/VALIDATION_GUIDE.md)
- **Create experiments**: Start your own prompts in `user_prompts/`
