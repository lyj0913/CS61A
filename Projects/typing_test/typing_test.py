
""" Typing Test implementation """

from utils import *
from ucb import main

# BEGIN Q1-5
"*** YOUR CODE HERE ***"
path = open("data/sample_paragraphs.txt",mode='r')

def process_line(line):
    """
    Process a line of text, remove front/end spaces and "\n"
    :param line -> [str] a line of text
    :return line -> [str] processed line of text
    """
    line = line.strip()
    line = "".join(line.split("\n"))
    return line

def lines_from_file(path):
    file = open(path, mode='r')
    lines = file.readlines()
    result = []
    for line in lines:
        result.append(process_line(line))
    return result

def new_sample(path, i):
    file = open(path, mode='r')
    line = file.readlines()[i]
    return process_line(line)

#Q2
def analyze(sample_paragraphs, typed_string, start_time, end_time):
    #number of words:len(typed_string)-text.count(" ")/5
    #words per minute= number of words/(endtime-start_time)/60
    noofcharacter = len(typed_string)#-typed_string.count(" ")
    noofwords = noofcharacter/5
    wordspermin = noofwords / ((end_time-start_time) / 60)

    accuracy = None
    if len(typed_string.strip()) == 0:
        accuracy = 0.0
    else:
        valid_length = min(len(typed_string.split()), len(sample_paragraphs.split()))
        ground_truth = sample_paragraphs.split()[:valid_length]
        typed_truth = typed_string.split()[:valid_length]
        count = 0
        for i, true_word in enumerate(ground_truth):
            if true_word == typed_truth[i]:
                count += 1
        accuracy = float(count / valid_length)
    return [wordspermin, accuracy * 100]


def q3_helper(word):
    vowels = ["a", "e", "i", "o", "u"]
    selected = []
    if word[0] not in vowels:
        for w in word:
            if w not in vowels:
                selected.append(w)
            else:
                break
        selected = "".join(selected)
        word = word[len(selected):]
        word = word + selected + "ay"
        return word
    else:
        return word + "way"

def pig_latin(paragraph):
    vowels = ["a", "e", "i", "o", "u"]
    words = paragraph.split()

    result = []
    for word in words:
        result.append(q3_helper(word))
    return " ".join(result)

def autocorrect(user_input,words_list,score_function):
    if user_input in words_list:
        return user_input
    else:
        a=[score_function(user_input,i) for i in words_list]
        return words_list[a.index(min(a))]

def swap_score(user_input,words_list):
    count=0
    if len(user_input)<=len(words_list):
        for i in range(len(user_input)):
            if user_input[i]!=words_list[i]:
                count+=1
    if len(user_input)>len(words_list):
        for i in range(len(words_list)):
            if user_input[i]!=words_list[i]:
                count+=1
    return count

# END Q1-5

# Question 6

# BEGIN Q6
"*** YOUR CODE HERE ***"
def score_function(word1, word2):
    """A score_function that computes the edit distance between word1 and word2.
    """
    if word1==word2:
        return 0 # Fill in the condition
    elif word1=="" or word2=="":
        return max(len(word1),len(word2))
    
    elif word1[0]==word2[0]:
        return score_function(word1[1:],word2[1:])

    else:
        add_char = 1+score_function(word2[0]+word1,word2)
        remove_char =1+score_function(word1[1:],word2)
        substitute_char =1+score_function(word1[1:],word2[1:])

        return min(add_char,remove_char,substitute_char)

# END Q6

KEY_DISTANCES = get_key_distances()

# BEGIN Q7-8
def score_function_accurate(word1, word2):
    if word1==word2:
        return 0
    elif word1=="" or word2=="":
        return max(len(word1),len(word2))
    
    elif word1[0]==word2[0]:
        return score_function_accurate(word1[1:],word2[1:])

    else:
        add_char = 1 + score_function_accurate(word2[0]+word1,word2)
        remove_char = KEY_DISTANCES[word1[0],word2[0]] + score_function_accurate(word1[1:],word2)
        substitute_char = KEY_DISTANCES[word1[0],word2[0]] + score_function_accurate(word1[1:],word2[1:])

        return min(add_char,remove_char,substitute_char)



"*** YOUR CODE HERE ***"

d = {}

def score_function_final(word1, word2):
    global d
    if (word1, word2) in d:
    	return d[(word1,word2)]
    elif word1 == word2:
        return 0
    elif word1=="" or word2=="":
        return max(len(word1),len(word2))
    
    elif word1[0]==word2[0]:
        return score_function_final(word1[1:],word2[1:])

    else:
        add_char = 1 + score_function_final(word2[0]+word1,word2)
        remove_char = KEY_DISTANCES[word1[0],word2[0]] + score_function_final(word1[1:],word2)
        substitute_char = KEY_DISTANCES[word1[0],word2[0]] + score_function_final(word1[1:],word2[1:])

    p = min(add_char,remove_char,substitute_char)
    d.update({(word1, word2): p})
    return p
        
# END Q7-8
