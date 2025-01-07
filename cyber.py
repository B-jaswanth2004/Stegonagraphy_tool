from PIL import Image

def encode_image(image_path, message, output_path):
    # Open the image
    image = Image.open(image_path)
    encoded_image = image.copy()
    width, height = image.size
    
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '11111111'  # End marker
    data_index = 0

    # Iterate over pixels
    for y in range(height):
        for x in range(width):
            # Get the pixel
            pixel = list(encoded_image.getpixel((x, y)))
            
            # Modify the red channel
            if data_index < len(binary_message):
                pixel[0] = (pixel[0] & ~1) | int(binary_message[data_index])  # Modify LSB
                data_index += 1

            # Update the pixel
            encoded_image.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    # Save the encoded image
    encoded_image.save(output_path)
    print("Message encoded successfully!")

def decode_image(image_path):
    image = Image.open(image_path)
    binary_message = ""
    
    width, height = image.size

    # Iterate over pixels
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            binary_message += str(pixel[0] & 1)  # Get the LSB of the red channel

    # Split binary message into bytes and convert to characters
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if byte == "11111111":  # End marker
            break
        message += chr(int(byte, 2))

    return message

# Example usage
if __name__ == "__main__":
    # Encoding
    encode_image('input_image.png', 'Hello, World!', 'output_image.png')
    
    # Decoding
    decoded_message = decode_image('output_image.png')
    print("Decoded Message:", decoded_message)
