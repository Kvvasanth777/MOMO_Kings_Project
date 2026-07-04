from django.urls import path
from .views import ProcessPaymentView, PaymentSuccessView, DownloadInvoiceView

urlpatterns = [
    path('process/<int:order_id>/', ProcessPaymentView.as_view(), name='process_payment'),
    path('success/<int:order_id>/', PaymentSuccessView.as_view(), name='payment_success'),
    path('invoice/<int:order_id>/', DownloadInvoiceView.as_view(), name='download_invoice'),
]
