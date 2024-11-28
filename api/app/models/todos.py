from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.session import Base


class Todos(Base):
    '''Todos table model'''
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer, default=0)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
