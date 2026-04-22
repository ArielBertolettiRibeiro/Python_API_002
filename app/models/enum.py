import enum
from sqlalchemy import Enum as SAEnum

class MovementType(enum.Enum):
    entrada = "entrada"
    saida = "saida"
    ajuste = "ajuste"
