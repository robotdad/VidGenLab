# Prompt Rewriter - Automatic Prompt Variations

**Purpose**: Generate multiple creative variations of a base prompt specification.

## Usage

```bash
uv run -m veo_lab.prompt_rewriter --base-spec path/to/base_spec.txt --n 5 --out variations.json
```

## Input Format

Plain text file with a base concept or specification:

```
A mysterious character in a dramatic scene with cinematic lighting
```

Or more detailed:

```
A detective story set in a noir cityscape with rain and neon lights.
Focus on atmosphere and mood rather than action.
Vintage 1940s aesthetic preferred.
```

## Examples

**Simple base spec**:
```
A lone traveler on an epic journey through unknown lands
```

**Detailed base spec**:
```
Commercial product showcase featuring premium consumer electronics.
Emphasize sleek design and premium materials.
Modern, minimalist aesthetic with dramatic lighting.
Target demographic: tech-savvy professionals.
```

## Output

JSON file containing array of prompt variations:

```json
[
  {
    "variation": 1,
    "prompt": "Subject: weathered explorer with ancient map\nAction: studies terrain from rocky outcrop\nStyle: golden hour adventure film\nCamera: wide establishing shot\n..."
  },
  {
    "variation": 2, 
    "prompt": "Subject: cloaked wanderer with glowing staff\nAction: navigates mystical forest path\nStyle: fantasy epic with magical elements\n..."
  }
]
```

## Use Cases

- **Creative exploration**: Generate unexpected interpretations of a concept
- **Style variations**: Same subject in different visual styles  
- **A/B testing**: Create variations to test against each other
- **Writer's block**: Get unstuck with AI-generated alternatives
- **Client presentations**: Show multiple creative directions

## Tips

- Start with broad concepts for more creative variations
- Include constraints in base spec for focused variations
- Use output JSON with other scripts (copy prompts to use elsewhere)
- Generate 3-6 variations for good diversity without overwhelming options