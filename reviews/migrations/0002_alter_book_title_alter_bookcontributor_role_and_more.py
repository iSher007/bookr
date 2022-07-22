# Generated by Django 4.0.3 on 2022-03-16 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(help_text='The title of the book.', max_length=70),
        ),
        migrations.AlterField(
            model_name='bookcontributor',
            name='role',
            field=models.CharField(choices=[('AUTHOR', 'Author'), ('CO_AUTHOR', 'Co-Author'), ('EDITOR', 'Editor')], max_length=20, verbose_name='The role this contributor had in the book.'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='email',
            field=models.EmailField(help_text="The Publisher's email address.", max_length=254),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='name',
            field=models.CharField(help_text='The name of the Publisher.', max_length=50),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='website',
            field=models.URLField(help_text="The Publisher's website."),
        ),
    ]
