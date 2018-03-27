from django.shortcuts import render
from .models import Entry, Member
from .forms import EntryAddForm
from django.http import Http404
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'birth_date', 'phone', 'email', 'about_me', 'profile_photo']

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
    
    author_entries = Entry.objects.filter(author=member).order_by("-pub_date")
    involved_entries = member.involved_entries.exclude(author=member).order_by("-pub_date")

    context = {"member":member,
               "author_entries":author_entries,
               "involved_entries":involved_entries}
    return render(request, "guest_book/member_detail.html", context)

def entries(request):
    entries = Entry.objects.all().order_by("-pub_date")
    context = {"entries":entries}
    return render(request, "guest_book/entries.html", context)

def edit_member(request, member_id):
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        raise Http404("Medlem eksisterer ikke")
    
    #This is a form request for someone who has filled out the form
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES, instance = member)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("guest_book:members"))

    form = MemberForm(instance=member)
    context = {"form":form, "member":member}
    return render(request, "guest_book/edit_member.html", context)

class MemberCreate(CreateView):
    template_name = "guest_book/create_member.html"
    model = Member
    fields = ['first_name', 'last_name', 'birth_date', 'phone', 'email', 'about_me', 'profile_photo']
    success_url = reverse_lazy("guest_book:members")

class MemberDelete(DeleteView):
    template_name = "guest_book/confirm_delete_member.html"
    model = Member
    success_url = reverse_lazy("guest_book:members")

class NewEntry(CreateView):
    template_name = "guest_book/new_entry.html"
    model = Entry
    form_class = EntryAddForm
    success_url = reverse_lazy("guest_book:entries")

class EditEntry(UpdateView):
    template_name = "guest_book/edit_entry.html"
    model = Entry
    form_class = EntryAddForm
    success_url = reverse_lazy("guest_book:entries")

class EntryDelete(DeleteView):
    template_name = "guest_book/confirm_delete_entry.html"
    model = Entry
    success_url = reverse_lazy("guest_book:entries")
