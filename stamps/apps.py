from django.apps import AppConfig

class StampsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stamps'

    def ready(self):
        import stamps.signals  # 신호 등록
