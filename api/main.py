from typing import Optional

from fastapi import FastAPI

from database_controller import DocsTableManipulator

app = FastAPI()


@app.get("/")
def home():
    docs_table = DocsTableManipulator()
    docs_table.add_docs("kitkod1", "3", "4")
    return {"Hello": "Ratibor"}

@app.get("/docs/{doc_id}")
def get_doc_by_id(doc_id: int):

    return {}
    


