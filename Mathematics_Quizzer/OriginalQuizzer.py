# Math Quizzer by Saqlain Anjum
# This program uses lists, while loops, and if-then statements to develop a game that tests the user on their multiplication abilities on a list of operands between 1-10. The user can earn/loose points based on their answers to randomly generated multiplication problems and the level that they select. They win if they are able to reach a specified winning score.
# Non-animated component of the quizzer application. Relies solely on the console.

# Importing random library.
import random

# Printing game title.
print("Multiplication Quizzer")

# Printing game description.
print("Welcome to Multiplication Quizzer! Here you can be quizzed on your ability to multiply randomly generated numbers, and gain a certain number of points for doing so. Your goal will be to reach a score of 10 points in order to win the game. Good luck!")

# Establishing lists.
LEVEL_NUMBERS = [1, 2, 3]
LEVEL_1_OPERANDS = [1, 2, 3]
LEVEL_2_OPERANDS = [4, 5, 6]
LEVEL_3_OPERANDS = [7, 8, 9, 10]
POINTS_PER_LEVEL = [0, 1, 2, 3]

# Establishing constants.
MIN_SCORE = 0
WINNING_SCORE = 10
MAX_OPERAND_LEVEL_1 = max(LEVEL_1_OPERANDS)
MAX_OPERAND_LEVEL_2 = max(LEVEL_2_OPERANDS)
MAX_OPERAND_LEVEL_3 = max(LEVEL_3_OPERANDS)
MIN_OPERAND_LEVEL_1 = min(LEVEL_1_OPERANDS)
MIN_OPERAND_LEVEL_2 = min(LEVEL_2_OPERANDS)
MIN_OPERAND_LEVEL_3 = min(LEVEL_3_OPERANDS)
LEVEL_1_MENU_MESSAGE = "   LEVEL 1:", str(POINTS_PER_LEVEL[1]), "point per question, operands will be between", str(MIN_OPERAND_LEVEL_1) + "-" + str(MAX_OPERAND_LEVEL_1) + "."
LEVEL_2_MENU_MESSAGE = "   LEVEL 2:", str(POINTS_PER_LEVEL[2]), "points per question, operands will be between", str(MIN_OPERAND_LEVEL_2) + "-" + str(MAX_OPERAND_LEVEL_2) + "."
LEVEL_3_MENU_MESSAGE = "   LEVEL 3:", str(POINTS_PER_LEVEL[3]), "points per question, operands will be between", str(MIN_OPERAND_LEVEL_3) + "-" + str(MAX_OPERAND_LEVEL_3) + "."
ERROR_MESSAGE = "INVALID INPUT, PLEASE TRY AGAIN!"
CONGRATULATIONS_MESSAGE = "Good job! You got the answer right!"
INCORRECT_MESSAGE = "Wrong answer! Better luck next time!"
CONGRATULATIONS_GAME_OVER_MESSAGE = "Congratulations! The game is now over! You have won!"
GAME_OVER_LOOP_EXIT = True

# Initializing changing values not able to be defined inside the loop.
user_score = 0
test = ""
user_points = 0
game_over = False
play_counter = 0

# The entire code is placed inside a while loop that is exited from when the user has reached the score of 10 points, causing a string variable named game_over to read "TRUE".
while (game_over != GAME_OVER_LOOP_EXIT):
    # This code is used to create a menu for the user to pick from either Level 1, 2, or 3 for the operands and points in their multiplication problems.
    print(" CHOOSE FROM THE FOLLOWING: ")
    print(LEVEL_1_MENU_MESSAGE)
    print(LEVEL_2_MENU_MESSAGE)
    print(LEVEL_3_MENU_MESSAGE)
    # Input statement for the user to choose which level they would like and while loop to have them re-input and print an error message if the level does not exist.
    user_level_choice = int(input("Level Choice: "))
    while (user_level_choice not in LEVEL_NUMBERS):
        print(ERROR_MESSAGE)
        user_level_choice = int(input("Level Choice: "))
    print("") # NOTE - Blank print statements are used throughout the code to create spaces for clarity in the output.
    # If-elif-elif statement used to randomly select the operands that are going to be used in the multiplication problems and the points a user can gain or loose per question depending on their level selection.
    if (user_level_choice == LEVEL_NUMBERS[0]):
        OPERAND_1 = random.randint(MIN_OPERAND_LEVEL_1, MAX_OPERAND_LEVEL_1)
        OPERAND_2 = random.randint(MIN_OPERAND_LEVEL_1, MAX_OPERAND_LEVEL_1)
        points_per_play = POINTS_PER_LEVEL[1]
    elif (user_level_choice == LEVEL_NUMBERS[1]):
        OPERAND_1 = random.randint(MIN_OPERAND_LEVEL_2, MAX_OPERAND_LEVEL_2)
        OPERAND_2 = random.randint(MIN_OPERAND_LEVEL_2, MAX_OPERAND_LEVEL_2)
        points_per_play = POINTS_PER_LEVEL[2]
    elif (user_level_choice == LEVEL_NUMBERS[2]):
        OPERAND_1 = random.randint(MIN_OPERAND_LEVEL_3, MAX_OPERAND_LEVEL_3)
        OPERAND_2 = random.randint(MIN_OPERAND_LEVEL_3, MAX_OPERAND_LEVEL_3)
        points_per_play = POINTS_PER_LEVEL[3]
    # Code for calculating what the answer will be and storing it in a variable.
    answer = OPERAND_1 * OPERAND_2
    # Printing the question and having the user input their answer, while a play counter goes up by one every time the user answers an equation.
    print("Q: " + str(OPERAND_1) + " X " + str(OPERAND_2))
    user_answer = int(input("A: "))
    print("")
    play_counter = play_counter + 1
    # If-then-else statements used to let the user know if they got the answer right, calculating their score, and how many points they gained or lost and printing these values.
    if (user_answer == answer):
        print(CONGRATULATIONS_MESSAGE)
        print("You gained:", str(points_per_play) + " point(s).")
        user_points = user_points + points_per_play
        if (user_points >= WINNING_SCORE):
            user_points = WINNING_SCORE
    else:
        print(INCORRECT_MESSAGE)
        print("The correct answer was:", str(answer))
        print("You lost:", str(points_per_play) + " point(s).")
        user_points = user_points - points_per_play
        if (user_points <= MIN_SCORE):
            user_points = MIN_SCORE
    # Code for printing the current score if the user has not already won the game.
    if (user_points < WINNING_SCORE):
        print("Current Score: ", str(user_points) + " point(s).")
    # Code for calculating and printing additional points they need to win the game if the user hasn't already won using an if-then statmement.
    additional_points_needed = WINNING_SCORE - user_points
    if (user_points < WINNING_SCORE):
        print("Additional Points Needed to Win:", str(additional_points_needed) + " point(s).")
    print("")
    # Code for exiting the loop if they have achieved the winning score, by setting an exiting variable to "TRUE".
    if (user_points == WINNING_SCORE):
        game_over = GAME_OVER_LOOP_EXIT
    
# Printing the final 'game over' messages, player score upon reaching the winning score, and how many equations it took to win the game using the previously established play counter.
print(CONGRATULATIONS_GAME_OVER_MESSAGE)
print("The goal of", str(WINNING_SCORE) + " points has been reached!")
print("You played", str(play_counter) + " equations to win the game!")
