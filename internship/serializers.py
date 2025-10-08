from rest_framework import serializers
from .models import Internship, Application

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = "__all__"
        read_only_fields = ["employer", "created_at"]


class ApplicationSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source="student.username")
    internship_title = serializers.ReadOnlyField(source="internship.title")

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["student", "status", "created_at"]
        
    def validate(self, attrs):
        student = self.context['request'].user
        internship = attrs.get('internship')
        if Application.objects.filter(student=student, internship=internship).exists():
            raise serializers.ValidationError("Вы уже подали заявку на эту стажировку.")
        return attrs