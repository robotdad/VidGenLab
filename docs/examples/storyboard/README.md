# Storyboard - Multi-Shot Video Production

**Purpose**: Generate multiple shots with rich metadata and optional concatenation into final video.

## Usage

```bash
# Generate individual shots
uv run -m veo_lab.storyboard --storyboard path/to/storyboard.json

# Generate shots AND concatenate final video  
uv run -m veo_lab.storyboard --storyboard path/to/storyboard.json --concat out/final.mp4
```

## Input Format

JSON file with shot definitions:

```json
{
  "title": "Project Name",
  "shots": [
    {
      "id": "s001",
      "prompt": "Subject: coffee steam rising\nAction: slow zoom on cup\nStyle: warm morning light",
      "negative": "harsh lighting, busy background"
    },
    {
      "id": "s002", 
      "prompt": "Subject: hands lift mug\nAction: gentle movement toward camera",
      "carry_last_frame": true
    }
  ]
}
```

## Examples

**Simple storyboard** ([examples/storyboard_demo.json](../../../examples/storyboard_demo.json)): 2-shot coffee shop scene

**Advanced storyboard**:
```json
{
  "title": "Car Chase Sequence",
  "shots": [
    {
      "id": "chase_01",
      "prompt": "Subject: sports car accelerates from traffic light\nAction: quick launch, tires screech\nStyle: high energy, urban grit\nCamera: low angle, wide lens\nAmbience: city intersection, neon lights\nAudio: engine roar, tire squeal",
      "negative": "slow motion, peaceful"
    },
    {
      "id": "chase_02", 
      "prompt": "Subject: same car weaves through traffic\nAction: sharp lane changes, near misses\nStyle: kinetic, handheld feel\nCamera: chase cam following behind\nAmbience: busy street, horns honking\nAudio: revving engine, radio chatter",
      "carry_last_frame": true
    },
    {
      "id": "chase_03",
      "prompt": "Subject: car takes sharp corner\nAction: controlled drift around turn\nStyle: dramatic angle, tire smoke\nCamera: static corner view\nAmbience: urban canyon, echoing sound\nAudio: tire screech, engine echo", 
      "image": "assets/corner_reference.jpg"
    }
  ]
}
```

## Features

- **`carry_last_frame`**: Uses last frame of previous shot as reference
- **`image`**: Uses custom reference image instead of previous frame
- **`negative`**: Negative prompt for this specific shot
- **Shot IDs**: Used in filename generation for organization

## Output

- Individual shots: `01_{prompt_snippet}_{model}.mp4`, `02_{prompt_snippet}_{model}.mp4`
- Frame extracts: `.last.jpg` files for chaining
- Concatenated video: Final stitched version (if `--concat` used)
- Rich metadata: Tracks all shots, timing, and relationships

## Tips

- Plan your shots like a real film storyboard
- Use `carry_last_frame` for continuity
- Use custom `image` references for specific compositions
- Test individual shots before concatenating
- Keep shot lengths reasonable (5-10 seconds each)