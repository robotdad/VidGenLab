# VidGenLab Examples

Quick-start examples for both image generation and video generation.

## Getting Started

### Image Generation First

1. **Generate your first image**:

   ```bash
   uv run imagen_lab generate "Professional headshot of D-Class personnel in orange jumpsuit, institutional lighting, clinical documentation style"
   ```

2. **Test with dry-run first** (no API costs):

   ```bash
   uv run imagen_lab generate "Professional headshot of D-Class personnel in orange jumpsuit, institutional lighting, clinical documentation style" --dry
   ```

3. **Create character references from prompts**:

   ```bash
   uv run imagen_lab generate "$(cat examples/characters/d_class_20384.txt)" --output examples/characters/generated/d_class_20384 --name d_class_20384
   ```

### Video Generation

1. **Try inline prompts** (simplest):

   ```bash
   uv run -m veo_lab.simple --prompt "Subject: small carved red stone disc lying flat on mirror, Action: hand reaches down to pick it up, Style: clinical documentation"
   ```

2. **Use prompt files** for longer/reusable prompts:

   ```bash
   uv run -m veo_lab.simple --prompt-file examples/basic_prompt.txt
   ```

3. **Complete pipeline** (image → video):

   ```bash
   # Generate reference, then create video using it
   uv run imagen_lab generate "$(cat examples/characters/security_officer.txt)" --output examples/characters/generated/security_officer --name security_officer
   uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
   ```

> **Tip**: Instead of `export GEMINI_API_KEY=...`, you can copy `.env.example` to `.env` and set your API key there.

4. **Explore advanced features** - See [docs/examples/](../docs/examples/) for comprehensive guides

## Image Generation Examples

### Basic Image Generation

```bash
# Simple generation
uv run imagen_lab generate "Sterile containment facility with monitoring equipment, clinical documentation style"

# With custom output location
uv run imagen_lab generate "Portrait of site technician in laboratory coat" --output my_images/technician --name site_technician

# Different models (check available models)
uv run imagen_lab generate "Concrete tunnel entrance" --model imagen-3.0-fast-generate-001
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
uv run imagen_lab generate "$(cat examples/characters/d_class_20384.txt)" --output examples/characters/generated/d_class_20384 --name d_class_20384 --dry

# Generate all provided character references
uv run imagen_lab generate "$(cat examples/characters/d_class_20384.txt)" --output examples/characters/generated/d_class_20384 --name d_class_20384
uv run imagen_lab generate "$(cat examples/characters/d_class_54493.txt)" --output examples/characters/generated/d_class_54493 --name d_class_54493
uv run imagen_lab generate "$(cat examples/characters/security_officer.txt)" --output examples/characters/generated/security_officer --name security_officer
uv run imagen_lab generate "$(cat examples/characters/site_technician.txt)" --output examples/characters/generated/site_technician --name site_technician

# Then use them in video generation
uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
```

### Style Reference Workflow

Generate style references for different atmospheric approaches, then test them with the same scene:

```bash
# Generate style reference images
uv run imagen_lab generate "$(cat examples/references/containment_facility.txt)" --output examples/references/generated/containment_facility --name containment_facility
uv run imagen_lab generate "$(cat examples/references/concrete_tunnel.txt)" --output examples/references/generated/concrete_tunnel --name concrete_tunnel
uv run imagen_lab generate "$(cat examples/references/abandoned_cityscape.txt)" --output examples/references/generated/abandoned_cityscape --name abandoned_cityscape
uv run imagen_lab generate "$(cat examples/references/green_farmland.txt)" --output examples/references/generated/green_farmland --name green_farmland

# Test with generated style references
uv run -m veo_lab.ref_image_lab --ref-dir examples/references/generated/ --scene examples/basic_prompt.txt
```

## Video Generation Examples

### Basic Usage

```bash
# Inline prompt (quickest way to test)
uv run -m veo_lab.simple --prompt "Subject: small carved red stone disc lying flat on mirror, Action: hand reaches down to pick it up, Style: clinical documentation"

# From file (better for complex prompts)
uv run -m veo_lab.simple --prompt-file examples/basic_prompt.txt

# With negative prompt
uv run -m veo_lab.simple -f examples/basic_prompt.txt -n "blurry, low quality, comedic elements"

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
uv run -m veo_lab.storyboard --storyboard examples/storyboard_demo.json --concat final_activation.mp4
```

### Template Matrix (`prompt_matrix`)

```bash
# Test matrix combinations (4 videos)
uv run -m veo_lab.prompt_matrix --template examples/base_template.j2 --config examples/matrix_demo.yml --dry

# Real generation (expect ~90 seconds due to rate limiting)
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
├── 2025-08-19/
│   ├── 143022_imagen_3.0-002_d_class_personnel/    # Image generation
│   │   ├── d_class_personnel.jpg
│   │   ├── metadata.json
│   │   └── prompt.txt
│   └── 143045_simple_veo2_red_stone_activation/     # Video generation
│       ├── red_stone_activation.mp4
│       ├── metadata.json
│       └── prompt.txt
└── latest -> 2025-08-19/143045_simple_veo2_red_stone_activation/
```

**Custom output locations** (using `--output` flag):
```
examples/characters/generated/
├── d_class_20384/
│   ├── d_class_20384.jpg
│   ├── metadata.json
│   └── prompt.txt
└── security_officer/
    ├── security_officer.jpg
    ├── metadata.json
    └── prompt.txt
```

## SCP-093 Extended Examples

The `user_prompts/scp_093_extras/` directory contains additional content themed around dimensional portal exploration:

```bash
# Test extended scenes
uv run -m veo_lab.simple --prompt-file user_prompts/scp_093_extras/farmhouse_crawler.txt --dry
uv run -m veo_lab.simple --prompt-file user_prompts/scp_093_extras/control_room_discovery.txt --dry

# Extended matrix testing
uv run -m veo_lab.prompt_matrix --template examples/base_template.j2 --config user_prompts/scp_093_extras/matrix_extended.yml --dry
```

These examples demonstrate clinical documentation aesthetics, institutional atmosphere, and dimensional exploration themes while maintaining the same technical workflows.

## Next Steps

- **Learn more**: Browse [docs/examples/](../docs/examples/) for detailed guides on each script
- **Validate setup**: Follow the validation guide in [ai_working/VALIDATION_GUIDE.md](../ai_working/VALIDATION_GUIDE.md)
- **Create experiments**: Start your own prompts in `user_prompts/`
