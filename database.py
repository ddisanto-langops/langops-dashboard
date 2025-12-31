from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. The Blueprint Factory
# This 'Base' is the parent class for all your database tables.
Base = declarative_base()

class ProductTable(Base):
    """
    This is a 'Mapped Class'. It links a Python class to a SQL table.
    """
    __tablename__ = 'translation_products'

    id = Column(String, primary_key=True)
    trello_title = Column(String)
    crowdin_proj_id = Column(Integer)
    crowdin_file_id = Column(Integer)
    status_percent = Column(Float, default=0.0)
    is_published = Column(Boolean, default=False)

# 2. The Engine (The Connection)
engine = create_engine('sqlite:///translations.db', echo=False)

# 3. The Session Creator (The Workspace)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """
    Called once when the server starts to ensure the table structure
    matches our Python code.
    """
    Base.metadata.create_all(engine)

def get_db_session():
    """
    Returns a fresh session for a single unit of work.
    """
    return SessionLocal()