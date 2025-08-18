# VidGenLab Examples - Comprehensive Guide

Detailed documentation and advanced examples for all VidGenLab scripts.

## All Scripts Overview

| Script | Purpose | Input Format | Output |
|--------|---------|-------------|--------|
| [simple](simple/) | Single video generation | Text prompt or file | 1 video |
| [shot_chain](shot_chain/) | Sequential videos (last frame → next) | YAML prompt list | N videos + frame extracts |
| [storyboard](storyboard/) | Multi-shot with metadata | JSON shot definitions | N videos + optional concat |
| [prompt_matrix](prompt_matrix/) | Template combinations | Jinja2 template + YAML vars | N×M videos (all combinations) |
| [prompt_rewriter](prompt_rewriter/) | Prompt variations | Base spec text | Multiple prompt variants |
| [character_pack](character_pack/) | Character-focused testing | Scene + reference images | Videos per character |
| [ref_image_lab](ref_image_lab/) | Reference image experiments | Scene + reference directory | Videos per reference |

## Quick Navigation

- **Start here**: [simple](simple/) - Basic single video generation
- **Storytelling**: [shot_chain](shot_chain/) and [storyboard](storyboard/)  
- **Experimentation**: [prompt_matrix](prompt_matrix/) and [prompt_rewriter](prompt_rewriter/)
- **Character work**: [character_pack](character_pack/) and [ref_image_lab](ref_image_lab/)

## Shared Templates

Common templates used across multiple scripts:

- [`base_template.j2`](../examples/base_template.j2) - Standard prompt structure
- More templates can be found in individual script folders

## Validation

To test all scripts with examples, see [ai_working/VALIDATION_GUIDE.md](../../ai_working/VALIDATION_GUIDE.md).