from django.shortcuts import render
from PIL import Image
import stepic
import io
import os

# Create your views here.
def home(request):
    return render(request, 'stagenography/base.html')

def hide_text_in_image(image, text):
    # Open the image and validate its format
    image = Image.open(image)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Encode the text into the image using stepic
    encoded_image = stepic.encode(image, text.encode('utf-8'))

    return encoded_image

def hide_text_image(image, text):
    data = text.encode('utf-8')
    return stepic.encode(image, data)

def encryption_view(request):
    message = ""
    encrypted_image = None

    if request.method == "POST":
        text = request.POST['text']
        image_file = request.FILES['image']
        image = Image.open(image_file)

        if image.mode != 'RGB':
            image = image.convert('RGB')

        new_image = hide_text_image(image, text)

        # Construct an absolute path for the image
        image_filename = 'new_' + image_file.name
        image_path = os.path.join(os.getcwd(), 'image', image_filename)

        try:
            # Save the encrypted image as PNG
            new_image.save(image_path, format='PNG')  # Save as PNG format
            encrypted_image = os.path.join('image', image_filename)
            message = "Text has been encrypted in the image"
        except Exception as e:
            message = "Failed to generate the encrypted image: " + str(e)

    return render(request, 'stagenography/encrypt.html', {'message': message, 'encrypted_image': encrypted_image})


def decryption_view(request):
    text = ""
    if request.method == "POST":
        image_file = request.FILES['image']
        image = Image.open(image_file)

        # Check if the image format is supported (e.g., JPEG)
        supported_formats = ('JPEG', 'PNG', 'GIF')  # Add more if needed
        if image.format not in supported_formats:
            return render(request, 'stagenography/decrypt.html', {'error_message': 'Unsupported image format'})

        if image.format != 'PNG':
            image = image.convert('RGBA')
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            image = Image.open(buffer)
        
        text = extract_text_from_image(image)
    
    return render(request, 'stagenography/decrypt.html', {'text': text})

def extract_text_from_image(image):
    decoded_data = stepic.decode(image)
    if isinstance(decoded_data, bytes):
        return decoded_data.decode('utf-8')
    return decoded_data