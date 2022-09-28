# Generated by Django 4.1.1 on 2022-09-28 01:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DairyContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=300, null=True, verbose_name='楽しかったことを記入しよう')),
                ('date', models.DateField(blank=True)),
                ('ranking', models.IntegerField(blank=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dairyContent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
