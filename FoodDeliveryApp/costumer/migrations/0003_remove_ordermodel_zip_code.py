# Generated by Django 4.1.7 on 2023-04-10 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costumer', '0002_ordermodel_city_ordermodel_email_ordermodel_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='zip_code',
        ),
    ]
