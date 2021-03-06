# Generated by Django 4.0.5 on 2022-06-27 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_comment_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='isParent',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.project'),
        ),
    ]
