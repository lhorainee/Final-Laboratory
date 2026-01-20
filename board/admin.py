from django.contrib import admin
from .models import Post, Comment, Reaction, Moderation

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_content_preview', 'category', 'status', 'created_at', 'is_anonymous')
    list_filter = ('status', 'category', 'created_at', 'is_anonymous')
    search_fields = ('user__username', 'content')
    actions = ['approve_selected_posts', 'remove_selected_posts']

    list_editable = ('status',)

    def get_content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    get_content_preview.short_description = "Content Preview"

    @admin.action(description="✅ Approve selected posts")
    def approve_selected_posts(self, request, queryset):
        updated = queryset.update(status='Approved')
        self.message_user(request, f"{updated} posts have been approved and are now live.")

    @admin.action(description="❌ Remove selected posts")
    def remove_selected_posts(self, request, queryset):
        updated = queryset.update(status='Removed')
        self.message_user(request, f"{updated} posts have been removed from the feed.")

@admin.register(Moderation)
class ModerationAdmin(admin.ModelAdmin):
    list_display = ('post', 'moderator', 'reviewed_at')
    list_filter = ('moderator', 'reviewed_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment_text', 'created_at')
    search_fields = ('comment_text', 'user__username')

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'reaction_type')
    list_filter = ('reaction_type',)

