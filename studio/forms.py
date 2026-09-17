from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, OrderReply, ContactMessage, Profile

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Ism', max_length=150)
    phone = forms.CharField(label='Telefon raqami', max_length=30)
    telegram = forms.CharField(label='Telegram username', max_length=80, required=False)
    class Meta:
        model = User
        fields = ('first_name','username','password1','password2')
        labels = {'username':'Foydalanuvchi nomi'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            Profile.objects.update_or_create(user=user, defaults={
                'phone': self.cleaned_data['phone'],
                'telegram': self.cleaned_data['telegram'],
            })
        return user

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service','website_info','budget','note']
        labels = {'service':'Qaysi xizmat kerak?','website_info':'Qanday sayt kerakligini sodda qilib tushuntiring','budget':'Taxminiy budjet','note':'Qo‘shimcha izoh (ixtiyoriy)'}
        widgets = {'website_info':forms.Textarea(attrs={'rows':4,'placeholder':'Masalan: kiyim do‘konim uchun mahsulotlar va buyurtma qabul qiladigan sayt kerak.'}),'note':forms.Textarea(attrs={'rows':3,'placeholder':'Muhim qo‘shimcha ma’lumotlaringizni yozing.'}), 'service':forms.Select(choices=[('', 'Xizmatni tanlang'),('Biznes sayt','Biznes sayt'),('Internet do‘kon','Internet do‘kon'),('Shaxsiy portfolio','Shaxsiy portfolio'),('Blog sayt','Blog sayt'),('Ta’lim platformasi','Ta’lim platformasi'),('Django web-ilovalar','Django web-ilovalar'),('Telegram bot','Telegram bot'),('Landing page','Landing page')])}

class OrderReplyForm(forms.ModelForm):
    class Meta:
        model = OrderReply
        fields = ['message','attachment']
        labels = {'message':'Javobingiz','attachment':'Rasm biriktirish (ixtiyoriy)'}
        widgets = {'message':forms.Textarea(attrs={'rows':5,'placeholder':'Mijozga javobingizni yozing. Emoji ham ishlatishingiz mumkin 🙂'})}

class ContactForm(forms.ModelForm):
    class Meta:
        model=ContactMessage
        fields=['name','email','message']
        labels={'name':'Ismingiz','email':'Email manzilingiz','message':'Xabaringiz'}
        widgets={'message':forms.Textarea(attrs={'rows':5})}

class ProfileForm(forms.ModelForm):
    first_name=forms.CharField(label='Ism', required=False)
    last_name=forms.CharField(label='Familiya', required=False)
    email=forms.EmailField(label='Email')
    class Meta:
        model=Profile
        fields=['phone','telegram','photo']
        labels={'phone':'Telefon','telegram':'Telegram username','photo':'Profil rasmi'}
