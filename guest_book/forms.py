from django import forms

from .models import Member, Entry

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'birth_date', 'phone', 'email', 'about_me', 'profile_photo']

class EntryAddForm (forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["author", "title", "pub_date", "text", "members_involved", "image"]

    def save(self, *args, **kwargs):
        obj = super(EntryAddForm, self).save(*args, **kwargs)
        # As djange resets manyToMany-fields after calling save from a
        # form, this line is necessary
        if not obj.author in obj.members_involved.all():
            obj.members_involved.add(obj.author) 
        return obj
