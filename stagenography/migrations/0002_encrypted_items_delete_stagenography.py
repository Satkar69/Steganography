# Generated by Django 4.2.4 on 2023-08-23 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stagenography', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encrypted_Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/encrypted_images')),
                ('message', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Stagenography',
        ),
    ]
