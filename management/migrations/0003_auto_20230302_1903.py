# Generated by Django 3.2.18 on 2023-03-02 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_rename_course_name_course_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostel',
            old_name='hostel_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='warden',
            old_name='warden_name',
            new_name='name',
        ),
    ]
