from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import  Upload


#importing loading from django template  
from django.template import loader  
# Create your views here.  
from django.http import HttpResponse  
from .forms import UploadForm
def index(request):
    if request.method == 'POST': 
        form = UploadForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('result')
    else: 
        form = UploadForm()  
    return render(request, 'home.html', {'form': form})
 


def result(request):  

  
      image = Upload.objects.latest('created')
        # entries= Upload.objects.all()
        # entries.delete()
      return render(request, 'result.html', 
                     {'upload' : image})