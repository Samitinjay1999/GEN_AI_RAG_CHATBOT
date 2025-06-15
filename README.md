
# 🔴 ChatFlow – GenAI RAG Chatbot (Flask + Gemini + ChromaDB)

ChatFlow is a lightweight Retrieval-Augmented Generation (RAG) chatbot that uses the **Google Gemini API** for embeddings and response generation, and **ChromaDB** as a vector database. Users can upload documents (PDF/TXT), ask questions, and get contextually aware answers from the chatbot — all in a sleek WhatsApp-style interface.

---

## 🚀 Features

✅ Upload PDF or TXT files  
✅ Split content into 200-word chunks  
✅ Generate & store Gemini embeddings in ChromaDB  
✅ Search for relevant chunks using user queries  
✅ Generate Gemini-powered responses using retrieved context  
✅ Stylish WhatsApp-inspired frontend  
✅ Session-based login & chat memory  
✅ No LangChain or Haystack — 100% custom RAG logic

---

## 🧱 Project Structure

```
genai_rag_chatbot/
├── main.py                     # Flask app entry point
├── config.py                   # API keys, limits, URLs
├── .env                        # Environment variables (API key)
├── requirements.txt            # Python dependencies
├── uploads/                    # Uploaded files
├── app/
│   ├── routes/                 # Flask API routes
│   │   ├── home.py             # Login/logout logic
│   │   ├── chat.py             # RAG chatbot endpoint
│   │   └── upload.py           # File upload + processing
│   ├── services/               # Core logic
│   │   ├── utils.py            # Read/clean/chunk documents
│   │   ├── embedding.py        # Gemini embedding + chat APIs
│   │   ├── chromadb_service.py # ChromaDB insert/query
│   │   └── rag_engine.py       # Full RAG pipeline
│   ├── templates/              # index.html UI
│   └── static/                 # CSS & JS for frontend
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/genai_rag_chatbot.git
cd genai_rag_chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file in the root:

```env
GEMINI_API_KEY=your_api_key_here
```

> 🔑 You can generate a Gemini API key from https://makersuite.google.com/app/apikey

---

## 🔑 Login Credentials (Demo)

```
Username: admin
Password: admin123
```

---

## 🖥️ Running the Application

```bash
python main.py
```

Visit: `http://localhost:5000`

---

## 🧪 How It Works

1. User logs in via `/login` API
2. Uploads a PDF or TXT file
3. Server extracts and chunks text
4. Each chunk is embedded via Gemini and stored in ChromaDB
5. User sends query → embedded → ChromaDB searched → context + query sent to Gemini
6. Gemini generates answer, returned via `/chat` API

---

## 🎨 Frontend Highlights

- Clean, responsive UI (styled via `style.css`)
- WhatsApp-like chat layout
- 📎 file upload pop-up (drag & drop)
- Logout button with session-based handling

---

## ✅ Evaluation Checklist

| Feature                                       | Status  |
|----------------------------------------------|---------|
| File Upload (PDF/TXT)                        | ✅ Done |
| Gemini Embedding API                         | ✅ Done |
| Store vectors in ChromaDB                    | ✅ Done |
| Chat UI + RAG query processing               | ✅ Done |
| Per-session memory                           | ✅ Done |
| Login & protected routes                     | ✅ Done |
| Stylish UI (WhatsApp-style + file upload)    | ✅ Done |
| No LangChain or third-party wrappers         | ✅ Done |

---

## 🛡️ Security Notes

- Uploads are sanitized via `secure_filename()`
- Session-based authentication protects chat and upload APIs
- Logging is enabled for auditability (in `app.log`)

---

## 📄 License

MIT License

Copyright (c) 2025 Samitinjay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...

---

## 🤝 Contributing

Want to enhance the UI or add support for more file types? PRs are welcome!

---

## 💬 Contact

For questions or collaboration:
**Samitinjay** – [GitHub](https://github.com/your-username) | [Email](mailto:samitinjay@example.com)
