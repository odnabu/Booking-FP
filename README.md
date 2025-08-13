# Booking FP

A Django-based REST API for managing rental offers, bookings, reviews, and user profiles, 
with JWT authentication via cookies, automatic token refresh, advanced filtering, and role-based permissions.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-5.2-darkgreen?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/DRF-3.16-red?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql&logoColor=white" />
</p>

---

## 1. Features

### 1.1. User Management
- **JWT Authentication** using cookies (Access + Refresh tokens).
- **Automatic token refresh** via custom middleware.
- Registration and login via email/password.
- Role-based profiles: **Tenant** or **Landlord**.
- Admin panel with [django-jazzmin](https://github.com/farridav/django-jazzmin) theme.

### 1.2. Offers
- Create, update, and manage **real estate listings**.
- Filtering by **price range**, **rooms**, **city**, and **type**.
- Search by title/description, sorting by price or update date.
- **Custom permission**: Only landlords or admins can modify offers.
- Toggle offer **active/inactive** status.

### 1.3. Bookings
- Tenants can book available offers.
- Prevents double-booking for the same date.
- Related to offers and users.

### 1.4. Reviews
- Tenants can leave reviews **only for their own bookings**.
- Ratings from 1 to 5, with optional comment.
- List reviews for a specific offer.

### 1.5. Addresses
- Separate model for storing country, city, street, etc.
- Linked to offers.

---

## 2. API Preview

### 2.1. Swagger UI
<p align="center">
  <img src="docs/swagger_ui_preview_1.png" alt="Swagger UI Screenshot - API" height="1500" />  
  <img src="docs/swagger_ui_preview_2.png" alt="Swagger UI Screenshot - Schemas" height="1500"  />
</p>

### 2.2. Endpoints Table (Generated)
<p align="center">
  <img src="utils/endpoints_dark.png" alt="Endpoints Table" width="800" />
</p>

---

## 3. Project Structure

```plaintext
.
├── apps/
│   ├── addresses/       # Address model & API
│   ├── bookings/        # Booking model & API
│   ├── offers/          # Offers model, serializers, views
│   ├── reviews/         # Reviews model, serializers, views
│   ├── users/           # User profiles, registration, login, logout
│   ├── routers.py       # Central URL registry
│   └── views.py         # Basic welcome endpoint
├── booking_fp/          # Project settings & middleware
│   └── middleware.py    # JWT Authentication Middleware
├── common/
│   └── permissions.py   # Custom DRF permissions
├── utils/
│   ├── management/commands/export_urls.py  # API endpoints exporter
│   └── show_tree.py     # Project structure printer
├── requirements.txt
└── manage.py
````

---

## 4. Installation

### 4.1. Clone the repository

```bash
git clone https://github.com/odnabu/Booking-FP.git
cd booking_fp
```

### 4.2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### 4.3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4.4. Configure environment variables

Create `.env` in the project root:

```env
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=mysql://user:password@localhost:3306/dbname
```

### 4.5. Apply migrations

```bash
python manage.py migrate
```

### 4.6. Create superuser

```bash
python manage.py createsuperuser
```

### 4.7. Run the server

```bash
python manage.py runserver
```

---

## 5. Authentication & Security

### 5.1. JWT via Cookies

- **Access token** (`access_token`) — short-lived.
- **Refresh token** (`refresh_token`) — long-lived, used for automatic re-authentication.

### 5.2. Automatic Token Refresh

- Implemented in `booking_fp/middleware.py`.
- If access token expires, it is refreshed automatically using the refresh token (if valid).
- If refresh token is blacklisted or invalid, both cookies are cleared.

### 5.3. Permissions

- `IsLandlordOrAdminOrReadOnly` — only landlords or admins can modify offers; all users can view them.
- Bookings and reviews are restricted to their owners.

---

## 6. Filtering, Search & Ordering

- **Offers**:

  - Filter by price range, rooms range, city, type.
  - Search in title and description.
  - Order by price or update date.

- **Reviews**:

  - Filter by rating, reviewer username, booking address.
  - Search by rating or related fields.
  - Order by creation date.

---

## 7. API Documentation

Once the server is running, open:

```
http://127.0.0.1:8000/swagger/      # Swagger UI
http://127.0.0.1:8000/redoc/        # Redoc
```

---

## 8. Utilities

### 8.1. Export API Endpoints

```bash
python manage.py export_urls
```

Generates:

* `utils/endpoints.md` — Markdown table of endpoints.
* `utils/endpoints_dark.png` — Colored PNG table.

### 8.2. Show Project Tree

```bash
python utils/show_tree.py
python utils/show_tree.py --save project_tree.txt
```

---

## 9. Example API Requests

Below are example requests using **cURL** and **HTTPie**.  
The API uses **JWT tokens in cookies**, so session handling is important.

---

### 9.1. Login (JWT Authentication)

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tenant@example.com",
    "password": "StrongPass123"
  }' \
  -c cookies.txt
```

Notes:
- -c cookies.txt saves cookies (including access_token and refresh_token) for later requests.
- If credentials are correct, the response will also contain the tokens in JSON.

---

### 9.2. Create Offer (Landlord Only)

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/offers/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Cozy Oceanfront Apartment",
    "description": "First line, amazing sea view",
    "price": 120,
    "rooms": 2,
    "address": 1,
    "is_active": true
  }'
```

---

### 9.3. Book an Offer (Tenant)

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "offer": 1,
    "start_date": "2025-08-15",
    "end_date": "2025-08-22"
  }'
```
**Notes:**
- Only tenants can book.
- Booking dates must not overlap with existing bookings.

---

### 9.4. Leave a Review (Tenant for Their Booking)

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "booking": 1,
    "rating": 5,
    "comment": "Amazing place! Highly recommend."
  }'
```

**Notes:**
- Only the tenant who made the booking can leave a review.
- Rating must be between 1 and 5.

---

### 9.5. Get Reviews for a Specific Offer

**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/v1/reviews/offer/1/ \
  -b cookies.txt
```

---

## 10. Dependencies

See [requirements.txt](requirements.txt) for full list.
Main packages:

- Django 5.2
- Django REST Framework
- django-filter
- django-cors-headers
- drf-spectacular
- Pillow
- mysqlclient
- PyJWT

---

## 11. License

MIT License — feel free to use and modify.
