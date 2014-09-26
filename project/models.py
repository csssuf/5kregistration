from sqlalchemy import Column, String, Boolean, Integer, DateTime
from project.database import Base

class RegisteredUser(Base):
    __tablename__ = 'registeredusers'
    id = Column(Integer, primary_key = True)
    date = Column(DateTime)
    name = Column(String(70))
    email = Column(String(254))
    emailverified = Column(Boolean)
    paid = Column(Boolean)
    reg_uuid = Column(String(37))

    def __init__(self, date=None, name=None, email=None, paid=False, reg_uuid=None, verified=False):
        self.date = date
        self.name = name
        self.email = email
        self.paid = paid
        self.reg_uuid = reg_uuid
        self.emailverified = verified

    def __repr__(self):
        return "<RegisteredUser %s (id %d)>" % (self.email, self.id)
