# Generated by Django 2.2 on 2019-05-10 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('designers', '0001_initial'),
        ('user_account', '0001_initial'),
        ('designs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_history', to='designs.Design')),
                ('designer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_history', to='designers.Designer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_history', to='user_account.UserAccount')),
            ],
        ),
    ]
