from django.apps import AppConfig

class PaymentappConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'paymentapp'
    
    def ready(self):
        import logging
        logger = logging.getLogger(__name__)
        logger.info("🔥 PaymentappConfig ready() called!")
        import paymentapp.signals  # 確保 signals 在 app 啟動時會被註冊    
