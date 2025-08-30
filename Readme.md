# 🩺 MedScribe – Medical Report Summarizer
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medscribe-summarizer.streamlit.app/)


MedScribe is a Streamlit-based AI tool that converts lengthy medical documents into concise, dual-format summaries:  

- 👨‍⚕️ **Technical version** for doctors  
- 🧑‍🤝‍🧑 **Simplified version** for patients & families  

---

## 🚀 Features
- Upload medical reports (`.pdf`, `.txt`)  
- Text preprocessing & cleaning pipeline  
- AI-powered summarization  
- Dual output (doctor + patient friendly)  
- Clean, intuitive Streamlit interface  

---

## 🛠 Tech Stack
- **Python 3.11+**  
- **Streamlit** – interactive web app  
- **PyPDF2** – PDF parsing  
- **Custom NLP pipeline** – summarization logic  

---

## 📂 Project Structure

MedScribe/
├── app.py # Main Streamlit app
├── utils/ # Helper functions
├── requirements.txt # Dependencies
├── sample_reports/ # Example patient reports
└── README.md


---

## ⚡ Installation (Local)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/MedScribe.git
cd MedScribe

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py


🌍 Live Demo

Coming soon on 🤗 Hugging Face Spaces

📄 License

This project is licensed under the MIT License.

🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
