# Generated by Django 2.0.3 on 2018-03-24 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest_book', '0007_entry_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
