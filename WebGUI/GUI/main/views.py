from django.shortcuts import render
from django.http import HttpResponse

tables=[]

# Create your views here.
def main(request):

    context={
        'tables':tables
    }

    return render(request,'main/main.html',context)
