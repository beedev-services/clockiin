# Generated by Django 4.0.5 on 2022-10-28 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_usercodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercodes',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='codeCreator', to='app.user'),
            preserve_default=False,
        ),
    ]