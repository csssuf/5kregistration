from sqlalchemy import Column, String, Boolean, Integer, DateTime
from project.database import Base

class RegisteredUser(Base):
    __tablename__ = 'registeredusers'
    id = Column(Integer, primary_key = True)
    date = Column(DateTime)
    email = Column(String(254))
    paid = Column(Boolean)

    def __init__(self, date=None, email=None, paid=False):
        self.date = date
        self.email = email
        self.paid = paid

    def __repr__(self):
        return "<RegisteredUser %s (id %d)>" % (self.email, self.id)
