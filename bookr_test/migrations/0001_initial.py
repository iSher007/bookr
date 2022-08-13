# Generated by Django 4.0.3 on 2022-08-12 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the Publisher', max_length=50)),
                ('email', models.EmailField(help_text='Email of the Publisher', max_length=254)),
                ('website', models.URLField(help_text='The website url of the Publisher')),
            ],
        ),
    ]
