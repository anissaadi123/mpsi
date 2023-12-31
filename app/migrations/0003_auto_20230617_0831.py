# Generated by Django 3.2.12 on 2023-06-17 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20230616_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classe',
            name='eleves',
        ),
        migrations.RemoveField(
            model_name='grp',
            name='classes',
        ),
        migrations.AddField(
            model_name='eleve',
            name='classe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.classe'),
        ),
        migrations.AddField(
            model_name='enseignant',
            name='classe',
            field=models.ManyToManyField(related_name='enseignants', to='app.Classe'),
        ),
        migrations.AddField(
            model_name='grp',
            name='classe',
            field=models.ManyToManyField(related_name='groupes', to='app.Classe'),
        ),
    ]
