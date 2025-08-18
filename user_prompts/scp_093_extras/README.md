# SCP-093 Extended Examples

Additional SCP-093 themed prompts and templates for advanced experimentation. These build on the core examples in `examples/` with more specific atmospheric scenes and extended template variations.

## Extra Scene Prompts

### farmhouse_crawler.txt
D-54493 farmhouse sighting of massive crawler entities - the Green Test perspective with specific distance and environmental details from the exploration logs.

### control_room_discovery.txt
Cylindrical control room with rotating pillar and multiple SCP-093 disc array - the Red Test discovery sequence with technical specifications.

### upper_city_view.txt
Security observation of Unclean entities from upper floor - professional documentation of the massive torso creatures on raised expressways.

## Extended Templates

### tunnel_storyboard_extended.json
More detailed tunnel discovery sequence with additional shots and environmental details.

### matrix_extended.yml
Full variable matrix including all locations, personnel types, and atmospheric variations from the SCP-093 exploration logs.

## Usage

These examples demonstrate how to organize your own prompts in the `user_prompts/` directory. You can:

1. **Test atmospheric variations**: Use the extra scene prompts to explore different SCP-093 moments
2. **Extended sequences**: Try the expanded storyboard and matrix templates
3. **Create your own**: Follow these patterns to develop prompts for other SCP entries or original themes

## Character and Reference Integration

All these prompts work with the character and reference image systems:

```bash
# Generate character references
uv run imagen_lab generate "$(cat examples/characters/d_class_54493.txt)" --output examples/characters/generated/d_class_54493 --name d_class_54493

# Use with extra scenes
uv run -m veo_lab.simple --prompt-file user_prompts/scp_093_extras/farmhouse_crawler.txt
uv run -m veo_lab.character_pack --scene "$(cat user_prompts/scp_093_extras/farmhouse_crawler.txt)" --ref-dir examples/characters/generated/

# Use with style references  
uv run -m veo_lab.ref_image_lab --ref-dir examples/references/generated/ --scene user_prompts/scp_093_extras/control_room_discovery.txt
```

This directory serves as an example of how to organize and extend the core examples for your own creative projects.