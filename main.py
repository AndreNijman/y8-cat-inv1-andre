#importing all my modules and files
import pygame
import sys
import random
import translation
import time
import calculations
import math
import triples

pygame.init() #starts pygame             

#defining all my variables
app_clock = pygame.time.Clock()
translator = translation.Translation()
base_font = pygame.font.Font(None, 25) 
my_font = pygame.font.Font(None, 20) 
error_font = pygame.font.Font(None, 25)
button_font = pygame.font.Font(None, 20)
win_font = pygame.font.Font(None, 200)
restartbutton_font = pygame.font.Font(None, 60)
user_text = '' 
input_rect = pygame.Rect(890, 100, 140, 32)
color_active = pygame.Color('lightskyblue3') 
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False
user_text2 = ''
input_rect2 = pygame.Rect(1040, 100, 140, 32)
color_active2 = pygame.Color('lightskyblue3') 
color_passive2 = pygame.Color('chartreuse4')
color2 = color_passive
color3 = color_passive
color4 = color_passive
color_active3 = pygame.Color('lightskyblue3') 
color_passive3 = pygame.Color('chartreuse4')
active2 = False
screen = pygame.display.set_mode([1225, 840])
clicked = False
clicked2 = False
button = pygame.Rect(1010-50, 200, 102, 34)
restartbutton = pygame.Rect(607.5-200, 500, 400, 100)
player = 1
plane = pygame.Rect(14, 14, 787, 812)
randtime = [0, False]
win = 0
do = [0, False]

def create_app_window(width, height): #Creates the app window
    print(f'\nWelcome. The Cartesian Plane goes from -{width/2} to {width/2} in both the x and y directions')
    pygame.display.set_caption("Cartesian Plane Game")        
    app_dimensions = ((width + 10), height + 10)            
    app_surf = pygame.display.set_mode(app_dimensions) 
    app_surf_rect = app_surf.get_rect()                 
    return app_surf, app_surf_rect

def drawplane(): #Draws the Cartesian Plane
    app_surf.fill('white') 
    pygame.draw.line(app_surf, 'grey',(0,app_surf_rect.height/2),(app_surf_rect.width,app_surf_rect.height/2),width=1)
    pygame.draw.line(app_surf, 'grey',((app_surf_rect.width/2)-200, 0),((app_surf_rect.width/2)-200,app_surf_rect.height),width=1)

def app_surf_update(destination, player_one, player_two): #Updates the entities
    pygame.draw.circle(app_surf, 'black',destination['pygame_coords'], radius = 3, width = 3)
    pygame.draw.circle(app_surf, player_one['colour'], player_one['pygame_coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, player_two['colour'], player_two['pygame_coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, npc['colour'], npc['pygame_coords'], radius = 3, width = 2)


def refresh_window(): #refreshes the window every frame
    pygame.display.flip()
    app_clock.tick(60)

def conv_cartesian_to_pygame_coords(x,y): #Converts the cartesian coordinates to pygame coordinates
    pygame_x = x + app_surf_rect.width / 2
    pygame_y = -y + app_surf_rect.height /2
    return(pygame_x, pygame_y)

def initialise_entities(): #initialises the entities, giving them random coordinates
    p1_rand_x, p1_rand_y = random.randint(-400,0), random.randint(-400,400)
    player_one['cartesian_coords'] = (p1_rand_x, p1_rand_y)
    player_one['pygame_coords'] = conv_cartesian_to_pygame_coords(p1_rand_x, p1_rand_y)

    p2_rand_x, p2_rand_y = random.randint(-400,0), random.randint(-400,400)
    player_two['cartesian_coords'] = (p2_rand_x, p2_rand_y)
    player_two['pygame_coords'] = conv_cartesian_to_pygame_coords(p2_rand_x, p2_rand_y)

    npc_rand_x, npc_rand_y = random.randint(-400,0), random.randint(-400,400)
    npc['cartesian_coords'] = (npc_rand_x, npc_rand_y)
    npc['pygame_coords'] = conv_cartesian_to_pygame_coords(npc_rand_x, npc_rand_y)

    dest_rand_x, dest_rand_y = random.randint(-400,0), random.randint(-400,400)
    destination['cartesian_coords'] = (dest_rand_x, dest_rand_y)
    destination['pygame_coords'] = conv_cartesian_to_pygame_coords(dest_rand_x, dest_rand_y)

def p1rand(): #randomly picks a movement for player 1
    distance = random.randint(5,300)
    direction = random.randint(1,8)
    p1cx, p1cy = player_one['cartesian_coords'][0], player_one['cartesian_coords'][1]
    triple1, triple2, direction = translator.Triple_Finder(distance, direction)
    triple = [triple1, triple2]
    move1, move2 = translator.Triple_to_Movement(triple, direction)
    np1cx = p1cx+move1
    np1cy = p1cy+move2
    np1px, np1py = conv_cartesian_to_pygame_coords(np1cx, np1cy)
    return np1px, np1py, np1cx, np1cy

def p2rand():  #randomly pickes a movement for player 2
    distance = random.randint(5,300)
    direction = random.randint(1,8)
    p2cx, p2cy = player_two['cartesian_coords'][0], player_two['cartesian_coords'][1]
    triple1, triple2, direction = translator.Triple_Finder(distance, direction)
    triple = [triple1, triple2]
    move1, move2 = translator.Triple_to_Movement(triple, direction)
    np2cx = p2cx+move1
    np2cy = p2cy+move2
    np2px, np2py = conv_cartesian_to_pygame_coords(np2cx, np2cy)
    return np2px, np2py, np2cx, np2cy

def npcrand(): #picks a random movement for the npc, usually towards the destination
    if do[1] == False:
        do[0] = random.randint(1,2)
        do[1] = True
    if do[0] == 1:
        pos1 = npc['pygame_coords']
        pos2 = destination['pygame_coords']
        diff_x = pos2[0] - pos1[0]
        diff_y = pos2[1] - pos1[1]
        angle_rad = math.atan2(diff_y, diff_x)
        angle_deg = math.degrees(angle_rad)
        if angle_deg >= 0 and angle_deg <= 45:
            direction = 8
        elif angle_deg >= 45 and angle_deg <= 90:
            direction = 7
        elif angle_deg >= 90 and angle_deg <= 135:
            direction = 6
        elif angle_deg >= 135 and angle_deg <= 180:
            direction = 5
        elif angle_deg >= 180 and angle_deg <= 225:
            direction = 4
        elif angle_deg >= 225 and angle_deg <= 270:
            direction = 3
        elif angle_deg >= 270 and angle_deg <= 315:
            direction = 2
        elif angle_deg >= 315 and angle_deg <= 360:
            direction = 1
        distance = random.randint(5,293)
    else:
        direction = random.randint(1,8)
        distance = random.randint(5,293)

    p1cx, p1cy = npc['cartesian_coords'][0], npc['cartesian_coords'][1]
    triple1, triple2, direction = translator.Triple_Finder(distance, direction)
    triple = [triple1, triple2]
    move1, move2 = translator.Triple_to_Movement(triple, direction)
    np1cx = p1cx+move1
    np1cy = p1cy+move2
    np1px, np1py = conv_cartesian_to_pygame_coords(np1cx, np1cy)
    return np1px, np1py, np1cx, np1cy, do, distance, direction

def print_player_info(): #prints all the player info
    text_surface = error_font.render(f"PLAYER ONE Location: ({player_one['cartesian_coords'][0]}, {player_one['cartesian_coords'][1]})", False, (255, 0, 0))
    screen.blit(text_surface, (828,320))
    dist = calculations.Distance.distance(player_one['cartesian_coords'], destination['cartesian_coords'])
    text_surface = error_font.render(f"Distance to destination: {round(dist, 1)} units", False, (255, 0, 0))
    screen.blit(text_surface, (828,350))
    gradient = calculations.Distance.gradient(player_one['cartesian_coords'], destination['cartesian_coords'])
    text_surface = error_font.render(f"Gradient with destination: {round(gradient, 1)}", False, (255, 0, 0))
    screen.blit(text_surface, (828,380))
    mid1 = calculations.Distance.midpoint(player_one['cartesian_coords'], player_two['cartesian_coords'])
    text_surface = error_font.render(f"Midpoint with Player Two: ({mid1[0]}, {mid1[1]})", False, (255, 0, 0))
    screen.blit(text_surface, (828,410))
    mid2 = calculations.Distance.midpoint(player_one['cartesian_coords'], npc['cartesian_coords'])
    text_surface = error_font.render(f"Midpoint with NPC: ({mid2[0]}, {mid2[1]})", False, (255, 0, 0))
    screen.blit(text_surface, (828,440))

    text_surface = error_font.render(f"PLAYER TWO Location: ({player_two['cartesian_coords'][0]}, {player_two['cartesian_coords'][1]})", False, (0, 0, 255))
    screen.blit(text_surface, (828,470+30))
    dist = calculations.Distance.distance(player_two['cartesian_coords'], destination['cartesian_coords'])
    text_surface = error_font.render(f"Distance to destination: {round(dist, 1)} units", False, (0, 0, 255))
    screen.blit(text_surface, (828,500+30))
    gradient = calculations.Distance.gradient(player_two['cartesian_coords'], destination['cartesian_coords'])
    text_surface = error_font.render(f"Gradient with destination: {round(gradient, 1)}", False, (0, 0, 255))
    screen.blit(text_surface, (828,530+30))
    mid1 = calculations.Distance.midpoint(player_two['cartesian_coords'], player_one['cartesian_coords'])
    text_surface = error_font.render(f"Midpoint with Player One: ({mid1[0]}, {mid1[1]})", False, (0, 0, 255))
    screen.blit(text_surface, (828,560+30))
    mid2 = calculations.Distance.midpoint(player_two['cartesian_coords'], npc['cartesian_coords'])
    text_surface = error_font.render(f"Midpoint with NPC: ({mid2[0]}, {mid2[1]})", False, (0, 0, 255))
    screen.blit(text_surface, (828,590+30))

    text_surface = error_font.render(f"NPC Location: ({npc['cartesian_coords'][0]}, {npc['cartesian_coords'][1]})", False, (0, 150, 0))
    screen.blit(text_surface, (828,620+60))
    dist = calculations.Distance.distance(npc['cartesian_coords'], destination['cartesian_coords'])
    text_surface = error_font.render(f"Distance to destination: {round(dist, 1)} units", False, (0, 150, 0))
    screen.blit(text_surface, (828,650+60))
    gradient = calculations.Distance.gradient(npc['cartesian_coords'], destination['cartesian_coords'])
    text_surface = error_font.render(f"Gradient with destination: {round(gradient, 1)}", False, (0, 150, 0))
    screen.blit(text_surface, (828,680+60))
    mid1 = calculations.Distance.midpoint(npc['cartesian_coords'], player_one['cartesian_coords'])
    text_surface = error_font.render(f"Midpoint with Player One: ({mid1[0]}, {mid1[1]})", False, (0, 150, 0))
    screen.blit(text_surface, (828,710+60))
    mid2 = calculations.Distance.midpoint(player_two['cartesian_coords'], npc['cartesian_coords'])
    text_surface = error_font.render(f"Midpoint with Player Two: ({mid2[0]}, {mid2[1]})", False, (0, 150, 0))
    screen.blit(text_surface, (828,740+60))

#player one's dictionary
player_one={
    'name': 'Player One',
    'cartesian_coords':None,
    'pygame_coords':None,
    'colour':'red',
}

#player two's dictionary
player_two={
    'name': 'Player Two',
    'cartesian_coords':None, 
    'pygame_coords':None,
    'colour':'blue',
}

#the destination's dictionary
destination={
    'name': 'Destination',
    'cartesian_coords':None,
    'pygame_coords':None,
    'colour':'black',
}

#the NPC's dictionary
npc={
    'name': 'NPC',
    'cartesian_coords':None, 
    'pygame_coords':None,
    'colour':(0, 150, 0),
}

#calls the create_app_window function so it actually creates an app window of 1215, 830
app_surf, app_surf_rect = create_app_window(1215, 830)
initialise_entities()

print('\nThree entities initialised... here is a raw printout of their dictionaries')
print(destination)
print(player_one)
print(player_two)
print(npc)

#starts a timer
current = round(time.time_ns()/1000000000)

#starts the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #checks if when there is a mouse click, it is on an input box
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if input_rect.collidepoint(event.pos):
                active = True
                clicked = True
            else:
                active = False
                clicked = False
            if input_rect2.collidepoint(event.pos):
                active2 = True
                clicked2 = True
            else:
                active2 = False
                clicked2 = False

        #always checking mouse position to see if its on any interactives
        mouse_pos = pygame.mouse.get_pos()
        if input_rect.collidepoint(mouse_pos):
            active = True
        else:
            if clicked == False:
                active = False
        if input_rect2.collidepoint(mouse_pos):
            active2 = True
        else:
            if clicked2 == False:
                active2 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and clicked == True:
                user_text = user_text[:-1]
            elif clicked:
                 user_text += event.unicode
            if event.key == pygame.K_BACKSPACE and clicked2 == True:
                user_text2 = user_text2[:-1]
            elif clicked2:
                    user_text2 += event.unicode

    if win == 0:
        screen.fill((255, 255, 255))
        if active:
            color = color_active
        else:
            color = color_passive
        if active2:
            color2 = color_active2
        else:
            color2 = color_passive2
        #draws everything
        drawplane()
        pygame.draw.circle(app_surf, (255, 0, 0), player_one['pygame_coords'], radius = 11, width = 11)
        pygame.draw.circle(app_surf, (0, 0, 255), player_two['pygame_coords'], radius = 11, width = 11)
        pygame.draw.circle(app_surf, (0, 150, 0), npc['pygame_coords'], radius = 11, width = 11)
        pygame.draw.circle(app_surf, 'black', destination['pygame_coords'], radius = 11, width = 11)
        pygame.draw.circle(app_surf, 'lightblue', player_one['pygame_coords'], radius = 10, width = 10)
        pygame.draw.circle(app_surf, 'lightblue', player_two['pygame_coords'], radius = 10, width = 10)
        pygame.draw.circle(app_surf, 'lightblue', npc['pygame_coords'], radius = 10, width = 10)
        pygame.draw.circle(app_surf, 'lightblue', destination['pygame_coords'], radius = 10, width = 10)
        app_surf_update(destination, player_one, player_two)
        pygame.draw.rect(app_surf, ("grey"), pygame.Rect(800, 0, 425, 840))
        pygame.draw.rect(app_surf, ("grey"), pygame.Rect(0, 0, 15, 840))
        pygame.draw.rect(app_surf, ("grey"), pygame.Rect(0, 0, 830, 15))
        pygame.draw.rect(app_surf, ("grey"), pygame.Rect(0, 825, 830, 15))
        pygame.draw.rect(app_surf, ("black"), pygame.Rect(14, 14, 787, 1))
        pygame.draw.rect(app_surf, ("black"), pygame.Rect(14, 14, 1, 812))
        pygame.draw.rect(app_surf, ("black"), pygame.Rect(800, 14, 1, 812))
        pygame.draw.rect(app_surf, ("black"), pygame.Rect(14, 825, 787, 1))
        pygame.draw.rect(app_surf, ("white"), pygame.Rect(814, 0, 800, 2000))
        pygame.draw.rect(app_surf, ("black"), pygame.Rect(813, -15, 1, 2000))
        pygame.draw.rect(app_surf, ("black"), pygame.Rect(889, 99, 102, 34))
        pygame.draw.rect(app_surf, ("black"), pygame.Rect(1039, 99, 102, 34))
        pygame.draw.rect(app_surf, ("black"), pygame.Rect(813, 300, 1000, 1))
        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+7.5))
        input_rect.w = max(100, 0)
        pygame.draw.rect(screen, color2, input_rect2)
        text_surface2 = base_font.render(user_text2, True, (255, 255, 255))
        screen.blit(text_surface2, (input_rect2.x+5, input_rect2.y+7.5))
        input_rect2.w = max(100, 0)
        if clicked:
            pygame.draw.line(screen, (255, 255, 255), (890+text_surface.get_width()+10, 132-5), (890+text_surface.get_width()+10, 100+5), 1)
        if clicked2:
            pygame.draw.line(screen, (255, 255, 255), (1040+text_surface2.get_width()+10, 132-5), (1040+text_surface2.get_width()+10, 100+5), 1)
            
        #text telling you what to input
        text_surface = my_font.render('Input Distance:', False, (0, 0, 0))
        screen.blit(text_surface, (890,80))
        text_surface = my_font.render('Input Direction:', False, (0, 0, 0))
        screen.blit(text_surface, (1040,80))
        pygame.draw.rect(app_surf, ("black"), pygame.Rect(1010-50, 200, 102, 34))
        pygame.draw.rect(app_surf, color3, pygame.Rect(1011-50, 201, 100, 32))
        
        #text saying which player's turn it is
        if player == 1:
            text_surface = error_font.render("Player One's turn:", False, (255, 0, 0))
        elif player == 2:
            text_surface = error_font.render("Player Two's turn:", False, (0, 0, 255))
        elif player == 3:
            text_surface = error_font.render("NPC's turn:  (NPC is ''thinking'')", False, (0, 150, 0))
        screen.blit(text_surface, (828,15))
        text_surface = button_font.render("Click to move", False, (255, 255, 255))
        screen.blit(text_surface, (1011-42.25,210))
        mouse_pos = pygame.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            color3 = color_active3
        else:
            color3 = color_passive3
        if user_text.isdigit() and user_text2.isdigit():
            distance = int(user_text)
            if distance < 5:
                #prints error messages
                text_surface = error_font.render('min distance value is 5', False, (255, 0, 0))
                screen.blit(text_surface, (910,150))
                text_surface = error_font.render('max directional value is 8 (min 1)', False, (255, 0, 0))
                screen.blit(text_surface, (880,170))
        if user_text2.isdigit():
            direction = int(user_text2)
        if user_text2.isdigit() and user_text.isdigit():
            if direction > 8 or direction < 1:
                #prints error messages
                text_surface = error_font.render('min distance value is 5', False, (255, 0, 0))
                screen.blit(text_surface, (910,150))
                text_surface = error_font.render('max directional value is 8 (min 1)', False, (255, 0, 0))
                screen.blit(text_surface, (880,170))
        if user_text.isdigit() == False or user_text2.isdigit() == False:
                #prints error messages 
                text_surface = error_font.render('You must input both values', False, (255, 0, 0))
                screen.blit(text_surface, (910,150))
                text_surface = error_font.render('correctly (as numeric values)', False, (255, 0, 0))
                screen.blit(text_surface, (910,170))
        if player == 1:
            #checks the time left on timer since the start of the players turn and if it is 0 seconds it will do the time penalty
            text_surface = error_font.render(f"Time Left: {10-((round(time.time_ns()/1000000000))-current)}", False, (255, 0, 0))
            screen.blit(text_surface, (1100,15))
            if 10-((round(time.time_ns()/1000000000))-current) == 0:
                np1px, np1py, np1cx, np1cy = p1rand()
                if plane.collidepoint(np1px, np1py):
                    current = round(time.time_ns()/1000000000)
                    player_one['pygame_coords'] = [np1px, np1py]
                    player_one['cartesian_coords'] = [np1cx, np1cy]
                    p1px = 0
                    p1py = 0
                    p1cx = 0
                    p1cy = 0
                    np1px = 0
                    np1py = 0
                    user_text = ''
                    user_text2 = ''
                    triple1 = 0
                    triple2 = 0
                    triple = 0
                    player = 2
                    dist = calculations.Distance.distance(point1=player_one['pygame_coords'], point2=player_two['pygame_coords'])
                    dist1 = calculations.Distance.distance(point1=player_one['pygame_coords'], point2=npc['pygame_coords'])
                    dist2 = calculations.Distance.distance(point1=player_one['pygame_coords'], point2=destination['pygame_coords'])
                    if dist <= 10 or dist1 <= 10 or dist2 <= 10:
                        win = 1
                else:
                    while plane.collidepoint(np1px, np1py) == False:
                        np1px, np1py, np1cx, np1cy = p1rand()
    
        if player == 2:
            #checks the time left on timer since the start of the players turn and if it is 0 seconds it will do the time penalty
            text_surface = error_font.render(f"Time Left: {10-((round(time.time_ns()/1000000000))-current)}", False, (0, 0, 255))
            screen.blit(text_surface, (1100,15))
            if 10-((round(time.time_ns()/1000000000))-current) == 0:
                np2px, np2py, np2cx, np2cy = p2rand()
                if plane.collidepoint(np2px, np2py):
                    current = round(time.time_ns()/1000000000)
                    player_two['pygame_coords'] = [np2px, np2py]
                    player_two['cartesian_coords'] = [np2cx, np2cy]
                    p2px = 0
                    p2py = 0
                    p2cx = 0
                    p2cy = 0
                    np2px = 0
                    np2py = 0
                    user_text = ''
                    user_text2 = ''
                    triple1 = 0
                    triple2 = 0
                    triple = 0
                    player = 3
                    dist = calculations.Distance.distance(point1=player_two['pygame_coords'], point2=player_one['pygame_coords'])
                    dist1 = calculations.Distance.distance(point1=player_two['pygame_coords'], point2=npc['pygame_coords'])
                    dist2 = calculations.Distance.distance(point1=player_two['pygame_coords'], point2=destination['pygame_coords'])
                    if dist <= 10 or dist1 <= 10 or dist2 <= 10:
                        win = 2
                else:
                    while plane.collidepoint(np2px, np2py) == False:
                        np2px, np2py, np2cx, np2cy = p2rand()
    
        if player == 3:
            #Does the npc movement
            if randtime[1] == False:
                randtime[0] = random.randint(1, 10)
                randtime[1] = True
            text_surface = error_font.render(f"Time Left: {10-((round(time.time_ns()/1000000000))-current)}", False, (0, 150, 0))
            screen.blit(text_surface, (1100,15))
            if ((round(time.time_ns()/1000000000))-current) == randtime[0]:
                np1px, np1py, np1cx, np1cy, do, distance, direction = npcrand()
                if plane.collidepoint(np1px, np1py):
                    current = round(time.time_ns()/1000000000)
                    npc['pygame_coords'] = [np1px, np1py]
                    npc['cartesian_coords'] = [np1cx, np1cy]
                    p1px = 0
                    p1py = 0
                    p1cx = 0
                    p1cy = 0
                    np1px = 0
                    np1py = 0
                    user_text = ''
                    user_text2 = ''
                    triple1 = 0
                    triple2 = 0
                    triple = 0
                    player = 1
                    randtime[1] = False
                    do[1] = False
                    dist = calculations.Distance.distance(point1=npc['pygame_coords'], point2=player_one['pygame_coords'])
                    dist = calculations.Distance.distance(point1=npc['pygame_coords'], point2=player_two['pygame_coords'])
                    dist2 = calculations.Distance.distance(point1=npc['pygame_coords'], point2=destination['pygame_coords'])
                    if dist <= 10 or dist1 <= 10 or dist2 <= 10:
                        win = 3
            else:
                while plane.collidepoint(np1px, np1py) == False:
                    np1px, np1py, np1cx, np1cy, do, distance, direction = npcrand()
        #checks if user input is valide and if so, does player movement script
        if user_text.isdigit() and user_text2.isdigit():
            distance = int(user_text)
            direction = int(user_text2)
            if player == 1:
                if distance >= 5 and direction <= 8 and direction >= 1:
                    p1px, p1py = player_one['pygame_coords'][0], player_one['pygame_coords'][1]
                    p1cx, p1cy = player_one['cartesian_coords'][0], player_one['cartesian_coords'][1]
                    triple1, triple2, direction = translator.Triple_Finder(distance, direction)
                    triple = [triple1, triple2]
                    move1, move2 = translator.Triple_to_Movement(triple, direction)
                    np1cx = p1cx+move1
                    np1cy = p1cy+move2
                    np1px, np1py = conv_cartesian_to_pygame_coords(np1cx, np1cy)
                    pygame.draw.line(screen, "black", (p1px, p1py), (np1px, np1py))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button.collidepoint(event.pos):
                            player_one['pygame_coords'] = [np1px, np1py]
                            player_one['cartesian_coords'] = [np1cx, np1cy]
                            p1px = 0
                            p1py = 0
                            p1cx = 0
                            p1cy = 0
                            np1px = 0
                            np1py = 0
                            user_text = ''
                            user_text2 = ''
                            triple1 = 0
                            triple2 = 0
                            triple = 0
                            player = 2
                            current = round(time.time_ns()/1000000000)
                            dist = calculations.Distance.distance(point1=player_one['pygame_coords'], point2=player_two['pygame_coords'])
                            dist1 = calculations.Distance.distance(point1=player_one['pygame_coords'], point2=npc['pygame_coords'])
                            dist2 = calculations.Distance.distance(point1=player_one['pygame_coords'], point2=destination['pygame_coords'])
                            if dist <= 10 or dist1 <= 10 or dist2 <= 10:
                                win = 1
            #checks if user input is valide and if so, does player movement script
            elif player == 2:
                if distance >= 5 and direction <= 8 and direction >= 1:
                    p2px, p2py = player_two['pygame_coords'][0], player_two['pygame_coords'][1]
                    p2cx, p2cy = player_two['cartesian_coords'][0], player_two['cartesian_coords'][1]
                    triple1, triple2, direction = translator.Triple_Finder(distance, direction)
                    triple = [triple1, triple2]
                    move1, move2 = translator.Triple_to_Movement(triple, direction)
                    np2cx = p2cx+move1
                    np2cy = p2cy+move2
                    np2px, np2py = conv_cartesian_to_pygame_coords(np2cx, np2cy)
                    pygame.draw.line(screen, "black", (p2px, p2py), (np2px, np2py))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button.collidepoint(event.pos):
                            player_two['pygame_coords'] = [np2px, np2py]
                            player_two['cartesian_coords'] = [np2cx, np2cy]
                            p2px = 0
                            p2py = 0
                            p2cx = 0
                            p2cy = 0
                            np2px = 0
                            np2py = 0
                            user_text = ''
                            user_text2 = ''
                            triple1 = 0
                            triple2 = 0
                            triple = 0
                            player = 3
                            current = round(time.time_ns()/1000000000)
                            dist = calculations.Distance.distance(point1=player_two['pygame_coords'], point2=player_one['pygame_coords'])
                            dist1 = calculations.Distance.distance(point1=player_two['pygame_coords'], point2=npc['pygame_coords'])
                            dist2 = calculations.Distance.distance(point1=player_two['pygame_coords'], point2=destination['pygame_coords'])
                            if dist <= 10 or dist1 <= 10 or dist2 <= 10:
                                win = 2
                                
        #prints player info
        print_player_info()
        
    #Shows player 1 win screen
    elif win == 1:
        mouse_pos = pygame.mouse.get_pos()
        if restartbutton.collidepoint(mouse_pos):
            color4 = color_active
        else:
            color4 = color_passive
        pygame.draw.rect(app_surf, ("white"), pygame.Rect(0, 0, 2000, 2000))
        text_surface = win_font.render('Player One Won!', False, (0, 0, 0))
        screen.blit(text_surface, (50,170))
        pygame.draw.rect(app_surf, ('black'), pygame.Rect(406.5, 499, 402, 102))
        pygame.draw.rect(app_surf, (color4), pygame.Rect(407.5, 500, 400, 100))
        text_surface = restartbutton_font.render('click to play again', False, (0, 0, 0))
        screen.blit(text_surface, (425.5,525))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restartbutton.collidepoint(event.pos):
                win = 0
                current = round(time.time_ns()/1000000000)
                player=1
                initialise_entities()
                
    
#shows player 2 win screen
    elif win == 2:
        mouse_pos = pygame.mouse.get_pos()
        if restartbutton.collidepoint(mouse_pos):
            color4 = color_active
        else:
            color4 = color_passive
        pygame.draw.rect(app_surf, ("white"), pygame.Rect(0, 0, 2000, 2000))
        text_surface = win_font.render('Player Two Won!', False, (0, 0, 0))
        screen.blit(text_surface, (50,170))
        pygame.draw.rect(app_surf, ('black'), pygame.Rect(406.5, 499, 402, 102))
        pygame.draw.rect(app_surf, (color4), pygame.Rect(407.5, 500, 400, 100))
        text_surface = restartbutton_font.render('click to play again', False, (0, 0, 0))
        screen.blit(text_surface, (425.5,525))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restartbutton.collidepoint(event.pos):
                win = 0
                current = round(time.time_ns()/1000000000)
                player=1
                initialise_entities()
#player 3 win screen
    elif win == 3:
        mouse_pos = pygame.mouse.get_pos()
        if restartbutton.collidepoint(mouse_pos):
            color4 = color_active
        else:
            color4 = color_passive
        pygame.draw.rect(app_surf, ("white"), pygame.Rect(0, 0, 2000, 2000))
        text_surface = win_font.render('NPC Won!', False, (0, 0, 0))
        screen.blit(text_surface, (300,170))
        pygame.draw.rect(app_surf, ('black'), pygame.Rect(406.5, 499, 402, 102))
        pygame.draw.rect(app_surf, (color4), pygame.Rect(407.5, 500, 400, 100))
        text_surface = restartbutton_font.render('click to play again', False, (0, 0, 0))
        screen.blit(text_surface, (425.5,525))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restartbutton.collidepoint(event.pos):
                win = 0
                current = round(time.time_ns()/1000000000)
                player=1
                initialise_entities()

    pygame.display.flip()
