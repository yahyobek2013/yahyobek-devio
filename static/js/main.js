const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('header nav');
const extraCss=document.createElement('link');extraCss.rel='stylesheet';extraCss.href='/static/css/replies.css';document.head.append(extraCss);
const profileCss=document.createElement('link');profileCss.rel='stylesheet';profileCss.href='/static/css/profile-menu.css';document.head.append(profileCss);
const clickFixCss=document.createElement('link');clickFixCss.rel='stylesheet';clickFixCss.href='/static/css/click-fix.css';document.head.append(clickFixCss);
const ordersAdminCss=document.createElement('link');ordersAdminCss.rel='stylesheet';ordersAdminCss.href='/static/css/orders-admin.css';document.head.append(ordersAdminCss);
const adminLayoutCss=document.createElement('link');adminLayoutCss.rel='stylesheet';adminLayoutCss.href='/static/css/admin-layout.css';document.head.append(adminLayoutCss);
const logoutModal=document.createElement('div');
logoutModal.className='logout-modal';
logoutModal.setAttribute('role','dialog');
logoutModal.setAttribute('aria-modal','true');
logoutModal.setAttribute('aria-labelledby','logout-modal-title');
logoutModal.hidden=true;
logoutModal.innerHTML='<div class="logout-modal__backdrop"></div><div class="logout-modal__panel"><h2 id="logout-modal-title">Chiqishni xohlaysizmi?</h2><div class="logout-modal__actions"><button type="button" class="btn ghost logout-cancel">Yo‘q</button><button type="button" class="btn primary logout-confirm">Ha</button></div></div>';
document.body.append(logoutModal);
let pendingLogoutForm=null;
const closeLogoutModal=()=>{logoutModal.hidden=true;pendingLogoutForm=null};
logoutModal.querySelector('.logout-cancel').addEventListener('click',closeLogoutModal);
logoutModal.querySelector('.logout-modal__backdrop').addEventListener('click',closeLogoutModal);
logoutModal.querySelector('.logout-confirm').addEventListener('click',()=>{const form=pendingLogoutForm;closeLogoutModal();if(form)form.submit()});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!logoutModal.hidden)closeLogoutModal()});
document.querySelectorAll('form[data-logout-form="true"]').forEach(form=>{form.addEventListener('submit',event=>{event.preventDefault();pendingLogoutForm=form;logoutModal.hidden=false;logoutModal.querySelector('.logout-cancel').focus()})});
if(menu)menu.onclick=()=>nav.classList.toggle('open');
const profileMenu=document.querySelector('.profile-menu'),avatar=document.querySelector('.avatar');
if(avatar){avatar.onclick=(event)=>{event.stopPropagation();profileMenu.classList.toggle('open');avatar.setAttribute('aria-expanded',profileMenu.classList.contains('open'))};profileMenu.querySelector('.profile-dropdown').addEventListener('click',event=>event.stopPropagation());document.addEventListener('click',()=>profileMenu.classList.remove('open'))}
document.querySelectorAll('.filters button').forEach(button=>button.onclick=()=>{document.querySelectorAll('.filters button').forEach(item=>item.classList.remove('active'));button.classList.add('active');document.querySelectorAll('#projects .project').forEach(project=>project.style.display=(button.dataset.filter==='all'||project.dataset.category===button.dataset.filter)?'block':'none')});
setTimeout(()=>document.querySelectorAll('.notice').forEach(n=>n.style.opacity='0'),5000);
if(window.location.pathname==='/'){const style=document.createElement('style');style.textContent='.devio-intro{position:fixed;inset:0;z-index:9999;background:#070918;display:flex;align-items:center;justify-content:center;gap:clamp(10px,3vw,38px);font-family:Space Grotesk,sans-serif;transition:opacity .7s ease,visibility .7s ease}.devio-intro span{font-size:clamp(16px,3vw,28px);color:#b5b7cf;letter-spacing:.05em}.devio-intro b{font-size:clamp(38px,9vw,110px);letter-spacing:-.08em;background:linear-gradient(120deg,#bf88ff,#45c8ff);background-clip:text;-webkit-background-clip:text;color:transparent}.devio-intro.is-hidden{opacity:0;visibility:hidden}';document.head.append(style);const intro=document.createElement('div');intro.className='devio-intro';intro.innerHTML='<span>Yahyobek</span><b>DEVIO</b><span>Db</span>';document.body.prepend(intro);setTimeout(()=>intro.classList.add('is-hidden'),1350);setTimeout(()=>intro.remove(),2150)}
