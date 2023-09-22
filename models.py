from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Enum
from database import Base
import enum

fuel_type = ({
    "petrol" : "petrol",
}
)

class item(Base):
    __tablename__ = "item"

    id = Column(Interger, primary_key=True, )