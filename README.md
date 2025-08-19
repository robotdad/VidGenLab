# VidGenLab

Python toolkit for experimenting with AI video generation using **Veo 3** and image generation using **Imagen 3** via Google's Gemini API.

Generate images from text prompts, analyze existing images, then create videos with reference images. Build complete visual pipelines from text descriptions to finished videos.

## What You Can Do

**Image Generation (`imagen_lab`)**:
- **Generate images** from text prompts using Imagen 3
- **Analyze existing images** to extract descriptive prompts
- **Create reference images** for consistent video generation

**Video Generation (`veo_lab`)**:
- **Generate single videos** from text descriptions  
- **Create sequential shots** where each builds on the last frame
- **Test variations systematically** using templates and matrices
- **Use reference images** for character and style consistency
- **Organize outputs automatically** with timestamps and metadata

**Complete Pipeline**: Text → Image → Video workflows for full creative control

All scripts save organized outputs to `out/` with descriptive filenames, metadata, and a `latest` symlink to your most recent work.

## Prerequisites

- **Python 3.11+**
- **FFmpeg** on your PATH  
- **Gemini API key** with Veo access ([Rate Limits Info](https://ai.google.dev/gemini-api/docs/rate-limits))

## Quick Setup

```bash
# Install dependencies
make install

# Configure API key (choose one method)
export GEMINI_API_KEY="your_key_here"
# OR copy .env.example to .env and edit it
cp .env.example .env
```

## Try It Now

**Generate your first image:**
```bash
# Generate a character reference image
uv run imagen_lab generate "Professional headshot of a D-Class personnel in orange jumpsuit, institutional lighting, clinical documentation style"
```

**Generate your first video:**
```bash
# Simple video from text prompt
uv run -m veo_lab.simple --prompt "Subject: small carved red stone disc lying flat on mirror surface, Action: hand reaches down to pick it up, Style: clinical documentation with building tension"

# Or with Veo 3 (limited rate limits)
uv run -m veo_lab.simple --prompt "Subject: small carved red stone disc lying flat on mirror surface, Action: hand reaches down to pick it up, Style: clinical documentation with building tension" --model veo-3.0-generate-preview
```

**Complete pipeline example:**
```bash
# 1. Generate reference image
uv run imagen_lab generate "$(cat examples/characters/d_class_20384.txt)" --output examples/characters/generated/d_class_20384 --name d_class_20384

# 2. Create video using the reference  
uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
```

All outputs are saved to `out/` with automatic organization by date and time. Check `out/latest/` for your most recent generation.

## Configuration & Testing

### Environment Variables

Control default models without specifying them in every command:

```bash
# Copy and edit the example environment file
cp .env.example .env

# Set your preferred defaults
export VEO_MODEL=veo-3.0-generate-preview        # For video generation
export IMAGEN_MODEL=imagen-3.0-generate-002      # For image generation  
```

Model selection precedence:
1. Explicit `--model` argument (highest priority)
2. Environment variable (`VEO_MODEL` or `IMAGEN_MODEL`) 
3. Default model (lowest priority)

### Dry Run Mode

Test prompts and validate configuration without consuming API quota:

```bash
# Test image generation setup
uv run imagen_lab generate "D-Class personnel in containment facility" --dry

# Shows what would be generated:
# • Model: imagen-3.0-generate-002
# • Output directory: out/2025-08-19/120506_imagen_3.0-002_d_class_personnel  
# • Files: d_class_personnel.jpg, prompt.txt, metadata.json
# ✅ Dry run complete - no API calls made

# Test with custom model
uv run imagen_lab generate "test prompt" --model imagen-3.0-fast-generate-001 --dry

# Test with environment variable  
IMAGEN_MODEL=custom-model uv run imagen_lab generate "test prompt" --dry
```

Dry-run is perfect for:
- **Validating environment variables** work correctly
- **Testing prompt files** and templates before spending quota  
- **Debugging CLI arguments** without API costs
- **Development and scripting** workflows

## More Examples

For comprehensive examples and all available scripts, see:

- **[examples/README.md](examples/README.md)** - Quick-start examples you can run immediately
- **[docs/examples/](docs/examples/)** - Detailed guides for all 7 video generation scripts  
- **[ai_working/VALIDATION_GUIDE.md](ai_working/VALIDATION_GUIDE.md)** - Test your setup step-by-step

## How It Works

Veo 3 generates ~8 second video clips from text prompts. For longer content, multiple clips can be stitched together. The toolkit provides several approaches:

- **Single videos** from text descriptions
- **Sequential chains** using the last frame of each video as the starting point for the next
- **Multi-shot storyboards** with rich metadata and automatic concatenation
- **Systematic variations** to test different approaches to the same concept

All outputs are automatically organized by date and time with descriptive filenames that include parts of your prompt.

## Development

This project follows the principles outlined in `AGENTS.md`. The codebase uses a modular, AI-friendly architecture designed for rapid experimentation and regeneration.

### Build Commands

- Install dependencies: `make install`
- Run all checks: `make check`
- Run all tests: `make test`

### Project Organization

- **`examples/`** - Quick-start examples for both image and video generation
- **`docs/examples/`** - Comprehensive guides for all generation tools
- **`user_prompts/`** - Save your personal experiments here (git-ignored)  
- **`out/`** - Generated images and videos, automatically organized by date/time
- **`src/veo_lab/`** - Core video generation modules
- **`src/imagen_lab/`** - Core image generation and analysis modules

## Example Themes

The included examples use a clinical documentation aesthetic inspired by dimensional research facilities. Characters include D-Class personnel, security officers, and site technicians in institutional settings. Extended examples in `user_prompts/scp_093_extras/` explore dimensional portal themes with concrete tunnels, abandoned cities, and farmland exploration.

## Personal Experiments

Save your own prompts and configurations in `user_prompts/` - this folder is git-ignored so your experiments stay private. See [user_prompts/README.md](user_prompts/README.md) for organization tips.

## AI-Assisted Development

This template includes powerful AI development tools:

- `/prime` - Set up environment and load project philosophy
- Context management in `ai_context/` for persistent reference docs
- Modular design philosophy optimized for AI-driven development

The project embraces AI-assisted development while maintaining human creativity and architectural vision.