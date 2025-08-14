# 🍔 Django Food Delivery App

This is a **Django-based food delivery platform** that allows customers to place food orders, restaurants to manage their offerings and deliveries, and delivery partners to fulfill orders — all using standard Django views and forms (no DRF API used).


> 📌 **Note:** This project is for **educational/demo purposes**. It includes simulated payment processing and **does not use real payment gateways**.

---


## 🚀 Features

### 👤 Customer
- Register and login
- Browse restaurants and menus
- Filter menu items by **category**
- Place orders with delivery address
- View past orders and status
- Submit feedback

### 🍽️ Restaurant
- Register/Login as a restaurant
- Manage restaurant profile
- Add, update, or delete **menu items** with **categories** (e.g., Beverages, Main Course)
- Handle incoming orders (accept/reject)
- Manage and assign **delivery users**
- Orders are automatically assigned to available delivery personnel using **round-robin** logic

### 🚚 Delivery Partner
- Automatically assigned new deliveries when available
- View assigned orders
- Update order status (picked up / delivered)
- Track delivery history

### 👨‍💼 Admin Panel
- Access Django Admin site (`/admin/`)
- Create restaurant users (restaurant admins)
- Add restaurants
- Manage users, restaurants, and deliveries

### 💳 Payments (Demo)
- Basic payment simulation included
- **Note:** This is a **demo setup only** — no real payment gateway is integrated

---

## 🔐 User Roles & Access Flow

- **Admin**:
  - Adds new restaurants
  - Assigns a restaurant admin to each
  - Manages models from `/admin/`

- **Restaurant Admin**:
  - Can only log in if created by admin
  - Manages the restaurant profile, menu, orders, and delivery personnel

- **Customer**:
  - Self-registers via frontend
  - Can log in to browse and place orders

- **Delivery Partner**:
  - Added by restaurant admin
  - Assigned orders automatically (round-robin)
  - Logs in to view and update delivery status
 

## ⚠️ Disclaimer

> 📌 **Note**: This was one of my early Django projects, built before I learned Django REST Framework.  
> It uses **traditional Django views** and forms — **no API or React/JS frontend**.  
> The code structure may not reflect production-grade modularity, but it's a full working system.

---

## 🛠️ Tech Stack

- **Backend:** Django (Traditional Views, not DRF)
- **Frontend:** Bootstrap 5 (for customers, restaurant and delivery partner views)
- **Database:** SQLite (can be swapped for PostgreSQL/MySQL)
- **Authentication:** Django’s built-in auth system

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/Sivaramakrishanan06/PS-FOOD-PARTNERS.git
cd food_delivery_app/deliver

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r ../req.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create a superuser (admin login)
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver

# Visit
http://127.0.0.1:8000/



