import customtkinter as ctk
import random
import os








class VocabularyGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Slovíčka Hrou")
        self.geometry("400x400")


# main menu - choosing  difficulty
        
        self.label_title = ctk.CTkLabel(self, text="Slovíčka hrou!", font=("Arial", 32))
        self.label_title.pack(pady=(20, 10))

        self.label_choose_dif = ctk.CTkLabel(self, text="Vyber obtížnost:", font=("Arial", 16))
        self.label_choose_dif.pack(pady=(30, 10))

        self.btn_A1 = ctk.CTkButton(self, text="A1", command=lambda: self.start_game("A1"), fg_color="lightgreen", text_color="black")
        self.btn_A1.pack(pady=4)

        self.btn_A2 = ctk.CTkButton(self, text="A2", command=lambda: self.start_game("A2"), fg_color="green", text_color="black")
        self.btn_A2.pack(pady=4)

        self.btn_B1 = ctk.CTkButton(self, text="B1", command=lambda: self.start_game("B1"), fg_color="#F8CD5F", text_color="black")
        self.btn_B1.pack(pady=4)

        self.btn_B2 = ctk.CTkButton(self, text="B2", command=lambda: self.start_game("B2"), fg_color="yellow", text_color="black")
        self.btn_B2.pack(pady=4)

        self.btn_C1 = ctk.CTkButton(self, text="C1", command=lambda: self.start_game("C1"), fg_color="#E0777D", text_color="black")
        self.btn_C1.pack(pady=4)

        self.btn_C2 = ctk.CTkButton(self, text="C2", command=lambda: self.start_game("C2"), fg_color="red", text_color="black")
        self.btn_C2.pack(pady=4)

    def load_vocabulary(self, filename):
        if not os.path.exists(filename):
            return {"Error": "Soubor nenalezen"}
        vocabulary = {}
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if " - " in line:
                    word, translation = line.strip().split(" - ", 1)
                    vocabulary[word] = translation
        return vocabulary

    def start_game(self, difficulty):
        selected_difficulty = difficulty
        get_vocabulary = self.load_vocabulary(f"assets\{selected_difficulty}.txt")
        print(get_vocabulary)


        






# --- Spuštění aplikace ---

if __name__ == "__main__":
    app = VocabularyGame()
    app.mainloop()
