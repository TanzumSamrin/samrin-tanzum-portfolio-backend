from rest_framework.pagination import PageNumberPagination


class ContactPagination(PageNumberPagination):
    page_size = 10  # spec requires 10 per page for /api/contact/

    page_size_query_param = "page_size"

    max_page_size = 50


class CommentPagination(PageNumberPagination):
    page_size = 10  # spec requires 10 per page for /api/comments/ moderation list

    page_size_query_param = "page_size"

    max_page_size = 50
