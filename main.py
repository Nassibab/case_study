from first_frontend import run_ui
from second_frontend import run_ui as run_second_frontend
import pandas as pd


def renormalize(weights: dict) -> dict:
    total = sum(weights.values())
    return {k: round(v / total, 6) for k, v in weights.items()}


def apply_room_type_modifier(df: pd.DataFrame, weights: dict, room_type: str):
    filtered = df[df["Zimmerkategorie"] == room_type]

    if room_type == "Suite":
        price_reduction = 0.70
        weights["Preis_pro_Nacht_EUR_weight"]     -= price_reduction
        weights["Kundenbewertung_(1-5)_weight"]   += price_reduction * 0.40
        weights["Anzahl_Sterne_weight"]            += price_reduction * 0.35
        weights["Stornierungsbedingungen_weight"]  += price_reduction * 0.25

    elif room_type == "Standard":
        star_reduction = 0.05
        weights["Anzahl_Sterne_weight"]       -= star_reduction
        weights["Preis_pro_Nacht_EUR_weight"] += star_reduction

    return filtered, renormalize(weights)


FALLBACK_CHAINS = {
    "Strandnähe":                ["Strandnähe", "Küstennähe", "Dorf", "Innenstadt Palma", "Berge/Serra de Tramuntana"],
    "Küstennähe":                ["Küstennähe", "Strandnähe", "Dorf", "Innenstadt Palma", "Berge/Serra de Tramuntana"],
    "Dorf":                      ["Dorf", "Innenstadt Palma", "Küstennähe", "Strandnähe", "Berge/Serra de Tramuntana"],
    "Innenstadt Palma":          ["Innenstadt Palma", "Dorf", "Küstennähe", "Strandnähe", "Berge/Serra de Tramuntana"],
    "Berge/Serra de Tramuntana": ["Berge/Serra de Tramuntana", "Dorf", "Küstennähe", "Innenstadt Palma", "Strandnähe"],
}

def apply_location_filter(df: pd.DataFrame, preferred_lage: str, min_results: int = 10):
    chain = FALLBACK_CHAINS.get(preferred_lage, [preferred_lage])
    included = []

    for lage in chain:
        included.append(lage)
        filtered = df[df["Lage"].isin(included)]
        if len(filtered) >= min_results:
            break

    if len(filtered) < min_results:
        print(f"  Warning: only {len(filtered)} results found even after full fallback chain.")

    print(f"  Location filter: using {included} → {len(filtered)} hotels")
    return filtered.copy()


def apply_beach_modifier(df: pd.DataFrame, weights: dict, max_km: float = 2.5):
    filtered = df[df["Entfernung_zum_Strand_km"] <= max_km].copy()

    original = weights["Entfernung_zum_Strand_km_weight"]
    boost = original * 3
    extra = boost - original

    other_keys = [k for k in weights if k != "Entfernung_zum_Strand_km_weight"]
    other_total = sum(weights[k] for k in other_keys)

    for k in other_keys:
        weights[k] -= extra * (weights[k] / other_total)

    weights["Entfernung_zum_Strand_km_weight"] = boost
    print(f"  Beach filter: {len(filtered)} hotels within {max_km}km")
    return filtered, renormalize(weights)


def apply_pet_modifier(df: pd.DataFrame, weights: dict, pet_friendly: bool):
    if pet_friendly:
        filtered = df[df["Haustierfreundlich"] == "Ja"].copy()
        print(f"  Pet filter: {len(filtered)} pet-friendly hotels")
    else:
        filtered = df.copy()
        weights["Haustier_weight"] = 0.0
        weights = renormalize(weights)
        print("  Pet filter: weight zeroed out (no pets)")

    return filtered, weights


def apply_pool_modifier(df: pd.DataFrame, weights: dict, pool_required: bool):
    if pool_required:
        filtered = df[df["Pool_vorhanden"] == "Ja"].copy()
        print(f"  Pool filter: {len(filtered)} hotels with pool")
    else:
        filtered = df.copy()
        weights["Pool_weight"] = 0.0
        weights = renormalize(weights)
        print("  Pool filter: weight zeroed out (no pool required)")

    return filtered, weights


MEAL_ORDER = {"Keine": 0, "Frühstück": 1, "Halbpension": 2, "Vollpension": 3, "All Inclusive": 4}

def apply_meal_modifier(df: pd.DataFrame, weights: dict, meal_preference: str):
    if meal_preference == "Keine":
        return df.copy(), weights

    min_level = MEAL_ORDER.get(meal_preference, 0)
    filtered = df[df["Verpflegung"].map(MEAL_ORDER) >= min_level].copy()

    boost_amount = 0.10
    other_keys = [k for k in weights if k != "Verpflegung_weight"]
    other_total = sum(weights[k] for k in other_keys)

    for k in other_keys:
        weights[k] -= boost_amount * (weights[k] / other_total)

    weights["Verpflegung_weight"] += boost_amount
    print(f"  Meal filter: {len(filtered)} hotels with at least '{meal_preference}'")
    return filtered, renormalize(weights)


selected_room_type, selected_holiday_type = run_ui()

if selected_room_type != "Suite":
    selected_beach_distance, selected_pool, selected_pet_friendly, selected_meal_plan = run_second_frontend()
else:
    selected_beach_distance = "Yes"
    selected_pool = "Yes"
    selected_pet_friendly = "Yes"
    selected_meal_plan = "Half Board"


ROOM_TYPE_MAP = {
    "Standard Room": "Standard",
    "Deluxe Room":   "Deluxe",
    "Superior Room": "Superior",
    "Suite":         "Suite",
    "No Preference": None,
}

HOLIDAY_TYPE_MAP = {
    "Beach Holiday":       "Strandnähe",
    "City Sightseeing":    "Innenstadt Palma",
    "Nature & Mountains":  "Berge/Serra de Tramuntana",
    "No Preference":       None,
}

BEACH_DISTANCE_MAP = {
    "Yes":           True,
    "No":            False,
    "No Preference": None,
}

POOL_MAP = {
    "Yes":           True,
    "No":            False,
    "No Preference": None,
}

PET_FRIENDLY_MAP = {
    "Yes":           True,
    "No":            False,
    "No Preference": None,
}

MEAL_PLAN_MAP = {
    "None":           "Keine",
    "Breakfast":      "Frühstück",
    "Half Board":     "Halbpension",
    "Full Board":     "Vollpension",
    "All Inclusive":  "All Inclusive",
    "No Preference":  None,
}

room_type       = ROOM_TYPE_MAP[selected_room_type]
preferred_lage  = HOLIDAY_TYPE_MAP[selected_holiday_type]
beach_distance  = BEACH_DISTANCE_MAP[selected_beach_distance]
pool_required   = POOL_MAP[selected_pool]
pet_friendly    = PET_FRIENDLY_MAP[selected_pet_friendly]
meal_preference = MEAL_PLAN_MAP[selected_meal_plan]


df = pd.read_excel("/Library/Projects/LearnPython/Check24/Raw_Dataset_Ranking.xlsx")

df["Kundenbewertung_(1-5)"] = df["Kundenbewertung_(1-5)"].fillna(df["Kundenbewertung_(1-5)"].quantile(0.25))

df["Verpflegung_value"] = df["Verpflegung"].map({"Keine": 0, "Frühstück": 0.6, "Halbpension": 0.7, "Vollpension": 0.9, "All Inclusive": 1})
df["Lage_value"] = df["Lage"].map({"Berge/Serra de Tramuntana": 0.3, "Dorf": 0.2, "Innenstadt Palma": 0.5, "Küstennähe": 0.8, "Strandnähe": 1})
df["Pool_value"] = df["Pool_vorhanden"].map({"Ja": 0.3, "Nein": 0.0})
df["Haustier_value"] = df["Haustierfreundlich"].map({"Ja": 0.03, "Nein": 0.0})
df["Stornierungsbedingungen_value"] = df["Stornierungsbedingungen"].map({"Strikt": 0, "Teilweise": 0.5, "Flexibel": 1})
df["Zimmerkategorie_value"] = df["Zimmerkategorie"].map({"Standard": 0, "Deluxe": 0.5, "Superior": 0.7, "Suite": 0.9})

for col in ["Kundenbewertung_(1-5)", "Anzahl_Sterne", "Zimmerkategorie_value", "Stornierungsbedingungen_value", "Provisionshoehe_CHECK24_%"]:
    df[col + "_value"] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

for col in ["Preis_pro_Nacht_EUR", "Entfernung_zum_Strand_km", "CHECK24_Note"]:
    df[col + "_value"] = 1 - (df[col] - df[col].min()) / (df[col].max() - df[col].min())


weights = {
    "Provisionshoehe_CHECK24_%_weight":  0.30,
    "Preis_pro_Nacht_EUR_weight":        0.20,
    "Kundenbewertung_(1-5)_weight":      0.10,
    "CHECK24_Note_weight":               0.10,
    "Anzahl_Sterne_weight":              0.10,
    "Zimmerkategorie_weight":            0.05,
    "Lage_weight":                       0.05,
    "Entfernung_zum_Strand_km_weight":   0.03,
    "Verpflegung_weight":                0.04,
    "Pool_weight":                       0.01,
    "Haustier_weight":                   0.01,
    "Stornierungsbedingungen_weight":    0.01,
}

print("\n=== Applying customer preference filters ===")

if room_type is not None:
    df, weights = apply_room_type_modifier(df, weights, room_type)
    print(f"  Room filter: {len(df)} hotels of type '{room_type}'")

if preferred_lage is not None:
    df = apply_location_filter(df, preferred_lage)

if beach_distance is True:
    df, weights = apply_beach_modifier(df, weights, max_km=2.5)

if pool_required is not None:
    df, weights = apply_pool_modifier(df, weights, pool_required)

if pet_friendly is not None:
    df, weights = apply_pet_modifier(df, weights, pet_friendly)

if meal_preference is not None:
    df, weights = apply_meal_modifier(df, weights, meal_preference)

print(f"\n  Hotels remaining after all filters: {len(df)}")


WEIGHT_TO_VALUE_COL = {
    "Provisionshoehe_CHECK24_%_weight":  "Provisionshoehe_CHECK24_%_value",
    "Preis_pro_Nacht_EUR_weight":        "Preis_pro_Nacht_EUR_value",
    "Kundenbewertung_(1-5)_weight":      "Kundenbewertung_(1-5)_value",
    "CHECK24_Note_weight":               "CHECK24_Note_value",
    "Anzahl_Sterne_weight":              "Anzahl_Sterne_value",
    "Zimmerkategorie_weight":            "Zimmerkategorie_value",
    "Lage_weight":                       "Lage_value",
    "Entfernung_zum_Strand_km_weight":   "Entfernung_zum_Strand_km_value",
    "Verpflegung_weight":                "Verpflegung_value",
    "Pool_weight":                       "Pool_value",
    "Haustier_weight":                   "Haustier_value",
    "Stornierungsbedingungen_weight":    "Stornierungsbedingungen_value",
}

df["final_score"] = sum(
    df[value_col] * weights[weight_key]
    for weight_key, value_col in WEIGHT_TO_VALUE_COL.items()
)

df_ranked = df.sort_values("final_score", ascending=False).reset_index(drop=True)
df_ranked["rank"] = df_ranked.index + 1

display_cols = [
    "rank", "name", "Preis_pro_Nacht_EUR", "Kundenbewertung_(1-5)",
    "Zimmerkategorie", "Lage", "Verpflegung", "Entfernung_zum_Strand_km",
    "Pool_vorhanden", "Haustierfreundlich", "Stornierungsbedingungen",
    "Anzahl_Sterne", "CHECK24_Note",
]
display_cols = [c for c in display_cols if c in df_ranked.columns]

df_display = df_ranked[display_cols].sort_values(by="rank")

df_display["Anzahl_Sterne"] = df_display["Anzahl_Sterne"].apply(lambda x: "⭐" * int(x) if pd.notnull(x) else "")
df_display["Haustierfreundlich"] = df_display["Haustierfreundlich"].map({"Ja": "🐶", "Nein": ""}).fillna("")
df_display["Pool_vorhanden"] = df_display["Pool_vorhanden"].map({"Ja": "🏊‍♂️", "Nein": ""}).fillna("")

df_display["Highlights"] = (
    df_display["Anzahl_Sterne"] + "  " +
    df_display["Pool_vorhanden"] + "  " +
    df_display["Haustierfreundlich"]
).str.strip()

df_display = df_display.drop(columns=["Anzahl_Sterne", "Pool_vorhanden", "Haustierfreundlich"])

df_top10 = df_display.head(10)
df_rest = df_display.iloc[10:]

file_path = "Top_Hotels_Selection.xlsx"

with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
    workbook = writer.book

    title_format    = workbook.add_format({"bold": True, "font_size": 14, "font_color": "white", "bg_color": "#4F81BD", "align": "center", "valign": "vcenter"})
    currency_format = workbook.add_format({"num_format": "#,##0.00 €", "valign": "vcenter", "align": "center"})
    center_format   = workbook.add_format({"valign": "vcenter", "align": "center"})
    emoji_format    = workbook.add_format({"valign": "vcenter", "align": "center", "font_size": 25})

    def create_formatted_sheet(df_subset, sheet_name, title_text):
        if df_subset.empty:
            return

        df_subset.to_excel(writer, sheet_name=sheet_name, startrow=2, header=False, index=False)
        worksheet = writer.sheets[sheet_name]

        max_col = len(df_subset.columns) - 1
        max_row = len(df_subset) + 1

        worksheet.merge_range(0, 0, 0, max_col, title_text, title_format)
        worksheet.set_row(0, 30)

        column_settings = []
        for col_name in df_subset.columns:
            col_dict = {"header": col_name}
            if col_name == "Preis_pro_Nacht_EUR":
                col_dict["format"] = currency_format
            elif col_name == "Highlights":
                col_dict["format"] = emoji_format
            else:
                col_dict["format"] = center_format
            column_settings.append(col_dict)

        worksheet.add_table(1, 0, max_row, max_col, {"columns": column_settings, "style": "Table Style Medium 9"})
        worksheet.set_column(0, max_col, 22)
        worksheet.set_column(df_subset.columns.get_loc("Highlights"), df_subset.columns.get_loc("Highlights"), 30)
        worksheet.freeze_panes(2, 0)
        worksheet.hide_gridlines(2)

        for row_num in range(2, max_row + 2):
            worksheet.set_row(row_num, 40)

    create_formatted_sheet(df_top10, "Top 10 Rankings", "🏆 Top 10 Hotel Rankings for you")
    create_formatted_sheet(df_rest, "Weitere Ergebnisse", "Weitere Ergebnisse (Ab Platz 11)")

print(f"Success! Data has been formatted and saved to {file_path}")
