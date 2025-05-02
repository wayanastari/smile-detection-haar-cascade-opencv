😄 Smile Detection with OpenCV and Streamlit

Proyek ini mendeteksi senyuman pada gambar, video, dan secara real-time menggunakan OpenCV, dan menyajikan antarmuka web dengan Streamlit.

📁 Struktur Folder
smile-detection/
├── __pycache__/           # Cache Python
├── output/                # Hasil deteksi: gambar/video dengan bounding box
├── venv/                  # Virtual environment
├── app.py                 # File utama untuk Streamlit
├── requirements.txt       # Daftar dependensi Python
├── smile.py               # Logika deteksi senyum (OpenCV)

🚀 Fitur
    Deteksi senyum pada:
        📷 Gambar
        🎞️ Video
        🎥 Kamera real-time
    Bounding box dan label (smile) pada hasil
    Antarmuka pengguna via Streamlit

🔧 Teknologi
    Python 3
    OpenCV
    Streamlit
    Haar Cascade Classifier
