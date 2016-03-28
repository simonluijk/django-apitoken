from django.contrib import admin
from .models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    readonly_fields = ('token', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user', )
        return self.readonly_fields
