import sys
from PIL import Image
import struct

def convert(input_path, output_path, model="3.5"):
    """
    Resizes an image according to the model ("3.5" or "2.8"), converts it to RGB mode if necessary,
    and saves it as a BMP file.

    Parameters:
    - input_path (str): Path to the input image.
    - output_path (str): Path to save the output BMP image.
    - model (str): If "3.5", resize to 320x480; if "2.8", resize to 320x240. Default is "3.5".
    """
    # 選択されたモデルに応じて解像度を決定
    if model == "3.5":
        width, height = 320, 480
    elif model == "2.8":
        width, height = 240, 320
    elif model == "1.8":
        width, height = 128, 160
    else:
        # 想定外の値ならデフォルトを採用
        print(f"Warning: Unknown model '{model}'. Falling back to default (3.5).")
        width, height = 320, 480

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
    """
    Usage:
        python main.py <operation> <input_file> [output_file] [model]

    Examples:
        # model省略時 (デフォルト3.5) -> 320x480
        python main.py conv input.jpg output.bmp

        # modelに2.8を指定 -> 320x240
        python main.py conv input.jpg output.bmp 2.8

        # modelに1.8を指定 -> 160x128
        python main.py conv input.jpg output.bmp 1.8

        # メタデータ表示
        python main.py show input.bmp
    """
    if len(sys.argv) < 3:
        print("Usage: python main.py <operation> <input_file> [output_file] [model]")
        print("Operations: conv, show")
        return

    operation = sys.argv[1]
    input_path = sys.argv[2]

    if operation == "conv":
        if len(sys.argv) < 4:
            print("Please provide an output file path for conversion.")
            return

        output_path = sys.argv[3]
        # modelパラメータを受け取る。なければ"3.5"をデフォルトとする
        model = sys.argv[4] if len(sys.argv) >= 5 else "3.5"

        convert(input_path, output_path, model)
    elif operation == "show":
        show(input_path)
    else:
        print("Invalid operation. Use 'conv' or 'show'.")

if __name__ == "__main__":
    main()
