from rest_framework import viewsets
from .models import Internship, Application
from .serializers import InternshipSerializer, ApplicationSerializer
from .permissions import IsOwnerBusinessmanOrReadOnly, IsStudentToApplyOrOwnerDelete



class InternshipViewSet(viewsets.ModelViewSet):
    serializer_class = InternshipSerializer
    permission_classes = [IsOwnerBusinessmanOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Internship.objects.all().order_by("-created_at")

        mine = self.request.query_params.get("mine")
        if mine == "true" and user.is_authenticated and user.role == "employer":
            return queryset.filter(employer=user)


        return queryset.filter(status="open")

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by("-created_at")
    serializer_class = ApplicationSerializer
    permission_classes = [IsStudentToApplyOrOwnerDelete]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == "employer":
            return Application.objects.filter(internship__employer=user)
        elif user.is_authenticated and user.role == "student":
            return Application.objects.filter(student=user)
        return Application.objects.none()
