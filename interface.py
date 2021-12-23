import tkinter as tk
from Movie import Movie
from 


# Récupération des données sur le site de scénarios

# ...

### pour le test ###
data = {
    "John Carter": "http://example.com",
    "Collateral Damage": "http://example.com"
}

# Conversion en objets Movie
movies = []
for title in data:
    # Récupération du script sur la page html
    ### pour le test ###
    script = "Mathieu: I think Thomas stole my donut\nThomas: No it's Tiphaine I saw her!"

    # Communication avec l'API The Movie DataBase pour connaître les genres du film
    # TODO : importer le module "fini" après l'avoir renommé et faire ce qu'il faut



root = tk.Tk()

nb_panneaux = 1

panneaux = [tk.Canvas(root, bg="grey") for _ in range(nb_panneaux)]

for panneau in panneaux:
    panneau.pack(side=tk.LEFT)

liste_genres = 

root.mainloop()