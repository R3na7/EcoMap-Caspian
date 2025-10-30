# Импорт всех моделей для Alembic
from app.db.session import Base
from app.db.models.users import User
from app.db.models.pollution_point import PollutionPoint
from app.db.models.image import Image
from app.db.models.history import StatusHistory, Comment