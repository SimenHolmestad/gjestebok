import datetime
import random, string

from django.test import TestCase
from django.utils import timezone

from .models import Member, Entry

def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def generate_email():
    return '{}@{}.com'.format(random_string(5), random_string(7))

def generate_member():
    return Member(first_name = "Test",
                  last_name = "Testesen",
                  phone = "1881",
                  email = generate_email(),
                  birth_date = timezone.now())

def create_date(delta_days):
    return timezone.now() + datetime.timedelta(days=delta_days)

class MemberTestCase(TestCase):
    def test_member_save(self):
        member = generate_member()
        member.save()
        self.assertEqual(member, Member.objects.get(first_name="Test"))
    
    def test_age(self):
        member = generate_member()
        member.birth_date = create_date(-368)
        member.save()
        self.assertEqual(member.get_age(), 1)

    def test_age_at(self):
        member = generate_member()
        member.birth_date = create_date(-750)
        member.save()
        self.assertEqual(member.get_age_at(create_date(-370)), 1)

class EntryTestCase(TestCase):
    def test_number_of_entries(self):
        member = generate_member()
        member.save()

        entry = Entry(author = member, pub_date = timezone.now())
        entry.save()
        self.assertEqual(member.number_of_entries, 1)

    def test_age_at_creation(self):
        member = generate_member()
        member.birth_date = create_date(-750)
        member.save()

        entry = Entry(author = member, pub_date = create_date(-370))
        self.assertEqual(entry.get_author_age_at_creation(), 1)

    def test_author_involved(self):
        member = generate_member()
        member.save()

        entry = Entry(author = member, pub_date=create_date(0))
        entry.save()

        members_involved = entry.members_involved.all()
        self.assertEqual(member in members_involved.all(), True)

    def test_multiple_members_involved(self):
        author = generate_member()
        author.save()

        member1 = generate_member()
        member2 = generate_member()
        member1.save()
        member2.save()

        entry = Entry(author=author, pub_date = timezone.now())
        entry.save()
        entry.members_involved.add(member1, member2)

        self.assertEqual(len(entry.members_involved.all()), 3)
