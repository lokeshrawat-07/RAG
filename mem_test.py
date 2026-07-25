import os
import psutil

process = psutil.Process(os.getpid())
print("Initial:", process.memory_info().rss / 1024 / 1024, "MB")

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
print("After pysqlite3:", process.memory_info().rss / 1024 / 1024, "MB")

from langchain_community.document_loaders import PyPDFLoader
print("After PyPDFLoader:", process.memory_info().rss / 1024 / 1024, "MB")

from langchain_text_splitters import RecursiveCharacterTextSplitter
print("After RecursiveCharacterTextSplitter:", process.memory_info().rss / 1024 / 1024, "MB")

from langchain_community.embeddings import HuggingFaceEmbeddings
print("After HuggingFaceEmbeddings:", process.memory_info().rss / 1024 / 1024, "MB")

from langchain_community.vectorstores import Chroma
print("After Chroma:", process.memory_info().rss / 1024 / 1024, "MB")

from langchain_mistralai import ChatMistralAI
print("After ChatMistralAI:", process.memory_info().rss / 1024 / 1024, "MB")
