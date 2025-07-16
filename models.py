from database import Base, engine
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy_utils import ChoiceType, UUIDType
from sqlalchemy.orm import relationship
import uuid

class User(Base):
    __tablename__ = 'users'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(70), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    orders = relationship('Order', back_populates='user') # one-to-many relationship

    def __repr__(self) -> str:
        return f"{self.id}"


class Product(Base):
    __tablename__ = 'products'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Integer, nullable=False)

    orders = relationship('Order', back_populates='product')  # one-to-many relationship

    def __repr__(self) -> str:
        return f"{self.id}"


class Order(Base):
    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('IN_TRANSIT', 'in_transit'),
        ('DELIVERED', 'delivered')
    )

    __tablename__ = 'orders'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), ForeignKey('users.id'))
    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    status = Column(ChoiceType(ORDER_STATUS), default=ORDER_STATUS[0][0])

    user = relationship('User', back_populates='orders') # many-to-one relationship
    product = relationship('Product', back_populates='orders') # many-to-one relationship

    def __repr__(self) -> str:
        return f"{self.id}"

Base.metadata.create_all(bind=engine)
