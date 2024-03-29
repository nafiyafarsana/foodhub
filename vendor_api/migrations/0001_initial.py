# Generated by Django 4.1.4 on 2023-01-12 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening_time', models.TimeField(null=True)),
                ('closing_time', models.TimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=100, null=True, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100, null=True)),
                ('location', models.CharField(max_length=100, null=True)),
                ('license', models.CharField(blank=True, max_length=100, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_vendor', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VendorToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_id', models.IntegerField()),
                ('token', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expired_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RestMenuModel',
            fields=[
                ('vendor_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='vendor_api.vendor')),
                ('Menu', models.CharField(max_length=3000)),
                ('special_items', models.CharField(blank=True, max_length=3000, null=True)),
                ('offer', models.CharField(blank=True, max_length=3000, null=True)),
                ('veg', models.BooleanField(blank=True, null=True)),
                ('non_veg', models.BooleanField(blank=True, null=True)),
                ('cover_photo', models.ImageField(blank=True, max_length=2000, null=True, upload_to='pictures/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='RestFoodModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=3000)),
                ('food_image', models.ImageField(blank=True, max_length=3000, null=True, upload_to='pictures/%Y/%m,/%d/')),
                ('food_category', models.CharField(blank=True, max_length=3000, null=True)),
                ('food_description', models.TextField(blank=True, max_length=3000, null=True)),
                ('food_prize', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=225, null=True, unique=True)),
                ('vendor_name', models.ManyToManyField(to='vendor_api.vendor')),
                ('Menu', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor_api.restmenumodel')),
            ],
        ),
    ]
