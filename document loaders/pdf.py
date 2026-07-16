from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter #TokenTextSplitter

data = PyPDFLoader("document loaders/human_health.pdf")

docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=40,
    chunk_overlap=1
)

chunks = splitter.split_documents(docs)

print(chunks[0].page_content)