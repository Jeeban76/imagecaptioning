from django.shortcuts import render, redirect
from .models import ImageModel
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

def home(request):
    if request.method == 'POST' and request.FILES['image']:
        # Save the uploaded image
        image_file = request.FILES['image']
        image = ImageModel(image=image_file)
        image.save()

        # Generate caption
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        img = Image.open(image_file).convert('RGB')
        inputs = processor(img, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)

        # Save the caption
        image.caption = caption
        image.save()

        return render(request, 'captiongen/home.html', {'image': image})

    return render(request, 'captiongen/home.html')