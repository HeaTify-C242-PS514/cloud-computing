import os
from google.cloud import storage
from tensorflow.keras.models import load_model

def load_model_from_gcs():
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./capstone-test-443716-0f00e066d4e2.json")

        # Cloud Storage settings
        bucket_name = 'capstonetest-storage'
        blob_name = 'model.keras'
        local_path = '/tmp/model.keras'

        # Download model.keras from Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(local_path)

        print(f"✅ Model {blob_name} berhasil diunduh dari bucket {bucket_name} ke {local_path}")

        # Load the Keras model
        model = load_model(local_path)
        print("✅ Model berhasil dimuat!")
        return model
    except Exception as e:
        print(f"❌ Gagal memuat model: {e}")
        return None
