import math


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
