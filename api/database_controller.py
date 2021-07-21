import datetime
import os

from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date


class DocsItem(BaseModel):
    name: str
    content: str
    owner: str


class DocsTableManipulator:

    def __init__(self):
        self.column_names = [
            'id',
            'name',
            'content',
            'owner',
            'creation_date',
        ]
        self.meta = MetaData()
        self.table = Table(
            'docs', self.meta,
            Column(self.column_names[0], Integer, primary_key = True),
            Column(self.column_names[1], String),
            Column(self.column_names[2], String),
            Column(self.column_names[3], String),
            Column(self.column_names[4], Date, default = datetime.date.today),
        )
        self.engine = create_engine(
            'postgresql://{user}:{pwd}@{host}/{db}'.format(user = os.environ['DB_USERNAME'],
                                                           pwd = os.environ['DB_PASSWORD'],
                                                           host = os.environ['DB_HOST'],
                                                           db = os.environ['DB_USERNAME']),
            echo = True
        )
        self.meta.create_all(self.engine)

    def add_docs(self, doc_item):
        with self.engine.connect() as conn:
            ins = self.table.insert().values(name = doc_item.name,
                                             content = doc_item.content,
                                             owner = doc_item.owner)
            conn.execute(ins)

    def get_doc(self, id = None):
        with self.engine.connect() as conn:
            if id is not None:
                selected = self.table.select().where(self.table.c.id == id)
            else:
                selected = self.table.select()
            result = conn.execute(selected)

        return self.__parse_query_result(result)

    def get_doc_by_date(self, date):
        with self.engine.connect() as conn:
            selected = self.table.select().where(self.table.c.creation_date == date)
            result = conn.execute(selected)

        return self.__parse_query_result(result)

    def update_doc(self, id, doc_item):
        with self.engine.connect() as conn:
            to_update = {k: v for k, v in doc_item.dict().items() if v}
            updated = self.table.update().where(self.table.c.id == id).values(**to_update)
            conn.execute(updated)

    def delete_doc(self, id):
        with self.engine.connect() as conn:
            deleted = self.table.delete().where(self.table.c.id == id)
            conn.execute(deleted)

    def __parse_query_result(self, result):
        parsed_data = []
        for row in result:
            parsed_data.append({x: y for x, y in zip(self.column_names, row)})
        return parsed_data
