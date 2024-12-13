# **Dokumentasi API: Heart Health Prediction**

## **Deskripsi**
API ini digunakan untuk memprediksi kondisi kesehatan jantung berdasarkan beberapa fitur input seperti aktivitas olahraga, riwayat penyakit jantung, kebiasaan merokok, dan pola konsumsi makanan.

---

## **Endpoint**

### **1. Prediksi Kesehatan Jantung**
- **URL**: `/predict`
- **Metode**: `POST`
- **Deskripsi**: Menerima data input untuk memprediksi kondisi kesehatan jantung dan menyimpan hasilnya ke Firestore.

---

### **Input**
- **Format**: JSON
- **Contoh Input**:
  ```json
  {
    "Exercise": "Yes",
    "Heart_Disease": "No",
    "Sex": "Male",
    "BMI": 25.0,
    "Smoking_History": "No",
    "Alcohol_Consumption": 1.5,
    "Fruit_Consumption": 3.0,
    "Green_Vegetables_Consumption": 2.5,
    "FriedPotato_Consumption": 0.5
  }

