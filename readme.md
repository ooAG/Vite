# 📊 ERP Reporting Dashboard — Vite Knowledge Pvt. Ltd. (Assessment Project)

This project is a full-stack ERP reporting dashboard built as part of the Vite Knowledge Pvt. Ltd. technical assessment.  
It demonstrates backend API design, authentication, CRUD operations, data visualization, filtering, and real-world dashboard behaviour.

---

## 🚀 Features

### 1. Authentication
- JWT-based login (Django REST Framework + SimpleJWT)
- Protected dashboard routing
- Tokens stored locally

**Demo Accounts**
- Viewer → viewer@vite.co.in / pass123  
- Analyst (staff) → analyst@vite.co.in / pass123  

---

## 2. Role-Based Access

| Feature | Viewer | Analyst |
|--------|--------|---------|
| View dashboard | ✔️ | ✔️ |
| Filter category | ✔️ | ✔️ |
| Auto-refresh | ✔️ | ✔️ |
| Add sale | ❌ | ✔️ |
| Edit sale | ❌ | ✔️ |
| Delete sale | ❌ | ✔️ |
| Export CSV | ❌ | ✔️ |

UI automatically hides analyst-only actions for viewers.

---

## 3. Dashboard Components

### ✔ Summary Cards
- Total Sales  
- Total Orders  
- Inventory Count  

### ✔ Interactive Chart
- Monthly sales trend (line chart)
- Chart.js
- Updates instantly with filters

### ✔ Data Table
- Paginated sales list  
- Columns: Date • Product • Category • Amount  
- Edit/Delete (analyst only)

### ✔ Filtering
- Category dropdown  
- Affects chart + summary + table

### ✔ Auto-Refresh
- Refreshes every 12 seconds
- “Last updated” indicator shown

---

## 🛠️ Technology Stack

### Backend
- Django
- Django REST Framework
- DRF SimpleJWT
- SQLite (lightweight setup)

### Frontend
- Pure HTML + CSS + Bootstrap
- Chart.js for visualization
- Vanilla JavaScript for API/logic

---

## 📁 Project Structure

backend/
│── erp/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ ├── urls.py
│── manage.py

frontend/
│── index.html (login page)
│── dashboard.html (dashboard UI)
│── script.js (API helpers)

---

## 🔗 API Endpoints

### Auth
POST /api/token/

### User
GET /api/me/

### Summary
GET /api/summary/?category=optional

### Sales
GET    /api/sales/  
POST   /api/sales/  
GET    /api/sales/<id>/  
PUT    /api/sales/<id>/  
DELETE /api/sales/<id>/  

### Export
GET /api/sales/export/  
(staff only)

---
