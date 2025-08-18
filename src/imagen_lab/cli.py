from __future__ import annotations

import pathlib
from typing import Annotated

import typer

from imagen_lab.common import create_client
from imagen_lab.common import create_output_path
from imagen_lab.common import list_models
from imagen_lab.common import save_generated_image
from imagen_lab.common import save_metadata
from imagen_lab.common import save_prompt_file

app = typer.Typer(
    name="imagen_lab",
    help="Image generation lab using Google's Imagen API",
    no_args_is_help=True,
)


@app.command()
def generate(
    prompt: Annotated[str, typer.Argument(help="Text prompt for image generation")],
    model: Annotated[
        str | None, typer.Option("--model", "-m", help="Model to use for generation")
    ] = None,
    output: Annotated[
        pathlib.Path | None,
        typer.Option("--output", "-o", help="Custom output directory"),
    ] = None,
    custom_name: Annotated[
        str | None,
        typer.Option("--name", help="Custom name for output folder"),
    ] = None,
    dry: Annotated[
        bool,
        typer.Option("--dry", help="Show what would be generated without calling API"),
    ] = False,
    list_models_flag: Annotated[
        bool,
        typer.Option("--list-models", help="List known model ids and current default"),
    ] = False,
) -> None:
    """Generate an image from a text prompt using Imagen."""
    import json
    import os
    
    if list_models_flag:
        print(json.dumps(list_models(), indent=2))
        return
        
    # Model selection precedence:
    # 1) Explicit --model argument
    # 2) IMAGEN_MODEL environment variable
    # 3) "imagen-3.0-generate-002" default

    picked_model = model or os.environ.get("IMAGEN_MODEL") or "imagen-3.0-generate-002"

    print(f"Generating image: {prompt}")
    print(f"Model: {picked_model}")

    # Create output path (but don't create directory for dry run)
    output_path = create_output_path("imagen", prompt, output, custom_name)
    print(f"Output: {output_path}")

    if dry:
        print("🔍 Dry run - showing what would be generated:")
        print(f"  • Prompt: {prompt}")
        print(f"  • Model: {picked_model}")
        print(f"  • Output directory: {output_path}")
        print(f"  • Image file: {output_path.name}.jpg")
        print("  • Would create: prompt.txt, metadata.json")
        print("✅ Dry run complete - no API calls made")
        return

    # Real execution: create directory and client
    output_path.mkdir(parents=True, exist_ok=True)
    client = create_client()

    try:
        # Generate image
        response = client.models.generate_images(model=picked_model, prompt=prompt)

        # Save files
        image_filename = f"{output_path.name}.jpg"
        image_path = save_generated_image(response, output_path, image_filename)
        save_prompt_file(output_path, prompt)
        save_metadata(output_path, prompt, "imagen", picked_model)

        print(f"✅ Generated: {image_path}")

    except Exception as e:
        print(f"❌ Generation failed: {e}")
        raise typer.Exit(1)


@app.command()
def analyze(
    image_path: Annotated[pathlib.Path, typer.Argument(help="Path to image file")],
    model: Annotated[
        str, typer.Option("--model", "-m", help="Vision model to use for analysis")
    ] = "gemini-2.0-flash-exp",
    output: Annotated[
        pathlib.Path | None,
        typer.Option("--output", "-o", help="Custom output directory"),
    ] = None,
) -> None:
    """Analyze an image and generate a descriptive prompt."""
    if not image_path.exists():
        print(f"❌ Image file not found: {image_path}")
        raise typer.Exit(1)

    print(f"Analyzing image: {image_path}")
    print(f"Model: {model}")

    # Create client and output paths
    client = create_client()
    analysis_prompt = "Describe this image in detail, focusing on visual elements, style, composition, and mood. Create a prompt that could be used to generate a similar image."

    output_path = create_output_path("analyze", f"analysis_of_{image_path.stem}", output)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Output: {output_path}")

    try:
        # Read and analyze image
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Create image part using genai types
        from google.genai import types

        image_part = types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_data))

        response = client.models.generate_content(
            model=model, contents=[analysis_prompt, image_part]
        )

        generated_prompt = (
            response.text if hasattr(response, "text") and response.text else str(response)
        )

        # Save analysis results
        save_prompt_file(output_path, generated_prompt)
        save_metadata(
            output_path,
            analysis_prompt,
            "analyze",
            model,
            source_image=str(image_path),
            generated_prompt=generated_prompt,
        )

        print(f"✅ Analysis complete: {output_path}")
        print(f"Generated prompt: {generated_prompt}")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
