from rest_framework import serializers
from .models import Profile, Skill, Experience, Education

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        from datetime import date
        if data.get('start_date') and data['start_date'] > date.today():
            raise serializers.ValidationError({'start_date': 'Start date cannot be in the future.'})
        if data.get('is_current') and data.get('end_date'):
            raise serializers.ValidationError({'end_date': 'End date must be empty for current position.'})
        if not data.get('is_current') and not data.get('end_date'):
            raise serializers.ValidationError({'end_date': 'End date is required for past positions.'})
        if data.get('end_date') and data.get('start_date') and data['end_date'] < data['start_date']:
            raise serializers.ValidationError({'end_date': 'End date must be after start date.'})
        return data

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')