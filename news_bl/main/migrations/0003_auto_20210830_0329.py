# Generated by Django 3.2.6 on 2021-08-30 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210830_0224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='published_at',
            new_name='publishedAt',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='url_to_image',
            new_name='urlToImage',
        ),
    ]