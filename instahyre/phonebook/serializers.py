from rest_framework import serializers
from .models import MyUser, PhoneEntry, SpamReport, ContactList


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['id', 'full_name', 'email', 'mobile', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_mobile(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Mobile number must be 10 digits.")
        return value

    def create(self, validated_data):
        mobile = validated_data.get('mobile')
        phone_entry, _ = PhoneEntry.objects.get_or_create(number=mobile,name = validated_data.get("full_name"))

        # Create the user instance
        user = MyUser.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data.get('email', ''),
            mobile=mobile,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class PhoneEntrySerializer(serializers.ModelSerializer):
    marked_by = serializers.StringRelatedField(many=True)

    class Meta:
        model = PhoneEntry
        fields = ['id', 'name', 'number', 'spam_score', 'is_spam', 'marked_by']

class SpamReportSerializer(serializers.ModelSerializer):
   class Meta:
        model = ContactList
        fields = "__all__"
    
class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactList
        fields = ['id', 'user', 'contact_name', 'contact_number']
    
    def create(self, validated_data):
        contact = super().create(validated_data)
        # Create or update the associated PhoneEntry record
        mobile = contact.contact_number
        _, _ = PhoneEntry.objects.get_or_create(number=mobile,name = contact.contact_name)
        return contact