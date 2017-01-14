''' This is a simple test where I'm just trying to create a database schema with sqlalchemy'''
import logging

from sqlalchemy import Column, String, Integer,  Enum, DateTime, create_engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema, DropSchema

from settings import conn_str

Base = declarative_base()

def check_schema_exists(engine, name):
	return name in Inspector.from_engine(engine).get_schema_names()

def create_counted_table(engine, checkfirst=True):
    """A function to create my only table (at the moment).  The key here should match the tablename of the class."""
    Base.metadata.tables['raw_data'].create(bind=engine, checkfirst=checkfirst)

class counted_data(Base):
	'''I think this data is left as-is in the files for now, but combine the two years into the same table'''
	__tablename__ = 'raw_data'
	
	name = Column('name', String(10), primary_key = True)
	age = Column('age', Integer, nullable = True)
	gender = Column('gender', Enum('F', 'M', name = 'gender'), nullable = True)
	raceethnicity = Column('raceethnicity', Enum('B', 'W', 'H', 'A', 'O', name = 'raceethnicity'), nullable = True)
	armed = Column('armed', Enum('no', 'firearm', 'knife', 'vehicle', 'nonlethal_firearm', 'other', name = 'armed'), nullable = True)
	date = Column('date', DateTime)	
	street_address = Column('street_address', String(20), nullable = True)
	city = Column('city', String(10), nullable = True)
	state = Column('state', String(10), nullable = True)
	lawenforcementagency = Column('lawenforcementagency', String(20))

def create_schema(schema):
	engine = create_engine(conn_str)
	
	'''First I want to check to make sure the schema exists'''
	if check_schema_exists(engine, schema):
		for table in Base.metadata.tables.values():
			table.schema = schema
		Base.metadata.drop_all(engine)
		engine.execute(DropSchema(schema, cascade=True))
		
	engine.execute(CreateSchema(schema))
	for table in Base.metadata.tables.values():
		table.schema = schema
	
	create_counted_table(engine)


if __name__ == '__main__':
		create_schema('the_counted_data_test')
