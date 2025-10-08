from rest_framework.routers import DefaultRouter
from .views import InternshipViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'internships', InternshipViewSet, basename='internship')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = router.urls
