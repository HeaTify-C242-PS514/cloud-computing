# **Heart Health Prediction API**

## **Deskripsi**
API ini dirancang untuk memprediksi kondisi kesehatan jantung seseorang berdasarkan fitur-fitur seperti aktivitas olahraga, riwayat penyakit jantung, kebiasaan merokok, pola konsumsi makanan, dan lainnya. API ini dibangun menggunakan FastAPI, dengan model machine learning yang disimpan di Google Cloud Storage dan hasil prediksi yang disimpan di Firestore.

---

## **Fitur**
1. Prediksi kondisi kesehatan jantung dengan endpoint `/predict`.
2. Preprocessing input data secara otomatis (konversi kategori menjadi numerik).
3. Penyimpanan hasil prediksi ke Firestore.
4. Dapat di-deploy ke Google Cloud Run menggunakan Docker.

---

## **Persyaratan**
1. Python 3.9 atau lebih baru.
2. Google Cloud Service Account untuk akses Firestore.
3. Dependensi Python (lihat `requirements.txt`).

---

## **Instalasi**
1. **Clone Repository**:
   ```bash
   git clone https://github.com/your-repo/heart-health-api.git
   cd heart-health-api

