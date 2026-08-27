from rest_framework import generics, permissions
from .models import Profile, Skill, Experience, Education
from .serializers import ProfileSerializer, SkillSerializer, ExperienceSerializer, EducationSerializer
from permissions import IsOwnerOrReadOnly

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        return Profile.objects.first()

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name']
    ordering_fields = ['display_order', 'proficiency']

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsOwnerOrReadOnly]

class ExperienceListCreateView(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsOwnerOrReadOnly]

class ExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsOwnerOrReadOnly]

class EducationListCreateView(generics.ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsOwnerOrReadOnly]

class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsOwnerOrReadOnly]