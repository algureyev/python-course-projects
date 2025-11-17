from rest_framework import serializers

from .models import EmployeeImage, EmployeeProfile, EmployeeSkill, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class EmployeeSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), source="skill", write_only=True
    )

    class Meta:
        model = EmployeeSkill
        fields = ["id", "skill", "skill_id", "level"]


class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImage
        fields = ["id", "image", "order"]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    skills = EmployeeSkillSerializer(
        many=True, read_only=True, source="employeeskill_set"
    )
    images = EmployeeImageSerializer(many=True, read_only=True)
    work_experience_days = serializers.ReadOnlyField()
    workplace_table = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "gender",
            "work_experience_days",
            "description",
            "hire_date",
            "skills",
            "images",
            "workplace_table",
        ]
        read_only_fields = ["id", "work_experience_days"]

    def get_workplace_table(self, obj):
        if hasattr(obj, "workplace") and obj.workplace:
            return obj.workplace.table_number
        return None


class EmployeeProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "gender",
            "description",
            "hire_date",
        ]
