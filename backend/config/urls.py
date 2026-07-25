from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/v1/roadmaps/", include("apps.roadmaps.urls")),
    path("api/v1/coding/", include("apps.coding.urls")),
    path("api/v1/aptitude/", include("apps.aptitude.urls")),
    path("api/v1/interviews/", include("apps.interviews.urls")),
    path("api/v1/resumes/", include("apps.resumes.urls")),
    path("api/v1/skills/", include("apps.skills.urls")),
    path("api/v1/analytics/", include("apps.analytics.urls")),
    path("api/v1/ai/", include("apps.ai_assistant.urls")),
    path("api/v1/portfolios/", include("apps.portfolios.urls")),

    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
