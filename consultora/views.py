from django.shortcuts import render

#vistas globales
def home (request):
    return render(request, 'home.html')


def dashboard (request):
    return render(request, 'dashboard.html')