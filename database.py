

from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}  
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    year = Column(String)
    photo = Column(String)
    brand = Column(String)
    color = Column(String)
    price = Column(String)
    orders = relationship("OrdersAssociation", back_populates="product")
    shoppingCarts = relationship("ShoppingCartAssociation", back_populates="product")


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    birthday = Column(DateTime())
    city = Column(String(255))
    email = Column(String(255), unique=True)
    hash_password= Column(String(255))
    shoppingCart = relationship("ShoppingCart", uselist=False, back_populates="customer")
    orders = relationship("Order", back_populates="customer")

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class ShoppingCart(Base):
    __tablename__ = 'shoppingCart'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="shoppingCart")
    products = relationship("ShoppingCartAssociation", back_populates="shoppingCart")


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    total = Column(Float)
    timestamp = Column(DateTime, default=func.now())
    confirmation = Column(String, unique=True)
    products = relationship("OrdersAssociation", back_populates="order")
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="orders")



class OrdersAssociation(Base):
    __tablename__ = 'OrdersAssociation'
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    product_qty = Column(Integer)
    product = relationship("Product", back_populates="orders")
    order = relationship("Order", back_populates="products")

class ShoppingCartAssociation(Base):
    __tablename__ = 'shoppingCartAssociation'
    shopping_cart_id = Column(Integer, ForeignKey('shoppingCart.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    quantity = Column(Integer)
    product = relationship("Product", back_populates="shoppingCarts")
    shoppingCart = relationship("ShoppingCart", back_populates="products")



engine = create_engine('sqlite:///fizzBuzz.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()