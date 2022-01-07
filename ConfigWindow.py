import tkinter as tk

class ConfigWindow:
    """
    Classe qui définit une fenêtre de configuration pour le client, qui lui
    permet de choisir le nombre de films et le nombre de mots par script de
    film il veut voir affiché.

    À cause de la nature 100% Python du module networkx, impossible d'afficher
    des graphes à des centaines de sommets, c'est donc la solution que nous
    avons choisie pour mettre le moins à mal l'expérience utilisateur.
    """
    @property
    def movie_nb(self):
        # print("type de movie_nb :", type(self._movie_nb.get()))
        return self._movie_nb.get()

    @property
    def word_nb(self):
        # print("type de word_nb :", type(self._word_nb.get()))
        return self._word_nb.get()


    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Config window")

        # Frames
        self._labelframe = tk.LabelFrame(self._root, text="Configure the graphs to create")
        self._labelframe.pack(padx=10, ipadx=10)

        self._buttonframe = tk.Frame(self._root)
        self._buttonframe.pack(side=tk.BOTTOM, expand=True, fill=tk.X, anchor='s')


        self._topframe = tk.Frame(self._labelframe)
        self._topframe.pack(side=tk.TOP, expand=True, fill=tk.X)
        self._centerframe = tk.Frame(self._labelframe)
        self._centerframe.pack(side=tk.BOTTOM, expand=True, fill=tk.X)
        self._bottomframe = tk.Frame(self._labelframe)
        self._bottomframe.pack(side=tk.BOTTOM, expand=True, fill=tk.X, anchor='s')

        # Variables
        self._movie_nb = tk.IntVar()
        self._movie_nb.set(2)

        self._word_nb = tk.IntVar()
        self._word_nb.set(50)


        # Entrees de texte
        tk.Label(self._bottomframe, text="Number of movies:", width=15).pack(side=tk.LEFT)
        self._movie_nb_sb = tk.Spinbox(self._bottomframe, from_=1, to=2000, increment=1,
                                          width=18, textvariable=self._movie_nb)
        self._movie_nb_sb.pack(side=tk.RIGHT)

        tk.Label(self._centerframe, text="Words per movie:", width=15).pack(side=tk.LEFT)
        self._word_nb_entry = tk.Entry(self._centerframe, textvariable=self._word_nb)
        self._word_nb_entry.pack(side=tk.RIGHT)


        # Bouton pour creer le serveur
        self._ok_button = tk.Button(self._buttonframe, text="Ok", command=self._ok)
        self._ok_button.pack(side=tk.BOTTOM, expand=True, fill=tk.X, padx=1, pady=1)

        # Bindings

        # Pour gerer la touche Entree
        self._root.bind("<Return>", self._on_return_key)
        
        # Pour gerer la fermeture de la fenetre
        self._root.protocol("WM_DELETE_WINDOW", self._quit_config)
        
        self._root.mainloop()

    
   # Bindings
    def _ok(self, event=None):
        try:
            if self._movie_nb.get() > 0 and self._word_nb.get() > 0:
                print("[Success] Starting interface")

                self._root.destroy()
        except tk._tkinter.TclError:
            print("[Error] Wrong movie number or word number")

    def _on_return_key(self, event):
        self._ok_button.invoke()

    def _quit_config(self):
        exit(1)


if __name__ == '__main__':
    c = ConfigWndow()