from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

# ✅ Error Handlers - JSON Response for API Consistency
def custom_404_view(request, exception):
    return JsonResponse({"error": "API endpoint not found"}, status=404)

def custom_500_view(request):
    return JsonResponse({"error": "Internal server error"}, status=500)

# ✅ Main URL Patterns
urlpatterns = [
    path("admin/", admin.site.urls),  # Django Admin Panel
    path("api/", include("tests.urls")),  # ✅ Include API routes
]

# ✅ Static & Media Files Handling (for local development)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ✅ Assign custom error handlers
handler404 = custom_404_view
handler500 = custom_500_view

