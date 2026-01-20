from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General Positivity'),
        ('Thanks', 'Giving Thanks'),
        ('Help', 'Need/Offer Help'),
        ('Inspiration', 'Daily Inspiration'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Removed', 'Removed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - [{self.category}] - {self.status} ({self.created_at.strftime('%Y-%m-%d')})"

    @property
    def like_count(self):
        return self.reactions.filter(reaction_type='Like').count()

    @property
    def love_count(self):
        return self.reactions.filter(reaction_type='Love').count()

    @property
    def smile_count(self):
        return self.reactions.filter(reaction_type='Smile').count()

    @property
    def wow_count(self):
        return self.reactions.filter(reaction_type='Wow').count()

    @property
    def sad_count(self):
        return self.reactions.filter(reaction_type='Sad').count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('Like', 'Like'),
        ('Love', 'Love'),
        ('Smile', 'Smile'),
        ('Wow', 'Wow'),
        ('Sad', 'Sad'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('post', 'user', 'reaction_type')

class Moderation(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='review_details')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for Post {self.post.id} by {self.moderator.username}"

