import os
import argparse
from PIL import Image

def parse_args ():
    
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")

    # Mandatory source argument
    parser.add_argument('source', help='Path of the source image.')

    # Optional max width and height argument
    parser.add_argument(
        'max_size', 
        type = int, 
        nargs = '*',  # Allows 0, 1, or 2 values
        help = 'Max width and height of final ASCII art (provide 1 value for both or 2 for width and height respectively).'
    )

    # Optional mode for brightness calculation
    parser.add_argument(
        '--mode', 
        default = 'average', 
        choices = ['average', 'lightness', 'luminosity'], 
        help = 'Method to map RGB to brightness [average, lightness, luminosity].'
    )

    parser.add_argument(
        '--repeat', 
        type = int, 
        default = 3,
        help = 'How many times to repeat an ASCII character in the final product, since characters are taller than they are wide.'
    )

    # Optional ASCII key string
    parser.add_argument(
        '--key', 
        default = ' `.-\':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@', 
        help = 'Key to translate brightness to ASCII characters (from light to dark).'
    )

    # Optional argument to save as .txt file
    parser.add_argument(
        '--save', 
        action = 'store_true',  # It's a flag, no value needed, just --save
        help = 'Save the ASCII output as a .txt file.'
    )

    args = parser.parse_args()

    # Handle max_size: default to 100x100 if not provided
    if len(args.max_size) == 0:
        width, height = None, None  # Default width and height
    elif len(args.max_size) == 1:
        width, height = args.max_size[0], args.max_size[0]  # Same value for both
    else:
        width, height = args.max_size[0], args.max_size[1]  # Use provided values
    
    return args, width, height

def image_to_ascii(source, width, height, mode, repeat, ascii_key, save):
    if source == None:
        print('No source image specified')
        return -1
    
    # TODO: allow other formats, because RGB is less efficient here
    im = Image.open(source).convert('RGB')
    print(im.format, im.size, im.mode)

    # resize image or use its original size
    if (width != None):    
        im.thumbnail((width, height))
    else:
        width, height = im.size[0], im.size[1]
    
    # Convert pixels to brightness
    brightness_matrix = []
    for pixel in im.getdata():
        brightness = calculate_brightness(pixel, mode)
        brightness_matrix.append(brightness)

    # Reshape brightness_matrix into the original image dimensions
    brightness_matrix = [brightness_matrix[(i * im.width):((i + 1) * im.width)] for i in range(im.height)]

    # Convert to ASCII characters by normalizing to length of key
    ascii_matrix = [[ascii_key[round((brightness / 255) * (len(ascii_key) - 1))] for brightness in row] for row in brightness_matrix]
    
    # Create the ASCII output string
    ascii_output = '\n'.join([''.join([char * repeat for char in row]) for row in ascii_matrix])
    print(ascii_output)
    
    # Save to .txt document
    if save:
        save_ascii(ascii_output, mode, width, height, source)

def calculate_brightness(pixel, mode):
    R, G, B = pixel
    if mode == 'average':
        return (R + G + B) / 3
    elif mode == 'lightness':
        return (max(R, G, B) + min(R, G, B)) / 2
    elif mode == 'luminosity':
        return (0.21 * R + 0.72 * G + 0.07 * B)
    
def save_ascii(output, mode, width, height, source):
    title = f"ascii_{mode}_{width}x{height}_{os.path.basename(source).split('.')[0]}.txt"
    with open(title, 'w') as file:
        file.write(output)

if __name__ == '__main__':
    args, width, height = parse_args()

    # Example usage of the parsed arguments
    print(f"Source: {args.source}")
    print(f"Max Width: {width}, Max Height: {height}")
    print(f"Brightness Mode: {args.mode}")
    print(f"ASCII Key: {args.key}")
    print(f"Save as txt: {args.save}")

    image_to_ascii(args.source, width, height, args.mode, args.repeat, args.key, args.save)