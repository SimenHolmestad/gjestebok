# Generated by Django 2.0.3 on 2018-03-24 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest_book', '0006_auto_20180322_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
