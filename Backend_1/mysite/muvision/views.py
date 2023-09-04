from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from PIL import Image
from .functions.image_reader import image_reader
from .functions.latex import write_latex
from .functions.classification import classify


def index(request):
    return HttpResponse(f"Hello, world. Youre at the muvision index.")


def classify_image(request):
    if request.method == "POST":
        print(request.FILES['image'])
        image_file = Image.open(request.FILES['image'])
        document_string = image_reader(image_file)
        #document = write_latex(document_string)
        return HttpResponse(f"{document_string}")
    return HttpResponse(f"Hello, world. Youre at the classification page. Please make a post request with the image in the body")