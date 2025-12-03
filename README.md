# Titraille Assistant

## Title Generator Assistant for Journalists

A Streamlit-based application that helps journalists generate compelling titles for their articles using AI-powered assistance.

### Features

- AI-powered title generation using Mistral AI
- User-friendly Streamlit interface
- Environment variable management with python-dotenv

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hericlibong/titraille_assistant.git
   cd titraille_assistant
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Mistral AI API key:
   ```
   MISTRAL_API_KEY=your_api_key_here
   ```

### Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

### Requirements

- Python 3.8+
- Streamlit
- Mistral AI
- python-dotenv