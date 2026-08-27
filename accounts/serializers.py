from django.contrib.auth import authenticate

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid username or password.",
                code="authorization",
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive.",
                code="authorization",
            )

        if not user.is_superuser:
            raise serializers.ValidationError(
                "Only the portfolio owner can log in.",
                code="authorization",
            )

        attrs["user"] = user

        return attrs