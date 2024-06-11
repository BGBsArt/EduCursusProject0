# Generated by Django 5.0.6 on 2024-06-02 09:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('password1', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AdminRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etablissement', models.CharField(max_length=100)),
                ('codeid', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('commune', models.CharField(max_length=50)),
                ('school', models.CharField(max_length=50)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_name='adminregister_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='adminregister_set', to='auth.permission')),
            ],
        ),
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=50)),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('entite', models.CharField(max_length=50)),
                ('filiere', models.CharField(max_length=50)),
                ('mesApprenants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adminstra', to='EduCursus.adminregister')),
            ],
        ),
        migrations.CreateModel(
            name='Cursus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filiereEnCours', models.CharField(max_length=30)),
                ('annee', models.CharField(max_length=9)),
                ('note', models.DecimalField(decimal_places=2, max_digits=4)),
                ('mention', models.CharField(max_length=10)),
                ('administrateurs', models.ManyToManyField(related_name='cursus', to='EduCursus.administrateur')),
                ('letablissement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cet_etablissement', to='EduCursus.adminregister')),
            ],
        ),
        migrations.CreateModel(
            name='AddAssociation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.CharField(max_length=9)),
                ('administrateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EduCursus.administrateur')),
                ('cursus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EduCursus.cursus')),
            ],
        ),
    ]