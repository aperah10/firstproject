# Generated by Django 3.1.2 on 2021-07-03 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('sales_price', models.FloatField()),
                ('discount_price', models.FloatField()),
                ('our_price', models.FloatField(blank=True, default=0, null=True)),
                ('category', models.CharField(choices=[('Clothes', 'Clothes'), ('Mobile', 'Mobile'), ('Beauty', 'Beauty'), ('Grocery', 'Grocery')], max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('stock', models.PositiveIntegerField()),
                ('pic', models.ImageField(blank=True, upload_to='ProdcutImg')),
                ('offers', models.IntegerField(blank=True, default=1, null=True)),
                ('uplod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInCart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('customer_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'unique_together': {('customer_cart', 'product')},
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('noti_type', models.CharField(choices=[('Like', 'Like'), ('addtocart', 'addtocart'), ('save for later', 'save for later')], max_length=50)),
                ('txt', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sendernoti', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receviernoti', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cr_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInSave',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('cart_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productincart')),
                ('customer_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'unique_together': {('customer_cart', 'product', 'cart_by')},
            },
        ),
    ]
