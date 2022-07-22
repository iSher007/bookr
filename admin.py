from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path


class BookrAdminSite(AdminSite):
    site_title = 'Bookr site Admin'
    site_header = 'Bookr administration'
    index_title = 'Site Administration'
    logout_template = 'logged_out.html'

    def get_urls(self):
        urls = super().get_urls()
        url_patterns = [path('admin_profile/', self.admin_view(self.profile_view))]
        return url_patterns + urls

    def profile_view(self, request):
        request.current_app = self.name
        context = self.each_context(request)
        context['username'] = request.user.username
        return TemplateResponse(request, "admin/admin_profile.html", context)
