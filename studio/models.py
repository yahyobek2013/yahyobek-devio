from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    telegram = models.CharField(max_length=80, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    def __str__(self): return self.user.username

class Service(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=30, default='✦')
    description = models.TextField()
    active = models.BooleanField(default=True)
    def __str__(self): return self.title

class PortfolioProject(models.Model):
    CATEGORIES = [('business','Biznes'),('shop','Internet do‘kon'),('portfolio','Portfolio'),('education','Ta’lim')]
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    link = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    def __str__(self): return self.name

class PricingPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    features = models.TextField(help_text='Har qatorga bitta imkoniyat')
    featured = models.BooleanField(default=False)
    def __str__(self): return self.name

class Order(models.Model):
    STATUS = [('new','Yangi'),('contacted','Bog‘lanildi'),('working','Ishlanmoqda'),('ready','Tayyor'),('done','Tugallandi')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    telegram = models.CharField(max_length=80, blank=True)
    service = models.CharField(max_length=100)
    website_info = models.TextField()
    budget = models.CharField(max_length=80)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.service})'

class OrderReply(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    attachment = models.ImageField(upload_to='order_replies/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta: ordering = ['created_at']
    def __str__(self): return f'Javob: {self.order.service}'

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self): return self.name

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=50, default='DEVIO')
    owner_name = models.CharField(max_length=100, default='Yahyobek Db')
    description = models.CharField(max_length=250, default='Raqamli g‘oyalaringizni kuchli web tajribaga aylantiramiz.')
    telegram = models.CharField(max_length=100, default='Yahyobek_bro')
    instagram = models.CharField(max_length=100, default='yahyobek_x')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_title = models.CharField(max_length=180, default='Zamonaviy va tezkor saytlar yaratamiz')
    hero_description = models.TextField(default='G‘oyangizni foydalanuvchilar sevib ishlatadigan, natija beradigan raqamli mahsulotga aylantiramiz.')
    contact_title = models.CharField(max_length=180, default='G‘oyangizni muhokama qilamiz.')
    def save(self,*args,**kwargs):
        self.pk = 1
        super().save(*args,**kwargs)
