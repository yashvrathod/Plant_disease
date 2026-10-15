# PlantCare AI

A leaf-photo diagnostic for 14 crop species. Photograph one leaf, get the crop,
the likely disease, how far it has progressed, and what to do next.

Built with TensorFlow/Keras on the PlantVillage dataset, served through Streamlit.

---

## What you get

Every diagnosis is presented as a single field sheet:

| | |
|---|---|
| **Finding** | The most likely disease, or "healthy" |
| **Confidence** | Model confidence, with a bar |
| **Severity** | None / Moderate / Severe, on a segmented meter |
| **Alternatives** | The next two most likely diseases |
| **What to look for** | Visible symptoms to check against the leaf |
| **What to do** | Practical management steps |

Predictions under 70% confidence are flagged as provisional and the sheet tells
you to retake the photo rather than act on it.

Supported crops: Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach,
Pepper bell, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato.
38 disease classes in total, including a healthy class per species where the
training data has one.

---

## Running it

```bash
git clone https://github.com/Anshika-Gangwar/PlantCare-AI.git
cd PlantCare-AI

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
streamlit run app/app.py
```

Opens at `http://localhost:8501`. TensorFlow is roughly 600 MB, so the first
install takes a few minutes.

> Camera capture only works over `localhost` or HTTPS. Browsers block camera
> access on plain HTTP, so on a public deployment use the upload field instead.

---

## The model

| | |
|---|---|
| Architecture | EfficientNetB0 (ImageNet weights, frozen) + global average pooling + 256-unit dense head |
| Framework | TensorFlow 2.21 / Keras 3.15 |
| Input | 224 × 224 RGB |
| Output | 38-class softmax |
| Optimiser | Adam, learning rate 0.001 |
| Loss | Sparse categorical crossentropy |
| Split | 80 / 10 / 10 train / validation / test |

Normalisation is inside the model (`Rescaling(1/255)` plus ImageNet channel
statistics), so callers pass raw 0–255 pixel values.

### Held-out test results

Measured on the PlantVillage test split. Per-class detail is in
[`reports/evaluation/classification_report.csv`](reports/evaluation/classification_report.csv).

| Metric | Value |
|---|---|
| Test accuracy | 98.20% |
| Test loss | 0.0549 |
| Macro precision | 0.978 |
| Macro recall | 0.970 |
| Macro F1 | 0.974 |

Read these carefully. PlantVillage images are collected under controlled
conditions — clean backgrounds, even light, one leaf per frame. Accuracy on
field photographs is materially lower, which is why the sheet treats every
prediction as a preliminary reading and refuses to stand behind low-confidence
ones.

---

## Design

The interface is built as a **field diagnostic sheet**, not a dashboard.
Two-ink printed-form treatment: hairline rules, dot-leader rows for the
findings table, and a segmented severity meter as the one strong visual
element. Type is Fraunces for findings against Public Sans for the interface.
The palette is ink on paper with a single diagnostic red; green appears only
as a result state (severity "None"), never as decoration.

The visual system lives in `app/style.py`. Theme defaults are in
`.streamlit/config.toml`.

---

## Project structure

```text
PlantCare-AI/
├── app/
│   ├── app.py           # page layout and diagnostic flow
│   ├── style.py         # CSS, masthead, report rows, severity meter
│   ├── prediction.py    # model loading and inference
│   └── disease_info.py  # 38-class descriptions, symptoms, severity, actions
├── models/
│   └── best_model.keras
├── notebooks/
│   ├── 01_dataset_analysis.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_model_building.ipynb
│   └── 04_model_evaluation.ipynb
├── reports/
│   ├── evaluation/      # metrics, per-class report, training history
│   └── figures/
├── data/
│   └── metadata/
├── .streamlit/config.toml
├── requirements.txt
└── README.md
```

`data/raw/` and `data/processed/` are gitignored. Download PlantVillage
separately and run `notebooks/02_data_preprocessing.ipynb` to rebuild the
train/validation/test split before training.

---

## Limitations

- Trained on PlantVillage only. It has not been validated on field
  photography, so complex backgrounds, shadows, overlapping leaves, and
  partially visible specimens will degrade results.
- Softmax confidence is not a reliability guarantee. A model can be highly
  confident and still wrong, particularly on images that are not leaves.
- Severity is derived from the disease profile, not measured from the image.
  It does not estimate lesion coverage on the photographed leaf.
- The 14 supported species are fixed by the training data. Anything else will
  still be classified, just incorrectly.

---

## Future work

- Wire the augmentation layers defined in `02_data_preprocessing.ipynb` into
  the training loop
- Compare architectures rather than training a single backbone
- Test on field-collected images across lighting and background conditions
- Image-derived severity instead of profile-based severity
- Localisation and offline use for low-connectivity areas

---

## Acknowledgements

PlantVillage dataset, TensorFlow, Streamlit, and the open-source community.

Corresponds to the proposed *AgriVision Assist* crop health diagnosis and
decision-support platform.
