# Generated migration for adding unique_together constraint

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_title_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('title', 'author')},
        ),
    ]
