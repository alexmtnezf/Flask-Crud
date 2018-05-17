from sqlalchemy import Column, ForeignKey, \
    Integer, String, Sequence
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AbstractBase(object):
    def __repr__(self):
        return str(self.__dict__)

    def serialize(self):
        raise NotImplemented()


class Restaurant(Base, AbstractBase):
    __tablename__ = 'restaurant'
    id = Column(Integer, Sequence('restaurant_id_seq'), primary_key=True)
    name = Column(String(80), nullable=False)

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class MenuItem(Base, AbstractBase):
    # Attributes
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, Sequence('menuitem_id_seq'), primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    # Navigation properties
    restaurant = relationship(Restaurant)

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


###
engine = create_engine("sqlite:///restaurantmenu.db", echo=True)
Base.metadata.create_all(engine)
