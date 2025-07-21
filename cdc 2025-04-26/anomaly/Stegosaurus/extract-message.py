from PIL import Image
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'meme.png')

def binary_to_text(binary_data):
    # Convert binary data to text
    return "".join(
        chr(
            int(
                binary_data[i:i+8], 2
            )
        ) for i in range(0, len(binary_data), 8)
    )

def extract_lsb(image_path):
    # Open the image file
    img = Image.open(image_path)
    pixels = list(img.getdata())  # Get RGB values

    print (f"Len(pixels): {len(pixels)}")

    # Extract LSBs from each color channel
    lsb_data = ""
    for pixel in pixels:
        for color_value in pixel[:3]:  # RGB channels
            lsb_data += str(color_value & 1)  # Get LSB
            if len(lsb_data) % 8 == 0:
                print(f"Last 8 bits: " +
                      f"{lsb_data[-8:]} -> {binary_to_text(lsb_data[-8:])}")
            if len(lsb_data) % 10000 == 0:
                print(f"Length(lsb_data): {len(lsb_data)}")
        if len(lsb_data) >= 1000:
            break


    # Use the function to convert binary data to text
    hidden_message = binary_to_text(lsb_data)
    return hidden_message

if __name__ == "__main__":
    print(extract_lsb(image_path))
