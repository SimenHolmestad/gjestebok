# Generated by Django 2.0.3 on 2018-03-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest_book', '0008_member_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='etternavn'),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='mobilnummer'),
        ),
    ]
