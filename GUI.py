import pygame
from pygame.locals import *
import subprocess


# pm2 commands
cam_start = 'pm2 start 0'
cam_stop = 'pm2 stop 0'
cry_detect_start = 'pm2 start 1'
cry_detect_stop = 'pm2 stop 1'


pygame.init()
pygame.mouse.set_visible(True)
fpsclock = pygame.time.Clock()
fps = 60
pos = (0, 0)

size = width, height = 640, 480
black = 0, 0, 0
white = 255, 255, 255
screen = pygame.display.set_mode(size)


"""
Main Menu Components
"""
# switch on buttons:
switch_on_image = pygame.image.load("turn_on.png")
switch_on_size = (100, 60)

cam_switch_on_button = pygame.transform.scale(switch_on_image, switch_on_size)
cam_switch_on_rect = cam_switch_on_button.get_rect()

cry_switch_on_button = pygame.transform.scale(switch_on_image, switch_on_size)
cry_switch_on_rect = cry_switch_on_button.get_rect()


# switch off button:
switch_off_image = pygame.image.load("turn_off.png")
switch_off_size = (100, 60)

cam_switch_off_button = pygame.transform.scale(switch_off_image, switch_off_size)
cam_switch_off_rect = cam_switch_off_button.get_rect()

cry_switch_off_button = pygame.transform.scale(switch_off_image, switch_off_size)
cry_switch_off_rect = cry_switch_off_button.get_rect()


# define title
title_font = pygame.font.Font(None, 50)
title = {'Baby Monitor': (320, 50)}

# define buttons
my_font = pygame.font.Font(None, 40)
my_buttons = {'Monitor Screen': (230, 180), 'Sound Detection': (235, 280)}

image_buttons = {'Cry Image': (100, 420), 'Loud Sound Image': (500, 420)}

main_menu = True
camera_state = False
sound_state = False


"""
Image Menu Components
"""
image_size = (480, 360)
back_buttons = {'Back': (320, 450)}
cry_menu = False
loud_menu = False


"""
Start Menu in Loop
"""
# Main Menu:
while main_menu:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu = False

        if event.type == MOUSEBUTTONUP:

            # record new coordinates
            pos = pygame.mouse.get_pos()

            # mouse clicked on switch-off images
            if(cam_switch_off_rect.collidepoint(pos)):
                camera_state = not camera_state
                if camera_state == True:
                    subprocess.check_output(cam_start, shell=True)
                else:
                    subprocess.check_output(cam_stop, shell=True)

            if(cry_switch_off_rect.collidepoint(pos)):
                sound_state = not sound_state
                if sound_state == True:
                    subprocess.check_output(cry_detect_start, shell=True)
                else:
                    subprocess.check_output(cry_detect_stop, shell=True)


            # mouse clicked on image buttons
            if sound_state == True:
                for (my_text, rect) in image_buttons_rect.items():
                    if (rect.collidepoint(pos)):
                        # display cry image
                        if (my_text == 'Cry Image'):
                            cry_menu = True
                            while cry_menu:
                                screen.fill(white)

                                # draw back button
                                back_button_rect = {}
                                for my_text, text_pos in back_buttons.items():
                                    text_surface = my_font.render(my_text, True, black)
                                    rect = text_surface.get_rect(center=text_pos)
                                    screen.blit(text_surface, rect)
                                    back_button_rect[my_text] = rect

                                # load cry image
                                try:
                                    cry = pygame.image.load("cry.jpg")
                                    cry_image = pygame.transform.scale(cry, image_size)
                                    cry_image_rect = cry_image.get_rect()
                                    cry_image_rect.x, cry_image_rect.y = 80, 60
                                    screen.blit(cry_image, cry_image_rect)
                                except:
                                    pass

                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        cry_menu = False
                                        main_menu = False

                                    if event.type == MOUSEBUTTONUP:
                                        # record new coordinates
                                        pos = pygame.mouse.get_pos()
                                        # click back
                                        for (my_text, rect) in back_button_rect.items():
                                            if rect.collidepoint(pos):
                                                # display cry image
                                                if (my_text == 'Back'):
                                                    cry_menu = False

                                pygame.display.flip()

                        # display loud sound image
                        if my_text == 'Loud Sound Image':
                            loud_menu = True
                            while loud_menu:
                                screen.fill(white)

                                # draw back button
                                back_button_rect = {}
                                for my_text, text_pos in back_buttons.items():
                                    text_surface = my_font.render(my_text, True, black)
                                    rect = text_surface.get_rect(center=text_pos)
                                    screen.blit(text_surface, rect)
                                    back_button_rect[my_text] = rect

                                # load sound image
                                try:
                                    loud = pygame.image.load("loud_sound.jpg")
                                    loud_image = pygame.transform.scale(loud, image_size)
                                    loud_image_rect = loud_image.get_rect()
                                    loud_image_rect.x, loud_image_rect.y = 80, 60
                                    screen.blit(loud_image, loud_image_rect)
                                except:
                                    pass

                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        loud_menu = False
                                        main_menu = False

                                    if event.type == MOUSEBUTTONUP:
                                        # record new coordinates
                                        pos = pygame.mouse.get_pos()
                                        # click back
                                        for (my_text, rect) in back_button_rect.items():
                                            if rect.collidepoint(pos):
                                                # display loud image
                                                if (my_text == 'Back'):

                                                    loud_menu = False

                                pygame.display.flip()

    # draw title
    for my_text, text_pos in title.items():
        text_surface = title_font.render(my_text, True, black)
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)

    # draw function buttons
    my_buttons_rect = {}
    for my_text, text_pos in my_buttons.items():
        text_surface = my_font.render(my_text, True, black)
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
        my_buttons_rect[my_text] = rect

    # draw switch-off buttons initially
    if camera_state == False:
        cam_switch_off_rect.x, cam_switch_off_rect.y = 380, 150
        screen.blit(cam_switch_off_button, cam_switch_off_rect)

    if sound_state == False:
        cry_switch_off_rect.x, cry_switch_off_rect.y = 380, 250
        screen.blit(cry_switch_off_button, cry_switch_off_rect)

    if camera_state == True:
        cam_switch_on_rect.x, cam_switch_on_rect.y = 380, 150
        screen.blit(cam_switch_on_button, cam_switch_on_rect)

    image_buttons_rect = {}
    if sound_state == True:
        cry_switch_on_rect.x, cry_switch_on_rect.y = 380, 250
        screen.blit(cry_switch_on_button, cry_switch_on_rect)
        # draw image buttons
        for my_text, text_pos in image_buttons.items():
            text_surface = my_font.render(my_text, True, black)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
            image_buttons_rect[my_text] = rect

    # refresh dislpay
    pygame.display.flip()

# stop functions
if camera_state == True:
    subprocess.check_output(cam_stop, shell=True)

if sound_state == True:
    subprocess.check_output(cry_detect_stop, shell=True)

pygame.quit()










