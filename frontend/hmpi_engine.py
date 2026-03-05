import numpy as np
from standards import standards, ideal_values

def calculate_hmpi(row):
    K = 1
    weighted_sum = 0
    total_weight = 0

    for metal in standards.keys():
        Mi = row[metal]
        Si = standards[metal]
        Ii = ideal_values[metal]

        Qi = ((Mi - Ii) / (Si - Ii)) * 100
        Wi = K / Si

        weighted_sum += Wi * Qi
        total_weight += Wi

    hmpi = weighted_sum / total_weight
    return round(hmpi, 2)


def classify_hmpi(value):
    if value < 50:
        return "Excellent"
    elif value < 100:
        return "Acceptable"
    elif value < 200:
        return "Polluted"
    else:
        return "Highly Polluted"