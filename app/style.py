"""Visual system for the PlantCare AI diagnostic sheet.

Design direction: a two-ink agricultural extension bulletin. Printed-form
hairline rules, a dot-leader findings table, and a segmented severity meter.
Type is Fraunces (display) against Public Sans (interface).
"""

import streamlit as st

PAPER = "#FBFBF9"
INK = "#14161A"
INK_MUTED = "#5A6169"
RULE = "#D5D5CE"
RULE_STRONG = "#1F2226"
SURFACE = "#F1F1EC"

SEVERITY = {
    "None": ("#3F6B4A", "No disease"),
    "Mild": ("#6C7A3A", "Mild"),
    "Moderate": ("#A15C00", "Moderate"),
    "Severe": ("#B3261E", "Severe"),
}
SEVERITY_ORDER = ["None", "Mild", "Moderate", "Severe"]

LEAF_SVG = """
<svg class="pc-leaf" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none"
     stroke="currentColor" stroke-width="1.35" stroke-linecap="round"
     stroke-linejoin="round" aria-hidden="true" focusable="false">
  <path d="M4.5 20.2c-.4-8.3 4.6-14.4 15.7-15.5.9 11-4.9 16.3-13.2 16.3H4.5z"/>
  <path d="M4.5 20.2c3.7-5.1 7.7-9.1 12.6-12.2"/>
</svg>
""".strip()

_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Public+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
  font-family: 'Public Sans', system-ui, sans-serif;
}}

[data-testid="stAppViewContainer"] {{
  background: {PAPER};
}}

[data-testid="stHeader"] {{
  background: transparent;
  height: 2.2rem;
}}

[data-testid="stToolbar"] {{ display: none; }}

#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}

[data-testid="stAppViewContainer"] > .main {{
  padding-top: 1.4rem;
}}

.block-container {{
  max-width: 1080px;
  padding-top: 1.2rem;
  padding-bottom: 4rem;
}}

.pc-markdown p, .pc-markdown li {{
  font-size: 0.95rem;
  line-height: 1.62;
  color: {INK};
}}

/* ---- masthead ---- */
.pc-masthead {{
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  border-bottom: 1.5px solid {RULE_STRONG};
  padding-bottom: 0.65rem;
  margin-bottom: 1.1rem;
}}
.pc-brand {{
  display: flex;
  align-items: center;
  gap: 0.55rem;
  color: {INK};
}}
.pc-leaf {{ display: block; flex: none; }}
.pc-wordmark {{
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 600;
  font-size: 1.5rem;
  letter-spacing: -0.015em;
  line-height: 1;
}}
.pc-masthead-meta {{
  font-size: 0.78rem;
  color: {INK_MUTED};
  letter-spacing: 0.01em;
}}

/* ---- lede ---- */
.pc-lede {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.32rem;
  line-height: 1.42;
  font-weight: 400;
  color: {INK};
  max-width: 46ch;
  margin: 0 0 1.1rem 0;
}}

/* ---- panels ---- */
.pc-panel {{
  border: 1px solid {RULE};
  background: {PAPER};
  padding: 1rem 1.05rem 1.05rem;
  height: 100%;
}}
.pc-panel--surface {{ background: {SURFACE}; }}
.pc-panel-label {{
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: {INK_MUTED};
  border-bottom: 1px solid {RULE};
  padding-bottom: 0.45rem;
  margin-bottom: 0.85rem;
}}

/* ---- report rows (dot leaders) ---- */
.pc-row {{
  display: flex;
  align-items: baseline;
  gap: 0.4rem;
  padding: 0.42rem 0;
  border-bottom: 1px dotted {RULE};
}}
.pc-row:last-child {{ border-bottom: none; }}
.pc-row-label {{
  font-size: 0.83rem;
  color: {INK_MUTED};
  flex: none;
}}
.pc-dots {{
  flex: 1 1 auto;
  border-bottom: 1px dotted {RULE};
  transform: translateY(-0.18rem);
  min-width: 1.5rem;
}}
.pc-row-value {{
  font-size: 0.95rem;
  font-weight: 600;
  color: {INK};
  flex: none;
  text-align: right;
}}

/* ---- finding ---- */
.pc-finding {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.85rem;
  line-height: 1.14;
  font-weight: 600;
  letter-spacing: -0.018em;
  color: {INK};
  margin: 0.1rem 0 0.85rem;
}}
.pc-finding--tentative {{ color: {INK_MUTED}; }}
.pc-finding-note {{
  font-size: 0.82rem;
  color: {INK_MUTED};
  margin: -0.45rem 0 0.9rem;
}}

/* ---- confidence bar ---- */
.pc-bar {{
  height: 4px;
  background: {RULE};
  margin: 0.55rem 0 0.1rem;
  overflow: hidden;
}}
.pc-bar-fill {{
  height: 100%;
  background: {INK};
}}
.pc-bar-fill--low {{ background: {SEVERITY["Severe"][0]}; }}

/* ---- severity meter ---- */
.pc-meter {{
  display: flex;
  gap: 3px;
  margin: 0.15rem 0 0.1rem;
}}
.pc-meter-seg {{
  flex: 1 1 0;
  text-align: center;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.28rem 0.1rem;
  border: 1px solid {RULE};
  color: {INK_MUTED};
  background: {PAPER};
}}
.pc-meter-seg.pc-on {{ color: #fff; border-color: transparent; }}

/* ---- advisory ---- */
.pc-advisory {{
  border-left: 3px solid {SEVERITY["Severe"][0]};
  background: {SURFACE};
  padding: 0.7rem 0.85rem;
  margin: 0.2rem 0 1rem;
}}
.pc-advisory-title {{
  font-weight: 700;
  font-size: 0.9rem;
  color: {INK};
  margin-bottom: 0.18rem;
}}
.pc-advisory p {{
  margin: 0;
  font-size: 0.86rem;
  line-height: 1.55;
  color: {INK};
}}

/* ---- empty state ---- */
.pc-empty {{
  font-size: 0.9rem;
  line-height: 1.6;
  color: {INK_MUTED};
}}
.pc-empty strong {{ color: {INK}; font-weight: 600; }}

/* ---- crop chips ---- */
.pc-chips {{
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 0.7rem;
}}
.pc-chip {{
  font-size: 0.74rem;
  padding: 0.16rem 0.5rem;
  border: 1px solid {RULE};
  color: {INK};
  background: {PAPER};
}}

/* ---- lists ---- */
.pc-list {{
  margin: 0;
  padding-left: 1.05rem;
  font-size: 0.9rem;
  line-height: 1.62;
}}
.pc-list li {{ margin-bottom: 0.3rem; }}
.pc-list li::marker {{ color: {INK_MUTED}; }}

.pc-caveat {{
  font-size: 0.78rem;
  line-height: 1.5;
  color: {INK_MUTED};
  margin-top: 0.45rem;
}}

/* ---- footer ---- */
.pc-footer {{
  border-top: 1.5px solid {RULE_STRONG};
  margin-top: 2.2rem;
  padding-top: 0.8rem;
  font-size: 0.79rem;
  line-height: 1.55;
  color: {INK_MUTED};
}}
.pc-footer strong {{ color: {INK}; }}

/* ---- controls ---- */
.stButton > button {{
  font-family: 'Public Sans', system-ui, sans-serif;
  font-weight: 600;
  font-size: 0.92rem;
  background: {INK};
  color: {PAPER};
  border: 1px solid {INK};
  border-radius: 2px;
  padding: 0.55rem 1.4rem;
  transition: background 150ms ease, transform 150ms ease;
}}
.stButton > button:hover {{
  background: #000;
  border-color: #000;
  color: {PAPER};
}}
.stButton > button:focus {{
  outline: 2px solid {SEVERITY["Severe"][0]};
  outline-offset: 2px;
}}
.stButton > button:disabled {{
  background: transparent;
  color: {INK_MUTED};
  border: 1px dashed {RULE};
}}

[data-testid="stFileUploader"] section {{
  border: 1px dashed {RULE_STRONG} !important;
  border-radius: 2px !important;
  background: {SURFACE};
  padding: 0.9rem !important;
}}
[data-testid="stFileUploader"] section::before {{
  color: {INK_MUTED} !important;
  font-size: 0.82rem !important;
}}
[data-testid="stFileUploader"] label p,
[data-testid="stCameraInput"] label p {{
  color: {INK} !important;
  font-size: 0.83rem !important;
  font-weight: 600 !important;
}}
[data-testid="stCameraInput"] button {{
  border-radius: 2px !important;
}}

@media (prefers-reduced-motion: reduce) {{
  .stButton > button {{ transition: none; }}
  .pc-reveal {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
}}

.pc-reveal {{
  animation: pc-settle 260ms ease-out both;
}}
@keyframes pc-settle {{
  from {{ opacity: 0; transform: translateY(4px); }}
  to {{ opacity: 1; transform: none; }}
}}
"""


def apply_theme() -> None:
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


def leaf_mark(size: int = 30) -> str:
    return LEAF_SVG.format(size=size)


def masthead(meta: str) -> None:
    st.markdown(
        f"""
<div class="pc-masthead">
  <div class="pc-brand">{leaf_mark()}<span class="pc-wordmark">PlantCare&nbsp;AI</span></div>
  <div class="pc-masthead-meta">{meta}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def panel(label: str, body: str, surface: bool = False) -> None:
    cls = "pc-panel pc-panel--surface" if surface else "pc-panel"
    st.markdown(
        f'<div class="{cls}"><div class="pc-panel-label">{label}</div>{body}</div>',
        unsafe_allow_html=True,
    )


def row(label: str, value: str) -> str:
    return (
        f'<div class="pc-row"><span class="pc-row-label">{label}</span>'
        f'<span class="pc-dots"></span><span class="pc-row-value">{value}</span></div>'
    )


def confidence_bar(pct: float, low: bool) -> str:
    fill = "pc-bar-fill pc-bar-fill--low" if low else "pc-bar-fill"
    return (
        f'<div class="pc-bar"><div class="{fill}" style="width:{pct:.1f}%"></div></div>'
    )


def severity_meter(level: str) -> str:
    segs = []
    for name in SEVERITY_ORDER:
        color, label = SEVERITY[name]
        on = name == level
        style = f' style="background:{color}"' if on else ""
        segs.append(
            f'<span class="pc-meter-seg{" pc-on" if on else ""}"{style}>{label}</span>'
        )
    return f'<div class="pc-meter">{"".join(segs)}</div>'


def advisory(title: str, body: str) -> None:
    st.markdown(
        f"""
<div class="pc-advisory">
  <div class="pc-advisory-title">{title}</div>
  <p>{body}</p>
</div>
""",
        unsafe_allow_html=True,
    )
