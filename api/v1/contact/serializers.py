from rest_framework import serializers
from apps.contact.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        """Validate email format."""
        if not value:
            raise serializers.ValidationError("Email address is required.")
        return value

    def validate_name(self, value):
        """Validate name field."""
        if not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_subject(self, value):
        """Validate subject field."""
        if not value.strip():
            raise serializers.ValidationError("Subject is required.")
        return value

    def validate_message(self, value):
        """Validate message field."""
        if not value.strip():
            raise serializers.ValidationError("Message is required.")
        return value
    