---
title: SheetFusion Excel Merger
emoji: ⚡
colorFrom: indigo
colorTo: cyan
sdk: docker
app_port: 7860
pinned: false
license: mit
---

<div align="center">

<br/>

```
  ____  _               _   _____           _
 / ___|| |__   ___  ___| |_|  ___|   _ ___ (_) ___  _ __
 \___ \| '_ \ / _ \/ _ \ __| |_ | | | / __| |/ _ \| '_ \
  ___) | | | |  __/  __/ |_|  _|| |_| \__ \ | (_) | | | |
 |____/|_| |_|\___|\___|\__|_|   \__,_|___/_|\___/|_| |_|
```

### ⚡ Premium Excel & Spreadsheet Merger

**Upload · Configure · Merge · Download — beautifully fast.**

<br/>

[![Live Demo](https://img.shields.io/badge/🤗%20Hugging%20Face-Live%20Demo-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/vssksn/excel_sheet_merger)
&nbsp;
[![GitHub](https://img.shields.io/badge/GitHub-Source%20Code-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/1919-14/excel_sheet_merger)
&nbsp;
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
&nbsp;
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

<br/>

---

</div>

## 🌟 What is SheetFusion?

**SheetFusion** is a high-performance, beautifully designed web application for merging, reconciling, and combining Excel spreadsheets (`.xlsx`, `.xls`, `.xlsb`) — all in your browser, with zero code required.

Whether you're reconciling financial ledgers, combining audit sheets, matching transaction records, or simply joining two datasets by a common key — SheetFusion handles it all with precision and style.

<br/>

---

## ✨ Features at a Glance

| Feature | Description |
|---|---|
| 🎨 **Light & Dark Theme** | Toggle between polished dark and clean light modes |
| 📂 **Flexible File Import** | Upload two files, choose sheets, set custom header rows |
| 🔑 **Column Key Mapping** | Pick any column from each file as the join key |
| 🔗 **4 Merge Strategies** | Outer, Left, Right, Inner join support |
| ⚙️ **Duplicate Handling** | Sequential, First-Match, or Many-to-Many modes |
| 🔄 **Skeleton Loading** | Animated loading states for smooth UX |
| 🔎 **In-Browser Preview** | Preview first 100 rows before downloading |
| 💾 **Excel Export** | Download the merged result as a clean `.xlsx` file |
| 🏛️ **Column Order Control** | File 1 columns always appear left, File 2 columns right |

<br/>

---

## 🔗 Merge Strategies Explained

### 🔵 Outer Join *(recommended for reconciliation)*
Keeps **all rows** from both files. Unmatched rows from either file are appended with blank values for the other file's columns. The output size = unique keys from File 1 + unique keys from File 2 − overlap.

### ⬅️ Left Join
Keeps **all rows from File 1** and pulls in matching data from File 2. Rows in File 2 that have no match in File 1 are discarded.

### ➡️ Right Join
Keeps **all rows from File 2** and pulls in matching data from File 1. Rows in File 1 that have no match in File 2 are discarded.

### 🟢 Inner Join
Keeps **only matched rows** — rows where the key value exists in both files.

<br/>

---

## ⚙️ Duplicate Handling Modes

When the same key value (e.g. `5000.00`) appears in multiple rows in both files, how those duplicates get matched is critical:

### 🔢 One-to-One — Sequential Match *(default)*
Pairs duplicates in sequence: 1st occurrence ↔ 1st occurrence, 2nd ↔ 2nd, etc.
**Best for:** Transaction matching, ledger reconciliation, ordered datasets.
**Result:** Row count = max(File 1 rows, File 2 rows) — no inflation.

### ✂️ First Match Only
Deduplicates both files first, then merges on the first occurrence of each key value.
**Best for:** Lookup tables, reference data joins.
**Result:** Row count = unique key count.

### 🔀 Many-to-Many *(All combinations)*
Standard pandas merge: every row in File 1 matching a key is paired with every row in File 2 matching that key (cartesian product per key).
**Best for:** Analytical cross-joins, understanding full match space.
**Warning:** Can heavily inflate row count when duplicates exist.

<br/>

---

## 🛠️ Local Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/1919-14/excel_sheet_merger.git
cd excel_sheet_merger

# 2. Set up a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

<br/>

---

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t sheetfusion .

# Run locally on port 7860
docker run -p 7860:7860 sheetfusion
```

The included `Dockerfile`:
- Exposes port `7860` (Hugging Face Spaces standard)
- Disables CORS / Xsrf for embedded frame compatibility
- Runs under a non-root `appuser` (UID 1000) for security

<br/>

---

## 🚀 CI/CD — GitHub → Hugging Face Sync

Every push to `main` automatically triggers `.github/workflows/sync-to-hf.yml`, which pushes a clean snapshot of the codebase to the Hugging Face Space — no manual deployment needed.

```
Push to main
    │
    ▼
GitHub Actions workflow
    │
    ▼
git push → Hugging Face Space repo (HF_TOKEN secret)
    │
    ▼
Space rebuilds Docker image & goes live 🟢
```

<br/>

---

## 📁 Project Structure

```
excel_sheet_merger/
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container config for HF Spaces
├── .gitignore
├── README.md                     # This file
└── .github/
    └── workflows/
        └── sync-to-hf.yml        # Auto-sync to Hugging Face
```

<br/>

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `pandas` | Data manipulation & merge logic |
| `openpyxl` | Excel file reading & writing |
| `xlrd` | Legacy `.xls` support |
| `pyxlsb` | Binary `.xlsb` support |

<br/>

---

## 🔗 Links

| | |
|---|---|
| 🤗 **Live App** | https://huggingface.co/spaces/vssksn/excel_sheet_merger |
| 💻 **Source Code** | https://github.com/1919-14/excel_sheet_merger |

<br/>

---

<div align="center">

Built with ❤️ using **Streamlit** &nbsp;·&nbsp; **SheetFusion**

*Merge smarter. Download cleaner.*

</div>
