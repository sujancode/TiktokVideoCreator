from django.http import HttpResponse
from django.shortcuts import render

def home(req):
    if req.method=="GET":
        return render(req,"./main/home.html")