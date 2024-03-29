from django.db import models
from .utils import get_filtered_image
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

ACTION_CHOICES = (
    
    
    ('CARTOON STYLE1', 'CARTOON STYLE1'),
    ('CARTOON STYLE2', 'CARTOON STYLE2'),
    ('CARTOON STYLE3', 'CARTOON STYLE3'),
    ('CARTOON STYLE4', 'CARTOON STYLE4'),
    
)

class Upload(models.Model):
    image = models.ImageField(default='default.jpg', upload_to='images/')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
    
        # open image
        pil_img = Image.open(self.image)
        
        # convert the image to array
        cv_image = np.array(pil_img)
        img = get_filtered_image(cv_image, self.action)
        
        im_pil = Image.fromarray(img)
        
        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_jpg = buffer.getvalue()
        
        self.image.save(str(self.image), ContentFile(image_jpg), save=False)
        
        super().save(args, **kwargs)