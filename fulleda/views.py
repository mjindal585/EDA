from django.shortcuts import render ,  redirect
from django.core.files.storage import FileSystemStorage
import pandas as pd
from pandas_profiling import ProfileReport
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
save_url = ''

def simple_frame(request):
    return render(request, 'eda/'+ save_url)

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        ext = uploaded_file_url.split('.')[-1]
        save_url = uploaded_file_url.split('.')[0]+".html"
        if ext == 'csv':
            data = pd.read_csv(uploaded_file_url)
            profile = ProfileReport(data)
            profile.to_file(output_file=save_url)

        elif ext == 'txt' or ext == 'tsv':
            data = pd.read_csv(uploaded_file_url , separator = '\t')
            profile = ProfileReport(data)
            profile.to_file(output_file=save_url)

        elif ext == 'xlsx':
            data = pd.read_excel(uploaded_file_url)
            profile = ProfileReport(data)
            profile.to_file(output_file=save_url)

        else :
            messages.success(request, 'Invalid File Format!')
            return render(request,'invalid.html')
        print(save_url)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url , 'ext' : ext , 'save_url' : save_url
        })
    return render(request, 'simple_upload.html')