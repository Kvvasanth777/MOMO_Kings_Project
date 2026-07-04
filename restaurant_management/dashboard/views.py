import csv
from decimal import Decimal
from io import BytesIO

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.utils import timezone

from orders.models import Order, OrderItem
from menu.models import FoodItem, Category
from accounts.models import User

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('login')


class AdminDashboardView(StaffRequiredMixin, View):
    def get(self, request):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)

        successful_statuses = [
            'Confirmed', 'Preparing', 'Ready',
            'Out For Delivery', 'Delivered', 'Completed'
        ]

        today_sales = (
            Order.objects
            .filter(created_at__date=today, status__in=successful_statuses)
            .aggregate(total=Sum('grand_total'))['total'] or Decimal('0.00')
        )
        monthly_sales = (
            Order.objects
            .filter(created_at__date__gte=start_of_month, status__in=successful_statuses)
            .aggregate(total=Sum('grand_total'))['total'] or Decimal('0.00')
        )
        total_revenue = (
            Order.objects
            .filter(status__in=successful_statuses)
            .aggregate(total=Sum('grand_total'))['total'] or Decimal('0.00')
        )
        total_profit = total_revenue * Decimal('0.35')

        orders_qs = Order.objects.all().order_by('-created_at')
        pending_count = orders_qs.filter(status='Pending').count()
        preparing_count = orders_qs.filter(status='Preparing').count()
        ready_count = orders_qs.filter(status='Ready').count()
        delivered_count = orders_qs.filter(status__in=['Delivered', 'Completed']).count()
        cancelled_count = orders_qs.filter(status='Cancelled').count()

        best_selling_items = (
            OrderItem.objects
            .values('food_item__name')
            .annotate(total_qty=Sum('quantity'))
            .order_by('-total_qty')[:5]
        )
        best_selling_categories = (
            OrderItem.objects
            .values('food_item__category__name')
            .annotate(total_qty=Sum('quantity'))
            .order_by('-total_qty')[:3]
        )

        context = {
            'today_sales': today_sales,
            'monthly_sales': monthly_sales,
            'total_revenue': total_revenue,
            'total_profit': total_profit,
            'orders': orders_qs[:10],
            'pending_count': pending_count,
            'preparing_count': preparing_count,
            'ready_count': ready_count,
            'delivered_count': delivered_count,
            'cancelled_count': cancelled_count,
            'best_selling_items': best_selling_items,
            'best_selling_categories': best_selling_categories,
            'total_customers': User.objects.count(),
            'total_items': FoodItem.objects.filter(is_active=True).count(),
        }
        return render(request, 'dashboard/dashboard.html', context)


class UpdateOrderStatusView(StaffRequiredMixin, View):
    def post(self, request, order_id):
        new_status = request.POST.get('status')
        valid_statuses = [
            'Pending', 'Confirmed', 'Preparing', 'Ready',
            'Out For Delivery', 'Delivered', 'Completed', 'Cancelled'
        ]
        order = get_object_or_404(Order, id=order_id)
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'message': f"Status updated to {new_status}."})
        return JsonResponse({'success': False, 'message': "Invalid status."}, status=400)


class ExportSalesCSVView(StaffRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="momo_kings_sales.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Order ID', 'Customer Name', 'Email', 'Phone',
            'Type', 'Subtotal', 'GST', 'Packing', 'Discount',
            'Grand Total', 'Status', 'Date'
        ])
        for order in Order.objects.all().order_by('-created_at'):
            writer.writerow([
                order.id, order.customer_name, order.email, order.phone_number,
                order.delivery_type, order.subtotal, order.gst, order.packing_charge,
                order.discount, order.grand_total, order.status,
                order.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        return response


class ExportSalesPDFView(StaffRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="momo_kings_sales_report.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            'T', parent=styles['Heading1'],
            fontName='Helvetica-Bold', fontSize=22,
            textColor=colors.black, spaceAfter=12
        )
        sub_style = ParagraphStyle(
            'S', parent=styles['Normal'], fontSize=10,
            textColor=colors.HexColor('#666666'), spaceAfter=20
        )
        bold_style = ParagraphStyle(
            'B', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=10
        )

        story.append(Paragraph("MOMO KINGS — Sales Report", title_style))
        story.append(Paragraph(
            f"Generated: {timezone.now().strftime('%d-%b-%Y %H:%M')}", sub_style
        ))

        successful = ['Confirmed', 'Preparing', 'Ready', 'Out For Delivery', 'Delivered', 'Completed']
        total_rev = (
            Order.objects.filter(status__in=successful)
            .aggregate(Sum('grand_total'))['grand_total__sum'] or Decimal('0.00')
        )
        total_orders = Order.objects.count()
        avg_order = (total_rev / total_orders) if total_orders > 0 else Decimal('0.00')

        summary_data = [
            [Paragraph("<b>Total Orders</b>", bold_style), str(total_orders)],
            [Paragraph("<b>Total Revenue</b>", bold_style), f"Rs. {total_rev:.2f}"],
            [Paragraph("<b>Average Order Value</b>", bold_style), f"Rs. {avg_order:.2f}"],
        ]
        summary_table = Table(summary_data, colWidths=[180, 200])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))

        header = [
            Paragraph("<b>ID</b>", bold_style),
            Paragraph("<b>Customer</b>", bold_style),
            Paragraph("<b>Type</b>", bold_style),
            Paragraph("<b>Total</b>", bold_style),
            Paragraph("<b>Status</b>", bold_style),
        ]
        rows = [header]
        for order in Order.objects.all().order_by('-created_at')[:25]:
            rows.append([
                f"#{order.id}", order.customer_name, order.delivery_type,
                f"Rs. {order.grand_total:.2f}", order.status
            ])

        data_table = Table(rows, colWidths=[50, 160, 80, 100, 100])
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
        ]))
        story.append(data_table)
        doc.build(story)
        return response
