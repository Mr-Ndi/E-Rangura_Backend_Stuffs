# Generated by Django 4.2 on 2024-12-21 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sellers', '0002_seller_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='seller',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
