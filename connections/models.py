from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Connection(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=True)  # For future use if we want to implement approval system

    class Meta:
        unique_together = ['follower', 'following']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def save(self, *args, **kwargs):
        # Prevent users from following themselves
        if self.follower == self.following:
            raise ValueError("Users cannot follow themselves")
        super().save(*args, **kwargs)


class ConnectionRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(max_length=500, blank=True, help_text="Optional message with your connection request")

    class Meta:
        unique_together = ['requester', 'target']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requester.username} -> {self.target.username} ({self.status})"

    def accept(self):
        """Accept the connection request and create a connection"""
        self.status = 'ACCEPTED'
        self.save()
        
        # Create the connection
        Connection.objects.create(
            follower=self.requester,
            following=self.target
        )

    def reject(self):
        """Reject the connection request"""
        self.status = 'REJECTED'
        self.save()


class Block(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['blocker', 'blocked']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"


class Skill(models.Model):
    """Skills that can be endorsed"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('physical', 'Physical Attributes'),
            ('technical', 'Technical Skills'),
            ('mental', 'Mental Attributes'),
            ('leadership', 'Leadership'),
            ('communication', 'Communication'),
            ('other', 'Other'),
        ],
        default='technical'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PlayerSkill(models.Model):
    """Skills associated with a player"""
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills', limit_choices_to={'user_type': 'player'})
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='players')
    proficiency_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['player', 'skill']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.player.username} - {self.skill.name} ({self.get_proficiency_level_display()})"


class Endorsement(models.Model):
    """Endorsements for player skills"""
    endorser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_endorsements')
    player_skill = models.ForeignKey(PlayerSkill, on_delete=models.CASCADE, related_name='endorsements')
    message = models.TextField(max_length=500, blank=True, help_text="Optional message with your endorsement")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['endorser', 'player_skill']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.endorser.username} endorsed {self.player_skill.player.username}'s {self.player_skill.skill.name}"
    
    def save(self, *args, **kwargs):
        # Prevent users from endorsing themselves
        if self.endorser == self.player_skill.player:
            raise ValueError("Users cannot endorse their own skills")
        super().save(*args, **kwargs)


class Recommendation(models.Model):
    """Written recommendations between users"""
    recommender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_recommendations')
    recommendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_recommendations')
    title = models.CharField(max_length=200, help_text="Job title or role")
    relationship = models.CharField(
        max_length=50,
        choices=[
            ('teammate', 'Teammate'),
            ('coach', 'Coach'),
            ('manager', 'Manager'),
            ('agent', 'Agent'),
            ('opponent', 'Opponent'),
            ('other', 'Other'),
        ],
        default='teammate'
    )
    recommendation_text = models.TextField(max_length=2000, help_text="Your recommendation")
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['recommender', 'recommendee']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recommender.username} recommended {self.recommendee.username}"
    
    def save(self, *args, **kwargs):
        # Prevent users from recommending themselves
        if self.recommender == self.recommendee:
            raise ValueError("Users cannot recommend themselves")
        super().save(*args, **kwargs)