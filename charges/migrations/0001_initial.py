# Generated by Django 5.0.2 on 2024-02-14 12:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Costumer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('credit', models.PositiveIntegerField()),
                ('logs', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('credit', models.PositiveIntegerField()),
                ('logs', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_type', models.CharField(max_length=500)),
                ('credit', models.PositiveIntegerField(default=None, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('costumer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='charges.costumer')),
                ('seller', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='charges.seller')),
            ],
        ),
        migrations.CreateModel(
            name='InnerCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=None, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('seller', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='charges.seller')),
            ],
        ),
        migrations.CreateModel(
            name='DeletionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_type', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('costumer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='charges.costumer')),
                ('seller', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='charges.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('costumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charges.costumer')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charges.seller')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_type', models.CharField(max_length=500)),
                ('amount', models.PositiveIntegerField(default=None, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('costumer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='charges.costumer')),
                ('seller', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='charges.seller')),
            ],
        ),
    ]
