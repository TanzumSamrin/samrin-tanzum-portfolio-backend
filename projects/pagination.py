from rest_framework.pagination import PageNumberPagination


class ProjectPagination(PageNumberPagination):
    page_size = 9  # spec requires 9 per page for /api/projects/

    page_size_query_param = "page_size"

    max_page_size = 50