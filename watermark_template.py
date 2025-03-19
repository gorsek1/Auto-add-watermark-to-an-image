from PIL import Image, ImageDraw, ImageFont
import os

def create_watermark_template():
    # Create a transparent image for the watermark
    width, height = 400, 100
    watermark = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # Get a drawing context
    draw = ImageDraw.Draw(watermark)
    
    # Try to use a default font or create text without a specific font
    try:
        # Try to find a font on the system
        font_size = 50
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # If arial is not available, try a default font
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Add text with semi-transparent white
        text = "iskrex.com"
        
        # Get text dimensions - handle both newer and older Pillow versions
        if hasattr(draw, 'textbbox'):
            # For newer Pillow versions
            _, _, text_width, text_height = draw.textbbox((0, 0), text, font=font)
            position = ((width - text_width) // 2, (height - text_height) // 2)
        elif hasattr(draw, 'textsize'):
            # For older Pillow versions
            text_width, text_height = draw.textsize(text, font=font)
            position = ((width - text_width) // 2, (height - text_height) // 2)
        else:
            # Fallback position if neither method is available
            position = (width//4, height//3)
        
        # Draw semi-transparent white text
        draw.text(position, text, fill=(255, 255, 255, 180), font=font)
    except Exception as e:
        print(f"Error creating text with font: {e}")
        
        # Fallback to simple text without specific font
        draw.text((width//4, height//3), "iskrex.com", fill=(255, 255, 255, 180))
    
    # Save the watermark
    watermark.save("watermark_template.png")
    print(f"Watermark template created: {os.path.abspath('watermark_template.png')}")

if __name__ == "__main__":
    create_watermark_template() 