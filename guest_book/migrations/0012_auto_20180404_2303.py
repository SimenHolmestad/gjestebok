# Generated by Django 2.0.3 on 2018-04-04 21:03

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('guest_book', '0011_auto_20180328_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=80, size=[2048, 2048], upload_to='', verbose_name='bilde'),
        ),
        migrations.AlterField(
            model_name='member',
            name='profile_photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=80, size=[2048, 2048], upload_to='', verbose_name='profilbilde'),
        ),
    ]