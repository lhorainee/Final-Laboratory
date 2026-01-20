from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('board', '0002_remove_moderation_status_post_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('General', 'General Positivity'),
                                            ('Thanks', 'Giving Thanks'),
                                            ('Help', 'Need/Offer Help'),
                                            ('Inspiration', 'Daily Inspiration')
                                            ], default='General', max_length=20),
        ),
    ]
