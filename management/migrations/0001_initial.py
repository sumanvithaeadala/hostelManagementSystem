# Generated by Django 3.2.18 on 2023-03-02 13:24

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userType', models.CharField(choices=[('1', 'Administration'), ('2', 'Student'), ('3', 'Warden')], default=1, max_length=60)),
                ('profile_pic', models.ImageField(upload_to='media/profile_pic')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostel_name', models.CharField(default=None, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default=None, max_length=1, null=True)),
                ('caretaker_name', models.CharField(blank=True, max_length=100)),
                ('course', models.ManyToManyField(blank=True, default=None, to='management.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=100, null=True)),
                ('room_type', models.CharField(choices=[('S', 'Single'), ('D', 'Double'), ('T', 'Triple')], default=None, max_length=1)),
                ('vacant', models.BooleanField(default=False)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.hostel')),
            ],
        ),
        migrations.CreateModel(
            name='year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_start', models.CharField(max_length=100, null=True)),
                ('year_end', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warden_name', models.CharField(max_length=100, null=True)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.hostel')),
                ('warden', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('gender', models.CharField(max_length=10, null=True)),
                ('scholar_number', models.CharField(max_length=15, null=True)),
                ('student_name', models.CharField(max_length=100, null=True)),
                ('dob', models.CharField(max_length=15, null=True)),
                ('branch', models.CharField(max_length=150, null=True)),
                ('father_name', models.CharField(max_length=100, null=True)),
                ('mother_name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.CharField(max_length=10, null=True)),
                ('semester', models.CharField(max_length=5, null=True)),
                ('course_year', models.CharField(max_length=10, null=True)),
                ('father_phone_number', models.CharField(max_length=100, null=True)),
                ('guardian_name', models.CharField(max_length=100, null=True)),
                ('guardian_phone_number', models.CharField(max_length=100, null=True)),
                ('guardian_address', models.CharField(max_length=100, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.course')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.room')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]