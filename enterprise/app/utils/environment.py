import os
from dotenv import load_dotenv

# Load .env **1 lần** khi import module
load_dotenv()

def getenv(var_name: str, default=None):
    """Lấy giá trị biến môi trường từ .env hoặc hệ thống"""
    return os.getenv(var_name, default)