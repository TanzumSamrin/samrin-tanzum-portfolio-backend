from rest_framework import serializers

from .models import (
    Education,
    Experience,
    Profile,
    Skill,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

    def validate_proficiency(self, value):
        if value < 1 or value > 100:
            raise serializers.ValidationError(
                "Proficiency must be between 1 and 100."
            )

        return value


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

    def validate(self, data):
        start_date = data.get(
            "start_date",
            getattr(self.instance, "start_date", None),
        )

        end_date = data.get(
            "end_date",
            getattr(self.instance, "end_date", None),
        )

        is_current = data.get(
            "is_current",
            getattr(self.instance, "is_current", False),
        )

        if is_current and end_date:
            raise serializers.ValidationError(
                {
                    "end_date": (
                        "Current experience cannot have an end date."
                    )
                }
            )

        if (
            start_date
            and end_date
            and end_date < start_date
        ):
            raise serializers.ValidationError(
                {
                    "end_date": (
                        "End date must be after start date."
                    )
                }
            )

        return data


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"

    def validate(self, data):
        start_year = data.get(
            "start_year",
            getattr(self.instance, "start_year", None),
        )

        end_year = data.get(
            "end_year",
            getattr(self.instance, "end_year", None),
        )

        if (
            start_year
            and end_year
            and end_year < start_year
        ):
            raise serializers.ValidationError(
                {
                    "end_year": (
                        "End year cannot be before start year."
                    )
                }
            )

        return data