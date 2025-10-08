from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP, Sequence
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger as log

Base = declarative_base()

class TechStats(Base):
    __tablename__ = "stats"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True, autoincrement=True)
    date = Column(TIMESTAMP)
    tech = Column(Text)
    any_time = Column(Integer)
    past_month = Column(Integer)
    past_week = Column(Integer)
    past_24_hours = Column(Integer)
    full_time = Column(Integer)
    part_time = Column(Integer)
    contract = Column(Integer)
    temporary = Column(Integer)
    internship = Column(Integer)
    entry_level = Column(Integer)
    associate = Column(Integer)
    mid_senior = Column(Integer)
    director = Column(Integer)
    on_site = Column(Integer)
    hybrid = Column(Integer)
    remote = Column(Integer)

def db_insert(technology_stats_object, db_url):
    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)

        from sqlalchemy.orm import Session

        log.debug(f"Storing tech stats to database")

        with Session(engine) as session:
        # Create technology stats record
            tech_stats_entity = TechStats(
                date=technology_stats_object['DATE'],
                tech=technology_stats_object['TECH'],
                any_time=technology_stats_object['ANY_TIME'],
                past_month=technology_stats_object['PAST_MONTH'],
                past_week=technology_stats_object['PAST_WEEK'],
                past_24_hours=technology_stats_object['PAST_24_HOURS'],
                full_time=technology_stats_object['FULL_TIME'],
                part_time=technology_stats_object['PART_TIME'],
                contract=technology_stats_object['CONTRACT'],
                temporary=technology_stats_object['TEMPORARY'],
                internship=technology_stats_object['INTERNSHIP'],
                entry_level=technology_stats_object['ENTRY_LEVEL'],
                associate=technology_stats_object['ASSOCIATE'],
                mid_senior=technology_stats_object['MID_SENIOR'],
                director=technology_stats_object['DIRECTOR'],
                on_site=technology_stats_object['ON_SITE'],
                hybrid=technology_stats_object['HYBRID'],
                remote=technology_stats_object['REMOTE'],
            )

        session.add(tech_stats_entity)
        session.commit()

    except Exception as e:
        log.error("DB save error:", e)
