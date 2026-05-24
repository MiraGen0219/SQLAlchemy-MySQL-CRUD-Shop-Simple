# 🛒 E-Commerce API

A RESTful E-Commerce API built with:

- Flask
- SQLAlchemy
- Marshmallow
- MySQL

This project demonstrates:

- CRUD operations
- Many-to-many relationships
- Association tables
- Data validation
- REST API design
- Database persistence

---

# 📦 Features

## 👤 User Management

- Create users
- Retrieve users
- Update users
- Delete users

## 📦 Product Management

- Create products
- Retrieve products
- Update products
- Delete products

## 🧾 Order Management

- Create orders
- Retrieve all orders for a user
- Add products to orders
- Remove products from orders
- Retrieve all products belonging to an order

---

# 🧠 Database Design

## Tables

### 👤 Users

| Column | Type |
|---|---|
| user_id | Integer |
| name | String |
| email | String (Unique) |
| address | String |

---

### 📦 Products

| Column | Type |
|---|---|
| product_id | Integer |
| product_name | String |
| price | Float |

---

### 🧾 Orders

| Column | Type |
|---|---|
| order_id | Integer |
| order_date | DateTime |
| user_id | Foreign Key |

---

### 🔗 Order_Product Association Table

| Column | Type |
|---|---|
| order_id | Foreign Key |
| product_id | Foreign Key |

The association table prevents duplicate products in the same order using a composite primary key.

---

# 🔄 Relationships

## One-to-Many

- One User → Many Orders

## Many-to-Many

- One Order → Many Products
- One Product → Many Orders

---

# ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Flask | Web Framework |
| SQLAlchemy | ORM |
| Marshmallow | Serialization & Validation |
| MySQL | Database |
| Postman | API Testing |

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone <your-repository-url>
cd E-Commerce-API
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install flask
pip install flask_sqlalchemy
pip install flask_marshmallow
pip install marshmallow-sqlalchemy
pip install mysql-connector-python
```

---

## 4️⃣ Configure Database

Update:

```python
app.config['SQLALCHEMY_DATABASE_URI']
```

with your MySQL credentials.

Example:

```python
mysql+mysqlconnector://username:password@localhost/e_commerce_api
```

---

## 5️⃣ Run Application

```bash
python app.py
```

Flask server should start at:

```text
http://127.0.0.1:5000
```

---

# 🧪 API Endpoints

# 👤 User Routes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Create user |
| GET | `/users/<id>` | Get user |
| GET | `/users` | Get all users |
| PUT | `/users/<id>` | Update user |
| DELETE | `/users/<id>` | Delete user |

---

# 📦 Product Routes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products` | Create product |
| GET | `/products/<id>` | Get product |
| GET | `/products` | Get all products |
| PUT | `/products/<id>` | Update product |
| DELETE | `/products/<id>` | Delete product |

---

# 🧾 Order Routes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/orders` | Create order |
| GET | `/orders/user/<user_id>` | Get orders for user |
| GET | `/orders/<order_id>/products` | Get products for order |
| PUT | `/orders/<order_id>/add_product/<product_id>` | Add product to order |
| DELETE | `/orders/<order_id>/remove_product/<product_id>` | Remove product from order |

---

# 📬 Example Requests

## Create User

```json
{
  "name": "Erin",
  "email": "erin@test.com",
  "address": "123 Main St"
}
```

---

## Create Product

```json
{
  "product_name": "Keyboard",
  "price": 99.99
}
```

---

## Create Order

```json
{
  "user_id": 1
}
```

---

# 🧪 Example Workflow

## 1️⃣ Create User

```text
POST /users
```

## 2️⃣ Create Product

```text
POST /products
```

## 3️⃣ Create Order

```text
POST /orders
```

## 4️⃣ Add Product to Order

```text
PUT /orders/1/add_product/1
```

## 5️⃣ Retrieve Products for Order

```text
GET /orders/1/products
```

---

# 🛡️ Validation Features

- Email validation
- Required fields
- Product price minimum validation
- Duplicate product prevention within orders
- Foreign key validation

---

# 📚 Learning Concepts Demonstrated

- REST APIs
- Flask routing
- SQLAlchemy ORM
- Database relationships
- Marshmallow schemas
- CRUD operations
- Association tables
- Many-to-many relationships
- JSON serialization
- API testing with Postman

---

# 📁 Project Structure

```text
E-Commerce-API/
│
├── app.py
├── venv/
└── README.md
```
