from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Service, PortfolioProject, PricingPlan, Order, OrderReply, ContactMessage, Profile
from .forms import RegisterForm, OrderForm, OrderReplyForm, ContactForm, ProfileForm
from django.forms import modelform_factory
from .models import SiteSettings

def home(request): return render(request,'home.html',{'services':Service.objects.filter(active=True)[:4],'projects':PortfolioProject.objects.filter(featured=True)[:3]})
def services(request): return render(request,'services.html',{'services':Service.objects.filter(active=True)})
def portfolio(request): return render(request,'portfolio.html',{'projects':PortfolioProject.objects.all()})
def pricing(request): return render(request,'pricing.html',{'plans':PricingPlan.objects.all()})
def about(request): return render(request,'about.html')
def contact(request):
    form=ContactForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        form.save(); messages.success(request,'Xabaringiz qabul qilindi. Tez orada siz bilan bog‘lanamiz!'); return redirect('contact')
    return render(request,'contact.html',{'form':form})
def register(request):
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save(); login(request,user); messages.success(request,'Xush kelibsiz! Hisobingiz muvaffaqiyatli yaratildi.'); return redirect('dashboard')
    return render(request,'accounts/register.html',{'form':form})
@login_required
def order(request):
    form=OrderForm(request.POST or None, initial={'service':request.GET.get('plan','')})
    if request.method=='POST' and form.is_valid():
        profile, _ = Profile.objects.get_or_create(user=request.user)
        obj=form.save(commit=False); obj.user=request.user; obj.name=request.user.get_full_name() or request.user.username; obj.phone=profile.phone; obj.telegram=profile.telegram; obj.save(); messages.success(request,'Zakazingiz qabul qilindi! Tez orada javob olasiz.'); return redirect('my_orders')
    return render(request,'order.html',{'form':form})
@login_required
def dashboard(request):
    orders=request.user.orders.all(); return render(request,'dashboard/home.html',{'orders':orders[:5],'active':orders.exclude(status='done').count(),'completed':orders.filter(status='done').count(),'unread_replies':OrderReply.objects.filter(order__user=request.user,is_read=False).count()})
@login_required
def my_orders(request): return render(request,'dashboard/orders.html',{'orders':request.user.orders.all()})
@login_required
def profile(request):
    profile,_=Profile.objects.get_or_create(user=request.user)
    form=ProfileForm(request.POST or None,request.FILES or None,instance=profile,initial={'first_name':request.user.first_name,'last_name':request.user.last_name,'email':request.user.email})
    if request.method=='POST' and form.is_valid():
        form.save(); request.user.first_name=form.cleaned_data['first_name']; request.user.last_name=form.cleaned_data['last_name']; request.user.email=form.cleaned_data['email']; request.user.save(); messages.success(request,'Profil yangilandi.'); return redirect('profile')
    return render(request,'dashboard/profile.html',{'form':form,'profile_obj':profile})
@login_required
def messages_page(request):
    replies=OrderReply.objects.filter(order__user=request.user).select_related('order')
    replies.filter(is_read=False).update(is_read=True)
    return render(request,'dashboard/messages.html', {'replies':replies})
@login_required
def settings_page(request): return render(request,'dashboard/settings.html')
@user_passes_test(lambda u:u.is_staff)
def admin_panel(request):
    orders = Order.objects.all()
    return render(request,'adminpanel/home.html',{
        'users':User.objects.count(), 'orders':orders[:8], 'messages':ContactMessage.objects.filter(is_read=False).count(),
        'projects':PortfolioProject.objects.count(), 'services':Service.objects.filter(active=True).count(),
        'new_orders':orders.filter(status='new').count(), 'working_orders':orders.filter(status='working').count(),
        'ready_orders':orders.filter(status='ready').count(), 'done_orders':orders.filter(status='done').count(),
        'unread_replies':OrderReply.objects.filter(is_read=False).count(),
    })

ADMIN_MODELS = {
    'zakazlar': (Order, ['status']),
    'xizmatlar': (Service, ['title','icon','description','active']),
    'portfolio': (PortfolioProject, ['name','category','description','image','link','featured']),
    'narxlar': (PricingPlan, ['name','price','features','featured']),
    'xabarlar': (ContactMessage, ['name','email','message','is_read']),
    'sozlamalar': (SiteSettings, ['site_name','owner_name','description','telegram','instagram','logo','hero_title','hero_description','contact_title']),
    'foydalanuvchilar': (User, ['username','first_name','last_name','email','is_active','is_staff']),
}
def _admin_model(section):
    if section not in ADMIN_MODELS: raise Http404
    return ADMIN_MODELS[section]
@user_passes_test(lambda u:u.is_staff)
def admin_list(request, section):
    model, _ = _admin_model(section)
    return render(request, 'adminpanel/list.html', {'section':section, 'items':model.objects.all(), 'model_name':model._meta.verbose_name_plural})
@user_passes_test(lambda u:u.is_staff)
def received_orders(request):
    orders = Order.objects.select_related('user', 'user__profile').prefetch_related('replies').all()
    return render(request, 'adminpanel/received_orders.html', {'orders': orders})
@user_passes_test(lambda u:u.is_staff)
def admin_edit(request, section, pk=None):
    model, fields = _admin_model(section)
    if section == 'sozlamalar':
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
    else: obj = get_object_or_404(model, pk=pk) if pk else None
    Form = modelform_factory(model, fields=fields)
    form = Form(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Ma’lumot muvaffaqiyatli saqlandi.'); return redirect('admin_list', section=section)
    return render(request, 'adminpanel/form.html', {'form':form, 'section':section, 'editing':bool(obj)})
@user_passes_test(lambda u:u.is_staff)
def admin_delete(request, section, pk):
    model, _ = _admin_model(section)
    if section == 'sozlamalar': messages.error(request, 'Asosiy sozlamalarni o‘chirib bo‘lmaydi.'); return redirect('admin_list', section=section)
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST': obj.delete(); messages.success(request, 'Ma’lumot o‘chirildi.'); return redirect('admin_list', section=section)
    return render(request, 'adminpanel/delete.html', {'item':obj, 'section':section})
@user_passes_test(lambda u:u.is_staff)
def admin_order_reply(request, pk):
    order = get_object_or_404(Order.objects.select_related('user__profile'), pk=pk)
    form = OrderReplyForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        reply=form.save(commit=False); reply.order=order; reply.author=request.user; reply.save(); messages.success(request, 'Javob mijozga yuborildi.'); return redirect('admin_order_reply', pk=pk)
    return render(request, 'adminpanel/order_reply.html', {'order':order, 'form':form, 'replies':order.replies.select_related('author')})
def error_404(request, exception): return render(request, '404.html', status=404)
