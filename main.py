import sys
from PIL import Image
import struct

def convert(input_path, output_path, width=320, height=480):
    """
    Resizes an image to the specified width and height, converts it to RGB mode if necessary,
    and saves it as a BMP file.

    Parameters:
    - input_path (str): Path to the input image.
    - output_path (str): Path to save the output BMP image.
    - width (int): Width to resize the image to (default is 320).
    - height (int): Height to resize the image to (default is 480).
    """
    # Open the original image
    image = Image.open(input_path)

    # Resize the image
    resized_image = image.resize((width, height), Image.Resampling.LANCZOS)

    # Convert to RGB mode if necessary
    if resized_image.mode != 'RGB':
        resized_image = resized_image.convert('RGB')

    # Save the image as a BMP file
    resized_image.save(output_path, format='BMP')
    print(f"Image saved as BMP at: {output_path}")

def show(file_path):
    """
    Displays metadata of a BMP file, including dimensions, header info, etc.

    Parameters:
    - file_path (str): Path to the BMP file.
    """
    with open(file_path, 'rb') as bmp_file:
        bmp_data = bmp_file.read()

    # Extract basic BMP metadata (first 54 bytes for header)
    file_size = struct.unpack('<I', bmp_data[2:6])[0]
    width = struct.unpack('<i', bmp_data[18:22])[0]
    height = struct.unpack('<i', bmp_data[22:26])[0]
    bits_per_pixel = struct.unpack('<H', bmp_data[28:30])[0]

    print(f"File: {file_path}")
    print(f"File Size: {file_size} bytes")
    print(f"Width: {width} pixels")
    print(f"Height: {height} pixels")
    print(f"Bits Per Pixel: {bits_per_pixel}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <operation> <input_file> [output_file]")
        print("Operations: conv, show_metadata")
        return

    operation = sys.argv[1]
    input_path = sys.argv[2]

    if operation == "conv":
        if len(sys.argv) < 4:
            print("Please provide an output file path for conversion.")
            return
        output_path = sys.argv[3]
        convert(input_path, output_path)
    elif operation == "show":
        show(input_path)
    else:
        print("Invalid operation. Use 'conv' or 'show'.")

if __name__ == "__main__":
    main()
