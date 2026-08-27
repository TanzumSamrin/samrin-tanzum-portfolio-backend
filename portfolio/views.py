from rest_framework import generics
from rest_framework.exceptions import NotFound

from permissions import IsOwnerOrReadOnly


from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Education,
    Experience,
    Profile,
    Skill,
)
from .serializers import (
    EducationSerializer,
    ExperienceSerializer,
    ProfileSerializer,
    SkillSerializer,
)





class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        try:
            return Profile.objects.get()
        except Profile.DoesNotExist:
            raise NotFound(
                "Profile has not been created yet."
            )
        


class SkillListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsOwnerOrReadOnly]


class SkillDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsOwnerOrReadOnly]




class ExperienceListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ExperienceDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsOwnerOrReadOnly]



class EducationListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsOwnerOrReadOnly]


class EducationDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsOwnerOrReadOnly]




class SkillListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "category",
    ]

    search_fields = [
        "name",
    ]

    ordering_fields = [
        "order",
        "proficiency",
        "name",
    ]

    ordering = [
        "order",
        "name",
    ]