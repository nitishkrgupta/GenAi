import emoji
import string
import contractions
from textblob import TextBlob

class TextNormalization:
    def __init__(self, data):
        self.data = data
        self.start()
    
    def start(self):
        print("Normalization started")
        print('''1. converting the lower case
              2. removing punctuations
              3. removing spl char
              4. handling emojies
              5. contractions(expanding and abbreviatons of words)
              6. removing extra space
              7. correcting the words''')
        self.lowercase()
    def lowercase(self):
        self.data = self.data.lower()
        print("Data converted to lowercase")
        print(self.data)
        self.expand_words()
    
    def expand_words(self):
        self.data = contractions.fix(self.data)
        print("All words expanded and abbreviations Done")
        print(self.data)
        self.handling_emojis()
    
    def handling_emojis(self):
        emoji_data = self.data
        print(emoji_data)
        emoji_option = int(input("Enter options:- \n1 to remove emoji, 2 for demojize and 0 to skip : "))
        if emoji_option == 1:
            self.data = emoji.replace_emoji(emoji_data, "")
            print("Emojies removed from data")
            print(self.data)
            self.remove_punctuations()
        elif emoji_option == 2:
            self.data = emoji.demojize(emoji_data)
            print("Demojize the data")
            print(self.data)
            self.remove_punctuations()
        else:
            self.remove_punctuations()

    def remove_punctuations(self):
        chars = self.data
        punctuation_option = int(input("Enter options for punctuations \n1 for remove and 0 to skip : "))
        if punctuation_option == 1:
            for char in string.punctuation:
                chars = chars.replace(char, "")
            self.data = chars
            print("Punctuations removed from data")
            print(self.data)
            self.removing_spl_char()
        else:
            self.removing_spl_char()
    
    def removing_spl_char(self):
        chars = self.data
        spl_char_option = int(input("Enter spl_char option : \n1 to remove spl chars and 0 to skip : "))
        if spl_char_option == 1:
            for char in chars:
                if not char.isalnum() and not ord(char) == 32:
                    chars = chars.replace(char, "")
            self.data = chars
            print("Special character removed")
            print(self.data)
            self.remove_extra_space()
        else:
            self.remove_extra_space()

    def remove_extra_space(self):
        words = self.data.split()
        self.data = " ".join(words)
        print("Extra spaces removed from data")
        print(self.data)
        self.correcting_words()

    def correcting_words(self):
        self.data = TextBlob(self.data).correct()
        print("Corrected the incorrect words")
        print(self.data)
        print("Text normalization Done")

obj = TextNormalization("I'll Havv t0 corret& 👌the    wods! for😂   txt    Normalization")