import uuid
import razorpay
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from orders.models import Order, Notification
from .models import Payment, Invoice

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def get_razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


class ProcessPaymentView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        amount_paise = int(order.grand_total * 100)
        razorpay_order_id = f"order_mock_{uuid.uuid4().hex[:12]}"

        try:
            client = get_razorpay_client()
            razorpay_order = client.order.create({
                'amount': amount_paise,
                'currency': 'INR',
                'payment_capture': '1'
            })
            razorpay_order_id = razorpay_order['id']
        except Exception:
            # Fallback to mock ID for sandbox / offline testing
            pass

        context = {
            'order': order,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order_id,
            'amount_paise': amount_paise,
        }
        return render(request, 'payment/process.html', context)


class PaymentSuccessView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        payment_id = request.GET.get('payment_id', f"PAY-MOCK-{uuid.uuid4().hex[:8].upper()}")
        method = request.GET.get('method', 'Razorpay')

        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                'payment_id': payment_id,
                'amount': order.grand_total,
                'status': 'Success',
                'method': method,
            }
        )

        # Update order status
        order.status = 'Confirmed'
        order.save()

        # Generate invoice
        Invoice.objects.get_or_create(order=order)

        # Award loyalty points (10% of subtotal rounded)
        try:
            points_earned = max(1, int(Decimal(str(order.subtotal)) * Decimal('0.10')))
        except Exception:
            points_earned = 10

        request.user.loyalty_points += points_earned
        request.user.save()

        Notification.objects.create(
            user=request.user,
            message=f"Payment of Rs.{order.grand_total} received. Order #{order.id} is Confirmed!"
        )

        return render(request, 'payment/success.html', {
            'order': order,
            'points_earned': points_earned
        })


class DownloadInvoiceView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if not request.user.is_staff and order.user != request.user:
            raise Http404("You do not have permission to view this invoice.")

        invoice, _ = Invoice.objects.get_or_create(order=order)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.invoice_number}.pdf"'

        doc = SimpleDocTemplate(
            response, pagesize=letter,
            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
        )
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle', parent=styles['Heading1'],
            fontName='Helvetica-Bold', fontSize=24,
            textColor=colors.HexColor('#C5A880'), spaceAfter=15
        )
        sub_style = ParagraphStyle(
            'SubStyle', parent=styles['Normal'],
            fontName='Helvetica', fontSize=10,
            textColor=colors.HexColor('#333333'), spaceAfter=20
        )
        bold_style = ParagraphStyle(
            'BoldStyle', parent=styles['Normal'],
            fontName='Helvetica-Bold', fontSize=10,
            textColor=colors.black
        )

        story.append(Paragraph("MOMO KINGS", title_style))
        story.append(Paragraph(
            "Luxury Fine Dining &amp; Online Ordering<br/>Email: royal@momokings.com",
            sub_style
        ))
        story.append(Spacer(1, 10))

        details_data = [
            [Paragraph("<b>Invoice:</b>", bold_style), invoice.invoice_number,
             Paragraph("<b>Order:</b>", bold_style), f"#{order.id}"],
            [Paragraph("<b>Customer:</b>", bold_style), order.customer_name,
             Paragraph("<b>Date:</b>", bold_style), order.created_at.strftime('%d-%b-%Y')],
            [Paragraph("<b>Phone:</b>", bold_style), order.phone_number,
             Paragraph("<b>Mode:</b>", bold_style), order.delivery_type],
        ]
        details_table = Table(details_data, colWidths=[100, 160, 100, 160])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(details_table)
        story.append(Spacer(1, 20))

        items_data = [
            [Paragraph("<b>Item</b>", bold_style),
             Paragraph("<b>Qty</b>", bold_style),
             Paragraph("<b>Price</b>", bold_style),
             Paragraph("<b>Total</b>", bold_style)]
        ]

        for item in order.items.all():
            name = item.food_item.name if item.food_item else 'Deleted Item'
            items_data.append([
                name, str(item.quantity),
                f"Rs. {item.price:.2f}",
                f"Rs. {item.get_total_price():.2f}"
            ])

        items_data.extend([
            ["", "", Paragraph("<b>Subtotal:</b>", bold_style), f"Rs. {order.subtotal:.2f}"],
            ["", "", Paragraph("<b>Discount:</b>", bold_style), f"-Rs. {order.discount:.2f}"],
            ["", "", Paragraph("<b>Packing:</b>", bold_style), f"Rs. {order.packing_charge:.2f}"],
            ["", "", Paragraph("<b>GST (5%):</b>", bold_style), f"Rs. {order.gst:.2f}"],
            ["", "", Paragraph("<b>Grand Total:</b>", bold_style), f"Rs. {order.grand_total:.2f}"],
        ])

        items_table = Table(items_data, colWidths=[240, 60, 100, 120])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#C5A880')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#C5A880')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
        ]))

        story.append(items_table)
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "<center><b>Thank you for dining with Momo Kings!</b></center>",
            sub_style
        ))

        doc.build(story)
        return response
