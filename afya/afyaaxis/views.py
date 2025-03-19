from django.shortcuts import render

def welcome_page(request):
    return render(request, 'base/welcome_page.html')