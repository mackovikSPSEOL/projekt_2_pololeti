import customtkinter as ctk
import random
import os, time, asyncio
import matplotlib.pyplot as plt

session_score = 0
total_score = 0 
correct = 0
incorrect = 0

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
        global global_difficulty
        global get_vocabulary
        global_difficulty = difficulty
        selected_difficulty = difficulty
        get_vocabulary = self.load_vocabulary(f"assets\{selected_difficulty}.txt")
        # print(list(get_vocabulary.keys()))
        gameplay_window()
        
        # print(get_vocabulary) # debug
    

# creating window - selecting word from chosen difficulty


def gameplay_window():
        
        
        global chosen_word
        global translated_word
        gameplay_window = ctk.CTk()
        gameplay_window.title(f"Obtížnost - {global_difficulty}")
        gameplay_window.geometry("500x450")


        locked = False

        title_label = ctk.CTkLabel(gameplay_window, text="Slovo:", font=("Arial", 32))
        title_label.pack(pady=20)

        list_chosen_word, list_chosen_word_translated = list(get_vocabulary.keys()), list(get_vocabulary.values())
        # print(f"{list_chosen_word}\n{list_chosen_word_translated}") # debug

        random_number = random.randint(0, (len(list_chosen_word) - 1))

        chosen_word = list_chosen_word[random_number]
        translated_word = list_chosen_word_translated[random_number]

        # chosen_word = list_chosen_word[random.randint(0, int((len(list(get_vocabulary.keys() - 1)))))] #totalni nesmysl

                #comparing input with translation
        def check_translation(event=None):
            nonlocal locked
            global incorrect, correct, session_score, total_score
            if locked:
                return  # ignore spam

            locked = True  # 🔒 lock input

            get_translation = input_window.get()

            if get_translation.lower() == translated_word.lower():
                result_label.configure(text="Správně!", text_color="green")
                session_score += 1
                correct += 1
            else:
                result_label.configure(text=f"Nesprávně! Správný překlad je: {translated_word}",text_color="red")
                session_score -= 1
                incorrect += 1

            input_window.delete(0, "end")

            gameplay_window.after(2000, generate_next_word)
            
       





            # print(f"{chosen_word}\n{translated_word}")
            # user_input = input_window.get()
            # if user_input.lower() == translated_word.lower():
            #     result_label.config(text="Správně!", text_color="green")
            # else:
            #     result_label.config(text=f"Nesprávně! Správný překlad je: {translated_word}", text_color="red")


        current_word_label = ctk.CTkLabel(gameplay_window, text=f"{chosen_word}", font=("Arial", 32))
        current_word_label.pack(pady=40)

        input_window = ctk.CTkEntry(gameplay_window, font=("Arial", 16))
        input_window.pack(pady=20)
        input_window.bind("<Return>", check_translation)
        input_window.focus()

        result_label = ctk.CTkLabel(gameplay_window, text="", font=("Arial", 16))
        result_label.pack(pady=10)
        

        confirm_button = ctk.CTkButton(gameplay_window, text="Ověřit", command=check_translation, fg_color="blue", text_color="white")
        confirm_button.pack(pady=10)


        def generate_next_word():
            global chosen_word
            global translated_word
            nonlocal locked

            result_label.configure(text="")
            input_window.delete(0, "end")
            list_chosen_word, list_chosen_word_translated = list(get_vocabulary.keys()), list(get_vocabulary.values())
            

            random_number = random.randint(0, (len(list_chosen_word) - 1))
            while chosen_word == list_chosen_word[random_number]:  # prevent same word twice in a row
                random_number = random.randint(0, (len(list_chosen_word) - 1))
                if chosen_word != list_chosen_word[random_number]:
                    break
                

            chosen_word = list_chosen_word[random_number]
            translated_word = list_chosen_word_translated[random_number]
            print(f"{chosen_word}\n{translated_word}") # debug
            print("\n")
            print(f"Session score: {session_score}\nTotal score: {total_score}\nCorrect: {correct}\nIncorrect: {incorrect}") # debug
            result_label.configure(text="")

            current_word_label.configure(text=f"{chosen_word}")
            locked = False  # unlock input
        def on_close():
            print("zavřel si okno?")
 
            with open("score.txt", "w") as score_file:
                score_file.write(f"Session score: {session_score}\nTotal score: {total_score}\nCorrect: {correct}\nIncorrect: {incorrect}")
            gameplay_window.destroy()

        # Override the close button behavior
        gameplay_window.protocol("WM_DELETE_WINDOW", on_close)

        gameplay_window.mainloop()
        


    # def get_random_word(self, none):
    #     word = random.choice(get_vocabulary)
    #     print(word)

    #     get_random_word()






# --- Spuštění aplikace ---

if __name__ == "__main__":
    app = VocabularyGame()
    app.mainloop()
