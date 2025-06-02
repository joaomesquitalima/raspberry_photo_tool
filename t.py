import easyocr
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models')
reader = easyocr.Reader(['pt', 'en'], model_storage_directory=MODEL_PATH)
