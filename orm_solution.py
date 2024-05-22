from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DECIMAL, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Merchant(Base):
    __tablename__ = 'merchants'
    merchant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

class Merchandise(Base):
    __tablename__ = 'merchandise'
    merchandise_id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_id = Column(Integer, ForeignKey('merchants.merchant_id'))
    name = Column(String(255), nullable=False)

class Orders(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_id = Column(Integer, ForeignKey('merchants.merchant_id'))
    carrier_id = Column(Integer, ForeignKey('carriers.carrier_id'))
    pieces = Column(Integer, nullable=False)
    shipped = Column(Boolean, nullable=False)
    shipped_date = Column(Date, nullable=False)

class Carrier(Base):
    __tablename__ = 'carriers'
    carrier_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    max_orders = Column(Integer, nullable=False)
    max_pieces = Column(Integer, nullable=False)
    cost_per_order = Column(DECIMAL(10, 2), nullable=False)


DATABASE_URL = "mysql+mysqlconnector://rajat:rajat@localhost/flow_shipping"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_available_carriers():
    return session.query(Carrier).all()

def get_orders_to_ship():
    return session.query(Orders).filter(Orders.shipped == False).all()

def assign_carrier_to_order(order_id, carrier_id):
    orders = Order(order_id=order_id, carrier_id=carrier_id, status='assigned')
    session.add(orders)
    session.commit()

def mark_order_as_shipped(order_id):
    orders = session.query(Orders).filter(Orders.order_id == order_id).one()
    orders.status = 'shipped'
    session.commit()

def get_orders_by_carrier(carrier_id):
    return session.query(Orders).filter(Orders.carrier_id == carrier_id).all()


def assign_most_economical_carrier(order):
    session = Session()
    carriers = session.query(Carrier).order_by(Carrier.cost_per_order)

    for carrier in carriers:
        total_pieces = session.query(func.sum(Orders.pieces)).filter(Orders.order_id == orders.order_id).scalar()
        if total_pieces <= carrier.max_pieces and session.query(func.count(Orders.order_id)).filter(Orders.carrier_id == carrier.carrier_id, Order.shipped_date == func.current_date()).scalar() < carrier.max_orders:
            order.carrier_id = carrier.carrier_id
            order.shipped = True
            order.shipped_date = datetime.now()
            session.commit()
            break

    session.close()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    
    # Example usage:
    orders = get_orders_to_ship()
    for order in orders:
        assign_most_economical_carrier(order)
    for order in orders:
        mark_order_as_shipped(order.order_id)
    carriers = get_available_carriers()
    for carrier in carriers:
        assigned_orders = get_orders_by_carrier(carrier.carrier_id)
        print(f"Orders assigned to {carrier.name}: ")
        for order in assigned_orders:
            print(order.__dict__)
