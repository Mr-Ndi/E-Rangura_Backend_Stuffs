# Generated by Django 4.2 on 2024-12-21 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sellers', '0003_remove_seller_profile_picture_seller_last_login_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='profile_pictures/'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
