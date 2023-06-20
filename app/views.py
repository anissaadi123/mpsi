from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Enseignant,Eleve,Classe,Travail,Commentaire
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



def check_user_role(user):
    try:
        enseignant = Enseignant.objects.get(user=user)
        return "enseignant"
    except Enseignant.DoesNotExist:
        pass

    try:
        eleve = Eleve.objects.get(user=user)
        return "eleve"
    except Eleve.DoesNotExist:
        pass

    return None

# Create your views here.
def home(request):

    return render(request,'all/home.html',{})

def lg(request):
     if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None :
            login(request, user)
            return redirect('app:home')  # Replace 'home' with the URL name of your home page
        else:
            error_message = 'username ou Mot de passe Invalide'
            return render(request, 'all/login.html', {'error_message': error_message})
     return render(request,'all/login.html',{})

def sign_up(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        classe = request.POST.get('classe')
        password = request.POST.get('password')
        is_teacher = 'teacherCheckbox' in request.POST
        user = User.objects.create(username=email,first_name=name,last_name=surname,password=password)
        

        if is_teacher: 
            enseignant = Enseignant.objects.create(user=user)
        else : 
            eleve = Eleve.objects.create(user=user)
            try:

                my_class = Classe.objects.get(name=classe)
            except ObjectDoesNotExist:
            # Class does not exist, create a new instance
                my_class = Classe(name=classe)
            
            my_class.eleves.add(eleve)
            my_class.save()

        # Redirect to a success page or do any further processing
        return redirect('app:home')
    return render(request,'all/signup.html',{})

def log_out(request):
    logout(request)
    return redirect("app:home")

def travaux(request):
    classes = Classe.objects.all()
    if request.method == 'POST':
        classe = request.POST.get('classe')
        if classe == "all": 
            trs = Travail.objects.all()
        else: 
            try:
                cl = Classe.objects.filter(name=classe)[0]
                trs = Travail.objects.filter(classe=cl)
                print("bbbbbbbbbbbbbbbb"+classe)
            except Classe.DoesNotExist or Travail.DoesNotExist:
               trs = Travail.objects.all()
               print("cccccccccccccccc"+classe)
           
    else:
        trs = Travail.objects.all()
    return render(request,'all/travaux.html',{"travaux":trs,'classes':classes})

@login_required
def mes_travaux(request):
    classes = Classe.objects.all()
    is_ens = True

    
    try:
        enseignant = Enseignant.objects.get(user=request.user)
        try:
            travaux = Travail.objects.filter(enseignant=enseignant)
        except Travail.DoesNotExist: 
            travaux = {}
    except Enseignant.DoesNotExist or Travail.DoesNotExist:
        is_ens = False

    if is_ens == False: 
        try:
            eleve = Eleve.objects.get(user=request.user)
            classe = Classe.objects.filter(name=eleve.classe.name)[0]

            travaux = Travail.objects.filter(classe=classe)
        except Eleve.DoesNotExist or Classe.DoesNotExist:
            travaux = {}
    
    return render(request,'all/mestravaux.html',{"travaux":travaux,'classes':classes,'is_ens':is_ens})


def ajouter_travail(request):  
    classes = Classe.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        date = request.POST.get('date')
        classe = request.POST.get('classe')
        up_file = request.FILES['file']

        cl = Classe.objects.get(id=classe)
        enseignant = Enseignant.objects.get(user=request.user)
        tr = Travail.objects.create(titre=name,description=desc,date_limite=date,classe=cl,fichier=up_file,enseignant =enseignant )
        return redirect('app:mestravaux')
    return render(request,'all/ajoutertravail.html',{'classes':classes})

def travail_details(request, pk): 
    tr = Travail.objects.get(pk=pk)
    cmnts = Commentaire.objects.filter(travail=tr)
    if request.method == 'POST': 
        gt = request.POST.get('desc')
        if gt  != "" :
            cmt = Commentaire.objects.create(travail=tr,auteur=request.user,contenu=gt)
            cmt.save()
            return redirect("app:travail_details", tr.pk)
    return render(request,'all/details.html', {"tr":tr,'cmnts': cmnts})