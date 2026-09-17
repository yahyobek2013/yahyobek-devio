from django.db import migrations

def seed(apps, schema_editor):
    Service=apps.get_model('studio','Service'); Plan=apps.get_model('studio','PricingPlan'); Project=apps.get_model('studio','PortfolioProject')
    for title,icon,description in [('Biznes sayt','◈','Kompaniyangizni ishonchli va zamonaviy ko‘rsatadigan korporativ sayt.'),('Internet do‘kon','▣','Qulay katalog, savat va xarid jarayoni bilan online savdo platformasi.'),('Shaxsiy portfolio','◇','Ishlaringiz va tajribangizni ta’sirli namoyish qiluvchi sayt.'),('Blog sayt','✎','Fikrlaringizni auditoriyaga yetkazish uchun tezkor blog.'),('Ta’lim platformasi','◎','Kurslar va o‘quvchilar uchun qulay raqamli muhit.'),('Django web-ilovalar','⌘','Murakkab jarayonlarni avtomatlashtiruvchi kuchli web-ilova.'),('Telegram bot','◉','Mijozlar bilan doimiy aloqada bo‘ladigan aqlli bot.'),('Landing page','↗','Konversiyaga yo‘naltirilgan bir sahifali taqdimot.')]: Service.objects.get_or_create(title=title,defaults={'icon':icon,'description':description})
    for name,price,features,featured in [('Boshlang‘ich','1 500 000 so‘mdan','Landing page\nMoslashuvchan dizayn\nAloqa formasi\n14 kunlik yordam',False),('Standart','3 500 000 so‘mdan','Ko‘p sahifali sayt\nIndividual dizayn\nAdmin boshqaruvi\nSEO asoslari\n30 kunlik yordam',True),('Premium','Kelishilgan narxda','Murakkab web-ilova\nMaxsus funksiyalar\nIntegratsiyalar\nTexnik yordam\nTo‘liq konsultatsiya',False)]: Plan.objects.get_or_create(name=name,defaults={'price':price,'features':features,'featured':featured})
    for name,cat,description in [('Nova Studio','business','Kreativ jamoa uchun zamonaviy raqamli vizitka.'),('Marketly','shop','Mahalliy brend uchun qulay online do‘kon.'),('Yahyobek Portfolio','portfolio','Ijodiy mutaxassisning ishlarini taqdim etuvchi portfolio.')]: Project.objects.get_or_create(name=name,defaults={'category':cat,'description':description,'featured':True})
def unseed(apps,schema_editor): pass
class Migration(migrations.Migration):
    dependencies=[('studio','0001_initial')]
    operations=[migrations.RunPython(seed,unseed)]
