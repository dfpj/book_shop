# Generated by Django 3.2.12 on 2022-02-15 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_book_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='image_link',
            new_name='image_link_scrap',
        ),
        migrations.RemoveField(
            model_name='book',
            name='image',
        ),
        migrations.AddField(
            model_name='book',
            name='image_link_arvan',
            field=models.CharField(default='1.jpg', max_length=255),
        ),
    ]
