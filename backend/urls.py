from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# ✅ Custom Error Handler for 404 (Page Not Found)
def custom_404_view(request, exception):
    return JsonResponse({"error": "API endpoint not found"}, status=404)

# ✅ Custom Error Handler for 500 (Server Error)
def custom_500_view(request):
    return JsonResponse({"error": "Internal server error"}, status=500)

urlpatterns = [
    path("admin/", admin.site.urls),  # Django Admin Panel
    path("api/", include("tests.urls")),  # ✅ Include API routes
]

# ✅ Assign custom error handlers
handler404 = custom_404_view
handler500 = custom_500_view
