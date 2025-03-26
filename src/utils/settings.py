import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')

IDLE_TIME = 0.5 #seconds
DATA_FILE = os.path.join(DATA_DIR, 'transactions.json')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.json')
