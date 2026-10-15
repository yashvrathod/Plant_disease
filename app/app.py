import html

import streamlit as st
from PIL import Image

from disease_info import DISEASE_INFO
from prediction import predict_disease
from style import (
    apply_theme,
    masthead,
    panel,
    row,
    confidence_bar,
    severity_meter,
    advisory,
)

CONFIDENCE_THRESHOLD = 0.70

CROPS = [
    "Apple", "Blueberry", "Cherry", "Corn", "Grape", "Orange", "Peach",
    "Pepper bell", "Potato", "Raspberry", "Soybean", "Squash",
    "Strawberry", "Tomato",
]

st.set_page_config(
    page_title="PlantCare AI — field diagnostic",
    layout="centered",
)
apply_theme()

masthead("Field diagnostic sheet &middot; 14 crops &middot; 38 classes")

st.markdown(
    '<p class="pc-lede">Photograph one leaf. Get the crop, the likely disease, '
    'how far it has gone, and what to do about it.</p>',
    unsafe_allow_html=True,
)

specimen_col, findings_col = st.columns([1, 1], gap="medium")

# ---------------------------------------------------------------- specimen
with specimen_col:
    uploaded_file = st.file_uploader(
        "Leaf photo", type=["jpg", "jpeg", "png"]
    )
    captured_file = st.camera_input("Or use the camera")

    image = None
    caption = None

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        caption = "Uploaded specimen"
    elif captured_file is not None:
        image = Image.open(captured_file).convert("RGB")
        caption = "Captured specimen"

    if image is not None:
        st.image(image, caption=caption, use_container_width=True)

    diagnose = st.button(
        "Diagnose this leaf",
        disabled=image is None,
        use_container_width=True,
    )

# ---------------------------------------------------------------- findings
result = None
if diagnose and image is not None:
    result = predict_disease(image, top_k=3)

with findings_col:
    if result is None:
        st.markdown(
            f"""
<div class="pc-panel pc-panel--surface" style="min-height:280px">
  <div class="pc-panel-label">Findings</div>
  <div class="pc-empty">
    <strong>No specimen yet.</strong> Add a leaf photo on the left, then run
    the diagnosis. One leaf per photo, filling most of the frame, gives the
    most reliable reading.
    <div class="pc-chips">{"".join(f'<span class="pc-chip">{c}</span>' for c in CROPS)}</div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        plant, disease, confidence, class_name, alternatives = result
        reliable = confidence >= CONFIDENCE_THRESHOLD
        pct = confidence * 100

        info = DISEASE_INFO.get(class_name, {})
        severity_text = info.get("severity", "")
        band = severity_text.split(" - ")[0] if severity_text else "Moderate"
        severity_note = severity_text.split(" - ", 1)[1] if " - " in severity_text else ""

        finding_cls = "pc-finding" if reliable else "pc-finding pc-finding--tentative"
        note = (
            "" if reliable
            else '<p class="pc-finding-note">Below the confidence threshold &mdash; treat as provisional.</p>'
        )

        alt_rows = ""
        if len(alternatives) >= 2:
            alt_rows = (
                row("Next best guess", html.escape(alternatives[0][1]))
                + row("Then", html.escape(alternatives[1][1]))
            )

        rows = (
            row("Crop", html.escape(plant.title()))
            + row("Confidence", f"{pct:.1f}%")
            + confidence_bar(pct, not reliable)
            + row("Severity", html.escape(band))
            + severity_meter(band)
            + alt_rows
        )

        body = f"""
<div class="pc-panel pc-reveal">
  <div class="pc-panel-label">Findings</div>
  <div class="{finding_cls}">{html.escape(disease)}</div>
  {note}
  {rows}
</div>
"""
        st.markdown(body, unsafe_allow_html=True)

        if not reliable:
            advisory(
                "Confidence below threshold",
                f"The model is only {pct:.0f}% sure, and this tool treats "
                f"anything under {CONFIDENCE_THRESHOLD * 100:.0f}% as unusable for a "
                "decision. Retake the photo: one leaf, close up, even light, "
                "plain background.",
            )

        if severity_note:
            st.markdown(
                f'<p class="pc-caveat">Severity is an estimate from the disease '
                f'profile &mdash; {html.escape(severity_note)}. It is not a '
                f'measurement of this leaf.</p>',
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------------- actions
if result is not None:
    plant, disease, confidence, class_name, alternatives = result
    info = DISEASE_INFO.get(class_name)

    if info:
        symptoms_col, actions_col = st.columns([1, 1], gap="medium")

        with symptoms_col:
            symptoms = "".join(f"<li>{html.escape(s)}</li>" for s in info["symptoms"])
            panel("What to look for", f'<ul class="pc-list">{symptoms}</ul>')

        with actions_col:
            actions = "".join(f"<li>{html.escape(t)}</li>" for t in info["prevention"])
            panel("What to do", f'<ul class="pc-list">{actions}</ul>', surface=True)

        with st.expander("In plain words"):
            st.markdown(
                f'<p class="pc-caveat" style="font-size:0.92rem">{html.escape(info["description"])}</p>',
                unsafe_allow_html=True,
            )

st.markdown(
    """
<div class="pc-footer">
  <strong>Not a substitute for an agronomist.</strong> This sheet gives a
  preliminary reading from a single photograph. Confirm with a local
  agricultural expert before spraying, and follow the label for any product
  you use.
</div>
""",
    unsafe_allow_html=True,
)
