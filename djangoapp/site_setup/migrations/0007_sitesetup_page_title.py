# Generated by Django 4.2.5 on 2023-09-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0006_alter_sitesetup_favicon'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetup',
            name='page_title',
            field=models.CharField(default='page_title', max_length=65),
        ),
    ]
