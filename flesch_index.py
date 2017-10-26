import re
def flesch_index(user_input):
    flesch_score = 206.835 - 1.015*(count_words(user_input)/count_sentences(user_input)) - 84.6*(count_syllables(user_input)/count_words(user_input))
    return flesch_score

def count_words(user_input):
    words = re.findall(r'\w+', user_input)
    return len(words)

def count_sentences(user_input):
    # finds all punctuation marks (".","?","!") that have a space immediately following the punctuation.
    sentences_space = re.findall(r'[.?!]\s', user_input)
    
    #find the exception case where a quote mark is the last item and a punctuation mark is the second to last item
    sentences_quote = re.findall(r'[.?!][\'\"]', user_input)
    
    #finds the exception case where punctuation is the last item in the user_input
    extra_count = 0
    if user_input[-1] not in [".","?","!"]:
        extra_count+=1

    return len(sentences_space) + len(sentences_quote) + extra_count

def count_syllables(user_input):
    syllables = count_vowels(user_input) - count_diagraphs_diphthongs(user_input) - count_silent_e(user_input)
    return syllables

def count_vowels(user_input):
    vowels = ["a","e","i","o","u","y"]
    vowels = re.findall(r'[aeiouy]', user_input, re.I) 
    return len(vowels)

def count_diagraphs_diphthongs(user_input):
    count_dd = re.findall(r'(ai|ay|ee|ea|ie|ei|oo|ou|oe|ue|ey|oy|oi|au|oa)',user_input, re.I)
    return len(count_dd)

def count_silent_e(user_input):
    end_e = re.findall(r'[e]\b',user_input)
    
    # finds the exception 'le' exception
    exception_le = re.findall(r'(le)\b', user_input)
    
    # finds the exception 'ed' exception
    exception_ed = re.findall(r'(ed)\b', user_input)    
    
    # finds the exception where 'ee' is the last two letters of a word (i.e. "see")
    exception_ee = re.findall(r'(ee)\b', user_input)

    
    return len(end_e) - len(exception_le) - len(exception_ed) - len(exception_ee)
