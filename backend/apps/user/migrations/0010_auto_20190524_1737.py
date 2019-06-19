# Generated by Django 2.0.4 on 2019-05-24 09:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20190516_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='group',
            field=models.ManyToManyField(related_name='user_group_join', to='user.UserGroup'),
        ),
        migrations.AlterField(
            model_name='users',
            name='jwt_secret',
            field=models.UUIDField(default=uuid.UUID('0afe4c33-30cb-4b86-9150-795d1cd129ce'), verbose_name='用户jwt加密秘钥'),
        ),
    ]