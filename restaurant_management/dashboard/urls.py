from django.urls import path
from .views import AdminDashboardView, UpdateOrderStatusView, ExportSalesCSVView, ExportSalesPDFView

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('order/<int:order_id>/update/', UpdateOrderStatusView.as_view(), name='update_order_status'),
    path('export/csv/', ExportSalesCSVView.as_view(), name='export_sales_csv'),
    path('export/pdf/', ExportSalesPDFView.as_view(), name='export_sales_pdf'),
]
