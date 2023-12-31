# Generated by Django 4.2.4 on 2023-08-29 09:57

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
            name='Category',
            fields=[
                ('title', models.CharField(max_length=30)),
                ('slug', models.SlugField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('title', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('title', models.CharField(max_length=25)),
                ('slug', models.SlugField(blank=True, max_length=25, primary_key=True, serialize=False)),
                ('texts', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='posts_img/', verbose_name='Pictures')),
                ('crated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='publication.category', verbose_name='Category')),
                ('tags', models.ManyToManyField(blank=True, related_name='posts', to='publication.tag')),
            ],
        ),
    ]
