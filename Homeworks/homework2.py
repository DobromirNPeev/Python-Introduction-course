def plugboard(text, plugboard_position):
    new_text = ""
    for letter in text:
        for pair in plugboard_position:
            if letter in pair:
                new_text += [other_letter for other_letter in pair if other_letter is not letter][0]
                break
        else:
            new_text += letter
    return new_text

def rotor(text, rotor_position):
    new_text = ""
    for letter in text:
        new_text += rotor_position.get(letter," ")
    return new_text

def enigma_encrypt(plugboard_position, rotor_position):
    def encrypt_decorator(func):
        def encrypt_function(text):
            text = plugboard(text,plugboard_position)
            text = rotor(text,rotor_position)
            return func(text)
        return encrypt_function
    return encrypt_decorator

def enigma_decrypt(plugboard_position, rotor_position):
    def enigma_decrypt_decorator(func):
        def decrypt_function(text):
            new_rotor_position={}
            for letter in rotor_position:
                new_rotor_position[rotor_position[letter]] = letter
            text = rotor(text,new_rotor_position)
            text = plugboard(text,plugboard_position)
            func(text)
        return decrypt_function
    return enigma_decrypt_decorator
    