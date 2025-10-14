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


        return queryset

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsStudentToApplyOrOwnerDelete]

    def get_queryset(self):
        user = self.request.user

        # Если пользователь не авторизован — ничего не возвращаем
        if not user.is_authenticated:
            return Application.objects.none()

        # Работодатель видит заявки только на свои стажировки
        if user.role == "employer":
            return Application.objects.filter(internship__employer=user)

        # Студент видит только свои заявки
        if user.role == "student":
            return Application.objects.filter(student=user)

        # Учитель видит все заявки, может фильтровать по студенту (?student_id=...)
        if user.role == "teacher":
            queryset = Application.objects.all().order_by("-created_at")
            student_id = self.request.query_params.get("student_id")
            if student_id:
                queryset = queryset.filter(student__id=student_id)
            return queryset

        # Остальные роли — ничего
        return Application.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

