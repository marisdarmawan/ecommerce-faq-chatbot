# 🛒 E-commerce FAQ Chatbot

A smart customer support chatbot powered by Google Gemini AI and TF-IDF similarity matching. This Streamlit application helps customers get instant answers to frequently asked questions about products, shipping, returns, and more.

## 🌟 Features

- **Intelligent Question Matching**: Uses TF-IDF vectorization and cosine similarity to find the most relevant FAQ answers
- **AI-Powered Responses**: Leverages Google Gemini 1.5 Flash to generate conversational, human-like responses
- **Secure API Key Management**: Supports both Streamlit secrets and manual input for API keys
- **Interactive Chat Interface**: Clean, user-friendly chat interface with message history
- **Relevance Threshold**: Filters out irrelevant questions to maintain response quality
- **Error Handling**: Robust error handling for API calls and data loading

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google API Key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))
- FAQ dataset in JSON format

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd ecommerce-faq-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key (choose one method):

**Option A: Using Streamlit Secrets (Recommended)**
- Create a `.streamlit` folder in your project directory
- Create a `secrets.toml` file inside `.streamlit/`
- Add your API key:
```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

**Option B: Manual Input**
- The app will prompt you to enter your API key when you run it

4. Prepare your FAQ dataset:
- Ensure your JSON file is named `Ecommerce_FAQ_Chatbot_dataset.json`
- Place it in the same directory as your Python script
- The JSON should have this structure:
```json
{
  "questions": [
    {
      "question": "What is your return policy?",
      "answer": "We offer a 30-day return policy..."
    },
    {
      "question": "How long does shipping take?",
      "answer": "Standard shipping takes 3-5 business days..."
    }
  ]
}
```

5. Run the application:
```bash
streamlit run app.py
```

## 📁 Project Structure

```
ecommerce-faq-chatbot/
├── app.py                                    # Main Streamlit application
├── requirements.txt                          # Python dependencies
├── README.md                                # This file
├── Ecommerce_FAQ_Chatbot_dataset.json      # FAQ dataset
└── .streamlit/
    └── secrets.toml                         # API key storage (optional)
```

## 🔧 Configuration

### Similarity Threshold
You can adjust the relevance threshold in the `find_most_relevant_question` function:
```python
if highest_similarity_score < 0.2:  # Adjust this value (0.0 to 1.0)
    return None, None
```

- Higher values (e.g., 0.3-0.5): More strict matching, fewer but more relevant responses
- Lower values (e.g., 0.1-0.2): More lenient matching, more responses but potentially less relevant

### FAQ Dataset Format
Your JSON file should contain a "questions" array with objects having "question" and "answer" keys:
```json
{
  "questions": [
    {
      "question": "Your question here",
      "answer": "Your answer here"
    }
  ]
}
```

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub (make sure `.streamlit/secrets.toml` is in `.gitignore`)
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy your app from your GitHub repository
4. Add your API key in the app settings under "Secrets":
```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

### Local Development
```bash
streamlit run app.py
```

## 🛠️ Dependencies

- `streamlit>=1.28.0` - Web application framework
- `google-generativeai>=0.3.0` - Google Gemini API client
- `pandas>=1.5.0` - Data manipulation and analysis
- `scikit-learn>=1.3.0` - Machine learning library for TF-IDF
- `numpy>=1.24.0` - Numerical computing

## 🔒 Security Notes

- Never commit your API keys to version control
- Use Streamlit secrets for production deployments
- Add `.streamlit/` to your `.gitignore` file
- Consider implementing rate limiting for production use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

**"File not found" error:**
- Ensure `Ecommerce_FAQ_Chatbot_dataset.json` is in the same directory as your Python script
- Check that the file name matches exactly (case-sensitive)

**API key errors:**
- Verify your Google API key is valid and active
- Check that the Gemini API is enabled in your Google Cloud Console
- Ensure you have sufficient API quota

**No responses or poor matching:**
- Check your FAQ dataset format
- Adjust the similarity threshold
- Ensure your questions are descriptive and varied

**Import errors:**
- Run `pip install -r requirements.txt` to install all dependencies
- Check that you're using Python 3.8 or higher

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the Streamlit and Google AI documentation

---

Made with ❤️ using Streamlit and Google Gemini AI
