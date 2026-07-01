from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from database.db import Base


class Report(Base):

    __tablename__ = "reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(String)

    description = Column(String)

    filepath = Column(String)

    summary = Column(String)

    risk_level = Column(String)

    risk_assessment = Column(String)

    analysis_json = Column(String)
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )