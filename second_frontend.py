import tkinter as tk

BG = "#FFFFFF"
LABEL_FONT = ("Helvetica", 17)
LABEL_COLOR = "#2C3E50"

def run_ui():
    result = {
        "beach_distance": None,
        "pool": None,
        "pet_friendly": None,
        "meal_plan": None,
    }

    def save_var():
        result["beach_distance"] = beach_distance_var.get()
        result["pool"] = pool_var.get()
        result["pet_friendly"] = pet_friendly_var.get()
        result["meal_plan"] = meal_plan_var.get()

        print("Walking Distance to Beach:", result["beach_distance"])
        print("Pool Available:", result["pool"])
        print("Pet Friendly:", result["pet_friendly"])
        print("Meal Plan:", result["meal_plan"])

        window.destroy()

    window = tk.Tk()
    window.config(bg=BG, padx=20, pady=20)
    window.geometry("500x270")
    window.title("Your Preferences")

    # Walking Distance to Beach
    beach_distance_label = tk.Label(window, text="Walking Distance to Beach:", font=LABEL_FONT, fg=LABEL_COLOR, bg=BG)
    beach_distance_label.grid(row=2, column=0, pady=10, sticky="w")

    beach_distance_var = tk.StringVar(value="No Preference")
    beach_distance_dropdown = tk.OptionMenu(
        window,
        beach_distance_var,
        "No Preference",
        "Yes",
        "No"
    )
    beach_distance_dropdown.config(width=20, font=("Helvetica", 15))
    beach_distance_dropdown.grid(row=2, column=1, sticky="w")

    # Pool Available
    pool_label = tk.Label(window, text="Pool Available:", font=LABEL_FONT, fg=LABEL_COLOR, bg=BG)
    pool_label.grid(row=3, column=0, pady=10, sticky="w")

    pool_var = tk.StringVar(value="No Preference")
    pool_dropdown = tk.OptionMenu(
        window,
        pool_var,
        "No Preference",
        "Yes",
        "No"
    )
    pool_dropdown.config(width=20, font=("Helvetica", 15))
    pool_dropdown.grid(row=3, column=1, sticky="w")

    # Pet Friendly
    pet_friendly_label = tk.Label(window, text="Pet Friendly:", font=LABEL_FONT, fg=LABEL_COLOR, bg=BG)
    pet_friendly_label.grid(row=4, column=0, pady=10, sticky="w")

    pet_friendly_var = tk.StringVar(value="No Preference")
    pet_friendly_dropdown = tk.OptionMenu(
        window,
        pet_friendly_var,
        "No Preference",
        "Yes",
        "No"
    )
    pet_friendly_dropdown.config(width=20, font=("Helvetica", 15))
    pet_friendly_dropdown.grid(row=4, column=1, sticky="w")

    # Meal Plan
    meal_plan_label = tk.Label(window, text="Meal Plan:", font=LABEL_FONT, fg=LABEL_COLOR, bg=BG)
    meal_plan_label.grid(row=5, column=0, pady=10, sticky="w")

    meal_plan_var = tk.StringVar(value="No Preference")
    meal_plan_dropdown = tk.OptionMenu(
        window,
        meal_plan_var,
        "No Preference",
        "None",
        "Breakfast",
        "Half Board",
        "Full Board",
        "All Inclusive"
    )
    meal_plan_dropdown.config(width=20, font=("Helvetica", 15))
    meal_plan_dropdown.grid(row=5, column=1, sticky="w")

    # Button
    button = tk.Button(window, text="Next", command=save_var, font=("Helvetica", 14))
    button.grid(row=6, column=0, columnspan=2, pady=20)

    window.mainloop()

    return (
        result["beach_distance"],
        result["pool"],
        result["pet_friendly"],
        result["meal_plan"],
    )