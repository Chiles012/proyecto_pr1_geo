# Generated by Django 4.0.1 on 2022-09-04 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ufo',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ufo',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ufo',
            name='described_duration_of_encounter',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ufo',
            name='ufo_shape',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
