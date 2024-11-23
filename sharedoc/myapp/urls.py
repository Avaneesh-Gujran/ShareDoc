from django.urls import path,register_converter
from . import views
from uuid import UUID

class UUIDConverter:
    regex = '[0-9a-f-]{36}'  # Matches UUID format

    def to_python(self, value):
        return UUID(value)

    def to_url(self, value):
        return str(value)

# Register the UUID converter
register_converter(UUIDConverter, 'uuid')


urlpatterns = [
   # path('create/', views.create_document, name='create_document'),  # URL pattern for create_document
    #path('', views.dashboard, name='dashboard'),
    #path("signup/", views.signup_view, name="signup"),
   # path("dashboard/", views.dashboard, name="dashboard"),
   # path("logout/", views.logout_view, name="logout"),
    path('', views.dashboard, name='dashboard'),  # Dashboard view
    path('create/', views.create_document, name='create_document'),  # Create document view
    path('edit/<int:document_id>/', views.edit_document, name='edit_document'),  # Edit document view
    path('delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('save/<int:document_id>/', views.save_document, name='save_document'), 
    #path('load_documents/', views.load_documents, name='load_documents'),
    
    

]

"""path("documents/share/<int:document_id>/", views.share_document, name="share_document"),"""