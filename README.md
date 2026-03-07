## Hotel Ranking Case Study

Small Python project that ranks hotels from an Excel dataset and exports a formatted Excel result file. It asks for user preferences via a simple `tkinter` UI and then applies filters + weighted scoring.

### What it does
- Loads `Raw_Dataset_Ranking.xlsx`
- Collects preferences (room type, holiday type, beach distance, pool, pets, meal plan)
- Applies filters / weight adjustments
- Exports `Top_Hotels_Selection.xlsx` (Top 10 + remaining results on different page)

### Setup
Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
python main.py
```
