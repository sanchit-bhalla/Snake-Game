import pygame
import random
import os

# for music
pygame.mixer.init()

pygame.init()

# Define colors
red  = (0, 0, 0)  # black color not red
white =(173, 240, 158)
black = (176, 165, 102)

screen_width = 600
screen_height = 400
# Creating window
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background image
bgimg = pygame.image.load("snake.png")

# convert_alpha bcz when we blit again and again to koi farak nhi padega
# Rest see from documentation
bgimg = pygame.transform.scale(bgimg, (screen_width,screen_height)).convert_alpha()

pygame.display.set_caption("Welcome to Snake Game")
pygame.display.update()

Clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)  # None se system ki default  font aa jaegi

def text_screen(text,color, x, y):
    screen_text = font.render(text, True, color)  # 2nd arg. True is basically when we change high resolution to low
    gameWindow.blit(screen_text, (x,y))  # To update ?

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x,y, snake_size, snake_size])

def Welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((179, 245, 164))
        gameWindow.blit(bgimg, (0,0))
        text_screen("Welcome to Snake Game", (0,0,0),100,10)
        text_screen("Press SpaceBar to Play", (0,0,0),120,350)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # For Spacebar Key
                    pygame.mixer.music.load("back.mp3")
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
    pygame.quit()
    quit()

# Game loop
def gameloop():
    #game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0   # initially
    velocity_y = 0
    init_velocity = 2
    snake_size = 10
    food_x = random.randint(20,screen_width/2)
    food_y = random.randint(20,screen_height/2)
    score = 0    # Initially
    # Frame per second
    fps  = 60

    snk_list = []
    snk_length = 1
    # Check if highscore file exist or not
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")
    # Read highscore
    with open("highscore.txt", "r") as f:
        highscore= f.read()   # in form of string

        
    while not exit_game:
        if game_over:
            if int(highscore)<score:
                highscore = score
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))   # write in form of string

            gameWindow.fill(white)
            text_screen("Game over, Press Enter To Continue", red,50,130)
            text_screen("Your Score: "+ str(score), red, 210, 200)
            text_screen("Highest Score: "+str(highscore), red, 180, 240)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # For Enter Key
                        Welcome()
            
        else:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                        
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                        
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score +=10

            snake_x += velocity_x
            snake_y += velocity_y

             # bcz rectangles  have size >1  so its not necessary that their centers overlapp completely
            if abs(snake_x - food_x)<=6 and abs(snake_y - food_y)<=6:
                score+=10
                if score>60:
                    init_velocity = 3
                if score>=110:
                    init_velocity = 4
                if score>150:
                    init_velocity = 5
                if score>200:
                    init_velocity = 7
                if score>250:
                    init_velocity = 9
                food_x = random.randint(20,screen_width/2)
                food_y = random.randint(20,screen_height/2)
                snk_length+=5

                if score>int(highscore):
                    highscore = score
            gameWindow.fill(white)
            
            text_screen("Score: "+ str(score), red, 5, 5)


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            # Bcz if head clashes with any part of body except head then its over
            if head in snk_list[:-1]:   # From starting excluding last which is head itself
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snk_list, snake_size)

            """   Rectangle
                    food_x, food_y    ==>   Initial position
                    snake_size   ==>  width and length of rectangle
            """
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
        pygame.display.update()  # this func. is used everytime when we change

        Clock.tick(fps)    # fps should be more if game lags 

    pygame.quit()
    quit()

Welcome()
