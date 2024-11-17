from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from .models import Document
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document,CustomUser
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.http import JsonResponse

def dashboard(request):
    owned_documents = Document.objects.all()
    
    #shared_documents = request.user.shared_documents.all()  # Documents shared with the user

    return render(request, "dashboard.html", {
        "documents": owned_documents,
        #"shared_documents": shared_documents,
    })


def create_document(request):
    
    new_doc = Document.objects.create()
    print("This is the user: ",request.user)
    return redirect('edit_document', document_id=new_doc.id)


def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return render(request, 'edit_document.html', {'document': document})


def save_document(request, document_id):
    if request.method == 'POST':
        document = get_object_or_404(Document, id=document_id)
        document.content = request.POST.get('content')
        
        document.save()
        # Redirect back to the edit page after saving
    
    return redirect('dashboard') 

def load_documents(request):
    page_number = request.GET.get('page', 1)
    documents = Document.objects.all().order_by('-created_at')
    paginator = Paginator(documents, 5)  
    # 5 documents per page
    page = paginator.get_page(page_number)

    documents_data = [{
        'id': str(document.id),
        'created_date': document.created_at.strftime('%Y-%m-%d %H:%M')
    } for document in page]

    return JsonResponse({
        'documents': documents_data,
        'has_more': page.has_next()
    })

def view_document(request, share_link):
    # Fetch the document using the unique share link
    document = get_object_or_404(Document, share_link=share_link)
    return render(request, 'edit_document.html', {'document': document})

"""def share_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)
    if request.method == "POST":
        email = request.POST.get("email")
        user_to_share = User.objects.filter(email=email).first()

        if user_to_share:
            document.shared_with.add(user_to_share)
            share_link = request.build_absolute_uri(f"/documents/view/{document.share_link}/")

            # Send email with the share link
            send_mail(
                subject="Document Shared with You",
                message=f"You've been invited to edit the document. Access it here: {share_link}",
                from_email="your-email@example.com",
                recipient_list=[email],
            )
            return redirect("edit_document", document_id=document_id)
    return render(request, "share_document.html", {"document": document})"""

def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':  # Ensure deletion is only performed with a POST request
        document.delete()
        return redirect('dashboard')
    

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        print("this is your name: ",name," this is the email: ",email," this is the phone number: ",phone_number," password for ths same: ",password)

        # Create a new user
        user = CustomUser.objects.create_user(
            username=email,  # Use email as the username
            email=email,
            name=name,
            phone_number=phone_number,
        )
        user.set_password(password)  # Set the password securely
        user.save()

        return redirect("login")  # Redirect to login page after sign-up

    return render(request, "signup.html")

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print("Hello my name is : ",username,"my password is this ",password)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")



def save_document(request, document_id):
    """
    Save document changes.
    """
    if request.method == 'POST':
        document = get_object_or_404(Document, id=document_id)
        document.content = request.POST.get('content', '')
        document.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")