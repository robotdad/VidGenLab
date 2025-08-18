# Simple - Single Video Generation

**Purpose**: Generate a single video from a text prompt.

## Usage

```bash
# From text prompt
uv run -m veo_lab.simple --prompt "Your prompt here"

# From file
uv run -m veo_lab.simple --prompt-file path/to/prompt.txt

# With negative prompt
uv run -m veo_lab.simple -f prompt.txt -n "blurry, low quality"

# Image-to-video
uv run -m veo_lab.simple -f prompt.txt -i reference.jpg

# Specify model
uv run -m veo_lab.simple -f prompt.txt --model veo-3.0-fast-generate-preview

# List available models
uv run -m veo_lab.simple --list-models
```

## Input Format

Plain text prompt with structured sections (recommended):

```
Subject: what's in the scene
Action: what happens
Style: visual aesthetic
Camera: camera movement/framing
Ambience: mood and environment
Audio: sound design notes
```

## Examples

**Basic prompt** ([examples/basic_prompt.txt](../../../examples/basic_prompt.txt)):
```
Subject: a lone sailboat in heavy fog
Action: slow push-in, fog horns echo
Style: cinematic, muted palette  
Camera: 50mm, shallow depth of field
Ambience: misty sea, low visibility
Audio: distant fog horn, soft waves
```

**Advanced prompt**:
```
Subject: cyberpunk street vendor in neon-lit alley
Action: arranges holographic wares, customers browse
Style: blade runner aesthetic, volumetric lighting
Camera: handheld, slight dutch angle
Ambience: rain-slicked pavement, steam from vents
Audio: electronic music, distant traffic
```

## Output

- Single video file: `{prompt_snippet}_{model}.mp4`
- Metadata: `metadata.json` and `prompt.txt`
- Organized in timestamped session directory

## Tips

- Use descriptive but concise prompts (1-2 sentences per section)
- Negative prompts help avoid unwanted elements
- Reference images work best with consistent lighting/style
- Model choice affects speed vs quality trade-off