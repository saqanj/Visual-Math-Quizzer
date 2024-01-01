# Animated Mathematics Quizzer by Saqlain Anjum
# Animated component of the original quizzer that utilizes a soccer game to show progress, still using the console for user inputs.

# Necessary imports.
import random
import Linear_Path_Asset as backfile
import time
import tkinter as tk

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
SHRINK_FACTOR = 3 # Shrink factor.
# Initializing starting and end-points for the animation.
START_X = 100
START_Y = 300
END_X = 700
END_Y = 300
# Initializing max steps, tick length, move type, and minimum point.
MAX_STEPS = 10
TICK_LEN = -20
MOVE_TYPE = 1
MIN_POINT = 0
# Initializing images.
SOCCER_BALL = "ball.png" # Soccer Ball Image.
SOCCER_PITCH = "soccer_pitch.png" # Soccer background.
EXPLOSION_IMAGE = "explosion.png" # Explosion image.
# Initializing sounds.
EXPLOSION_SOUND = "explosion_sound.wav" # Explosion sound.
WOOSH_SOUND = "Woosh_Sound.wav" # Woosh sound.


# Initializing changing values not able to be defined inside the loop.
user_points = 0
game_over = False
play_counter = 0


root = tk.Tk()

# Creating an instance of the asset.
o = backfile.Image(root,SOCCER_PITCH,SOCCER_BALL,SHRINK_FACTOR,START_X,START_Y,END_X,END_Y,MAX_STEPS,TICK_LEN,MOVE_TYPE)


o.pack(expand=True, fill=tk.BOTH)
root.update()
looper = True

try:
   
    while looper:
      
        # Set sound to be played at each movement
        o.set_move_sound(WOOSH_SOUND)

        
        # This code is used to create a menu for the user to pick from either Level 1, 2, or 3 for the operands and points in their multiplication problems.
        while (game_over != GAME_OVER_LOOP_EXIT):
            print(" CHOOSE FROM THE FOLLOWING: ")
            print(LEVEL_1_MENU_MESSAGE)
            print(LEVEL_2_MENU_MESSAGE)
            print(LEVEL_3_MENU_MESSAGE)
            

        # Input statement for the user to choose which level they would like and while loop to have them re-input and print an error message if the level does not exist.
            user_level_choice = int(input("Level Choice: "))
            while (user_level_choice not in LEVEL_NUMBERS):
                print(ERROR_MESSAGE)
                user_level_choice = int(input("Level Choice: "))
            print("")

            
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
                for i in range (1, points_per_play + 1):
                    if (user_points + 1 <= MAX_STEPS):
                        o.move_object(1)
                        user_points = user_points + 1
            else:
                print(INCORRECT_MESSAGE)
                print("The correct answer was:", str(answer))
                print("You lost:", str(points_per_play) + " point(s).")
                for i in range (1, points_per_play + 1):
                    if (user_points - 1 >= MIN_POINT):
                        o.move_object(-1)
                        user_points = user_points - 1

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

                
            # changing move element to an explosion once the user wins and playing explosion sound.
                o.set_moving_element(EXPLOSION_IMAGE, SHRINK_FACTOR)
                o.play_sound(EXPLOSION_SOUND)

            # setting looper to false to exit the animation
            looper = False

        root.update()
        # Loop exit and program + animation end condition.
        if looper is False:        
            root.quit()
except tk.TclError:
    print('\nWindow Closed')
