from django.conf import settings
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('board', '0003_post_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together={('post', 'user', 'reaction_type')},
        ),
    ]
