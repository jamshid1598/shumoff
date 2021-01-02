# Generated by Django 3.1.1 on 2021-01-01 15:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='article/%Y/%m/%d/', verbose_name='Изображение статьи:')),
                ('title', models.CharField(max_length=350, unique=True, verbose_name='заглавие:')),
                ('slug', models.SlugField(max_length=400, unique=True)),
                ('description', models.TextField(verbose_name='Описание:')),
                ('author', models.CharField(default='ShumOff', max_length=50, verbose_name='Автор:')),
                ('view_counter', models.PositiveIntegerField(default=0)),
                ('published_at', models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано:')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено:')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'ordering': ['published_at', 'updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='имя: ')),
                ('phone', models.CharField(max_length=200, null=True, verbose_name='Телефонный номер: ')),
                ('address', models.CharField(max_length=500, null=True, verbose_name='Адрес: ')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete', models.BooleanField(default=False, verbose_name='Завершено: ')),
                ('date_ordered', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа: ')),
                ('transaction_id', models.CharField(max_length=100, null=True, verbose_name='номер транзакции: ')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.customer')),
            ],
            options={
                'verbose_name': 'порядок',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_price', models.DecimalField(decimal_places=2, default=100, max_digits=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000000)], verbose_name='Цена')),
                ('option_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000000)], verbose_name='Скидка Цена')),
                ('option_info', models.CharField(blank=True, max_length=100, null=True, verbose_name='Вариант продукта')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество: ')),
                ('option_pk', models.CharField(blank=True, max_length=5, null=True, verbose_name='вариант pk')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа: ')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordered_product', to='core.product')),
            ],
            options={
                'verbose_name': 'Позиция заказа',
                'verbose_name_plural': 'Позиция заказа',
            },
        ),
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(blank=True, max_length=300, null=True, verbose_name='Продукт: ')),
                ('product_option', models.CharField(blank=True, max_length=100, null=True, verbose_name='Вариант продукта')),
                ('image', models.ImageField(blank=True, null=True, upload_to='ordered-product/%Y/%m/%d/', verbose_name='Образ:')),
                ('product_amount', models.IntegerField(default=0, verbose_name='Количество товара: ')),
                ('single_price', models.FloatField(default=0, verbose_name='Цена продукта: ')),
                ('total_price', models.FloatField(default=0, verbose_name='Итоговая цена: ')),
                ('date_ordered', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа: ')),
                ('completed', models.BooleanField(default=False, verbose_name='Завершено: ')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_orders', to='cart.customer', verbose_name='Клиент: ')),
            ],
            options={
                'verbose_name': 'Заказанный товар',
                'verbose_name_plural': 'Заказанные товары',
                'ordering': ['-date_ordered'],
            },
        ),
    ]