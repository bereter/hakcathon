# Generated by Django 4.2.7 on 2023-11-18 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_net', '0002_alter_subscriberscategory_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subscribers',
        ),
        migrations.AddField(
            model_name='profile',
            name='subscribers',
            field=models.ManyToManyField(blank=True, through='social_net.SubscribersCategory', to='social_net.category'),
        ),
        migrations.AlterField(
            model_name='subscriberscategory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_net.profile'),
        ),
    ]
