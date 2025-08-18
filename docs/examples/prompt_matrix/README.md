# Prompt Matrix - Template Combination Testing

**Purpose**: Generate multiple videos from all combinations of template variables for systematic experimentation.

## Usage

```bash
uv run -m veo_lab.prompt_matrix --template path/to/template.j2 --config path/to/matrix.yml
```

## Input Format

**Template file** (Jinja2 format):
```jinja2
Subject: {{ subject }}
Action: {{ action }}
Style: {{ style }}
Camera: {{ camera }}
Ambience: {{ ambience }}
Audio: {{ audio }}
```

**Matrix configuration** (YAML):
```yaml
matrix:
  subject:
    - a red vintage convertible
    - a silver sports motorcycle
  action:
    - cruises coastal highway
    - speeds through mountain curves
  style:
    - golden hour warmth
    - crisp modern digital
  camera:
    - aerial drone tracking
    - low ground-level shot
  ambience:
    - ocean breeze, seagulls
    - mountain air, pine trees
  audio:
    - wind rush, engine purr
    - tire grip, gear shifts
```

## Examples

**Basic matrix** ([examples/matrix_demo.yml](../../../examples/matrix_demo.yml) + [examples/base_template.j2](../../../examples/base_template.j2)): 2×2 car variations

**Character testing matrix**:
```yaml
matrix:
  character:
    - young wizard with staff
    - elderly sage with scrolls
    - battle-worn knight
  setting:
    - mystical forest clearing
    - ancient library hall
    - crumbling castle courtyard
  action:
    - studies glowing runes carefully
    - prepares for epic battle
    - discovers hidden secret
  lighting:
    - warm magical glow
    - dramatic torchlight
    - cold moonbeam shafts
```

## How It Works

1. **Cartesian product**: Generates all possible combinations (2×2×2 = 8 videos)
2. **Template rendering**: Each combination fills the Jinja2 template
3. **Batch generation**: Creates all videos in one session
4. **Organized output**: Videos named by combination indices

## Output

- Multiple videos: `combo_001_{snippet}_{model}.mp4`, `combo_002_{snippet}_{model}.mp4`
- Matrix mapping: `matrix_combinations.json` shows which variables created each video
- Session metadata: Tracks template and all generated combinations

## Use Cases

- **A/B testing**: Compare different styles or camera angles
- **Character exploration**: Test character in different scenarios
- **Style development**: Find optimal visual approach
- **Systematic variation**: Explore parameter space methodically

## Tips

- Start small (2×2 matrix = 4 videos) to test
- Use meaningful variable names in template
- Consider API rate limits for large matrices
- Review matrix_combinations.json to understand which combo is which
- Variables can have 1 item to keep that element constant