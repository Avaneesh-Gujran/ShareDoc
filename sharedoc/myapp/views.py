from django.shortcuts import render
from .forms import DocumentForm
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Document
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Document, Cursor

def dashboard(request):
    documents = Document.objects.all()
    return render(request, 'dashboard.html', {'documents': documents})

def create_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save()
            return redirect('edit_document', document_id=document.id)
    else:
        form = DocumentForm()
    return render(request, 'create_document.html', {'form': form})

def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.content = request.POST.get('content')
        document.save()
        return redirect('dashboard')
    return render(request, 'edit_document.html', {'document': document})

def save_document(request, document_id):
    if request.method == 'POST':
        document = get_object_or_404(Document, id=document_id)
        document.content = request.POST.get('content')
        document.save()
        return redirect('dashboard')

def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    return redirect('dashboard')


def get_document_state(request, document_id):
    try:
        document = Document.objects.get(id=document_id)
        cursors = document.cursors.all()
        cursor_data = [
            {'user_id': cursor.user_id, 'cursor_position': cursor.cursor_position}
            for cursor in cursors
        ]
        return JsonResponse({
            'content': document.content,
            'cursors': cursor_data
        })
    except Document.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

@csrf_exempt
def update_document_content(request, document_id):
    if request.method == "POST":
        try:
            document = Document.objects.get(id=document_id)
            document.content = request.POST.get('content', '')
            document.save()
            return JsonResponse({'status': 'success'})
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Document not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def update_cursor(request, document_id):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        cursor_position = request.POST.get('cursor_position')
        try:
            document = Document.objects.get(id=document_id)
            cursor, created = Cursor.objects.update_or_create(
                document=document,
                user_id=user_id,
                defaults={'cursor_position': cursor_position}
            )
            return JsonResponse({'status': 'success'})
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Document not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)
