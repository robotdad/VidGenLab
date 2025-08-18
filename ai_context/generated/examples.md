# examples/**/*

[collect-files]

**Search:** ['examples/**/*']
**Exclude:** ['*.mp4', '*.jpg', '*.png', '*.jpeg']
**Include:** []
**Date:** 8/18/2025, 10:40:52 AM
**Files:** 20

=== File: examples/README.md ===
# VidGenLab Examples

Quick-start examples for both image generation and video generation.

## Getting Started

### Image Generation First

1. **Generate your first image**:

   ```bash
   uv run imagen_lab generate "Portrait of a cyberpunk character with neon lighting, dramatic atmosphere"
   ```

2. **Create character references from prompts**:

   ```bash
   uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch
   ```

### Video Generation

1. **Try inline prompts** (simplest):

   ```bash
   uv run -m veo_lab.simple --prompt "Cloaked figure traces glowing symbols, cyberpunk occult atmosphere"
   ```

2. **Use prompt files** for longer/reusable prompts:

   ```bash
   uv run -m veo_lab.simple --prompt-file examples/basic_prompt.txt
   ```

3. **Complete pipeline** (image → video):

   ```bash
   # Generate reference, then create video using it
   uv run imagen_lab generate "$(cat examples/characters/digital_monk.txt)" --output examples/characters/generated/digital_monk --name digital_monk
   uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
   ```

> **Tip**: Instead of `export GEMINI_API_KEY=...`, you can copy `.env.example` to `.env` and set your API key there.

4. **Explore advanced features** - See [docs/examples/](../docs/examples/) for comprehensive guides

## Image Generation Examples

### Basic Image Generation

```bash
# Simple generation
uv run imagen_lab generate "Digital art of a futuristic cityscape at night, neon lights, cyberpunk style"

# With custom output location
uv run imagen_lab generate "Portrait of a wise wizard" --output my_images/wizard --name wizard_portrait

# Different models (check available models with veo_lab for now)
uv run imagen_lab generate "Landscape painting" --model imagen-3.0-generate-001
```

### Image Analysis

```bash
# Analyze any image to get a descriptive prompt
uv run imagen_lab analyze path/to/your/image.jpg

# Use generated prompt to create variations
uv run imagen_lab generate "$(cat out/YYYY-MM-DD/HHMMSS_analyze_*/prompt.txt)"
```

### Character Reference Workflow

```bash
# Generate all provided character references
uv run imagen_lab generate "$(cat examples/characters/cyber_witch.txt)" --output examples/characters/generated/cyber_witch --name cyber_witch
uv run imagen_lab generate "$(cat examples/characters/digital_monk.txt)" --output examples/characters/generated/digital_monk --name digital_monk
uv run imagen_lab generate "$(cat examples/characters/hooded_cybermancer.txt)" --output examples/characters/generated/hooded_cybermancer --name hooded_cybermancer
uv run imagen_lab generate "$(cat examples/characters/neon_occultist.txt)" --output examples/characters/generated/neon_occultist --name neon_occultist

# Then use them in video generation
uv run -m veo_lab.character_pack --scene "$(cat examples/basic_prompt.txt)" --ref-dir examples/characters/generated/
```

## Video Generation Examples

### Basic Usage

```bash
# Inline prompt (quickest way to test)
uv run -m veo_lab.simple --prompt "Subject: cyber-witch casting holographic spells, Style: neon-lit gothic atmosphere, Action: mystical energy flows"

# From file (better for complex prompts)
uv run -m veo_lab.simple --prompt-file examples/basic_prompt.txt

# With negative prompt
uv run -m veo_lab.simple -f examples/basic_prompt.txt -n "bright lighting, cheerful atmosphere"

# Image-to-video (requires reference image)
uv run -m veo_lab.simple -f examples/basic_prompt.txt -i path/to/reference.jpg

# Specify model (default is veo-2.0-generate-001)
uv run -m veo_lab.simple -f examples/basic_prompt.txt --model veo-3.0-generate-preview
uv run -m veo_lab.simple -f examples/basic_prompt.txt --model veo-3.0-fast-generate-preview

# List available models
uv run -m veo_lab.simple --list-models
```

### Video Chain (`shot_chain`)

```bash
uv run -m veo_lab.shot_chain --file examples/chain_demo.yml
```

### Storyboard (`storyboard`)

```bash
# Generate shots
uv run -m veo_lab.storyboard --storyboard examples/storyboard_demo.json

# Generate and concatenate into final video
uv run -m veo_lab.storyboard --storyboard examples/storyboard_demo.json --concat final_seance.mp4
```

### Template Matrix (`prompt_matrix`)

```bash
uv run -m veo_lab.prompt_matrix --template examples/base_template.j2 --config examples/matrix_demo.yml
```

## Model Selection

All scripts support the `--model` option to choose between Veo versions:

- **`veo-2.0-generate-001`** (default) - Reliable, good rate limits
- **`veo-3.0-generate-preview`** - Best quality, very limited rate limits
- **`veo-3.0-fast-generate-preview`** - Faster Veo 3, still limited rate limits

You can also set a default in `.env`: `VEO_MODEL=veo-2.0-generate-001`

**Note**: Veo 3 has much lower rate limits. See [Rate Limits Documentation](https://ai.google.dev/gemini-api/docs/rate-limits).

## File Organization

Both images and videos are organized in `out/` with consistent naming:

```
out/
├── 2025-01-15/
│   ├── 143022_imagen_cyberpunk_character/    # Image generation
│   │   ├── cyberpunk_character.jpg
│   │   ├── metadata.json
│   │   └── prompt.txt
│   └── 143045_simple_sailboat_in_fog/        # Video generation
│       ├── sailboat_in_fog_veo3.mp4
│       ├── metadata.json
│       └── prompt.txt
└── latest -> 2025-01-15/143045_simple_sailboat_in_fog/
```

**Custom output locations** (using `--output` flag):
```
examples/characters/generated/
├── cyber_witch/
│   ├── cyber_witch.jpg
│   ├── metadata.json
│   └── prompt.txt
└── digital_monk/
    ├── digital_monk.jpg
    ├── metadata.json
    └── prompt.txt
```

## Next Steps

- **Learn more**: Browse [docs/examples/](../docs/examples/) for detailed guides on each script
- **Validate setup**: Follow the validation guide in [ai_working/VALIDATION_GUIDE.md](../ai_working/VALIDATION_GUIDE.md)
- **Create experiments**: Start your own prompts in `user_prompts/`


=== File: examples/base_template.j2 ===
Subject: {{ subject }}
Action: {{ action }}
Style: {{ style }}
Camera: {{ camera }}
Ambience: {{ ambience }}
Audio: {{ audio }}

=== File: examples/basic_prompt.txt ===
Subject: hooded figure studies glowing sigils on massive server racks
Action: traces symbols with fingertip, circuits pulse in response  
Style: cyberpunk noir, neon-lit shadows
Camera: low angle, mysterious framing
Ambience: humming electronics, dark data center
Audio: electronic drones, whispered incantations

=== File: examples/chain_demo.yml ===
# Each shot uses the last frame of the previous as a starting point
prompts:
  - |
    Subject: lone explorer in abandoned megacity ruins
    Action: navigates through fog-shrouded debris
    Style: desaturated cyberpunk, oppressive atmosphere
    Camera: wide shot, industrial decay visible
    Ambience: toxic mist, crumbling neon signs
    Audio: distant machinery, static interference
  - |
    Subject: explorer finds strange geometric portal
    Action: cautiously approaches pulsing anomaly
    Style: eldritch horror meets sci-fi, unsettling glow
    Camera: slow push-in, building tension
    Ambience: reality warping around the portal
    Audio: otherworldly harmonics, electronic whispers
  - |
    Subject: portal reveals glimpse of impossible space
    Action: tentacles of light emerge, reach toward explorer
    Style: cosmic horror, digital distortion effects
    Camera: extreme close-up on face, awe and terror
    Ambience: space-time bending, fractal patterns
    Audio: reality tearing, digital screams


=== File: examples/characters/README.md ===
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

=== File: examples/characters/analysis/cyber_witch/metadata.json ===
{
  "prompt": "Describe this image in detail, focusing on visual elements, style, composition, and mood. Create a prompt that could be used to generate a similar image.",
  "script": "analyze",
  "model": "gemini-2.0-flash-exp",
  "timestamp": "2025-08-18T10:21:48.084313",
  "output_path": "examples/characters/analysis/cyber_witch",
  "source_image": "examples/characters/cyber_witch.png",
  "generated_prompt": "Here's a detailed description of the image, followed by a prompt that could generate a similar image:\n\n**Image Description**\n\n*   **Visual Elements:** The image is a portrait of a woman with dark skin and long, dark dreadlocks. A few dreadlocks are adorned with thin, hair tinsel that contains tiny blue lights, adding a subtle magical effect. She's wearing a plain black t-shirt and a dark grey or black cardigan. Her hands are clasped gently in front of her, displaying several rings on her fingers, each appearing to have a blue, slightly iridescent or luminous design embedded within. She wears multiple necklaces of varying lengths, each with unique pendants\u2014a coin-like pendant, a crystal tassel, and other rectangular pendants with intricate details. Bracelets are visible on her right wrist.\n\n*   **Style:** The style blends modern portraiture with elements of fantasy or mysticism. The use of the blue lights in the hair and the varied jewelry creates a feeling of bohemian chic with a hint of otherworldly wonder.\n\n*   **Composition:** The composition is a tight to medium shot, focusing on the woman's face and upper body. The subject is centered, drawing the viewer's attention directly to her face and expression. The slightly low angle creates a sense of subtle power and confidence. The depth of field seems shallow, keeping the focus sharp on the subject while subtly blurring the background.\n\n*   **Mood:** The mood is calm, serene, and perhaps a little mysterious. Her expression is neutral but conveys a sense of inner strength and quiet confidence. The lighting is soft, creating a warm and inviting atmosphere, with a slight ethereal glow from the blue lights.\n\n**Image Generation Prompt**\n\n\"Create a portrait of a Black woman with long dark dreadlocks, some strands adorned with sparkling blue hair tinsel. She wears a black t-shirt and a dark-colored cardigan. She has multiple necklaces with various pendants: including a coin, a crystal tassel, and other geometric shapes. She's wearing several rings with a blue iridescent shimmer, as well as thin metal bracelets. Her hands are clasped gently. Use soft, warm lighting to evoke a mood of serene confidence and subtle mysticism. The background should be a dark, subtly textured grey. Use a shallow depth of field to keep the subject in sharp focus.\"\n"
}

=== File: examples/characters/analysis/cyber_witch/prompt.txt ===
Here's a detailed description of the image, followed by a prompt that could generate a similar image:

**Image Description**

*   **Visual Elements:** The image is a portrait of a woman with dark skin and long, dark dreadlocks. A few dreadlocks are adorned with thin, hair tinsel that contains tiny blue lights, adding a subtle magical effect. She's wearing a plain black t-shirt and a dark grey or black cardigan. Her hands are clasped gently in front of her, displaying several rings on her fingers, each appearing to have a blue, slightly iridescent or luminous design embedded within. She wears multiple necklaces of varying lengths, each with unique pendants—a coin-like pendant, a crystal tassel, and other rectangular pendants with intricate details. Bracelets are visible on her right wrist.

*   **Style:** The style blends modern portraiture with elements of fantasy or mysticism. The use of the blue lights in the hair and the varied jewelry creates a feeling of bohemian chic with a hint of otherworldly wonder.

*   **Composition:** The composition is a tight to medium shot, focusing on the woman's face and upper body. The subject is centered, drawing the viewer's attention directly to her face and expression. The slightly low angle creates a sense of subtle power and confidence. The depth of field seems shallow, keeping the focus sharp on the subject while subtly blurring the background.

*   **Mood:** The mood is calm, serene, and perhaps a little mysterious. Her expression is neutral but conveys a sense of inner strength and quiet confidence. The lighting is soft, creating a warm and inviting atmosphere, with a slight ethereal glow from the blue lights.

**Image Generation Prompt**

"Create a portrait of a Black woman with long dark dreadlocks, some strands adorned with sparkling blue hair tinsel. She wears a black t-shirt and a dark-colored cardigan. She has multiple necklaces with various pendants: including a coin, a crystal tassel, and other geometric shapes. She's wearing several rings with a blue iridescent shimmer, as well as thin metal bracelets. Her hands are clasped gently. Use soft, warm lighting to evoke a mood of serene confidence and subtle mysticism. The background should be a dark, subtly textured grey. Use a shallow depth of field to keep the subject in sharp focus."


=== File: examples/characters/analysis/digital_monk/metadata.json ===
{
  "prompt": "Describe this image in detail, focusing on visual elements, style, composition, and mood. Create a prompt that could be used to generate a similar image.",
  "script": "analyze",
  "model": "gemini-2.0-flash-exp",
  "timestamp": "2025-08-18T10:21:56.088370",
  "output_path": "examples/characters/analysis/digital_monk",
  "source_image": "examples/characters/digital_monk.png",
  "generated_prompt": "Here's a detailed description of the image, followed by a prompt to generate a similar image:\n\n**Image Description:**\n\nThe image is a studio portrait of a young man with a shaved head, likely a monk or someone practicing a related spiritual discipline. The composition is centered, with the man occupying the majority of the frame. He's dressed in a dark, traditional robe with wide sleeves and a folded neckline. Around his neck, he wears a string of brown wooden beads with a rectangular metallic pendant attached.\n\nHis hands are clasped gently in front of him, near his waist. His expression is serene and introspective; his eyes are cast downwards, suggesting contemplation. The lighting is soft and focused, creating a subtle glow around his head and shoulders, while the rest of the background fades into a deep, rich brown, almost black. This lighting effect emphasizes his face and posture, drawing the viewer's attention to his inner peace and stillness.\n\nThe overall style is clean and modern, despite the traditional attire and spiritual theme. The colors are muted, primarily black, brown, and beige, which contributes to the mood of tranquility and solemnity.\n\n**Prompt:**\n\n\"Studio portrait of a young Asian man with a shaved head, wearing a black traditional robe, facing forward, looking down with a serene expression. He wears a brown wooden mala necklace with a rectangular pendant. Soft, focused lighting with a subtle halo effect around his head, fading to a dark brown background. Introspective, tranquil mood. Modern photography style.\"\n"
}

=== File: examples/characters/analysis/digital_monk/prompt.txt ===
Here's a detailed description of the image, followed by a prompt to generate a similar image:

**Image Description:**

The image is a studio portrait of a young man with a shaved head, likely a monk or someone practicing a related spiritual discipline. The composition is centered, with the man occupying the majority of the frame. He's dressed in a dark, traditional robe with wide sleeves and a folded neckline. Around his neck, he wears a string of brown wooden beads with a rectangular metallic pendant attached.

His hands are clasped gently in front of him, near his waist. His expression is serene and introspective; his eyes are cast downwards, suggesting contemplation. The lighting is soft and focused, creating a subtle glow around his head and shoulders, while the rest of the background fades into a deep, rich brown, almost black. This lighting effect emphasizes his face and posture, drawing the viewer's attention to his inner peace and stillness.

The overall style is clean and modern, despite the traditional attire and spiritual theme. The colors are muted, primarily black, brown, and beige, which contributes to the mood of tranquility and solemnity.

**Prompt:**

"Studio portrait of a young Asian man with a shaved head, wearing a black traditional robe, facing forward, looking down with a serene expression. He wears a brown wooden mala necklace with a rectangular pendant. Soft, focused lighting with a subtle halo effect around his head, fading to a dark brown background. Introspective, tranquil mood. Modern photography style."


=== File: examples/characters/analysis/hooded_cybermancer/metadata.json ===
{
  "prompt": "Describe this image in detail, focusing on visual elements, style, composition, and mood. Create a prompt that could be used to generate a similar image.",
  "script": "analyze",
  "model": "gemini-2.0-flash-exp",
  "timestamp": "2025-08-18T10:22:04.843455",
  "output_path": "examples/characters/analysis/hooded_cybermancer",
  "source_image": "examples/characters/hooded_cybermancer.png",
  "generated_prompt": "Here's a description of the image, followed by a prompt you could use to generate a similar image:\n\n**Image Description:**\n\nThis is a studio portrait of an Asian woman, presented in a medium shot, from the chest up. She wears a black, hooded sweatshirt, with the hood pulled up, partially obscuring her hair. She gazes directly at the viewer with a serious and intense expression. \n\nHer clothing is dark, almost monochrome, adding to the overall mood of mystery. She is also wearing a black leather glove on one hand, and the index finger of that hand is raised and seems to have some sort of intricate, ornate design or tattoo on it. A thin wire is visible, seemingly connected to a small, bright point on the sweatshirt just below her right shoulder, suggesting a technological or cyberpunk element.\n\nThe lighting is diffused, casting soft shadows and highlighting her face. The background is a gradient of grey, further emphasizing the subject and creating a sense of isolation. The style appears to be leaning towards a gritty, contemporary aesthetic, with hints of futuristic or cyberpunk themes. The composition is balanced, with the subject positioned centrally. The mood is serious, perhaps even a little ominous, hinting at a hidden identity or purpose.\n\n**Prompt for a Similar Image:**\n\n\"Studio portrait. An Asian woman in her 30s wearing a black hooded sweatshirt and leather gloves. Her index finger is raised and displays a complex, ornate design. One glove is on. A thin wire leads to a small, glowing light on her chest. Serious expression, looking directly at the camera. Dark, gradient grey background. Cyberpunk, gritty, mysterious atmosphere. Dramatic lighting.  Medium shot.\"\n"
}

=== File: examples/characters/analysis/hooded_cybermancer/prompt.txt ===
Here's a description of the image, followed by a prompt you could use to generate a similar image:

**Image Description:**

This is a studio portrait of an Asian woman, presented in a medium shot, from the chest up. She wears a black, hooded sweatshirt, with the hood pulled up, partially obscuring her hair. She gazes directly at the viewer with a serious and intense expression. 

Her clothing is dark, almost monochrome, adding to the overall mood of mystery. She is also wearing a black leather glove on one hand, and the index finger of that hand is raised and seems to have some sort of intricate, ornate design or tattoo on it. A thin wire is visible, seemingly connected to a small, bright point on the sweatshirt just below her right shoulder, suggesting a technological or cyberpunk element.

The lighting is diffused, casting soft shadows and highlighting her face. The background is a gradient of grey, further emphasizing the subject and creating a sense of isolation. The style appears to be leaning towards a gritty, contemporary aesthetic, with hints of futuristic or cyberpunk themes. The composition is balanced, with the subject positioned centrally. The mood is serious, perhaps even a little ominous, hinting at a hidden identity or purpose.

**Prompt for a Similar Image:**

"Studio portrait. An Asian woman in her 30s wearing a black hooded sweatshirt and leather gloves. Her index finger is raised and displays a complex, ornate design. One glove is on. A thin wire leads to a small, glowing light on her chest. Serious expression, looking directly at the camera. Dark, gradient grey background. Cyberpunk, gritty, mysterious atmosphere. Dramatic lighting.  Medium shot."


=== File: examples/characters/analysis/neon_occultist/metadata.json ===
{
  "prompt": "Describe this image in detail, focusing on visual elements, style, composition, and mood. Create a prompt that could be used to generate a similar image.",
  "script": "analyze",
  "model": "gemini-2.0-flash-exp",
  "timestamp": "2025-08-18T10:22:13.691859",
  "output_path": "examples/characters/analysis/neon_occultist",
  "source_image": "examples/characters/neon_occultist.png",
  "generated_prompt": "Here's a detailed description of the image and a corresponding prompt:\n\n**Image Description**\n\nThe image is a close-up portrait of a serious-looking Black man, positioned centrally within the frame. He is wearing dark, futuristic-looking sunglasses that obscure his eyes. He has short, neatly groomed hair and light stubble.\n\nHe is dressed in a black T-shirt covered by a black leather jacket with a hood. The jacket is detailed with subtle geometric patterns. Bright cyan blue neon lights run along the edges of the jacket, adding a cyberpunk aesthetic. He also wears two delicate gold chain necklaces, each with a small pendant. One pendant is a turquoise-blue square shape, the other is a glowing pink triangle. There is also a small star design tattooed near his left ear, with hints of blue around it.\n\nThe lighting is dramatic. There is a cool-toned light illuminating the left side of his face and jacket, contrasting with the warmer tone on the right. The background is a smooth gradient, transitioning from dark at the top to a lighter shade around the subject's mid-section. This helps to isolate the subject and create a sense of depth.\n\nThe overall mood is serious, intense, and futuristic. The combination of leather, neon, and geometric shapes creates a distinct cyberpunk vibe.\n\n**Prompt for a Similar Image**\n\n\"Close-up portrait of a stoic, handsome Black man with short hair and stubble. He wears dark, futuristic sunglasses. He is wearing a black leather hooded jacket with subtle geometric patterns and neon blue highlights along the seams. Underneath, he wears a plain black T-shirt with two thin gold necklaces, one with a turquoise-blue square pendant and the other with a glowing pink triangle. Cyberpunk style, dramatic cool and warm lighting, smooth gradient background. Mood: intense, futuristic.\"\n"
}

=== File: examples/characters/analysis/neon_occultist/prompt.txt ===
Here's a detailed description of the image and a corresponding prompt:

**Image Description**

The image is a close-up portrait of a serious-looking Black man, positioned centrally within the frame. He is wearing dark, futuristic-looking sunglasses that obscure his eyes. He has short, neatly groomed hair and light stubble.

He is dressed in a black T-shirt covered by a black leather jacket with a hood. The jacket is detailed with subtle geometric patterns. Bright cyan blue neon lights run along the edges of the jacket, adding a cyberpunk aesthetic. He also wears two delicate gold chain necklaces, each with a small pendant. One pendant is a turquoise-blue square shape, the other is a glowing pink triangle. There is also a small star design tattooed near his left ear, with hints of blue around it.

The lighting is dramatic. There is a cool-toned light illuminating the left side of his face and jacket, contrasting with the warmer tone on the right. The background is a smooth gradient, transitioning from dark at the top to a lighter shade around the subject's mid-section. This helps to isolate the subject and create a sense of depth.

The overall mood is serious, intense, and futuristic. The combination of leather, neon, and geometric shapes creates a distinct cyberpunk vibe.

**Prompt for a Similar Image**

"Close-up portrait of a stoic, handsome Black man with short hair and stubble. He wears dark, futuristic sunglasses. He is wearing a black leather hooded jacket with subtle geometric patterns and neon blue highlights along the seams. Underneath, he wears a plain black T-shirt with two thin gold necklaces, one with a turquoise-blue square pendant and the other with a glowing pink triangle. Cyberpunk style, dramatic cool and warm lighting, smooth gradient background. Mood: intense, futuristic."


=== File: examples/characters/cyber_witch.txt ===
Create a portrait of a Black woman with long dark dreadlocks, some strands adorned with sparkling blue hair tinsel. She wears a black t-shirt and a dark-colored cardigan. She has multiple necklaces with various pendants: including a coin, a crystal tassel, and other geometric shapes. She's wearing several rings with a blue iridescent shimmer, as well as thin metal bracelets. Her hands are clasped gently. Use soft, warm lighting to evoke a mood of serene confidence and subtle mysticism. The background should be a dark, subtly textured grey. Use a shallow depth of field to keep the subject in sharp focus.

=== File: examples/characters/digital_monk.txt ===
Studio portrait of a young Asian man with a shaved head, wearing a black traditional robe, facing forward, looking down with a serene expression. He wears a brown wooden mala necklace with a rectangular pendant. Soft, focused lighting with a subtle halo effect around his head, fading to a dark brown background. Introspective, tranquil mood. Modern photography style.

=== File: examples/characters/hooded_cybermancer.txt ===
Studio portrait. An Asian woman in her 30s wearing a black hooded sweatshirt and leather gloves. Her index finger is raised and displays a complex, ornate design. One glove is on. A thin wire leads to a small, glowing light on her chest. Serious expression, looking directly at the camera. Dark, gradient grey background. Cyberpunk, gritty, mysterious atmosphere. Dramatic lighting. Medium shot.

=== File: examples/characters/neon_occultist.txt ===
Close-up portrait of a stoic, handsome Black man with short hair and stubble. He wears dark, futuristic sunglasses. He is wearing a black leather hooded jacket with subtle geometric patterns and neon blue highlights along the seams. Underneath, he wears a plain black T-shirt with two thin gold necklaces, one with a turquoise-blue square pendant and the other with a glowing pink triangle. Cyberpunk style, dramatic cool and warm lighting, smooth gradient background. Mood: intense, futuristic.

=== File: examples/matrix_demo.yml ===
matrix:
  subject:
    - cloaked archivist in neon-lit library
    - cyber-witch casting holographic spells
  setting:
    - abandoned server farm filled with fog
    - gothic cathedral with digital stained glass
  mood:
    - ominous anticipation, something watching
    - melancholic beauty, faded grandeur
  lighting:
    - harsh neon cutting through shadows
    - soft bioluminescent glow, organic tech
  atmosphere:
    - electric tension, reality feels unstable
    - dreamlike calm, otherworldly peace
  audio:
    - synthetic ambient, distant machinery
    - ethereal tones, digital wind chimes


=== File: examples/references/README.md ===
# Reference Images for Style Testing

Reference images for testing different moods/styles with the same scene using `ref_image_lab` script.

## Usage

```bash
uv run -m veo_lab.ref_image_lab --ref-dir examples/references/ --scene examples/basic_prompt.txt
```

## Expected Images

These should show different atmospheric approaches to the cyberpunk occult aesthetic:

- **neon_server_room.jpg** - Bright cyberpunk data center atmosphere
- **occult_ritual_space.jpg** - Dark mystical environment 
- **digital_corruption.jpg** - Glitched, distorted aesthetic
- **ethereal_glow.jpg** - Soft, otherworldly lighting

Each image will influence how the scene from `basic_prompt.txt` is rendered, testing different visual approaches.

=== File: examples/storyboard_demo.json ===
{
  "title": "Digital Séance",
  "shots": [
    {
      "id": "ritual_01",
      "prompt": "Subject: ancient ritual circle projected as hologram\nAction: symbols slowly rotate and pulse\nStyle: occult cyberpunk, ethereal blue light\nCamera: overhead view, sacred geometry emphasized\nAmbience: darkened room, technology and mysticism merged\nAudio: electronic chanting, data streams",
      "negative": "bright lighting, cheerful atmosphere"
    },
    {
      "id": "ritual_02", 
      "prompt": "Subject: ghostly figure materializes in digital static\nAction: form solidifies from glitched pixels\nStyle: haunting beauty, digital corruption aesthetic\nCamera: medium shot, figure emerging from noise\nAmbience: reality glitching, spectral presence\nAudio: digital whispers, phantom voices",
      "carry_last_frame": true
    }
  ]
}

