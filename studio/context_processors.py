from .models import SiteSettings

def site_settings(request):
    settings, _ = SiteSettings.objects.get_or_create(pk=1)
    return {'site': settings, 'is_admin_area': request.path.startswith('/devio-admin/')}
