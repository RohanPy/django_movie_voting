# Generated by Django 3.0.8 on 2020-08-07 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('plot', models.TextField()),
                ('year', models.PositiveIntegerField()),
                ('rating', models.IntegerField(choices=[(0, 'NR - not rated'), (1, 'G - General Audience'), (2, 'PG - Parential GuidanceSuggested'), (3, 'R - Restricted')], default=0)),
                ('runtime', models.PositiveIntegerField()),
                ('website', models.URLField(blank=True)),
            ],
        ),
    ]