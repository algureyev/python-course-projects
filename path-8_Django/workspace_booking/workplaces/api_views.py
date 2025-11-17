from rest_framework import permissions, viewsets

from employees.permissions import IsAdmin, IsKeeper

from .models import Workplace
from .serializers import WorkplaceSerializer


class WorkplaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления рабочими местами
    """

    queryset = Workplace.objects.select_related("employee").all()
    serializer_class = WorkplaceSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsKeeper | IsAdmin]

        return [permission() for permission in permission_classes]
