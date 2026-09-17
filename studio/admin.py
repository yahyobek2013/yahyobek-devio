from django.contrib import admin
from .models import Profile, Service, PortfolioProject, PricingPlan, Order, OrderReply, ContactMessage, SiteSettings
admin.site.site_header = 'DEVIO boshqaruvi'
admin.site.register([Profile, Service, PortfolioProject, PricingPlan, Order, OrderReply, ContactMessage, SiteSettings])
