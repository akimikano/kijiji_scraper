from src import settings
from sqlalchemy import create_engine
from src.db.models import Base

engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(engine)
