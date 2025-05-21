# 🧳 Time Travellers - A Tourism Booking Platform

**Book Buses 🚌, Trains 🚆, Flights ✈️, and Hotels 🏨 in one place.**

---

## 🚀 Overview

**Time Travellers** is a full-stack tourism web application for booking transportation and accommodation services. It allows users to book buses, trains, flights, and hotels in a centralized platform with a smooth user experience, secure payments, and admin management features.

---

## ❓ Problem It Solves

Tourists waste time juggling multiple platforms for travel and hotel bookings. This app provides a **one-stop solution** with all essential features built-in.

---

## ✨ Features

### 🔹 User Side
- Register & login/logout
- Search and book:
  - 🚌 Buses
  - 🚆 Trains
  - ✈️ Flights
  - 🏨 Hotels
- Add to cart and checkout
- Make payments using a dummy Stripe integration
- Chatbot for assistance

### 🔸 Admin Side
- Admin login
- Add/Edit/Delete:
  - Categories
  - Listings
- View and remove users
- Manage bookings and payments

---

## 🛠️ Tech Stack

| Layer      | Technologies                     |
|------------|----------------------------------|
| Frontend   | HTML, CSS, JavaScript            |
| Backend    | Python (Flask)                   |
| Database   | MongoDB (via PyMongo)            |
| Payment    | Stripe (dummy/test cards)        |
| Chatbot    | API-based chatbot integration    |

---

## 🧩 Key Routes & Modules

### 📦 Booking Modules

| Feature  | Endpoint      | Method     |
|----------|---------------|------------|
| Bus      | `/Bus`        | GET/POST   |
| Train    | `/Trains`     | GET/POST   |
| Flight   | `/Flights`    | GET/POST   |
| Hotel    | `/Hotels`     | GET/POST   |

### 🛒 Cart
- `/AddToCart`
- `/ShowAllCartItems`
- `/RemoveFromCart`

### 🔐 User Authentication
- `/register`
- `/login`
- `/logout`

### ⚙️ Admin
- `/adlogin`
- `/Users`
- `/RemoveUser`
- `/Category`
- `/AddProduct`
- `/EditProduct`

### 💳 Payment
- `/MakePayment`
- `/add-cake` (Stripe demo)

### 💬 Chatbot
- `/chat`
- `/chat/query`

---

## 🔑 Sample Credentials

| Role  | Email               | Password   |
|-------|---------------------|------------|
| Admin | admin@example.com   | admin123   |

---

## 🖼️ Screenshots

> Add your screenshots here  
Example:

![Homepage](https://github.com/user-attachments/assets/a66e5696-0203-4e97-a327-f547f6e72a29)

---

## 🔧 Installation & Run Locally

### 📋 Prerequisites
- Python 3.8+
- MongoDB (local or Atlas URI)
- Git (optional)

### 🖥️ Steps to Run

```bash
# 1. Clone the repo
git clone https://github.com/your-username/time-travellers.git
cd time-travellers

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# On Windows
venv\Scripts\activate
# On Unix/macOS
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set environment variables (optional)
export FLASK_APP=app.py
export FLASK_ENV=development

# 6. Run the Flask app
flask run
