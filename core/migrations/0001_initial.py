# Generated by Django 3.1.1 on 2021-01-01 15:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200, unique=True, verbose_name='Категория:')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='category/%Y/%m/%d/', verbose_name='Категория Образ:')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('primary', models.BooleanField(default=True, verbose_name='Основная')),
                ('tools', models.BooleanField(default=False, verbose_name='инструменты')),
                ('accessory', models.BooleanField(default=False, verbose_name='Аксессуар')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['added_date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='product/%Y/%m/%d/', verbose_name='Образ')),
                ('caption', models.CharField(blank=True, max_length=300, null=True, verbose_name='Заголовок')),
                ('name', models.CharField(max_length=300, verbose_name='Hазвание')),
                ('slug', models.SlugField(max_length=320, unique=True)),
                ('short_description', models.TextField(null=True, verbose_name='Краткое описание')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, default=100, max_digits=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000000)], verbose_name='Цена')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000000)], verbose_name='Скидка Цена')),
                ('price_info', models.CharField(blank=True, max_length=300, null=True, verbose_name='О цене')),
                ('product_option', models.CharField(blank=True, max_length=300, null=True, verbose_name='Вариант продукта')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('published_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='core.category', verbose_name='Категория:')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['name', 'published_at', 'updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=100, max_digits=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000000)], verbose_name='Цена')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000000)], verbose_name='Скидка Цена')),
                ('price_info', models.CharField(blank=True, max_length=300, null=True, verbose_name='О цене')),
                ('product_option', models.CharField(blank=True, max_length=300, null=True, verbose_name='Вариант продукта')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_price_option', to='core.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name_plural': 'Тип продукта',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='product-images/%Y/%m/%d/', verbose_name='Образ')),
                ('caption', models.CharField(blank=True, max_length=300, null=True, verbose_name='Заголовок')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='core.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name_plural': 'Изображений',
            },
        ),
    ]
