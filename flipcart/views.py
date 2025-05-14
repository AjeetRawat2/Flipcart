from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')
def check(request):
    return render(request,'check.html')
def cart(request):
    return render(request,'cart.html')