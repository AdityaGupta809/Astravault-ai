import os
import json

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    
)


def load_pdf(path, access_level):
    docs = []
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(path, file))
            for d in loader.load():
                d.metadata["access_level"] = access_level
                docs.append(d)
    return docs

def load_csv(path, access_level):
    docs = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            loader = CSVLoader(os.path.join(path, file))
            for d in loader.load():
                d.metadata["access_level"] = access_level
                docs.append(d)
    return docs



def load_txt(path, access_level):
    docs = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(path, file))
            doc = loader.load()[0]
            doc.metadata["access_level"] = access_level
            docs.append(doc)
    return docs



def load_json(path, access_level):
    docs = []
    for file in os.listdir(path):
        if file.endswith(".json"):
            with open(os.path.join(path, file)) as f:
                data = json.load(f)
            text = json.dumps(data, indent=2)
            docs.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file,
                        "access_level": access_level
                    }
                )
            )
    return docs





def load_all_documents():
    docs = []
    docs += load_pdf("data/pdf", "research")
    docs += load_csv("data/csv", "public")
    docs += load_txt("data/txt", "public")
    docs += load_json("data/json", "admin")
    return docs