from rest_framework import serializers
from .models import Project
from core.serializers import SkillSerializer

class ProjectSerializer(serializers.ModelSerializer):
    tech_stack_detail = SkillSerializer(source='tech_stack', many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('slug', 'created_at', 'updated_at')

    def validate(self, data):
        if not data.get('live_url') and not data.get('github_url'):
            raise serializers.ValidationError('At least one of live_url or github_url must be provided.')
        return data