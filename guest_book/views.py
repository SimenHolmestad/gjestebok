from django.shortcuts import render
from .models import Entry, Member

# Create your views here.

def index(request):
    try:
        text_entered=request.POST["message"]
        print (text_entered)
    except (KeyError):
        pass
    user_list = User.objects.get()
    context = {}
    return render(request, "guest_book/index.html", context)
