"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.
FIRST_101_DIGITS_OF_PI = 31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    dice_times = 0
    temp_outcome = 0
    total = 0
    flag = False
    while dice_times < num_rolls:
        dice_times = dice_times + 1
        temp_outcome = dice()
        if temp_outcome == 1:
            flag = True
        total = total + temp_outcome
    if flag == True:
        return(1)
    else:
        return(total)
    
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    pi = FIRST_101_DIGITS_OF_PI

    # Trim pi to only (score + 1) digit(s)
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    # END PROBLEM 2
    pi = pi // pow(10, 100-score)

    return pi % 10 + 3


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        x = roll_dice(num_rolls,dice)
        return x
    # END PROBLEM 3


def extra_turn(player_score, opponent_score):
    """Return whether the player gets an extra turn."""
    return (pig_pass(player_score, opponent_score) or
            swine_align(player_score, opponent_score))


def swine_align(player_score, opponent_score):
    """Return whether the player gets an extra turn due to Swine Align.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> swine_align(30, 45)  # The GCD is 15.
    True
    >>> swine_align(35, 45)  # The GCD is 5.
    False
    """
    # BEGIN PROBLEM 4a
    "*** YOUR CODE HERE ***"
    pot_gcd = 1
    gcd = 0
    if player_score == 0 or opponent_score == 0:
        return (False)    
    elif (player_score % opponent_score == 0 or opponent_score % player_score == 0) and (player_score > 9 and opponent_score > 9):
        return (True)
    while player_score > pot_gcd or opponent_score > pot_gcd:
        if player_score % pot_gcd == 0 and opponent_score % pot_gcd == 0: 
            gcd = pot_gcd
        pot_gcd = pot_gcd + 1
    if gcd > 9:
        return (True)
    else:
        return (False)


        
    # END PROBLEM 4a  
    



def pig_pass(player_score, opponent_score):
    """Return whether the player gets an extra turn due to Pig Pass.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> pig_pass(9, 12)
    False
    >>> pig_pass(10, 12)
    True
    >>> pig_pass(11, 12)
    True
    >>> pig_pass(12, 12)
    False
    >>> pig_pass(13, 12)
    False
    """
    # BEGIN PROBLEM 4b
    "*** YOUR CODE HERE ***"
    skip = False
    if opponent_score - player_score < 3 and opponent_score - player_score > 0:
        skip = True
    return skip
    # END PROBLEM 4b


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"      
    extra0, extra1 = False, False
    turn = 0
    while score0 < goal and score1 < goal:
        if who == 0 or extra0:
            play0_num_dice = strategy0(score0, score1)
            turn_score0 = take_turn(play0_num_dice, score1, dice)
            score0 = score0 + turn_score0
            # BEGIN PROBLEM 6
            if turn == 0:
                announce = say(score0, score1) #不能写成say = 某个function，否则无法再为say赋值
            else:
                announce = announce(score0, score1)
            # END PROBLEM 6
            if score0 >= goal:
                return score0, score1 
            if extra_turn(score0, score1):
                extra0 = True
            else: 
                extra0 = False
            if extra0 == False:
                who = other(who)
            turn = turn + 1


        if who == 1 or extra1:
            play1_num_dice = strategy1(score1, score0)
            turn_score1 = take_turn(play1_num_dice, score0, dice)
            score1 = score1 + turn_score1
            # BEGIN PROBLEM 6
            announce = announce(score0, score1)
            # END PROBLEM 6
            if score1 >= goal:
                return score0, score1
            if extra_turn(score1, score0):
                extra1 = True
            else:
                extra1 = False
            if extra1 == False:
                who = other(who)
            turn = turn + 1
    # END PROBLEM 5
    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 8)
    Player 0 now has 10 and Player 1 now has 8
    >>> h3 = h2(10, 17)
    Player 0 now has 10 and Player 1 now has 17
    Player 1 takes the lead by 7
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, last_score=0, running_high=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 9)
    9 point(s)! The most yet for Player 1
    >>> f3 = f2(20, 9)
    >>> f4 = f3(20, 30)
    21 point(s)! The most yet for Player 1
    >>> f5 = f4(20, 47) # Player 1 gets 17 points; not enough for a new high
    >>> f6 = f5(21, 47)
    >>> f7 = f6(21, 77)
    30 point(s)! The most yet for Player 1
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    def highest_score(score0, score1):
        nonlocal who
        running_high0, running_high1 = running_high, running_high
        last_score0, last_score1 = last_score, last_score

        if who == 0:
            if score0 == last_score0:
                return announce_highest(who, last_score0, running_high1)
            if score0 != last_score0:
                last_score0 = score0 - last_score0
            if last_score0 > running_high0:
                running_high0 = last_score0
                print (running_high0, "point(s)! The most yet for Player 0")
                return announce_highest(who, score0, running_high0)
            else:
                return announce_highest(who, score0, running_high0)
            
        
        if who == 1:
            if score1 == last_score1:
                return announce_highest(who, last_score1, running_high1)
            if score1 != last_score1:
                last_score1 = score1 - last_score1
            if last_score1 > running_high1:
                running_high1 = last_score1
                print (running_high1, "point(s)! The most yet for Player 1" )
                return announce_highest(who, score1, running_high1)
            else:
                return announce_highest(who, score1, running_high1)

    return highest_score
    # END PROBLEM 7

# f0 = announce_highest(1) # Only announce Player 1 score gains
# f1 = f0(12, 0)
# f2 = f1(12, 10)
# f3 = f2(20, 10)
# f4 = f3(22, 20)
# f5 = f4(22, 35)
# f6 = f5(30, 47)
# f7 = f6(31, 47)

#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def new_func(*args): #*args带星号的表示接受任意数量的arguments
        i = 1
        total_value = 0
        while i <= trials_count:     
            turn_value = original_function(*args)
            total_value = total_value + turn_value
            i = i + 1

        avg = total_value / trials_count
        return (avg)


    return new_func    
    # END PROBLEM 8

def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    num_rolls = 1
    avg = 0
    while num_rolls <= 10:
        temp_avg = make_averaged(roll_dice, trials_count)(num_rolls, dice)
        if temp_avg > avg:
            avg = temp_avg
            max_num_roll = num_rolls
        num_rolls = num_rolls + 1    
    return (max_num_roll)
    # END PROBLEM 9



def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test extra_turn_strategy
        print('extra_turn_strategy win rate:', average_win_rate(extra_turn_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"



def bacon_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if free_bacon(opponent_score) >= cutoff:
        return 0
    else:
        return num_rolls  # Replace this statement
    # END PROBLEM 10


def extra_turn_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers an extra turn. It also
    rolls 0 dice if it gives at least CUTOFF points and does not give an extra turn.
    Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    if extra_turn(score + free_bacon(opponent_score), opponent_score):
        return 0
    elif bacon_strategy(score, opponent_score, cutoff, num_rolls) == 0:
        return 0
    else:
        return num_rolls  # Replace this statement
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 6  # Replace this statement
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()

# always_one = make_test_dice(1)
# always_two = make_test_dice(2)
# always_three = make_test_dice(3)
# always = always_roll
# s0, s1 = play(always(1), always(1), goal=25, dice=make_test_dice(5, 10, 3, 1, 11, 6))

# always_three = make_test_dice(3)
# always = always_roll
# s0, s1 = play(always(5), always(5), goal=25, dice=always_three)


# import hog, importlib, hog_gui
# import tests.play_utils
# turns = tests.play_utils.describe_game(hog, hog_gui, test_number=45891, score0=47, score1=53, goal=54)
# print(turns[0])

# always_three = make_test_dice(3)
# always = always_roll
# s0, s1 = play(always(5), always(3), score0=91, score1=10, dice=always_three)

# Fuzz Testing
# Plays a lot of random games, and calculates a secret value.
# Failing this test means something is wrong, but you should
# look at other tests to see where the problem might be.
# Hint: make sure you're only calling take_turn once per turn!


# import hog, importlib, hog_gui
# import tests.play_utils
# turns = tests.play_utils.describe_game(hog, hog_gui, test_number=19709, score0=27, score1=6, goal=85)
# print(turns[0])
# # Start scores = (27, 6).
# # Player 0 rolls 0 dice and gets outcomes [].
# # End scores = (32, 6)
# print(turns[1])
# # Start scores = (32, 6).
# # Player 1 rolls 1 dice and gets outcomes [4].
# # End scores = (32, 10)
# print(turns[2])
# # Start scores = (32, 10).
# # Player 0 rolls 0 dice and gets outcomes [].
# # End scores = (40, 10)
# print(turns[3])
# # Start scores = (40, 10).
# # Player 0 rolls 10 dice and gets outcomes [4, 4, 1, 3, 6, 2, 4, 4, 6, 3].
# # End scores = (41, 10)
# print(turns[4])
# # Start scores = (41, 10).
# # Player 0 rolls 5 dice and gets outcomes [1, 6, 2, 3, 4].
# # End scores = (42, 10)

#Phase2#################################################################################

# def echo(s0, s1):
#      print(s0, s1)
#      return echo

# s0, s1 = play(always_roll(1), always_roll(1), dice=make_test_dice(3), goal=5, say=echo)


# def count(n):
#      def say(s0, s1):
#          print(n, s0)
#          return count(n + 1)
#      return say
# s0, s1 = play(always_roll(1), always_roll(1), dice=make_test_dice(5), goal=10, say=count(1))

# def echo(s0, s1):
#      print(s0, s1)
#      return echo

# strat0 = lambda score, opponent: 1 - opponent // 10
# strat1 = always_roll(3)
# s0, s1 = play(strat0, strat1, dice=make_test_dice(4, 2, 6), goal=15, say=echo)