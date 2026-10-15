import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, "app")

import numpy as np
from PIL import Image

from prediction import predict_disease, model, CLASS_NAMES

print("classes:", len(CLASS_NAMES))
print("model input:", model.input_shape)
print("model output:", model.output_shape)

rng = np.random.default_rng(0)
img = Image.fromarray(rng.integers(0, 255, (260, 320, 3), dtype="uint8"))
plant, disease, conf, cls, alts = predict_disease(img, top_k=3)
print(f"random-noise image -> {plant} / {disease} / {conf*100:.2f}%  ({cls})")
for p, d, c in alts:
    print(f"    alt: {p} / {d} / {c*100:.2f}%")

sample = Image.open("data/metadata/sample_processed.jpg").convert("RGB")
plant, disease, conf, cls, alts = predict_disease(sample, top_k=3)
print(f"sample_processed.jpg -> {plant} / {disease} / {conf*100:.2f}%  ({cls})")
print("below threshold:", conf < 0.70)
