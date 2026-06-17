import streamlit as st
import pandas as pd
import io
import time

st.set_page_config(
    page_title="SheetFusion · Excel Merger",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state init ──────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

for k in ["merged_df", "file1_df", "file2_df"]:
    if k not in st.session_state:
        st.session_state[k] = None

# ── Dynamic theme CSS vars ──────────────────────────────────────────────────
if st.session_state.theme == "light":
    theme_vars = """
    :root {
      --bg:#f8fafc; --surface:#ffffff; --surface2:#f1f5f9;
      --border:#cbd5e1; --accent:#4f46e5; --accent2:#06b6d4;
      --success:#10b981; --muted:#64748b; --text:#0f172a;
    }"""
    checked_color = "#4f46e5"
    label_color   = "#0f172a"
else:
    theme_vars = """
    :root {
      --bg:#0a0d14; --surface:#111520; --surface2:#181d2e;
      --border:#1e2640; --accent:#6c63ff; --accent2:#00d4ff;
      --success:#00e5a0; --muted:#6b7280; --text:#e8ecf4;
    }"""
    checked_color = "#6c63ff"
    label_color   = "#e8ecf4"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
{theme_vars}

html,body,[class*="css"]{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);}}
#MainMenu,footer,header{{visibility:hidden;}}
.block-container{{padding:2rem 3rem !important;max-width:1400px !important;}}

/* ── Lucide icons ── */
.lucide{{width:1.1rem;height:1.1rem;stroke-width:2.2px;vertical-align:middle;display:inline-block;}}
@keyframes spin{{0%{{transform:rotate(0deg);}}100%{{transform:rotate(360deg);}}}}
.animate-spin{{animation:spin 1.2s linear infinite;}}

/* ── Hero ── */
.hero{{text-align:center;padding:2.5rem 1rem 1.5rem;
  background:radial-gradient(ellipse 80% 60% at 50% -10%,#6c63ff18,transparent);}}
.hero h1{{font-size:3.2rem;font-weight:800;letter-spacing:-1.5px;margin:0 0 .4rem;
  background:linear-gradient(135deg,var(--text) 30%,var(--accent2) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
.hero p{{font-size:1rem;color:var(--muted);margin:0;font-weight:300;}}
.badge{{display:inline-flex;align-items:center;gap:.4rem;margin-bottom:.8rem;
  background:linear-gradient(135deg,#6c63ff15,#00d4ff15);
  border:1px solid #6c63ff33;border-radius:50px;
  padding:.3rem 1.1rem;font-size:.75rem;color:var(--accent2);
  letter-spacing:2px;text-transform:uppercase;font-weight:600;}}

/* ── Card columns ── */
[data-testid="column"]{{
  background:var(--surface) !important;border:1px solid var(--border) !important;
  border-radius:14px !important;padding:1.4rem 1.4rem 1.6rem !important;
  transition:border-color .3s,box-shadow .3s;}}
[data-testid="column"]:hover{{
  border-color:#6c63ff55 !important;box-shadow:0 0 24px #6c63ff14 !important;}}

/* ── Upload zone ── */
[data-testid="stFileUploader"]{{
  background:var(--surface2) !important;border:2px dashed var(--border) !important;
  border-radius:12px !important;}}
[data-testid="stFileUploader"]:hover{{border-color:var(--accent) !important;}}

/* ── Selectbox / number ── */
[data-testid="stSelectbox"]>div>div,
[data-testid="stNumberInput"] input{{
  background:var(--surface2) !important;border:1px solid var(--border) !important;
  border-radius:10px !important;color:var(--text) !important;}}
[data-testid="stWidgetLabel"] p{{color:{label_color};}}

/* ── Radio pill toggles ── */
[data-testid="stRadio"]>div{{width:100% !important;}}
[data-testid="stRadio"] div[role="radiogroup"]{{
  display:flex !important;flex-direction:column !important;
  width:100% !important;gap:.4rem !important;}}
[data-testid="stRadio"] div[role="radiogroup"]>label{{
  background:var(--surface2) !important;border:1px solid var(--border) !important;
  border-radius:10px !important;padding:.6rem 1rem !important;margin:0 !important;
  display:flex !important;align-items:center !important;gap:.6rem !important;
  cursor:pointer !important;font-size:.88rem !important;font-weight:500 !important;
  transition:all .22s !important;width:100% !important;box-sizing:border-box !important;
  min-height:2.5rem !important;color:var(--text) !important;}}
[data-testid="stRadio"] div[role="radiogroup"]>label:hover{{
  border-color:var(--accent) !important;background:#6c63ff12 !important;}}
[data-testid="stRadio"] div[role="radiogroup"]>label:has(input:checked){{
  border-color:var(--accent) !important;background:#6c63ff1e !important;
  box-shadow:0 0 12px #6c63ff28 !important;color:{checked_color} !important;}}

/* ── Gradient divider ── */
.grad-div{{height:1px;margin:1.8rem 0;
  background:linear-gradient(90deg,transparent,var(--accent),var(--accent2),transparent);}}

/* ── Labels ── */
.step-lbl{{font-size:.68rem;font-weight:700;letter-spacing:2px;
  text-transform:uppercase;color:var(--accent);margin-bottom:.5rem;}}
.card-title{{font-size:1.05rem;font-weight:600;color:var(--text);margin-bottom:.8rem;
  display:flex;align-items:center;gap:.5rem;}}

/* ── Merge progress ── */
.mrg-prog{{background:var(--surface2);border-radius:50px;padding:.85rem 1.3rem;
  border:1px solid var(--border);display:flex;align-items:center;gap:.8rem;font-size:.85rem;}}
.pulse{{width:10px;height:10px;border-radius:50%;background:var(--accent2);flex-shrink:0;
  animation:pulse-anim 1.2s ease-in-out infinite;}}
@keyframes pulse-anim{{0%,100%{{opacity:1;transform:scale(1);}}50%{{opacity:.4;transform:scale(1.5);}}}}

/* ── Skeleton ── */
.sk{{background:linear-gradient(90deg,var(--surface2) 25%,var(--border) 50%,var(--surface2) 75%);
  background-size:200% 100%;border-radius:8px;animation:shimmer 1.6s infinite;}}
@keyframes shimmer{{0%{{background-position:200% 0;}}100%{{background-position:-200% 0;}}}}
.sk-h{{height:42px;margin-bottom:10px;}}.sk-r{{height:34px;margin:5px 0;}}

/* ── Stats ── */
.stat{{background:var(--surface2);border:1px solid var(--border);
  border-radius:12px;padding:.9rem 1.2rem;text-align:center;}}
.stat-n{{font-size:2rem;font-weight:800;color:var(--accent2);line-height:1;}}
.stat-l{{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-top:.3rem;}}

/* ── Buttons ── */
.stButton>button{{
  background:linear-gradient(135deg,var(--accent),#8b83ff) !important;
  color:#fff !important;border:none !important;border-radius:50px !important;
  padding:.6rem 2rem !important;font-weight:600 !important;font-size:.9rem !important;
  box-shadow:0 4px 20px #6c63ff40 !important;transition:all .3s !important;}}
.stButton>button:hover{{transform:translateY(-2px) !important;box-shadow:0 8px 30px #6c63ff60 !important;}}
[data-testid="stDownloadButton"]>button{{
  background:linear-gradient(135deg,var(--success),#00b37a) !important;
  color:#0a0d14 !important;border:none !important;border-radius:50px !important;
  padding:.65rem 2.2rem !important;font-weight:700 !important;font-size:.95rem !important;
  box-shadow:0 4px 22px #00e5a040 !important;transition:all .3s !important;}}
[data-testid="stDownloadButton"]>button:hover{{
  transform:translateY(-2px) !important;box-shadow:0 8px 32px #00e5a060 !important;}}

/* ── Banners ── */
.ok-banner{{background:#00e5a015;border:1px solid #00e5a040;border-radius:10px;
  padding:.75rem 1rem;color:var(--success);font-weight:500;font-size:.85rem;
  display:flex;align-items:center;gap:.5rem;margin-top:.5rem;}}
</style>
""", unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="badge">
    <i data-lucide="zap"></i> SheetFusion
  </div>
  <h1>Excel Sheet Merger</h1>
  <p>Upload · Configure · Merge · Download — beautifully fast.</p>
</div>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def get_sheet_names(f):
    try:
        return pd.ExcelFile(f).sheet_names
    except Exception:
        return ["Sheet1"]

def read_sheet(f, sheet, hdr):
    try:
        df = pd.read_excel(f, sheet_name=sheet, header=int(hdr))
        df.columns = df.columns.astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return None

def skeleton(rows=4):
    html = '<div class="sk sk-h"></div>'
    for _ in range(rows):
        html += '<div class="sk sk-r"></div>'
    return f'<div style="margin-top:1rem">{html}</div>'

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Upload
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="grad-div"></div>', unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown('<div class="step-lbl">Step 1A · File One</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i data-lucide="upload"></i> Upload First Spreadsheet</div>', unsafe_allow_html=True)
    file1 = st.file_uploader("file1", type=["xlsx", "xls", "xlsb"],
                              key="fu1", label_visibility="collapsed")
with c2:
    st.markdown('<div class="step-lbl">Step 1B · File Two</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><i data-lucide="upload"></i> Upload Second Spreadsheet</div>', unsafe_allow_html=True)
    file2 = st.file_uploader("file2", type=["xlsx", "xls", "xlsb"],
                              key="fu2", label_visibility="collapsed")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Sheet & Header
# ─────────────────────────────────────────────────────────────────────────────
if file1 and file2:
    st.markdown('<div class="grad-div"></div>', unsafe_allow_html=True)

    sheets1 = get_sheet_names(file1)
    sheets2 = get_sheet_names(file2)

    s1, s2 = st.columns(2, gap="large")
    with s1:
        st.markdown('<div class="step-lbl">Step 2A · Sheet & Header</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i data-lucide="table"></i> File 1 — Sheet Selection</div>', unsafe_allow_html=True)
        sheet1  = st.selectbox("Select sheet (File 1)", sheets1, key="sh1")
        header1 = st.number_input("Header row index (0 = first row)", 0, 50, 0, 1, key="hdr1")
    with s2:
        st.markdown('<div class="step-lbl">Step 2B · Sheet & Header</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><i data-lucide="table"></i> File 2 — Sheet Selection</div>', unsafe_allow_html=True)
        sheet2  = st.selectbox("Select sheet (File 2)", sheets2, key="sh2")
        header2 = st.number_input("Header row index (0 = first row)", 0, 50, 0, 1, key="hdr2")

    sk_ph = st.empty()
    sk_ph.markdown(skeleton(), unsafe_allow_html=True)
    df1 = read_sheet(file1, sheet1, header1)
    df2 = read_sheet(file2, sheet2, header2)
    time.sleep(0.25)
    sk_ph.empty()

    if df1 is not None and df2 is not None:
        st.session_state.file1_df = df1
        st.session_state.file2_df = df2

        # ─────────────────────────────────────────────────────────────────
        # STEP 3 — Column picker
        # ─────────────────────────────────────────────────────────────────
        st.markdown('<div class="grad-div"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:1.2rem">
          <div class="step-lbl" style="display:inline-block">Step 3 · Column Mapping</div>
          <div style="font-size:1.25rem;font-weight:700;margin-top:.3rem;color:var(--text)">
            Select one merge key from each file</div>
          <div style="color:var(--muted);font-size:.83rem;margin-top:.25rem">
            Rows are matched where these column values are equal</div>
        </div>""", unsafe_allow_html=True)

        p1, p2 = st.columns(2, gap="large")
        with p1:
            st.markdown('<div class="step-lbl">File 1 columns</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title"><i data-lucide="key"></i> Pick merge key — File 1</div>', unsafe_allow_html=True)
            sel1 = st.radio("key1", df1.columns.tolist(), index=None,
                            key="col1_radio", label_visibility="collapsed")
            if sel1:
                st.markdown(f'<div class="ok-banner"><i data-lucide="check-circle"></i> Selected: <strong>{sel1}</strong></div>',
                            unsafe_allow_html=True)
        with p2:
            st.markdown('<div class="step-lbl">File 2 columns</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title"><i data-lucide="key"></i> Pick merge key — File 2</div>', unsafe_allow_html=True)
            sel2 = st.radio("key2", df2.columns.tolist(), index=None,
                            key="col2_radio", label_visibility="collapsed")
            if sel2:
                st.markdown(f'<div class="ok-banner"><i data-lucide="check-circle"></i> Selected: <strong>{sel2}</strong></div>',
                            unsafe_allow_html=True)

        # ── Merge strategy ────────────────────────────────────────────────
        if sel1 and sel2:
            st.markdown('<div class="grad-div"></div>', unsafe_allow_html=True)

            _, mc, _ = st.columns([1, 3, 1])
            with mc:
                st.markdown('<div class="step-lbl" style="text-align:center">Merge Strategy</div>',
                            unsafe_allow_html=True)
                merge_type = st.selectbox(
                    "How to combine rows",
                    options=["outer", "left", "right", "inner"],
                    format_func=lambda x: {
                        "outer": "Outer — Keep ALL rows from both files (recommended)",
                        "left":  "Left  — Keep all rows from File 1 only",
                        "right": "Right — Keep all rows from File 2 only",
                        "inner": "Inner — Keep only matched rows",
                    }[x],
                    key="merge_type",
                )

                st.markdown("""
                <div style="background:#6c63ff12;border:1px solid #6c63ff33;border-radius:10px;
                  padding:.9rem 1.1rem;margin:.6rem 0;font-size:.83rem;color:#c4bfff;line-height:1.6">
                  <strong style="color:#a89cff;display:flex;align-items:center;gap:.4rem">
                    <i data-lucide="settings"></i> Duplicate Match Handling
                  </strong><br>
                  Choose how to handle duplicate key values (e.g. multiple transactions with the same amount):
                </div>""", unsafe_allow_html=True)

                dup_mode = st.selectbox(
                    "Duplicate handling strategy",
                    options=[
                        "One-to-One (Sequential Match)",
                        "First Match Only",
                        "Many-to-Many (All combinations)"
                    ],
                    index=0,
                    help="Sequential Match pairs duplicate values in order (1st↔1st, 2nd↔2nd) — no row inflation. First Match Only drops subsequent duplicates. Many-to-Many produces every combination.",
                    key="dup_mode_sel"
                )

                st.markdown('<div class="grad-div"></div>', unsafe_allow_html=True)
                do_merge = st.button("⚡  Merge Files Now", use_container_width=True)

            if do_merge:
                prog_ph = st.empty()
                steps = [
                    ('Reading & cleaning columns…',   0.5),
                    ('Converting numeric values…',    0.4),
                    (f'Performing {merge_type} join…', 0.7),
                    ('Filling blanks for unmatched rows…', 0.35),
                    ('Finalising output…',             0.25),
                ]
                for msg, delay in steps:
                    prog_ph.markdown(
                        f'<div class="mrg-prog"><div class="pulse"></div><span>{msg}</span></div>',
                        unsafe_allow_html=True)
                    time.sleep(delay)

                try:
                    d1 = df1.copy()
                    d2 = df2.copy()
                    d1[sel1] = pd.to_numeric(d1[sel1], errors="coerce").fillna(d1[sel1])
                    d2[sel2] = pd.to_numeric(d2[sel2], errors="coerce").fillna(d2[sel2])

                    if dup_mode == "First Match Only":
                        d1 = d1.drop_duplicates(subset=[sel1], keep="first")
                        d2 = d2.drop_duplicates(subset=[sel2], keep="first")
                        merged = pd.merge(d1, d2, left_on=sel1, right_on=sel2,
                                          how=merge_type, suffixes=("_File1", "_File2"))
                    elif dup_mode == "One-to-One (Sequential Match)":
                        d1["_seq_id"] = d1.groupby(sel1).cumcount()
                        d2["_seq_id"] = d2.groupby(sel2).cumcount()
                        merged = pd.merge(d1, d2,
                                          left_on=[sel1, "_seq_id"],
                                          right_on=[sel2, "_seq_id"],
                                          how=merge_type, suffixes=("_File1", "_File2"))
                        merged = merged.drop(columns=["_seq_id"])
                    else:
                        merged = pd.merge(d1, d2, left_on=sel1, right_on=sel2,
                                          how=merge_type, suffixes=("_File1", "_File2"))

                    merged = merged.fillna("")

                    # File 1 cols LEFT, File 2 cols RIGHT
                    f1_cols = [c for c in merged.columns if c in df1.columns or c.endswith("_File1")]
                    f2_cols = [c for c in merged.columns if c not in f1_cols]
                    merged  = merged[f1_cols + f2_cols]

                    st.session_state.merged_df = merged
                except Exception as e:
                    prog_ph.error(f"Merge failed: {e}")
                    st.stop()

                prog_ph.empty()

        # ─────────────────────────────────────────────────────────────────
        # STEP 4 — Preview & Download
        # ─────────────────────────────────────────────────────────────────
        if st.session_state.merged_df is not None:
            merged = st.session_state.merged_df
            st.markdown('<div class="grad-div"></div>', unsafe_allow_html=True)

            _anchor = {"left": len(df1), "right": len(df2),
                       "inner": min(len(df1), len(df2)), "outer": None}[merge_type]
            _show_warn = (_anchor is not None) and (len(merged) > _anchor)

            if _show_warn:
                st.markdown(f"""
                <div style="background:#ffb34710;border:1px solid #ffb34740;border-radius:12px;
                  padding:1rem 1.2rem;margin-bottom:1rem;">
                  <div style="color:#ffb347;font-weight:700;font-size:.92rem;margin-bottom:.4rem;
                    display:flex;align-items:center;gap:.4rem;">
                    <i data-lucide="alert-triangle"></i> Row count inflated — Many-to-Many matches detected
                  </div>
                  <div style="color:#c9a66b;font-size:.82rem;line-height:1.65">
                    The merged result has <strong style="color:#ffcc80">{len(merged)}</strong> rows,
                    which is more than the target limit.<br>
                    <strong>Why?</strong> When a key value exists in multiple rows of both files,
                    pandas creates every combination — inflating row count.<br>
                    <strong>Fix:</strong> Set <em>"Duplicate handling strategy"</em> to
                    <strong>One-to-One (Sequential Match)</strong> or <strong>First Match Only</strong>.
                  </div>
                </div>""", unsafe_allow_html=True)
            elif merge_type == "outer" and len(merged) > max(len(df1), len(df2)):
                st.markdown(f"""
                <div style="background:#00d4ff10;border:1px solid #00d4ff40;border-radius:12px;
                  padding:1rem 1.2rem;margin-bottom:1rem;">
                  <div style="color:#00d4ff;font-weight:700;font-size:.92rem;margin-bottom:.4rem;
                    display:flex;align-items:center;gap:.4rem;">
                    <i data-lucide="info"></i> Outer Join — Row count explained
                  </div>
                  <div style="color:#9bc9d3;font-size:.82rem;line-height:1.65">
                    The merged result has <strong style="color:#ffffff">{len(merged)}</strong> rows.
                    An <strong>Outer Join</strong> keeps unmatched rows from both files, so the total can
                    exceed the larger source.<br>
                    <strong>Formula:</strong> Unique File 1 keys + Unique File 2 keys − Overlap.<br>
                    To keep only File 1 rows, switch the strategy to <strong>Left Join</strong>.
                  </div>
                </div>""", unsafe_allow_html=True)

            # Stats
            key_col = sel1 if merge_type != "right" else sel2
            matched = int((merged[key_col] != "").sum()) if sel1 and sel2 else 0
            sc1, sc2, sc3, sc4 = st.columns(4)
            for col, num, lbl in [
                (sc1, len(df1),    "File 1 rows"),
                (sc2, len(df2),    "File 2 rows"),
                (sc3, len(merged), "Merged rows"),
                (sc4, matched,     "Non-blank key rows"),
            ]:
                with col:
                    st.markdown(f'<div class="stat"><div class="stat-n">{num}</div>'
                                f'<div class="stat-l">{lbl}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="card-title"><i data-lucide="eye"></i> Merged Preview (first 100 rows)</div>',
                        unsafe_allow_html=True)

            sk2 = st.empty()
            sk2.markdown(skeleton(5), unsafe_allow_html=True)
            time.sleep(0.4)
            sk2.empty()

            st.dataframe(merged.head(100), use_container_width=True, height=400)

            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as w:
                merged.to_excel(w, index=False, sheet_name="Merged")
            buf.seek(0)

            st.markdown("<br>", unsafe_allow_html=True)
            _, dc, _ = st.columns([1, 2, 1])
            with dc:
                st.download_button(
                    label="⬇  Download Merged Excel",
                    data=buf,
                    file_name="merged_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:4rem;padding-top:2rem;
  border-top:1px solid var(--border);color:var(--muted);font-size:.8rem">
  Built with ❤️ using Streamlit &nbsp;·&nbsp; <strong>SheetFusion</strong>
</div>

<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<script>
  function initLucide() {
    if (window.lucide) { window.lucide.createIcons(); }
    else { setTimeout(initLucide, 150); }
  }
  document.addEventListener('DOMContentLoaded', initLucide);
  setTimeout(initLucide, 200);

  // Re-init after Streamlit re-renders
  const obs = new MutationObserver(() => { if (window.lucide) window.lucide.createIcons(); });
  obs.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)
