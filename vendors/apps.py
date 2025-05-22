from django.apps import AppConfig
# import firebase_admin
# from firebase_admin import credentials

class VendorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendors'
    def ready(self):
        # if not firebase_admin._apps:
        #     cred = credentials.Certificate('firebase/service-account.json')
        #     firebase_admin.initialize_app(cred)
        from caller_on.firebase import ensure_firebase_initialized
        ensure_firebase_initialized()


    
