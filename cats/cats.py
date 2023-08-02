"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    valid_para = []
    for i in range(len(paragraphs)):
        if select(paragraphs[i]):
            valid_para.append(paragraphs[i])
    if k >= len(valid_para):
        return('')
    else:
        return valid_para[k]
    

# ps = ['short', 'really long', 'tiny']
# s = lambda p: len(p) <= 5
# choose(ps, s, 0)
        

    


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def select(paragraph):
        paragraph = remove_punctuation(paragraph)
        paragraph = lower(paragraph)
        paragraph = split(paragraph)
        for word in topic:
            if word in paragraph:
                return True
        return False  #不需要写else，直接写return就行
        # i = 0
        # while i < len(topic):
        #     if topic[i] in paragraph:
        #         return True
        #     i = i + 1
        # else:
        #     return False
    return select
    # END PROBLEM 2
# dogs = about(['dogs', 'hounds'])
# c = dogs('Release the Hounds!')


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if typed == '':
        return 0.0
    # if len (reference_words) == 1:
    #     if typed_words == reference_words:
    #         return 100.0
    #     else:
    #         return 0.0 
    else:
        correct = 0
        for i in range(len(typed_words)):
            if i > len(reference_words) - 1:
                return (correct / len(typed_words)) * 100
            if typed_words[i] == reference_words[i]:
                correct = correct + 1
        return (correct / len(typed_words)) * 100
    
#n = accuracy("a b c d", " a d ")
           



    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return (60 / elapsed) * (len(typed) / 5)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if user_word in valid_words:
        return user_word
    else:
        valid_num_list = []
        valid_more_num_list = []     
        for word in valid_words:
            valid_num_list.append(diff_function(user_word, word, limit))
        min_index = valid_num_list.index(min(valid_num_list))
        if valid_num_list.count(min(valid_num_list)) >= 2 and limit > min(valid_num_list):
            min_indexes = [i for i, x in enumerate(valid_num_list) if x == min(valid_num_list)]
            for element in min_indexes:
                valid_more_num_list.append(valid_words[element])
            return valid_more_num_list[0]
        else:
            if min(valid_num_list) <= limit:            
                return valid_words[min_index] 
            return user_word
    # END PROBLEM 5

# abs_diff = lambda w1, w2, limit: abs(len(w2) - len(w1))
# c = autocorrect("cul", ["culture", "cult", "cultivate"], abs_diff, 10)
# first_diff = lambda w1, w2, limit: 1 if w1[0] != w2[0] else 0
# p = autocorrect("wrod", ["word", "rod"], first_diff, 1) 
# words_list = sorted(lines_from_file('data/words.txt')[:10000])
# q = autocorrect("gesting", words_list, lambda w1, w2, limit: sum([w1[i] != w2[i] for i in range(min(len(w1), len(w2)))]) + abs(len(w1) - len(w2)), 10)
#p = autocorrect('hyalinization', ['ripe', 'spatuliform', 'serpent', 'truantship', 'epicrystalline', 'endosteitis', 'shark'], lambda x, y, lim: min(lim + 1, abs(len(x) - len(y))), 1)



def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if limit == -1:
        return limit + 1
    if start == goal == "":
        return 0
    if len(start) < len(goal):
        return len(goal) - len(start) + shifty_shifts(start, goal[ : len(start)], limit + len(start) - len(goal)) #range是elusive的，不包括len(start)
    if len(start) > len(goal):
        return len(start) - len(goal) + shifty_shifts(start[ : len(goal)], goal, limit + len(goal) - len(start))
    if start[0] == goal[0]:
        return 0 + shifty_shifts(start[1:], goal[1:], limit)
    else:
        return 1 + shifty_shifts(start[1:], goal[1:], limit - 1)
    
#x = shifty_shifts("awful", "awesome", 10)
#t = shifty_shifts("cats", "scat", 10)



    #END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    

    if start == goal and len(start) == len(goal) == 1 : # Fill in the condition
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 0
        # END

    elif start != goal and len(start) == len(goal) == 1:
        return 1

    elif len(start) != len(goal) and (len(goal) == 1 or len(goal) == 1): # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        if len(start) > len(goal) and goal in start:
            return 1
        if len(goal) > len(start) and start in goal:
            return 1
        else:
            return 2
        # END


    else:
        # add_diff = 1 + pawssible_patches(start, goal[ : len(goal) - 1], limit - 1) # Fill in these lines
        # remove_diff = 1 + pawssible_patches(start[ : len(start) - 1], goal, limit - 1)
        # substitute_diff = 1 + pawssible_patches(start[1 : ], goal[1 : ], limit - 1)
        # BEGIN
        "*** YOUR CODE HERE ***"
        if len(start) < len(goal):
            if start[0] in goal:
                return pawssible_patches(start[1:], goal[1:], limit)
            else:
                return 1 + pawssible_patches(start, goal[ : len(goal) - 1], limit - 1)
        if len(start) > len(goal):
            if goal[0] in start:
                return pawssible_patches(start[1:], goal[1:], limit)
            else:
                return 1 + pawssible_patches(start[ : len(start) - 1], goal, limit - 1)
        else:
            if start[0] in goal or goal[0] in start:
                return pawssible_patches(start[1:], goal[1:], limit)
            if goal[0] not in start:
                return 1 + pawssible_patches(start[0:], goal[1:], limit - 1)
            if start[0] not in goal:
                return 1 + pawssible_patches(start[1:], goal[0:], limit - 1)
            else:
                return 1 + pawssible_patches(start[1 : ], goal[1 : ], limit - 1)



        # END
big_limit = 10
pawssible_patches("wird", "bird", big_limit)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    accurate = 0
    if len(typed) == len(prompt):
        for word_t, word_p in zip(typed, prompt):           
            if word_t == word_p:
                accurate = accurate + 1
            if word_t != word_p:
                send({'id': user_id, 'progress': accurate / len(prompt)})
                return accurate / len(prompt)

    else:
        for word_t, word_p in zip(typed, prompt[ : len(typed)]):
            if word_t == word_p:
                accurate = accurate + 1
            if word_t != word_p:
                send({'id': user_id, 'progress': accurate / len(prompt)})
                return accurate / len(prompt)
    send({'id': user_id, 'progress': accurate / len(prompt)})
    return accurate / len(prompt)

# print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
# prompt = ['I', 'have', 'begun', 'to', 'type']
# c = report_progress(['I', 'hve', 'begun', 'to', 'type'], prompt, 3, print_progress)
            


    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    time_list_0 = []
    empty_list = []
    for time_list_index in range(0, len(times_per_player)):
            time_list_0.append(empty_list * time_list_index)
            for time_index in range(1, len(times_per_player[time_list_index])):
                time_list_0[time_list_index].append(times_per_player[time_list_index][time_index] - times_per_player[time_list_index][time_index - 1]) 
    # if len(times_per_player) > 1: 
    #     for time_index in range(1, len(times_per_player[1])):
    #         time_list_1.append(times_per_player[1][time_index] - times_per_player[1][time_index - 1])
    #     return [words,[time_list_0, time_list_1]] 
    return [words,time_list_0]
           
    
    # END PROBLEM 9
# p = [[1, 4, 6, 7], [0, 4, 6, 9]]
# words = ['This', 'is', 'fun']
# game = time_per_word(p, words)
#p = [[16, 18, 23, 28, 30, 33]]
#game = time_per_word(p, ['unsimilar', 'conditioning', 'crystallogenical', 'mennom', 'foreannouncement'])
# p = [[16, 21, 22, 23], [73, 77, 82, 86], [8, 9, 11, 16]]
# game = time_per_word(p, ['antimonarchial', 'archaeology', 'oopod'])
# p = [[1, 4, 6, 7], [0, 4, 6, 9]]
# words = ['This', 'is', 'fun']
# game = time_per_word(p, words)


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    min_indexes = {}
    time_compare_list = [[] for _ in word_indices]
    word_fatest_list = [[] for _ in player_indices]
    for player_index in player_indices:
        for word_index in word_indices:
            time_compare_list[word_index].append(all_times(game)[player_index][word_index])
    my_dict = dict(zip(all_words(game), time_compare_list))
    for key, value in my_dict.items():
        min_value = min(value)
        min_index = value.index(min_value)
        min_indexes[key] = min_index
    for key, value in min_indexes.items():
        for player_index in player_indices:
            if player_index == value:
                word_fatest_list[player_index].append(key) 
    return word_fatest_list 



    

  
        

        

    

    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

# p0 = [2, 2, 3]
# p1 = [6, 1, 2]
# c = fastest_words(game(['What', 'great', 'luck'], [p0, p1]))

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)