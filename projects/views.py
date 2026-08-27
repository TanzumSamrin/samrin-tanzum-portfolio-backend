import django_filters
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project
from .serializers import ProjectSerializer
from .pagination import ProjectPagination
from permissions import IsOwnerOrReadOnly


class ProjectFilter(django_filters.FilterSet):
    # Spec's documented param is ?tech=<skill id or name>, not the raw
    # M2M field name ?tech_stack=.
    tech = django_filters.CharFilter(method='filter_tech')

    class Meta:
        model = Project
        fields = ['category', 'is_featured', 'tech']

    def filter_tech(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(tech_stack__id=value).distinct()
        return queryset.filter(tech_stack__name__iexact=value).distinct()


class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ProjectPagination  # 9 per page, per spec B-18
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['title', 'summary', 'description']
    # ordering_fields must be bare field names; DRF's OrderingFilter matches
    # the query param (e.g. ?ordering=-completed_date) against these and
    # applies the +/- direction itself.
    ordering_fields = ['completed_date', 'display_order']

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'slug'