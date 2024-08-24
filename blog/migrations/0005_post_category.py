# Generated by Django 5.0.6 on 2024-07-24 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, choices=[('agriculture', 'Agriculture'), ('health', 'Health'), ('climate', 'Climate'), ('law & order', 'Law & Order'), ('society', 'Society'), ('education', 'Education'), ('politics', 'Politics')], max_length=800, null=True),
        ),
    ]
