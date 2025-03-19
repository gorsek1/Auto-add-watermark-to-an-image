import os
from PIL import Image
import glob

# ===== USER CONFIGURATION =====
# Watermark size as percentage of image size
# This determines how large the watermark will be relative to the image
# Higher values make watermark larger, smaller values make it smaller
WATERMARK_SIZE_PERCENT = 1.5  # 150% of image width 

# Minimum and maximum watermark sizes to prevent extremes
MIN_WATERMARK_WIDTH = 400  # Minimum width in pixels
MAX_WATERMARK_WIDTH = 3200  # Maximum width in pixels

# Fixed margin in pixels - will use these exact values regardless of image size
# Higher values place the watermark further from the edges
MARGIN_X_PIXELS = 20  # 20 pixels from right edge
MARGIN_Y_PIXELS = 20  # 20 pixels from bottom edge

# Maximum watermark coverage percentage
# Prevents watermark from covering too much of small images
MAX_COVERAGE_PERCENT = 0.5  # Maximum 50% of image width for small images

# Folder paths
INPUT_FOLDER = "To be watermarked"
OUTPUT_FOLDER = "Watermarked"
# ==============================

def add_watermark(image_path, watermark_path, output_path=None):
    # Open the original image
    img = Image.open(image_path).convert("RGBA")
    
    # Open the watermark
    watermark = Image.open(watermark_path).convert("RGBA")
    
    # Get the dimensions of the image
    img_width, img_height = img.size
    
    # Calculate the dimensions for the watermark based on image size
    base_watermark_width = int(img_width * WATERMARK_SIZE_PERCENT)
    
    # Adjust for very small or very large images
    watermark_width = max(MIN_WATERMARK_WIDTH, min(base_watermark_width, MAX_WATERMARK_WIDTH))
    
    # For small images, make sure watermark doesn't exceed MAX_COVERAGE_PERCENT of width
    max_allowed_width = int(img_width * MAX_COVERAGE_PERCENT)
    if watermark_width > max_allowed_width:
        watermark_width = max_allowed_width
    
    # Calculate height while maintaining aspect ratio
    watermark_ratio = watermark.width / watermark.height
    watermark_height = int(watermark_width / watermark_ratio)
    
    # Check if watermark is larger than the image and scale down if necessary
    if watermark_width > img_width - (2 * MARGIN_X_PIXELS):
        watermark_width = img_width - (2 * MARGIN_X_PIXELS)
        watermark_height = int(watermark_width / watermark_ratio)
    
    if watermark_height > img_height - (2 * MARGIN_Y_PIXELS):
        watermark_height = img_height - (2 * MARGIN_Y_PIXELS)
        watermark_width = int(watermark_height * watermark_ratio)
    
    # Resize the watermark
    watermark = watermark.resize((watermark_width, watermark_height), Image.LANCZOS)
    
    # Calculate position (bottom-right corner)
    # Use fixed pixel margins instead of percentage-based
    x_position = img_width - watermark_width - MARGIN_X_PIXELS
    y_position = img_height - watermark_height - MARGIN_Y_PIXELS
    
    # Ensure watermark stays within image boundaries
    x_position = max(0, x_position)
    y_position = max(0, y_position)
    
    # Final position
    position = (x_position, y_position)
    
    # Create a new transparent image the same size as the original
    transparent = Image.new('RGBA', img.size, (0, 0, 0, 0))
    
    # Paste the watermark onto the transparent image
    transparent.paste(watermark, position, watermark)
    
    # Combine the original image with the watermark
    watermarked_img = Image.alpha_composite(img.convert("RGBA"), transparent)
    
    # Convert back to RGB if the original was RGB
    if Image.open(image_path).mode == 'RGB':
        watermarked_img = watermarked_img.convert('RGB')
    
    # Save the watermarked image
    if output_path:
        watermarked_img.save(output_path)
    else:
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
        
        # Get the filename without path
        filename = os.path.basename(image_path)
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        
        # Determine the output format
        if filename.lower().endswith('.webp'):
            watermarked_img.save(output_path, 'WEBP')
        else:
            watermarked_img.save(output_path)
    
    # Return additional info for reporting
    coverage_percent = (watermark_width / img_width) * 100
    position_info = f"{MARGIN_Y_PIXELS}px from bottom, {MARGIN_X_PIXELS}px from right"
    relative_size = f"{watermark_width}x{watermark_height} px ({coverage_percent:.1f}% of width)"
    
    return output_path, watermark_width, coverage_percent, position_info, relative_size

def main():
    # Path to watermark image - check for specific file first
    watermark_path = None
    
    # First, check if the specific watermark file exists
    if os.path.exists('Watermark_Transparent_Final.png'):
        watermark_path = 'Watermark_Transparent_Final.png'
    else:
        # Look for any watermark template in the current directory
        for file in os.listdir('.'):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')) and 'watermark' in file.lower():
                watermark_path = file
                break
    
    if not watermark_path:
        print("Watermark template not found. Please ensure there's an image with 'watermark' in its filename.")
        return
    
    print(f"Using {watermark_path} as watermark template.")
    print(f"Watermark settings: Base size={WATERMARK_SIZE_PERCENT*100}% of image width (max {MAX_COVERAGE_PERCENT*100}%)")
    print(f"Position: Fixed at {MARGIN_Y_PIXELS}px from bottom, {MARGIN_X_PIXELS}px from right")
    
    # Create the input folder if it doesn't exist
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"Created input folder: {INPUT_FOLDER}")
        print(f"Please place your images in the '{INPUT_FOLDER}' folder and run the script again.")
        input("Press Enter to exit...")
        return
        
    # Check if the input folder is empty
    if not os.listdir(INPUT_FOLDER):
        print(f"No images found in the '{INPUT_FOLDER}' folder.")
        print(f"Please place your images in the '{INPUT_FOLDER}' folder and run the script again.")
        input("Press Enter to exit...")
        return
    
    # Get all images in the input directory
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp']
    image_files = []
    
    for extension in image_extensions:
        found_files = glob.glob(os.path.join(INPUT_FOLDER, extension))
        if found_files:
            image_files.extend(found_files)
    
    # Filter out any watermark files
    exclude_terms = ['watermark']
    filtered_image_files = []
    
    for img in image_files:
        # Skip any file with 'watermark' in the name
        if any(term in os.path.basename(img).lower() for term in exclude_terms):
            continue
            
        filtered_image_files.append(img)
    
    if not filtered_image_files:
        print(f"No valid images found in the '{INPUT_FOLDER}' folder.")
        print(f"Please place your images in the '{INPUT_FOLDER}' folder and run the script again.")
        input("Press Enter to exit...")
        return
    
    print(f"Found {len(filtered_image_files)} images to watermark:")
    for img in filtered_image_files:
        print(f"- {os.path.basename(img)}")
    print("")
    
    # Process each image
    image_details = []
    for image_path in filtered_image_files:
        try:
            output_path, used_width, coverage, position_info, relative_size = add_watermark(image_path, watermark_path)
            img_size = Image.open(image_path).size
            image_details.append((os.path.basename(image_path), img_size, relative_size, position_info))
            print(f"Added watermark to {os.path.basename(image_path)} -> {output_path}")
        except Exception as e:
            print(f"Error processing {os.path.basename(image_path)}: {e}")
    
    print(f"\nWatermarking complete! {len(filtered_image_files)} images processed.")
    print(f"Watermarked images are saved in the '{OUTPUT_FOLDER}' folder.")
    
    # Display detailed sizing information
    print("\nImage size information:")
    for name, size, watermark_size, position_info in image_details:
        print(f"- {name}: Image size {size[0]}x{size[1]}, Watermark: {watermark_size}, Position: {position_info}")

if __name__ == "__main__":
    main() 