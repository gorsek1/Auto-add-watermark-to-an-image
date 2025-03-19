# Image Watermark Tool

A robust Python utility to automatically add watermarks to images while maintaining consistent positioning and appropriate sizing.

## Features

- **Batch processing**: Automatically watermarks all images in a designated folder
- **Consistent positioning**: Places watermarks in the exact same position (bottom-right corner) on all images
- **Smart sizing**: Scales watermarks proportionally based on image dimensions
- **Multiple format support**: Works with JPG, JPEG, PNG, BMP, TIFF, and WebP formats
- **Easy to use**: Simple double-click batch file to run the script
- **Highly configurable**: Easily adjust watermark size, position, and constraints

## Installation

### Requirements
- Python 3.x
- Pillow (PIL fork) library

### Setup
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/image-watermark-tool.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
1. Place your watermark image in the same folder as the script
   - The script looks for `Watermark_Transparent_Final.png` by default
   - Alternatively, any image with "watermark" in the filename will work

2. Place the images you want to watermark in the "To be watermarked" folder

3. Run the script:
   - Double-click `watermark.bat` file (Windows)
   - Or run from command line: `python watermark.py`

4. Find your watermarked images in the "Watermarked" folder

### Configuration

Open `watermark.py` and adjust these parameters:

```python
# Watermark size as percentage of image width
WATERMARK_SIZE_PERCENT = 1.5  # 150% of image width 

# Minimum and maximum watermark sizes
MIN_WATERMARK_WIDTH = 400  # Minimum width in pixels
MAX_WATERMARK_WIDTH = 3200  # Maximum width in pixels

# Fixed margins (pixels from edges)
MARGIN_X_PIXELS = 20  # 20 pixels from right edge
MARGIN_Y_PIXELS = 20  # 20 pixels from bottom edge

# Maximum coverage for small images
MAX_COVERAGE_PERCENT = 0.5  # Maximum 50% of image width
```

## How It Works

1. The script scans for images in the "To be watermarked" folder
2. For each image:
   - Calculates the appropriate watermark size based on image dimensions
   - Positions the watermark exactly at the configured distance from edges
   - Creates a transparent layer for the watermark
   - Applies the watermark and saves to the output folder
3. Detailed information about each processed image is displayed

## Examples

Before | After
:-----:|:-----:
Original Image | Image with Watermark
Text-heavy Image | Text-heavy Image with Watermark
Photo | Photo with Watermark

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Pillow](https://python-pillow.org/) for image processing capabilities
