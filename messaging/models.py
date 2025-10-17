from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        participant_names = [user.username for user in self.participants.all()]
        return f"Conversation between {', '.join(participant_names)}"

    def get_other_participant(self, user):
        """Get the other participant in a 2-person conversation"""
        other_participants = self.participants.exclude(id=user.id)
        return other_participants.first()

    def get_last_message(self):
        """Get the most recent message in this conversation"""
        return self.messages.first()

    def get_unread_count(self, user):
        """Get count of unread messages for a specific user"""
        return self.messages.exclude(sender=user).filter(is_read=False).count()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}..."

    def mark_as_read(self):
        """Mark this message as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update conversation's updated_at timestamp
        self.conversation.updated_at = self.timestamp
        self.conversation.save(update_fields=['updated_at'])


class MessageNotification(models.Model):
    """Track unread message notifications for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_notifications')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='notifications')
    unread_count = models.PositiveIntegerField(default=0)
    last_checked = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'conversation']

    def __str__(self):
        return f"{self.user.username}: {self.unread_count} unread messages"

    def increment_unread(self):
        """Increment unread message count"""
        self.unread_count += 1
        self.save(update_fields=['unread_count'])

    def mark_as_read(self):
        """Reset unread count to 0"""
        self.unread_count = 0
        self.save(update_fields=['unread_count', 'last_checked'])


class MessageAttachment(models.Model):
    """File attachments for messages"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='message_attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.filename} ({self.message.sender.username})"


class MessageReaction(models.Model):
    """Reactions to messages (like, heart, etc.)"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_reactions')
    reaction_type = models.CharField(
        max_length=20,
        choices=[
            ('like', '👍 Like'),
            ('love', '❤️ Love'),
            ('laugh', '😂 Laugh'),
            ('wow', '😮 Wow'),
            ('sad', '😢 Sad'),
            ('angry', '😠 Angry'),
        ],
        default='like'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['message', 'user', 'reaction_type']
    
    def __str__(self):
        return f"{self.user.username} {self.get_reaction_type_display()} on {self.message.sender.username}'s message"


class MessageThread(models.Model):
    """Threaded conversations for better organization"""
    parent_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='thread_messages')
    reply_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='thread_reply')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Thread: {self.parent_message.id} -> {self.reply_message.id}"