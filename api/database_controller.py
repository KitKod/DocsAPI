import os, datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date


class DocsTableManipulator:

    def __init__(self):
        self.meta = MetaData()
        self.table = Table(
            'docs', self.meta,
            Column('id', Integer, primary_key = True),
            Column('name', String),
            Column('content', String),
            Column('owner', String),
            Column('creation_date', Date, default = datetime.date.today),
        )
        self.engine = create_engine(
            'postgresql://{user}:{pwd}@{host}/{db}'.format(user = os.environ['DB_USERNAME'],
                                                           pwd = os.environ['DB_PASSWORD'],
                                                           host = os.environ['DB_HOST'],
                                                           db = os.environ['DB_USERNAME']),
            echo = True
        )
        self.meta.create_all(self.engine)

    def add_docs(self, name, content, owner):
        with self.engine.connect() as conn:
            ins = self.table.insert().values(name = name, content = content, owner = owner)
            result = conn.execute(ins)
            print(result)

    def get_doc(self, id):
        pass