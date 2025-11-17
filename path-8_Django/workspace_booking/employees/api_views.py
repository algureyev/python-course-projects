from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from workplaces.models import Workplace

from .filters import EmployeeFilter
from .models import EmployeeImage, EmployeeProfile, EmployeeSkill
from .permissions import IsAdmin, IsAdminOrReadOnly, IsKeeper, IsViewer
from .serializers import (EmployeeImageSerializer,
                          EmployeeProfileCreateSerializer,
                          EmployeeProfileSerializer, EmployeeSkillSerializer)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления сотрудниками с разными уровнями доступа
    """

    queryset = (
        EmployeeProfile.objects.prefetch_related("employeeskill_set__skill", "images")
        .select_related("workplace")
        .all()
    )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = ["first_name", "last_name", "middle_name"]
    ordering_fields = ["first_name", "last_name", "hire_date", "work_experience_days"]
    ordering = ["-hire_date"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return EmployeeProfileCreateSerializer
        return EmployeeProfileSerializer

    def get_permissions(self):
        """
        Настройка прав доступа в зависимости от действия и роли пользователя
        """
        if self.action in ["list", "retrieve"]:
            # Просмотр доступен всем аутентифицированным пользователям
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == "update_workplace":
            # Обновление рабочего места - смотрителям и администраторам
            permission_classes = [permissions.IsAuthenticated, IsKeeper | IsAdmin]
        elif self.action in ["create", "destroy"]:
            # Создание и удаление - только администраторам
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        elif self.action in ["update", "partial_update"]:
            # Обновление информации - администраторам
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Создание сотрудника с привязкой к пользователю (только для администраторов)
        """
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied(
                "Только администраторы могут создавать сотрудников"
            )

        username = f"{serializer.validated_data['first_name'].lower()}_{serializer.validated_data['last_name'].lower()}"
        user = User.objects.create_user(
            username=username, password="defaultpassword123"
        )
        serializer.save(user=user)

    @action(detail=True, methods=["patch"])
    def update_workplace(self, request, pk=None):
        """
        Эндпоинт для перемещения сотрудника между столами
        Доступен смотрителям и администраторам
        """
        employee = self.get_object()
        workplace_id = request.data.get("workplace_id")

        if not workplace_id:
            return Response(
                {"error": "workplace_id обязателен"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            workplace = Workplace.objects.get(id=workplace_id)
            employee.workplace = workplace
            employee.save()

            serializer = self.get_serializer(employee)
            return Response(serializer.data)

        except Workplace.DoesNotExist:
            return Response(
                {"error": "Рабочее место не найдено"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["get"])
    def skills(self, request, pk=None):
        """
        Получение навыков конкретного сотрудника
        """
        employee = self.get_object()
        skills = EmployeeSkill.objects.filter(employee=employee)
        serializer = EmployeeSkillSerializer(skills, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def images(self, request, pk=None):
        """
        Получение изображений конкретного сотрудника
        """
        employee = self.get_object()
        images = EmployeeImage.objects.filter(employee=employee)
        serializer = EmployeeImageSerializer(images, many=True)
        return Response(serializer.data)


class EmployeeSkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления навыками сотрудников
    """

    queryset = EmployeeSkill.objects.select_related("employee", "skill").all()
    serializer_class = EmployeeSkillSerializer
    permission_classes = [permissions.IsAdminUser]  # Только администраторы


class EmployeeImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления изображениями сотрудников
    """

    queryset = EmployeeImage.objects.select_related("employee").all()
    serializer_class = EmployeeImageSerializer
    permission_classes = [permissions.IsAdminUser]  # Только администраторы
