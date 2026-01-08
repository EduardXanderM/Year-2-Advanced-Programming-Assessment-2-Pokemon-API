import requests
from io import BytesIO
from PIL import Image, ImageTk
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
        "height": f"{data['height'] / 10} m",
        "weight": f"{data['weight'] / 10} kg",
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

    # Pokemon App Methods

    def load_pokemon_image(self, image_url):
        response = requests.get(image_url)
        image_data = response.content
        img = Image.open(BytesIO(image_data))
        img = img.resize((330, 330), Image.LANCZOS)

        self.pokemon_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.pokemon_img)
        self.image_label.image = self.pokemon_img

    def search_pokemon(self):
        pokemon_name = self.pokemon_input.get().strip()
        if not pokemon_name:
            messagebox.showwarning("Input Error", "Please enter a Pokémon name.")
            return
        pokemon = get_pokemon_data(pokemon_name)
        if not pokemon:
            messagebox.showerror("Not Found", "Pokémon not found.")
            return
        self.load_pokemon_image(pokemon["image_url"])

        pokemon = get_pokemon_data(pokemon_name)
        info_text = (
            f"Name: {pokemon['name']}\n"
            f"Pokédex #: {pokemon['pokedex_number']}\n"
            f"Height: {pokemon['height']}\n"
            f"Weight: {pokemon['weight']}\n\n"
            f"Types: {', '.join(pokemon['types'])}\n"
            f"Abilities: {', '.join(pokemon['abilities'])}"
        )
        stats_text = "\n".join(
            f"{stat}: {value}"
            for stat, value in pokemon["stats"].items()
        )

        full_text = info_text + "\n\nStats:\n" + stats_text
        self.data_label.config(text=full_text)

    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon API")
        self.root.geometry("800x560")
        self.root.minsize(width=670, height=550)
        self.root.maxsize(width=1050, height=700)

        self.root.columnconfigure(0, weight=9)
        self.root.columnconfigure(1, weight=1)

        self.root.rowconfigure(0, weight=1)

        self.left = tk.Frame(self.root, bg="#E02A2A")
        self.left.grid(row=0, column=0, sticky="nsew")

        self.right = tk.Frame(self.root, bg="#E02A2A")
        self.right.grid(row=0, column=1, sticky="nsew")

        # Left Column Content

        self.title = tk.Label(self.left, text="Pokemon API", bg="#E02A2A", fg="white", font=("Helvetica", 22, "bold")).pack(pady=30)

        self.label = tk.Label(self.left, text="Enter your Pokemon name:", bg="#E02A2A", fg="white", font=("Helvetica", 13, "bold")).pack()

        self.pokemon_input = tk.Entry(self.left, width=24, border=None, font=("Helvetica", 13))
        self.pokemon_input.pack(pady=20)

        self.search_button = tk.Button(self.left, text="Search", bg="#D9CD31", fg="white", font=("Helvetica", 13, "bold"), activeforeground="black", command=self.search_pokemon)
        self.search_button.pack()

        self.image_frame = tk.Frame(self.left, bg="white", width=400, height=500)
        self.image_frame.pack(anchor="s", pady=30, padx=20)

        self.image_label = tk.Label(self.image_frame, bg="#E02A2A")
        self.image_label.grid(row=0, column=0)

        # Right Column Content

        self.white_frame = tk.Frame(self.right, bg="white", width=50, height=50)
        self.white_frame.pack(anchor="w", padx=20, pady=20)
        
        self.data_label = tk.Label(self.white_frame, bg="white", font=("Helvetica", 14), width=35, height=16, anchor="n", justify="center")
        self.data_label.grid(row=0, column=1, pady=30)

# Running the App

root = tk.Tk()
app = PokemonApp(root)
root.mainloop()