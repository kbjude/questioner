# Generated by Django 2.1.7 on 2019-03-28 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_comment_is_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.TextField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reactions', to='comment.Comment')),
            ],
        ),
    ]
