
import tkinter as tk

BG = "#FFFFFF"
LABEL_FONT = ("Helvetica", 17)
LABEL_COLOR = "#2C3E50"

def run_ui():
    result = {"room_type": None, "holiday_type": None}

    def save_var():
        result["room_type"] = room_type_var.get()
        result["holiday_type"] = holiday_type_var.get()
        window.destroy()

        # you can still print here if you like
        print("Room Type:", result["room_type"])
        print("Holiday Type:", result["holiday_type"])

    

    window = tk.Tk()
    window.title("Your Preferences")
    window.config( bg=BG, padx= "20", pady= "20")
    window.geometry("400x200")

    # Room Type
    room_type_label = tk.Label(
        window,
        text="Holiday Type:",
        font=LABEL_FONT,
        fg=LABEL_COLOR,
        bg=BG
    )
    room_type_label.grid(row=1, column=0, pady=10, sticky="w")

    room_type_var = tk.StringVar(value="No Preference")
    room_type_dropdown = tk.OptionMenu(
        window,
        room_type_var,
        "No Preference",
        "Standard Room",
        "Deluxe Room",
        "Superior Room",
        "Suite"
    )

    room_type_dropdown.config(width=20, font=("Helvetica", 15))
    room_type_dropdown.grid(row=2, column=1, columnspan=2, sticky="w")


    # Holiday Type
    holiday_type_label = tk.Label(
        window,
        text="Room Type:",
        font=LABEL_FONT,
        fg=LABEL_COLOR,
        bg=BG
    )
    holiday_type_label.grid(row=2, column=0, pady=10, sticky="w")

    holiday_type_var = tk.StringVar(value="No Preference")
    holiday_type_dropdown = tk.OptionMenu(
        window,
        holiday_type_var,
        "No Preference",
        "Beach Holiday",
        "City Sightseeing",
        "Nature & Mountains"
    )
    holiday_type_dropdown.config(width=20, font=("Helvetica", 15))
    holiday_type_dropdown.grid(row=1, column=1, columnspan=2, sticky="w")



    # Button
    button = tk.Button(
        window,
        text="Next",
        command=save_var
    )
    button.grid(row=4, column=1, columnspan=2, pady=10)



    window.mainloop()

    return result["room_type"], result["holiday_type"]












    