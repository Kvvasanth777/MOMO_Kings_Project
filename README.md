# MOMO KINGS - Luxury Restaurant Management & Online Food Ordering System

Welcome to **Momo Kings**, a premium, production-ready full-stack web application designed for a luxury 5-star fine-dining restaurant. The interface draws elegant inspiration from Marriott, Taj, and ITC properties using dark mode overlays, gold gradients, glassmorphism cards, and fluid animations.

---

## Technical Stack
- **Backend:** Python 3.13, Django 5.x, Django REST Framework, SQLite (Default with MySQL option), Pillow, Razorpay SDK, ReportLab (PDF), Qrcode (Dynamic QR generator)
- **Frontend:** HTML5, CSS3 (Custom Luxury variables, responsive grids), Bootstrap 5, Javascript, AJAX, FontAwesome Icons, Google Fonts (Playfair Display / Outfit)

---

## Features
1. **Dynamic Menu System:** Organized by categories with Veg/Non-Veg badges, spice intensities, ratings, calories, prep time, price sorting, and voice search.
2. **Slide-Out Shopping Cart:** AJAX-powered slide cart drawer calculating GST (5%), Packing Fees (Rs. 30), and coupons.
3. **Interactive Checkout & Dining Modes:** Choice of Delivery (with address field), Takeaway, or Dine-In (reveals conditional Table Number field).
4. **Secure Payment Gateways:** Live Razorpay checkout script callback, Mock UPI payment triggers, and Cash on Delivery support.
5. **Interactive Order Tracking:** Dynamic visual progress line tracking state changes (Pending -> Confirmed -> Cooking -> Ready -> Out For Delivery -> Enjoyed).
6. **Luxury Admin Dashboard:** Metric logs detailing Today's Sales, Monthly Volume, Profit Margin, Live Orders, popular items, PDF Reports, and CSV logs download.
7. **Dynamic QR Code Menu:** Automatic QR code generator view streaming a PNG pointing to the `/menu/` page.
8. **Restful API Console:** Fully integrated Django REST Framework ViewSets for categories, menu, users, reviews, carts, and transactions.
9. **Loyalty Rewards & Wishlists:** Heart-toggle wishlist trackers and 10% cash-back loyalty points accumulation.
10. **Voice Search Integration:** Web Speech recognition for hands-free menu querying.

---

## Installation & Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute Database Migrations:**
   *(Note: Categories, FoodItems, and Coupons are automatically seeded during migration via custom RunPython steps!)*
   ```bash
   python restaurant_management/manage.py migrate
   ```

3. **Create Administrative Superuser:**
   ```bash
   python restaurant_management/manage.py createsuperuser
   ```

4. **Spin Up Server:**
   ```bash
   python restaurant_management/manage.py runserver
   ```
   Navigate to: `http://127.0.0.1:8000/`

---

## Testing Simulated Workflows
- **Accounts:** Register a user at `/accounts/signup/`.
- **Cart/Checkout:** Add items from the Menu, apply coupon `ROYAL10` or `MOMOKINGS20`, and choose delivery type.
- **Mock Payment:** Choose Razorpay or select Cash on Delivery.
- **Invoice:** Download the branded PDF invoice generated via `reportlab` at the payment success page.
- **Track Status:** Open the live tracking page, scroll to the *Developer Simulation Panel*, and click order status levels to watch the progress bar animate in real-time.
- **Admin Dashboard:** Log in with superuser credentials, go to `/dashboard/` to view analytics, change statuses, and download CSV/PDF logs.
