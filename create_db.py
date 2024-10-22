from sqlalchemy import create_engine
from models import Base


engine = create_engine(url='sqlite:///cryptogame.db')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)