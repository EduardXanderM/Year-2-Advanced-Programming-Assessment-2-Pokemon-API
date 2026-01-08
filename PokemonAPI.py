import requests
import tkinter as tk
from tkinter import messagebox

#Back-End Code

def get_pokemon_data(pokemon_name): # Function for fetching data
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    data = response.json()

    # Compiles Stats into the Dictionary for easy access
    stats = { 
        stat["stat"]["name"]: stat["base_stat"]
        for stat in data["stats"]
    }

    # General Pokemon Info as a Dictionary
    pokemon_info = {
        "name": data["name"].capitalize(),
        "pokedex_number": data["id"],
        "height": f"{data["height"] / 10} m",
        "weight": f"{data["weight"] / 10} kg",
        "types": [t["type"]["name"].capitalize() for t in data["types"]],
        "abilities": [a["ability"]["name"].replace("-", " ").title() for a in data["abilities"]],
        "image_url": data["sprites"]["other"]["official-artwork"]["front_default"],
        "stats": {
            "HP": stats.get("hp"),
            "Attack": stats.get("attack"),
            "Defense": stats.get("defense"),
            "Special Attack": stats.get("special-attack"), 
            "Special Defense": stats.get("special-defense"),   
            "Speed": stats.get("speed"),
        }
    }

    return pokemon_info

#Front-End (GUI)

class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon API")
        self.root.geometry("900x600")
        self.root.minsize(width=800, height=550)
        self.root.maxsize(width=1150, height=700)

        root.columnconfigure(0, weight=2)
        root.columnconfigure(1, weight=5)

        root.rowconfigure(0, weight=1)

        left = tk.Frame(root, bg="#E02A2A")
        left.grid(row=0, column=0, sticky="nsew")

        right = tk.Frame(root, bg="#E02A2A")
        right.grid(row=0, column=1, sticky="nsew")

        # Left Column Content

        title = tk.Label(left, text="Pokemon API", bg="#E02A2A", fg="white", font=("Helvetica", 22, "bold")).pack(pady=30)

        enter = tk.Label(left, text="Enter your Pokemon name:", bg="#E02A2A", fg="white", font=("Helvetica", 13, "bold")).pack()

        pokemon_input = tk.Entry(left, width=24, border=None, font=("Helvetica", 13)).pack(pady=20)

        search_button = tk.Button(left, text="Search", bg="#D9CD31", fg="white", font=("Helvetica", 13, "bold"), activeforeground="black").pack()

        image_frame = tk.Frame(left, bg="white", width=400, height=500).pack(anchor="s", pady=30, padx=20)

        # Right Column Content

        white_frame = tk.Frame(right, bg="white", width=700, height=700).pack(anchor="w", padx=20, pady=20)
        
        data = tk.Label(white_frame, text="?", bg="white", font=("Helvetica", 14)).grid(row=0, column=1)


# --- Run app ---
root = tk.Tk()
app = PokemonApp(root)
root.mainloop()