# Generated by Django 4.2.6 on 2023-10-27 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_payments_stripe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Сумма оплаты'),
        ),
    ]
