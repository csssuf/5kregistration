from sqlalchemy import Column, String, Boolean, Integer, DateTime, Enum
from project.database import Base

class RegisteredUser(Base):
    __tablename__ = 'registeredusers'
    id = Column(Integer, primary_key = True)
    date = Column(DateTime)
    name = Column(String(70))
    email = Column(String(254))
    emailverified = Column(Boolean)
    paid = Column(Integer)
    reg_uuid = Column(String(37))
    racetype = Column(Enum('5k', 'funrun', name='racetypes'))
    phone = Column(Integer)

    def __init__(self, date=None, name=None, email=None, paid=-1, reg_uuid=None, verified=False, rtype='5k'):
        self.date = date
        self.name = name
        self.email = email
        self.paid = paid
        self.reg_uuid = reg_uuid
        self.emailverified = verified
        self.racetype = rtype

    def __repr__(self):
        return "<RegisteredUser %s (id %d)>" % (self.email, self.id)

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key = True)
    username = Column(String(16))
    pwhash = Column(String(128))
    superadmin = Column(Boolean)

    def __init__(self, uname=None, pwhash=None, superadmin=False):
        self.username = uname
        self.pwhash = pwhash
        self.superadmin = superadmin

    def __repr__(self):
        return "<Admin %s (superadmin = %b)>" % (self.username, self.superadmin)
