import random
import base64
import requests
from PIL import Image
from io import BytesIO
from django.db import models
from user.models import CustomUser as User

class Photo(models.Model):
    b64_photo = models.TextField()

class Container(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    b64_photo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def input(self, text: str) -> None:
        image_data = base64.b64decode(self.b64_photo)
        image = Image.open(BytesIO(image_data))
        size_x, size_y = image.size
        if (len(text) * 8) >= (size_x * size_y):
            raise Exception("A lot of text")
        ascii_bin_bits = ''.join(f'{ord(i):08b}' for i in text)
        bit_index = 0
        total_bits = len(ascii_bin_bits)
        for x in range(size_x):
            for y in range(size_y):
                if bit_index < total_bits:
                    r, g, b = image.getpixel((x, y))
                    r_bin = f'{r:08b}'
                    new_r_bin = r_bin[:-1] + ascii_bin_bits[bit_index]
                    new_r = int(new_r_bin, 2)
                    image.putpixel((x, y), (new_r, g, b))
                    bit_index += 1
                else:
                    break
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        self.b64_photo = base64.b64encode(buffered.getvalue()).decode("utf-8")
        self.save()
    
    @staticmethod
    def get_base_photo() -> str:
        categories = ['nature', 'city', 'technology', 'food', 'still_life', 'abstract', 'wildlife']
        category = random.choice(categories)
        api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
        response = requests.get(api_url, headers={'X-Api-Key': 'Q6o1+pZlO5zsuirrPraOUw==pwASF3iH8NcglPfT', 'Accept': 'image/jpg'}, stream=True)
        if response.status_code == requests.codes.ok:
            image_data = response.content
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            new_photo = Photo(
                b64_photo = encoded_image
            )
            new_photo.save()
            return encoded_image
        else:
            random_photo = Photo.objects.order_by('?').first()
            if not random_photo:
                raise Exception("There are no photos available.")
            return random_photo
