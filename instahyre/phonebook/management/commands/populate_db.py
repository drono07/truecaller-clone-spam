import random
from faker import Faker
from django.core.management.base import BaseCommand
from phonebook.models import MyUser, PhoneEntry, SpamReport, ContactList

class Command(BaseCommand):
    help = 'Populate the database with random data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Clear existing data
        MyUser.objects.all().delete()
        PhoneEntry.objects.all().delete()
        SpamReport.objects.all().delete()
        ContactList.objects.all().delete()

        # Create random users
        for _ in range(10):
            user = MyUser.objects.create_user(
                email=fake.email(),
                mobile=fake.unique.msisdn()[:15],  # Ensuring mobile number is within 15 characters
                password='password123',
                full_name=fake.name()
            )
            self.stdout.write(f"Created user {user.mobile}")

        # Create random phone entries
        phone_entries = []
        for _ in range(20):
            entry = PhoneEntry.objects.create(
                name=fake.name(),
                number=fake.unique.msisdn()[:15],  # Ensuring phone number is within 15 characters
                spam_score=random.randint(0, 100),
                is_spam=random.choice([True, False])
            )
            phone_entries.append(entry)
            self.stdout.write(f"Created phone entry {entry.number}")

        # Create random spam reports
        users = list(MyUser.objects.all())
        for _ in range(30):
            user = random.choice(users)
            phone_entry = random.choice(phone_entries)
            if not SpamReport.objects.filter(user=user, phone_entry=phone_entry).exists():
                SpamReport.objects.create(user=user, phone_entry=phone_entry)
                phone_entry.spam_score += 1
                phone_entry.is_spam = True
                phone_entry.save()
                self.stdout.write(f"Created spam report for user {user.mobile} on {phone_entry.number}")

        # Create random contact lists
        for user in users:
            for _ in range(5):
                contact_name = fake.name()
                contact_number = fake.unique.msisdn()[:15]  # Ensuring contact number is within 15 characters
                ContactList.objects.create(
                    user=user,
                    contact_name=contact_name,
                    contact_number=contact_number
                )
                self.stdout.write(f"Added contact {contact_name} ({contact_number}) to user {user.mobile}")

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data'))
