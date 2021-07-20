from fastapi import FastAPI

from database_controller import DocsTableManipulator, DocsItem

app = FastAPI()
docs_table = DocsTableManipulator()


@app.post("/documents/add_doc")
def add_doc(doc_item: DocsItem):
    docs_table.add_docs(doc_item)


@app.get("/documents/{doc_id}")
def get_doc_by_id(doc_id: int):
    return docs_table.get_doc(doc_id)[0]


@app.put("/documents/{doc_id}")
def update_doc_by_id(doc_id: int, doc_item: DocsItem):
    return docs_table.update_doc(doc_id, doc_item)


@app.delete("/documents/{doc_id}")
def delete_doc_by_id(doc_id: int):
    return docs_table.delete_doc(doc_id)
