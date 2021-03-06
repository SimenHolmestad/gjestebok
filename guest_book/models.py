from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

class Member(models.Model):
    first_name = models.CharField("fornavn", max_length=50)
    last_name = models.CharField("etternavn", max_length=50)
    phone = models.CharField("mobilnummer", max_length=20, null=True, blank=True)
    number_of_entries = models.IntegerField(default = 0)
    profile_photo = ResizedImageField(null = True, blank = True, verbose_name="profilbilde")
    email = models.EmailField(
        verbose_name = "e-post",
        max_length=255,
        unique=True,
        blank=True,
        null=True)
    about_me = models.TextField("litt om meg selv", blank=True, default="")
    birth_date = models.DateField("Fødselsdato", default=datetime.now)
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def get_age(self):
        return relativedelta(timezone.localdate(), self.birth_date).years

    # to check age of members at a certain time, use time.date()
    def get_age_at(self, date):
        return relativedelta(date, self.birth_date).years

class Entry(models.Model):
    author = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="forfatter")
    pub_date = models.DateTimeField("dato publisert", default=datetime.now)
    title = models.CharField(max_length=255, unique=False, verbose_name="tittel")
    text = models.TextField("tekst")
    image = ResizedImageField(blank = True, null = True, verbose_name="bilde")
    members_involved = models.ManyToManyField(Member,
                                              blank=True,
                                              related_name="involved_entries",
                                              verbose_name="medlemmer med")
    def __str__(self):
        return self.title + " av " + self.author.__str__()
    
    def save(self, *args, **kwargs):
        """
        saves the object to the database, upping number_of_entries
        of the related user.
        """
        self.author.number_of_entries += 1
        self.author.save()

        super(Entry, self).save(*args, **kwargs)
        if not self.author in self.members_involved.all():
            self.members_involved.add(self.author)

    def get_author_age_at_creation(self):
        return relativedelta(self.pub_date.date(), self.author.birth_date).years

#TODO: change from pub_date to pub_time
