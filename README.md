# DocMind AI

> 📖 RAG-Powered Document Q&A Assistant

## Overview

**DocMind AI** is a Retrieval-Augmented Generation (RAG) system that lets you upload PDF documents and ask questions about their content. The system uses semantic search to retrieve relevant document chunks and a large language model to generate accurate, context-aware answers.

## Key Features

- 📄 **PDF Document Upload & Processing**: Load and split PDFs into searchable chunks
- 🔍 **Semantic Search**: Uses Hugging Face embeddings and ChromaDB vector store for accurate retrieval
- 🤖 **Mistral AI Integration**: Generates answers using state-of-the-art LLM
- 🎨 **Streamlit Web UI**: Modern, user-friendly interface for interacting with your documents
- 💬 **Command-line Interface**: Simple CLI for quick testing
- 📊 **Source Citations**: Shows which document chunks were used to generate answers

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | LangChain |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| LLM | Mistral AI (mistral-small-latest) |
| UI | Streamlit |
| Environment Management | python-dotenv |

## Getting Started

### Prerequisites

- Python 3.9+
- A Mistral AI API key (get one from [Mistral AI Console](https://console.mistral.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

### Usage

#### Option 1: Streamlit Web Interface
```bash
streamlit run app.py
```
Open the URL shown in your browser, upload a PDF in the sidebar, and start asking questions!

#### Option 2: Command-line Interface
First, create the vector database (update `create_database.py` to point to your PDF):
```bash
python create_database.py
```
Then run the CLI:
```bash
python main.py
```

## Project Structure

```
docmind-ai/
├── app.py                   # Streamlit web UI
├── main.py                  # Command-line interface
├── create_database.py       # Vector DB creation script
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (not tracked in git)
├── document loaders/        # Document loading test scripts
├── retrievers/              # Retrieval strategy test scripts
├── vector store/            # Vector storage test scripts
└── chroma-db/               # Persistent vector DB (not tracked in git)
```

## Example Use Cases

- 📚 **Academic Research**: Ask questions about research papers
- 📝 **Document Analysis**: Get insights from reports or manuals
- 🎓 **Study Aid**: Create a Q&A bot for your study materials

## Future Enhancements

- [ ] Support for more document types (DOCX, TXT, MD, web pages)
- [ ] Multi-document upload and querying
- [ ] Hybrid search (keyword + semantic)
- [ ] Multi-query retriever
- [ ] Conversation memory
- [ ] Multiple embedding model options
- [ ] Multiple LLM options
- [ ] Deployment to Streamlit Community Cloud

## License

MIT License (feel free to use this project for your resume/portfolio!)
