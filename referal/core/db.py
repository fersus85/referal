from sqlalchemy import create_engine

from referal.core.config import settings


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
