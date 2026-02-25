import customtkinter as ctk
import random
import os

# Nastavení vzhledu (volitelné)
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class VocabularyGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Konfigurace okna ---
        self.title("Slovíčka Hrou")
        self.geometry("400x350")
        
        # Data
        self.vocabulary = {}
        self.current_word = None
        
        # Načtení slovíček
        self.load_vocabulary("A1.txt")

        # --- UI Prvky (Layout) ---
        
        # Nadpis / Skóre (volitelné)
        self.label_title = ctk.CTkLabel(self, text="Přelož do češtiny:", font=("Arial", 16))
        self.label_title.pack(pady=(20, 10))

        # Anglické slovo (Otázka)
        self.label_question = ctk.CTkLabel(self, text="...", font=("Arial", 28, "bold"))
        self.label_question.pack(pady=10)

        # Vstupní pole
        self.entry_answer = ctk.CTkEntry(self, placeholder_text="Napiš překlad...", width=250)
        self.entry_answer.pack(pady=10)
        # Nabindování klávesy Enter pro rychlé potvrzení
        self.entry_answer.bind("<Return>", self.check_answer)

        # Tlačítko Kontrola
        self.btn_check = ctk.CTkButton(self, text="Zkontrolovat", command=self.check_answer)
        self.btn_check.pack(pady=10)

        # Tlačítko Další (ze začátku skryté nebo neaktivní)
        self.btn_next = ctk.CTkButton(self, text="Další slovo", command=self.next_word, fg_color="gray")
        self.btn_next.pack(pady=10)
        self.btn_next.configure(state="disabled")

        # Zpětná vazba (Správně/Chyba)
        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.label_feedback.pack(pady=10)

        # Spuštění prvního slova
        self.next_word()

    def load_vocabulary(self, filename):
        """Načte slovíčka ze souboru 'slovo - preklad'."""
        if not os.path.exists(filename):
            self.vocabulary = {"Error": "Soubor nenalezen"}
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    if " - " in line:
                        # Rozdělíme na anglickou a českou část a odstraníme mezery/nové řádky
                        eng, cz = line.strip().split(" - ")
                        self.vocabulary[eng] = cz
        except Exception as e:
            print(f"Chyba při načítání: {e}")

    def next_word(self):
        """Vybere nové náhodné slovo a resetuje UI."""
        if not self.vocabulary:
            self.label_question.configure(text="Žádná data")
            return

        # Vyber náhodný klíč (anglické slovo)
        self.current_word = random.choice(list(self.vocabulary.keys()))
        
        # Aktualizace UI
        self.label_question.configure(text=self.current_word)
        self.entry_answer.delete(0, 'end') # Vymaže vstup
        self.label_feedback.configure(text="") # Vymaže feedback
        
        # Reset tlačítek
        self.btn_check.configure(state="normal", fg_color="#1f6aa5") # Modrá (default)
        self.btn_next.configure(state="disabled", fg_color="gray")
        
        # Focus do inputu, aby uživatel mohl hned psát
        self.entry_answer.focus()

    def check_answer(self, event=None):
        """Porovná vstup uživatele se správným překladem."""
        if not self.current_word:
            return

        user_input = self.entry_answer.get().strip().lower()
        correct_answer = self.vocabulary[self.current_word].lower()

        if user_input == correct_answer:
            self.label_feedback.configure(text="✅ Správně!", text_color="green")
            self.handle_post_answer(True)
        else:
            self.label_feedback.configure(
                text=f"❌ Chyba! Správně je: {self.vocabulary[self.current_word]}", 
                text_color="red"
            )
            self.handle_post_answer(False)

    def handle_post_answer(self, is_correct):
        """Přepne stavy tlačítek po odpovědi."""
        self.btn_check.configure(state="disabled", fg_color="gray")
        self.btn_next.configure(state="normal", fg_color="green" if is_correct else "#1f6aa5")
        self.btn_next.focus() # Přesune focus na tlačítko "Další" (Enter ho odpálí)
        self.btn_next.bind("<Return>", lambda e: self.next_word())

if __name__ == "__main__":
    app = VocabularyGame()
    app.mainloop()