import numpy as np # type: ignore
import re


CAT_INDEX = {
    "Природа": 0,
    "Спорт": 1, 
    "Настольные игры": 2,
    "Искусство": 3,
    "Питание": 4
}

SEX_INDEX = {
    'male': 0,
    'female': 1
}

MAX_DURATION = 240
MAX_CAPACITY = 100
MAX_AGE = 100



def cosine_distance(x1, x2):
    return np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))


def filter_str(s):
    return re.sub(r'[^\w\s]', '', s.lower())
