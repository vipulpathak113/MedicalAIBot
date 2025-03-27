# MedicalAIBot

This is a bot designed to answer any medical query by processing and querying medical documents efficiently.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [How It Works](#how-it-works)
   - [Steps in `memory_llm.py`](#steps-in-memory_llm.py)
   - [Steps in `llm_connect_memory.py`](#steps-in-llm_connect_memory.py)
4. [Usage](#usage)
5. [Example Queries](#example-queries)
6. [Contributing](#contributing)

---

## Overview

MedicalAIBot leverages advanced AI techniques to process medical documents and provide accurate, contextually relevant answers to user queries. It uses **FAISS** for similarity search and **Hugging Face models** for embeddings and language generation.

---

## Features

- Load and process medical documents in bulk.
- Perform semantic similarity searches using FAISS.
- Generate accurate responses using a pre-trained language model.
- Customizable prompt templates for tailored responses.

---

## How It Works

### Steps in `memory_llm.py`

1. **Load PDF Documents**:
   - Uses `PyPDFDirectoryLoader` to load all PDF files from the `data/` directory.
   - Recursively searches for PDF files while ignoring hidden files.

2. **Split Text into Chunks**:
   - Splits text into 500-character chunks with a 50-character overlap using `RecursiveCharacterTextSplitter`.

3. **Generate Vector Embeddings**:
   - Converts text chunks into vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`.

4. **Store Embeddings in FAISS**:
   - Saves embeddings in a FAISS index at `vectorstore/db_faiss`.

### Steps in `llm_connect_memory.py`

1. **Load the FAISS Database**:
   - Loads the FAISS index using `FAISS.load_local`.

2. **Setup the LLM**:
   - Connects to the Hugging Face model `mistralai/Mistral-7B-Instruct-v0.3` with a temperature of 0.5.

3. **Define the Prompt Template**:
   - Guides the LLM to answer questions based on the retrieved context.

4. **Query Embedding and Similarity Search**:
   - Converts queries into embeddings and retrieves the top 3 relevant document chunks.

5. **LLM Tokenization and Response Generation**:
   - Generates responses based on the context and user query.

---

## Usage

### Prerequisites

- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Running the Pipeline

1. **Generate FAISS Index**:
   ```bash
   python memory_llm.py
   ```

2. **Query the Bot**:
   ```bash
   python llm_connect_memory.py
   ```

---

## Example Queries

Here’s how you can interact with the bot:

**User Query**:
> What are the symptoms of diabetes?

**Bot Response**:
> Based on the documents, the symptoms of diabetes include increased thirst, frequent urination, extreme hunger, and unexplained weight loss.

---

## Visual Workflow

Below is a simplified flowchart of the pipeline:

```plaintext
Load PDFs --> Split Text --> Generate Embeddings --> Store in FAISS
       |                                                        |
       v                                                        v
Retrieve Context <-- Query Embedding <-- User Query <-- Generate Response
```

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push:
   ```bash
   git push origin feature-name
   ```
4. Submit a pull request.

---


