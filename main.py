import os
import argparse
from PIL import Image, ImageDraw, ImageFont

def validate_spritesheet_name(name: str) -> str:
    """Validates the spritesheet name, ensuring it has a proper .png extension."""
    if not name.lower().endswith(".png"):
        print(f"""\033[1;33m[Warning]: The spritesheet name "{name}" does not have a .png extension. Using "{name}.png" instead.\033[0m""")
        name += ".png"
    return name

def render_font(
    font_path: str,
    output_folder: str,
    characters: str,
    font_size: int = 64,
    padding: tuple = (10, 10, 10, 10),  # (left, top, right, bottom)
    bg_type: str = "transparent",  # "transparent" or "filled"
    export_type: str = "separate",  # "separate" or "spritesheet"
    spritesheet_name: str = "spritesheet.png",  # Custom name for spritesheet
    bg_color: tuple = (255, 255, 255),  # Background color (RGB)
    text_color: tuple = (0, 0, 0)  # Text color (RGB)
):
    """Renders a font and exports characters as separate images or a sprite sheet."""
    
    # Validate spritesheet name
    if export_type == "spritesheet":
        spritesheet_name = validate_spritesheet_name(spritesheet_name)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    images = []
    max_height = 0
    total_width = 0

    for char in characters:
        # Get character dimensions
        char_width, char_height = font.getbbox(char)[2:]
        img_width = char_width + padding[0] + padding[2]
        img_height = char_height + padding[1] + padding[3]

        # Create canvas
        if bg_type == "transparent":
            image = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
        else:
            image = Image.new("RGB", (img_width, img_height), bg_color)

        draw = ImageDraw.Draw(image)
        
        # Define text position
        text_x = padding[0]
        text_y = padding[1]

        # Draw the character
        draw.text((text_x, text_y), char, font=font, fill=text_color)

        if export_type == "separate":
            image.save(os.path.join(output_folder, f"{char}.png"))
        else:
            images.append(image)
            max_height = max(max_height, img_height)
            total_width += img_width

    # Export as a sprite sheet
    if export_type == "spritesheet" and images:
        spritesheet = Image.new(
            "RGBA",
            (total_width, max_height),
            (0, 0, 0, 0) if bg_type == "transparent" else bg_color
        )
        x_offset = 0
        for img in images:
            spritesheet.paste(img, (x_offset, 0), img)
            x_offset += img.width

        spritesheet.save(os.path.join(output_folder, spritesheet_name))

    print("Rendering complete!")


# 🔹 Command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Font rendering tool.")

    parser.add_argument("--font_path", type=str, required=True, help="Path to the font file (TTF).")
    parser.add_argument("--output_folder", type=str, required=True, help="Directory to save images.")
    parser.add_argument("--characters", type=str, required=True, help="Characters to render.")
    parser.add_argument("--font_size", type=int, default=64, help="Font size.")
    parser.add_argument("--padding", type=int, nargs=4, default=[10, 10, 10, 10], help="Padding (left, top, right, bottom).")
    parser.add_argument("--bg_type", type=str, choices=["transparent", "filled"], default="transparent", help="Background type.")
    parser.add_argument("--export_type", type=str, choices=["separate", "spritesheet"], default="separate", help="Export format.")
    parser.add_argument("--spritesheet_name", type=str, default="spritesheet.png", help="Custom name for the spritesheet (must be .png).")
    parser.add_argument("--bg_color", type=int, nargs=3, default=[255, 255, 255], help="Background color (RGB).")
    parser.add_argument("--text_color", type=int, nargs=3, default=[0, 0, 0], help="Text color (RGB).")

    args = parser.parse_args()

    # Run with CLI parameters
    render_font(
        font_path=args.font_path,
        output_folder=args.output_folder,
        characters=args.characters,
        font_size=args.font_size,
        padding=tuple(args.padding),
        bg_type=args.bg_type,
        export_type=args.export_type,
        spritesheet_name=args.spritesheet_name,
        bg_color=tuple(args.bg_color),
        text_color=tuple(args.text_color),
    )
