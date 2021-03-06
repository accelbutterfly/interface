# Generated by Django 2.0.6 on 2018-06-27 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interfapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='rdfurl',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='xmlurl',
            field=models.TextField(default='0'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='documents/'),
        ),
    ]
