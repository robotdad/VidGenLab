# Shot Chain - Sequential Video Generation

**Purpose**: Generate a sequence of videos where each shot starts from the last frame of the previous shot.

## Usage

```bash
uv run -m veo_lab.shot_chain --file path/to/chain.yml
```

## Input Format

YAML file with `prompts` array. Each prompt is plain text (multiline supported):

```yaml
prompts:
  - |
    Subject: astronaut on desert plateau
    Action: walks toward camera
    Style: golden hour, cinematic
    Camera: wide establishing shot
    Ambience: vast emptiness
    Audio: wind, radio static
  - |
    Subject: astronaut reaches ancient structure
    Action: stops, looks up in awe
    Style: dramatic shadows
    Camera: low angle looking up
    Ambience: mysterious monument
    Audio: heartbeat, silence
```

## Examples

**Basic chain** ([examples/chain_demo.yml](../../../examples/chain_demo.yml)): 3-shot astronaut discovery sequence

**Advanced chain**:
```yaml
prompts:
  - "Subject: vintage car on empty highway\nAction: drives toward camera\nStyle: 1970s film stock\nCamera: wide road shot"
  - "Subject: car passes camera\nAction: camera whip-pans to follow\nStyle: motion blur, kinetic\nCamera: handheld tracking"
  - "Subject: car disappears over hill\nAction: dust settles\nStyle: melancholy, fading light\nCamera: static wide"
```

## How It Works

1. Generates first video from first prompt
2. Extracts last frame as `.last.jpg` 
3. Uses that frame as reference image for next prompt
4. Repeats for all prompts in sequence

## Output

- Multiple videos: `01_{prompt_snippet}_{model}.mp4`, `02_{prompt_snippet}_{model}.mp4`, etc.
- Frame extracts: `01_{prompt_snippet}_{model}.last.jpg` for chaining
- All organized in single session directory
- Metadata tracks entire chain

## Tips

- Each prompt should logically continue from the previous
- Consider continuity of lighting, camera angle, and subjects
- Don't make dramatic scene changes between shots
- Test with shorter chains (2-3 shots) first