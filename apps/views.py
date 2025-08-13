# apps/views.py
from django.http import HttpResponse

def hello_user(request):
    return HttpResponse(f"<h1>Welcome to the my 1-st Application.</h1>")


