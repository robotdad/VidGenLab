# VidGenLab Validation Guide

Step-by-step guide to validate that all scripts work correctly with the provided examples. **Do not run this all at once** - these are API calls that consume credits.

## Prerequisites

1. **Environment Setup**:
   ```bash
   # Install dependencies
   make install
   source .venv/bin/activate
   
   # Verify API key is set
   echo $GEMINI_API_KEY  # Should show your API key
   ```

2. **Check Models**:
   ```bash
   uv run -m veo_lab.simple --list-models
   ```

3. **Verify imagen_lab CLI**:
   ```bash
   # Check imagen_lab is available
   uv run imagen_lab --help
   ```

## Image Generation Validation (Run One at a Time)

**Tip**: Use `--dry` flag first to test commands without consuming credits:
```bash
# Test any imagen_lab command with --dry first
uv run imagen_lab generate "test prompt" --dry
```

### 1. Basic Image Generation ✓
**Purpose**: Generate single image from text prompt  
**Expected**: 1 image file + metadata

```bash
# Test basic image generation
uv run imagen_lab generate "A red balloon floating in blue sky, minimalist style"

# Test with custom output location
uv run imagen_lab generate "Digital art of a cyberpunk city" --output test_images/cyberpunk --name cyberpunk_test
```

**Check Output**:
- `out/YYYY-MM-DD/HHMMSS_imagen_*/` directory created
- Contains: `*.jpg`, `metadata.json`, `prompt.txt`
- If custom output used: files in specified location

---

### 2. Image Analysis ✓
**Purpose**: Analyze existing image and generate descriptive prompt
**Expected**: Analysis output with generated prompt

```bash
# Test with any existing image file
uv run imagen_lab analyze path/to/your/image.jpg
```

**Check Output**:
- `out/YYYY-MM-DD/HHMMSS_analyze_*/` directory created
- Contains: `prompt.txt` (with generated description), `metadata.json`
- Generated prompt should be detailed and accurate

---

### 3. Character Reference Generation ✓
**Purpose**: Generate character references for video generation
**Expected**: 4 character reference images

```bash
# First test with dry-run to validate prompts
uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch --dry

# Generate all character references (THIS CONSUMES API CREDITS)
uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch
uv run imagen_lab generate "$(cat examples/characters/digital_monk.txt)" --output examples/characters/generated/digital_monk --name digital_monk
uv run imagen_lab generate "$(cat examples/characters/hooded_cybermancer.txt)" --output examples/characters/generated/hooded_cybermancer --name hooded_cybermancer  
uv run imagen_lab generate "$(cat examples/characters/neon_occultist.txt)" --output examples/characters/generated/neon_occultist --name neon_occultist
```

**Check Output**:
- `examples/characters/generated/*/` directories created
- Each contains: `*.jpg`, `metadata.json`, `prompt.txt`
- Images should match character descriptions

---

## Video Generation Validation (Run One at a Time)

### 1. Simple Script ✓
**Purpose**: Single video generation
**Expected**: 1 video file + metadata

```bash
# Test basic prompt file
uv run -m veo_lab.simple --prompt-file examples/basic_prompt.txt

# Test inline prompt
uv run -m veo_lab.simple --prompt \"Subject: red balloon floating upward\nAction: gentle drift against blue sky\nStyle: minimalist, soft focus\"

# Test with negative prompt
uv run -m veo_lab.simple -f examples/basic_prompt.txt -n \"blurry, low quality\"
```

**Check Output**:
- `out/YYYY-MM-DD/HHMMSS_simple_*/` directory created
- Contains: `*.mp4`, `metadata.json`, `prompt.txt`
- `out/latest` points to most recent generation

---

### 2. Shot Chain Script ✓
**Purpose**: Sequential videos using last frames
**Expected**: 3 videos + frame extracts for chaining

```bash
uv run -m veo_lab.shot_chain --file examples/chain_demo.yml
```

**Check Output**:
- Single session directory with sequential videos: `01_*.mp4`, `02_*.mp4`, `03_*.mp4`
- Frame extracts: `01_*.last.jpg`, `02_*.last.jpg`, `03_*.last.jpg`
- Metadata shows all 3 files in the session

---

### 3. Storyboard Script ✓
**Purpose**: Multi-shot with metadata and optional concatenation
**Expected**: 2 videos from storyboard

```bash
# Test shot generation only
uv run -m veo_lab.storyboard --storyboard examples/storyboard_demo.json

# Test with concatenation (creates final stitched video)
uv run -m veo_lab.storyboard --storyboard examples/storyboard_demo.json --concat final_coffee.mp4
```

**Check Output**:
- Individual shots: `01_*.mp4`, `02_*.mp4` 
- If `--concat` used: `final_coffee.mp4` (concatenated video)
- Frame extracts for chaining: `*.last.jpg`

---

### 4. Prompt Matrix Script ✓
**Purpose**: Generate all combinations of template variables
**Expected**: 8 videos (2×2×2×2 combinations)

```bash
uv run -m veo_lab.prompt_matrix --template examples/base_template.j2 --config examples/matrix_demo.yml
```

**Check Output**:
- Multiple videos: `combo_001_*.mp4`, `combo_002_*.mp4`, etc.
- `matrix_combinations.json` showing which variables created each video
- Should generate 8 total videos (2 subjects × 2 actions × 2 styles × 2 cameras)

---

### 5. Prompt Rewriter Script ⚠️
**Purpose**: Generate prompt variations from base specification
**Expected**: JSON file with multiple prompt variants

**Note**: This script needs a base specification file. Create one first:

```bash
# Create a base spec file
echo \"A character in a dramatic scene with cinematic lighting\" > test_base_spec.txt

# Run prompt rewriter  
uv run -m veo_lab.prompt_rewriter --base-spec test_base_spec.txt --n 3 --out rewrites_test.json

# Check output
cat rewrites_test.json
```

**Check Output**:
- JSON file with multiple prompt variations
- Each variant should be a different interpretation of the base spec

---

### 6. Character Pack Script ✓
**Purpose**: Test same scene with multiple character references
**Expected**: Multiple videos, one per reference image

**Prerequisites**: First generate character references (see Image Generation section #3 above)

```bash
# Use generated character references (after generating them above)
uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
```

**Expected Output**:
- One video per character reference: 4 videos total
- Videos show same scene with different character references (cyber_witch, digital_monk, etc.)
- Files named with character types: `cyber_witch_*.mp4`, `digital_monk_*.mp4`, etc.

---

### 7. Ref Image Lab Script ✓
**Purpose**: Test reference images with scene variations  
**Expected**: Multiple videos testing different reference images

**Prerequisites**: First generate style references:

```bash
# First test with dry-run to validate prompts
uv run imagen_lab generate "Bright neon-lit cyberpunk server room with glowing data streams" --output examples/references/generated/neon_server --name neon_server_room --dry

# Generate style reference images (THIS CONSUMES API CREDITS)
uv run imagen_lab generate "Bright neon-lit cyberpunk server room with glowing data streams" --output examples/references/generated/neon_server --name neon_server_room
uv run imagen_lab generate "Dark occult ritual space with candles and mystical symbols" --output examples/references/generated/occult_space --name occult_ritual_space
```

Then test with references:

```bash
# Use generated style references
uv run -m veo_lab.ref_image_lab --ref-dir examples/references/generated/ --scene examples/basic_prompt.txt
```

**Expected Output**:
- Multiple videos testing different reference images with same scene
- Helps compare how different styles/atmospheres affect output
- Should generate videos for each reference image in the directory

---

## Validation Checklist

After running each script, verify:

- ✓ **Output Structure**: Files organized in `out/YYYY-MM-DD/HHMMSS_script_*/`
- ✓ **File Naming**: Videos named with prompt snippets: `{snippet}_{model}.mp4`
- ✓ **Metadata**: `metadata.json` and `prompt.txt` files present
- ✓ **Latest Link**: `out/latest` points to most recent generation
- ✓ **Video Playback**: Generated videos actually play
- ✓ **Expected Count**: Correct number of output files

## Common Issues

**API Key Issues**:
```bash
export GEMINI_API_KEY=\"your-key-here\"
```

**Model Not Available**:
```bash
# Check available models
uv run -m veo_lab.simple --list-models

# Use specific model if needed  
uv run -m veo_lab.simple -f examples/basic_prompt.txt --model veo-2.0-generate-001
```

**Permission Errors**:
```bash
chmod +x out/latest  # Fix symlink permissions if needed
```

## Success Criteria

**Image Generation (3 tests)**:
1. `imagen_lab` commands run without errors
2. Images generate and save to correct locations
3. Metadata files created with proper structure
4. Character references match text descriptions

**Video Generation (7 tests)**:
1. All `veo_lab` scripts run without Python errors  
2. Create organized output in `out/` directory
3. Generate expected number of files
4. Create valid video files that play
5. Save metadata correctly
6. Character pack and ref image lab work with generated references

**Complete Pipeline Test**:
Text prompts → `imagen_lab generate` → Reference images → `veo_lab.character_pack` → Character videos