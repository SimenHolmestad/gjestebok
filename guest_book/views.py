from django.shortcuts import render
from .models import Entry, Member
from django.http import Http404

def index(request):
    members = Member.objects.all()
    last_entries = Entry.objects.all().order_by("-pub_date")[:5];
    context = {"entries":last_entries}
    return render(request, "guest_book/index.html", context)

def members(request):
    members = Member.objects.all()
    context = {"members":members}
    return render(request, "guest_book/members.html", context)

def member_detail(request, member_id):
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        raise Http404("Medlem eksisterer ikke")
    
    author_entries = Entry.objects.filter(author=member)
    involved_entries = member.involved_entries.exclude(author=member)

    print (author_entries)
    context = {"member":member,
               "author_entries":author_entries,
               "involved_entries":involved_entries}
    return render(request, "guest_book/member_detail.html", context)
