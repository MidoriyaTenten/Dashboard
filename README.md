## Setup Environment - Shell/Terminal
Sebelum menginstall library, disarankan untuk menggunakan virtual environment agar dependensi tetap terisolasi.
Jalankan perintah berikut :
python -m venv venv
venv\Scripts\activate

## Setup Library
Setelah mengaktifkan virtual environment, install semua dependensi dari file requirements.txt dengan perintah berikut :
pip install -r requirements.txt

## Run steamlit app
Jika semua library sudah terinstall, jalankan aplikasi dengan perintah berikut :
streamlit run dashboard.py
