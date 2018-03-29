from django.shortcuts import render
from .models import Entry, Member
from .forms import EntryAddForm
from django.http import Http404
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from datetime import datetime
import pytz

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

def search_entries(request):
    return render(request, "guest_book/search_entries.html",{})

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

class Entries(ListView):
    template_name = "guest_book/entries.html"
    model = Entry
    context_object_name = "entries"
    paginate_by = 5
    def get_queryset(self):
        objects = Entry.objects.all()
        get_data = self.request.GET

        if "before_date" in self.request.GET:
            if get_data["before_date"] != "":
                before_date=datetime.strptime(get_data["before_date"], "%Y-%m-%d")
                before_date_aware=pytz.utc.localize(before_date)
                objects = objects.filter(pub_date__lte=before_date_aware)

        if "search_for" in get_data:
            if get_data["search_for"] != "":
                title_objects = objects.filter(title__contains=get_data["search_for"])
                content_objects = objects.filter(text__contains=get_data["search_for"])
                objects = title_objects.union(content_objects)

        return objects.order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # creates a get_string to be able to make links to other pages
        # of a search. Also creates "search descriptive" string to let
        # the user know what was searched for
        get_data = self.request.GET
        get_string=""
        search_descriptive_string=""
        if "search_for" in get_data:
            get_string += "&search_for="
            get_string += get_data["search_for"]
            if get_data["search_for"] != "":
                search_descriptive_string += ("med frasen \"" + get_data["search_for"] + "\" ")
        if "before_date" in get_data:
            get_string += "&before_date="
            get_string += get_data["before_date"]
            if get_data["before_date"] != "":
                search_descriptive_string += ("før \"" + get_data["before_date"] + "\" ")
        context["get_string"] = get_string
        context["descriptive_string"] = search_descriptive_string
        return context

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
