from __future__ import annotations

def delta_encode(points):
    if not points:
        return []
    out = [points[0]]
    previous = points[0]
    for point in points[1:]:
        out.append(tuple(b - a for a, b in zip(previous, point)))
        previous = point
    return out

def delta_decode(encoded):
    if not encoded:
        return []
    out = [tuple(encoded[0])]
    current = tuple(encoded[0])
    for delta in encoded[1:]:
        current = tuple(a + b for a, b in zip(current, delta))
        out.append(current)
    return out

def quantize(points, scale):
    if scale <= 0.0:
        raise ValueError('positive scale')
    return [tuple(round(x / scale) for x in point) for point in points]

def max_quantization_error(original, quantized, scale):
    reconstructed = [tuple(x * scale for x in point) for point in quantized]
    return max((max(abs(a - b) for a, b in zip(o, r)) for o, r in zip(original, reconstructed)), default=0.0)
