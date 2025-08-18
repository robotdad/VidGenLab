# Character Reference Prompts

Character prompts for generating reference images using `imagen_lab`, then testing the same scene with different characters using `character_pack` script.

## Generate Reference Images

First, generate the character reference images from the prompts:

```bash
# Generate all character reference images
uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch
uv run imagen_lab generate "$(cat examples/characters/digital_monk.txt)" --output examples/characters/generated/digital_monk --name digital_monk  
uv run imagen_lab generate "$(cat examples/characters/hooded_cybermancer.txt)" --output examples/characters/generated/hooded_cybermancer --name hooded_cybermancer
uv run imagen_lab generate "$(cat examples/characters/neon_occultist.txt)" --output examples/characters/generated/neon_occultist --name neon_occultist
```

## Create Character Pack Videos

Use the generated images with the character pack script:

```bash
uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
```

## Character Types

These complement the cyberpunk occult theme in `basic_prompt.txt`:

- **cyber_witch.txt** - Mystical practitioner with digital elements  
- **digital_monk.txt** - Spiritual figure in tech environment
- **hooded_cybermancer.txt** - Hooded figure with tech integration
- **neon_occultist.txt** - Occult practitioner in neon-lit setting

Each character prompt generates a reference image, then creates a video showing that character type performing the scene from `basic_prompt.txt`.