# Generated by Django 4.2.7 on 2023-11-28 19:03

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
            name='Feedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wizyta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pdf_file', models.FileField(upload_to='diet_pdfs/')),
                ('feedback', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='panel.feedback')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
