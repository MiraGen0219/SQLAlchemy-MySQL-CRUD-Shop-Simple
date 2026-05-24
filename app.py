from __future__ import annotations
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, Column, String, Integer, select, DateTime, Float
from marshmallow import ValidationError, fields, validate
from typing import List
from datetime import datetime
from sqlalchemy.sql import func

# Initialize Flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:FerretGarden2026%21@localhost/e_commerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create Base Model:
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy and Marshamllow:
db = SQLAlchemy(model_class = Base)
db.init_app(app)
ma = Marshmallow(app)




# Association Table:
# Two primary key columns prevents duplicate product entries for the same order
order_product = Table(
    'order_product',
    Base.metadata,
    Column("order_id", ForeignKey("orders.order_id"), primary_key=True),
    Column("product_id", ForeignKey("products.product_id"), primary_key=True)
)


# Models
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column("user_id", Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
# One-to-Many relationship from a User to a list of Orders
    orders: Mapped[List["Order"]] = relationship(back_populates="user")

class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column("product_id", Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column("productname", String(200), nullable=False)
    price: Mapped[Float] = mapped_column(Float, nullable=False)

# One-to-Many relationship = one product to many orders
    orders: Mapped[List["Order"]] = relationship(secondary=order_product, back_populates="products")
    
class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column("order_id", Integer, primary_key=True, autoincrement=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    
# Relationships:    
    user: Mapped["User"] = relationship(back_populates="orders")
    products: Mapped[List["Product"]] = relationship(secondary=order_product, back_populates="orders")
 
 
 
#Schemas - User and Order
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
         model = User
         load_instance = False
         
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    address = fields.String(required=True)
         
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
         model = Order
         load_instance = False
         include_fk = True
    
    user_id = fields.Integer(required=True)
    order_date = fields.DateTime(required=False)
    
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = False
        
    product_name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    price = fields.Float(required=True, validate=validate.Range(min=0))     
         
         
# Initialize Schemas:
user_schema = UserSchema()
users_schema = UserSchema(many=True) # Allows for serialization of a list of user objects

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)



#--------------CRUD Endpoints---------------

# POST (create) a user:
@app.route('/users', methods=['POST'])
def create_user():
    
    try: 
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_user = User(name=user_data['name'], email=user_data['email'], address=user_data['address'])
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user), 201
    
# GET (retrieve) a user:
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    
    user = db.session.get(User, id)
    
    if not user: 
        return jsonify({"message": "Invalid user ID"}), 404
    
    return user_schema.jsonify(user), 200

# GET (retrieve) all users:
@app.route('/users', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    
    return users_schema.jsonify(users), 200

# PUT (update) a user:
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user ID"}), 404
    
    try: 
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user.name = user_data['name']
    user.email = user_data['email']
    user.address = user_data['address']
    
    db.session.commit()
    return user_schema.jsonify(user), 200

# DELETE (delete) a user:
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user ID}"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"successfully deleted user{id}"}), 200



# POST (create) a product: 
@app.route('/products', methods=['POST'])
def create_product():
    try: 
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Product(
        product_name=product_data["product_name"], 
        price=product_data["price"]
    )

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201

    
# GET (retrieve) a product:
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid product ID"}), 404
    
    return product_schema.jsonify(product), 200


# GET (retrieve) all products:
@app.route('/products', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    
    return products_schema.jsonify(products), 200


# PUT (update) a product:
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid product ID"}), 404
    
    try: 
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    product.product_name = product_data["product_name"]
    product.price = product_data["price"]
    
    db.session.commit()
    return product_schema.jsonify(product), 200


# DELETE (delete) a product:
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid product ID}"}), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"successfully deleted product{id}"}), 200


# POST (create) an order (requires user ID and order date):
@app.route('/orders', methods=['POST'])
def create_order():
    try: 
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user = db.session.get(User, order_data["user_id"])
    
    if not user:
        return jsonify({"message": "Invalid user ID"}), 404
    
    new_order = Order(user_id=order_data["user_id"])
    db.session.add(new_order)
    db.session.commit()
    
    return order_schema.jsonify(new_order), 201

    
# GET (retrieve) all orders for a user:
@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_order_by_user(user_id):
    query = select(Order).where(Order.user_id == user_id)
    orders = db.session.execute(query).scalars().all()
    
    return orders_schema.jsonify(orders), 200


# Get (retrieve) all products for an order:
@app.route('/orders/<int:order_id>/products', methods=['GET'])
def get_order_products(order_id):
    order = db.session.get(Order, order_id)
    
    if not order: 
        return jsonify({"message": "Invalid order ID"}), 404
    
    return products_schema.jsonify(order.products), 200


# PUT (add) a product to an order (and prevent duplicates)
@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
        order = db.session.get(Order, order_id)
        product = db.session.get(Product, product_id)
        
        if not order:
            return jsonify({"message": "Invalid order ID"}), 404
        
        if not product:
            return jsonify({"message": "Invalid product ID"}), 404
        
        if product in order.products:
            return jsonify({"message": "Product already exists in this order"}), 400
        
        order.products.append(product)
        db.session.commit()
    
        return jsonify({"message": "Product added to order"}), 200
    
    
# DELETE (delete) a product from an order
@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    
    if not order: 
        return jsonify({"message": "Invalid order ID"}), 404
    
    if not product:
        return jsonify({"message": "Invalid product ID}"}), 404
    
    if product not in order.products:
        return jsonify({"message": "Product is not in this order"}), 400
    
    order.products.remove(product)
    db.session.commit()
    
    return jsonify({"message": "Product removed from order."}), 200




with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True)