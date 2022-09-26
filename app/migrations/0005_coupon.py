# Generated by Django 4.0.5 on 2022-07-21 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_delete_coupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount', models.IntegerField(default=100)),
                ('minimum_amount', models.IntegerField(default=500)),
            ],
        ),
    ]
