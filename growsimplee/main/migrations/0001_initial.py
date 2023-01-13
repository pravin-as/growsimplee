# Generated by Django 3.2.4 on 2023-01-13 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('person', models.CharField(max_length=200)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('locationtype', models.BooleanField()),
                ('productID', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productID', models.CharField(max_length=200)),
                ('length', models.IntegerField()),
                ('breadth', models.IntegerField()),
                ('height', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('delivered', models.BooleanField(default=False)),
            ],
        ),
    ]