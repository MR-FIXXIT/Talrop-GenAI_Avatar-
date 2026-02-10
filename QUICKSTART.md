# 🚀 Quick Start Guide

## Step 1: Get Your HuggingFace API Token

1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give it a name (e.g., "RAG Chatbot")
4. Select "Read" permission
5. Click "Generate token"
6. Copy the token

## Step 2: Configure the API Key

### Option 1: Through the Web UI (Easiest)
1. Run the app: `./venv/bin/streamlit run app.py`
2. In the sidebar, you'll see "🔑 API Configuration"
3. Paste your token in the input field
4. Click "Save"

### Option 2: Through the .env file
1. Open the `.env` file in the project directory
2. Replace the line with: `HUGGINGFACEHUB_API_TOKEN=your_actual_token_here`
3. Save the file

## Step 3: Run the Application

```bash
./venv/bin/streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Step 4: Upload Documents and Chat

1. Click "Browse files" in the sidebar
2. Select PDF or TXT files
3. Click "Process Documents"
4. Wait for processing to complete
5. Start chatting in the main interface!

## Tips

- **Choose a personality**: Select from Professional, Friendly, Concise, Teacher, Creative, or create your own Custom personality
- **View statistics**: Check the sidebar to see how many chunks and files are loaded
- **Clear chat**: Use the "Clear Chat" button to start a fresh conversation
- **Clear database**: Use the "Clear DB" button to remove all documents and start over
