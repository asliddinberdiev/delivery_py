from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.env import cfg

pg_config = f"postgresql://{cfg.get_postgres_url()}"

engine = create_engine(pg_config)

session = sessionmaker()

Base = declarative_base()
