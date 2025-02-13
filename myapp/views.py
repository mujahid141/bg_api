import base64
from io import BytesIO
from PIL import Image
from rembg import remove
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def remove_bg(request):
    try:
        data = request.data.get('image')
        if not data:
            return Response({'error': 'No image provided'}, status=400)

        # Decode base64 to image
        image_data = base64.b64decode(data)
        image = Image.open(BytesIO(image_data))

        # Remove background
        output_image = remove(image)

        # Convert output image to base64
        buffered = BytesIO()
        output_image.save(buffered, format="PNG")
        encoded_output = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return Response({'image': encoded_output})
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)
