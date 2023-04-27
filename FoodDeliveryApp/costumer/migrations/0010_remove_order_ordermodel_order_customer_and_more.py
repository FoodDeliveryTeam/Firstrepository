# Generated by Django 4.1.7 on 2023-04-26 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costumer', '0009_order_orderitem_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ordermodel',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='costumer.customer'),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='costumer.customer'),
        ),
    ]
