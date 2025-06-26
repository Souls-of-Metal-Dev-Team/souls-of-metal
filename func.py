def lerp(i, f, t):
    return (i * (1 - t) + (f * t)) if t < 1 else f
