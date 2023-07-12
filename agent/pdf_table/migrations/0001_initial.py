# Generated by Django 4.2.3 on 2023-07-12 18:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PdfTable',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.UUIDField(null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('modified_by', models.UUIDField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('deleted_by', models.UUIDField(null=True)),
                ('status', models.IntegerField(default=0)),
                ('pdf_cv_file', models.FileField(upload_to='pdf-cv')),
                ('data', models.JSONField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]