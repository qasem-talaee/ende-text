import os

class Menu:
    
    def __init__(self):
        self.codec = [x for x in os.listdir('lib') if os.path.isdir(os.path.join('lib', x))]
        if '__pycache__' in self.codec : self.codec.remove('__pycache__')
        self.choose_codec()
    
    def generate_menu(self, input, back):
        if back:
            text = ""
            for i in range(len(input)):
                text += str(i + 1) + ". " + input[i] + "\n"
            text += str(len(input) + 1) + ". " + 'Back'
            return text
        else:
            text = ""
            for i in range(len(input)):
                text += str(i + 1) + ". " + input[i] + "\n"
            return text
    
    def choose_codec(self):
        text = self.generate_menu(self.codec, False)
        while True:
            try:
                user_input = int(input("Please select your codec : \n" + text + "\n"))
            except:
                print("Sorry, I didn't understand that.Please try again.")
            else:
                break
        self.choose_lang(self.codec[user_input - 1])
        
    def choose_lang(self, codec):
        langs = [x for x in os.listdir('lib/' + codec)]
        if '__init__.py' in langs : langs.remove('__init__.py')
        if '__pycache__' in langs : langs.remove('__pycache__')
        if '.gitignore' in langs : langs.remove('.gitignore')
        langs = list(map(lambda x : x.replace('.py', ''), langs))
        text = self.generate_menu(langs, True)
        while True:
            try:
                user_input_lang = int(input("Please select your language : \n" + text + "\n"))
            except:
                print("Sorry, I didn't understand that.Please try again.")
            else:
                break
        if user_input_lang - 1 == len(langs):
            self.choose_codec()
        else:
            self.translate(codec, langs[user_input_lang - 1])
        
    def translate(self, codec, lang):
        while True:
            input_file = input("Please enter your input text file path : \n")
            if os.path.exists(input_file):
               break
        out_file = input("Please enter your output text file path : \n")
        imported = getattr(__import__('lib.' + codec, fromlist=[lang]), lang)
        #
        user_input = int(input("What do you want to do? \n1. Encoding\n2. Decoding\n"))
        #
        space_words = imported.space_words
        space_chars = imported.space_chars
        codes = imported.codes
        result = ''
        if user_input == 1:
            with open(input_file, 'r') as f:
                for line in f:
                    words = line.split()
                    for word in words:
                        for char in word:
                            result += codes[char.upper()]
                            result += space_chars
                        result += space_words
                    result += codes['\n']
                    result += space_chars
                    result += space_words
            with open(out_file, 'w') as f:
                f.write(result)
                print('OK')
        elif user_input == 2:
            result = ''
            with open(input_file, 'r') as f:
                for line in f:
                    words = line.split(space_chars + space_words)
                    for word in words:
                        chars = word.split(space_chars)
                        for i, char in enumerate(chars):
                            for key, value in codes.items():
                                if value == char:
                                    result += key.lower()
                        if char != codes['\n']:
                            result += ' '
            with open(out_file, 'w') as f:
                f.write(result)
                print('OK')