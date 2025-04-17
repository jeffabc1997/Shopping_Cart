from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import logging
from cartapp.models import OrdersModel
from django.conf import settings

logger = logging.getLogger(__name__)  # 取得此模組的 logger
logger.info(f"📦 Signal module loaded! {settings.BASE_URL}")  # ← 加在這裡，app 啟動時就會印出來！
def paypal_payment_completed(sender, **kwargs):
    ipn_obj = sender
    # ipn_obj = kwargs['instance'] 
    logger.info("Received PayPal IPN: status=%s, invoice=%s", ipn_obj.payment_status, ipn_obj.invoice)
    # print(f"Received PayPal IPN: status=%s, invoice=%s", ipn_obj.payment_status, ipn_obj.invoice)
    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
        logger.warning("IPN receiver email does not match! Ignoring IPN.")
        return
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        try:
            order = OrdersModel.objects.get(id=ipn_obj.invoice)
            order.payment_completed = True
            order.save()
            logger.info("Order %s marked as paid.", order.id)

        except OrdersModel.DoesNotExist:
            logger.warning("Order with token %s not found!", ipn_obj.invoice)
            

valid_ipn_received.connect(paypal_payment_completed)