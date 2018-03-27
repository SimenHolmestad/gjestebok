import datetime
import random, string

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Member, Entry

def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def generate_email():
    return '{}@{}.com'.format(random_string(5), random_string(7))

def generate_member():
    return Member.objects.create(first_name = "Test",
                                 last_name = "Testesen",
                                 phone = "1881",
                                 email = generate_email(),
                                 birth_date = timezone.now())

def create_date(delta_days):
    return timezone.localdate() + datetime.timedelta(days=delta_days)

def create_time(delta_days):
    return timezone.now() + datetime.timedelta(days=delta_days)

class MemberModelTestCase(TestCase):
    def test_member_save(self):
        member = generate_member()
        member.save()
        self.assertEqual(member, Member.objects.get(first_name="Test"))
    
    def test_age(self):
        member = generate_member()
        member.birth_date = create_date(-368*2)
        member.save()
        self.assertEqual(member.get_age(), 2)

    def test_age_at(self):
        member = generate_member()
        member.birth_date = create_date(-750)
        member.save()
        self.assertEqual(member.get_age_at(create_date(-370)), 1)

class EntryModelTestCase(TestCase):
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

        entry = Entry(author = member, pub_date = create_time(-370))
        self.assertEqual(entry.get_author_age_at_creation(), 1)

    def test_author_involved(self):
        member = generate_member()
        member.save()
        entry = Entry.objects.create(author = member)

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

def generate_entry(title, pub_date_offset):
    return Entry.objects.create(author=generate_member(), title = title, pub_date = create_time(pub_date_offset))

def generate_entry_with_author(author, title, pub_date_offset):
    return Entry.objects.create(author=author, title = title, pub_date = create_time(pub_date_offset))

class IndexViewTestCase (TestCase):
    def test_single_entry(self):
        entry = generate_entry("The test is real", pub_date_offset=0)
        response = self.client.get(reverse("guest_book:index"))
        self.assertContains(response, "The test is real")

    def test_no_entry(self):
        response = self.client.get(reverse("guest_book:index"))
        self.assertContains(response, "Det er ingen innlegg ennå")

    def test_two_entries_sorted(self):
        entry1 = generate_entry("entry nr.1", -30)
        entry2 = generate_entry("entry nr.2", -5)
        response = self.client.get(reverse("guest_book:index"))
        self.assertQuerysetEqual(response.context["entries"],
                                 ["<Entry: entry nr.2 av Test Testesen>", 
                                  "<Entry: entry nr.1 av Test Testesen>"])

    def test_last_5_elements(self):
        entry1 = generate_entry("The test is real", -30)
        for i in range(5):
            generate_entry("random entry", -5)
        response = self.client.get(reverse("guest_book:index"))
        self.assertEqual(len(response.context["entries"]), 5)
        self.assertNotContains(response, "The test is real")

class MembersViewTestCase (TestCase):
    def test_no_members(self):
        response = self.client.get(reverse("guest_book:members"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There´s no members")

    def test_two_members(self):
        member1 = generate_member();
        member2 = generate_member();
        response = self.client.get(reverse("guest_book:members"))
        self.assertContains(response, member1.__str__())
        self.assertContains(response, member2.__str__())

class Member_detailViewTestCase(TestCase):
    def test_illegal_member(self):
        response = self.client.get(reverse("guest_book:member_detail", args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_legal_member(self):
        member = generate_member()
        response = self.client.get(reverse("guest_book:member_detail", args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, member.__str__())

    def test_author_articles(self):
        member1 = generate_member()
        entry = generate_entry_with_author(member1, "The test is real", -200);
        response = self.client.get(reverse("guest_book:member_detail", args=(1,)))
        self.assertQuerysetEqual(response.context["author_entries"],
                                 ["<Entry: The test is real av Test Testesen>"])
        self.assertFalse(response.context["involved_entries"].exists())

    def test_involved_articles(self):
        member1 = generate_member()
        member2 = generate_member()
        entry = generate_entry_with_author(member2, "The test is real", -200);
        entry.members_involved.add(member1)
        response = self.client.get(reverse("guest_book:member_detail", args=(1,)))
        self.assertQuerysetEqual(response.context["involved_entries"],
                                 ["<Entry: The test is real av Test Testesen>"])
        self.assertFalse(response.context["author_entries"].exists())

    def test_article_sorting(self):
        member1 = generate_member()
        member2 = generate_member()
        entry1 = generate_entry_with_author(member1, "The test is real", -200)
        entry2 = generate_entry_with_author(member1, "The other test is real", -100)

        response = self.client.get(reverse("guest_book:member_detail", args=(1,)))
        self.assertQuerysetEqual(response.context["author_entries"],
                                 ["<Entry: The other test is real av Test Testesen>",
                                  "<Entry: The test is real av Test Testesen>"])
        self.assertFalse(response.context["involved_entries"].exists())

        entry1.members_involved.add(member2)
        entry2.members_involved.add(member2)

        response = self.client.get(reverse("guest_book:member_detail", args=(2,)))
        self.assertQuerysetEqual(response.context["involved_entries"],
                                 ["<Entry: The other test is real av Test Testesen>",
                                  "<Entry: The test is real av Test Testesen>"])
        self.assertFalse(response.context["author_entries"].exists())

class entriesViewTestCase(TestCase):
    def test_no_entries(self):
        response = self.client.get(reverse("guest_book:entries"))
        self.assertContains(response, "Det er ingen innlegg ennå")

    def test_member_ages(self):
        member = generate_member()
        member.birth_date = create_date(-800)
        entry = generate_entry_with_author(member, "The test is real", -300)
        response = self.client.get(reverse("guest_book:entries"))
        print (member.get_age_at(entry.pub_date.date()))
        self.assertContains(response, "Test Testesen")
        self.assertContains(response, " 1 år")
