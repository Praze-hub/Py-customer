# Generated by Django 3.2 on 2022-03-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0004_auto_20220316_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]