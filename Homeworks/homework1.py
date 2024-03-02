def beginning(word):
    word_length = len(word)
    if word_length%3 == 0 or word_length%3 == 1:
         offset = word_length//3
         return word[0:offset]
    elif word_length%3 == 2:
        offset = word_length//3+1
        return word[0:offset]
    
def middle(word):
    word_length = len(word)
    if word_length%3 == 0:
         offset = word_length//3
         return word[offset:offset+offset]
    elif word_length%3 == 2:
        offset = word_length//3
        return word[offset+1:offset+offset+1]
    else:
        offset = word_length//3
        return word[offset:offset+offset+1]
    
def end(word):
    word_length = len(word)
    if word_length%3 == 0:
         offset = word_length//3
         return ''.join(reversed(word[word_length:offset+offset-1:-1]))
    elif word_length%3== 2 or word_length%3==1:
        offset=word_length//3
        return ''.join(reversed(word[word_length:offset+offset:-1]))
    
def split_sentence(sentence):
    split_in_words = sentence.split()
    list_of_tuples = []
    for word in split_in_words:
        list_of_tuples.append((beginning(word),middle(word),end(word)))
    return list_of_tuples
