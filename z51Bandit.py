#!/usr/bin/env python3

import pygame
import time
import random

pygame.init()

display_width = 1200
display_height = 800

black = (0,0,0)
white = (255,255,255)
c_blue = (28,133,238)
red = (255,0,0)
green = (70,250,0)
dark_green = (0,102,51)
blue = (0,0,255)
brown = (204,104,0)
grey = (192,192,192)

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Z51 Bandit')

clock = pygame.time.Clock()

z51Img = pygame.image.load('z51.png')
popoImg = pygame.image.load('popo.png')
blahImg = pygame.image.load('blah.png')
nsxImg = pygame.image.load('nsx.png')
obs_list = [popoImg, blahImg, nsxImg]
leftEdge = 170
rightEdge = display_width - leftEdge
lineWidth = 10
car_width = 80
obsLeft = leftEdge + lineWidth
obsRight = display_width - leftEdge - car_width

def car(x,y):
  gameDisplay.blit(z51Img, (x,y))

def obsticles(junker, obsx, obsy, obsw, obsh):
  gameDisplay.blit(junker, (obsx, obsy))

def grass():
  grassw = leftEdge
  grassh = display_height
  left_rect = pygame.Rect(0, 0, grassw, grassh)
  right_rect = pygame.Rect(rightEdge, 0, grassw, grassh)
  l_image = pygame.Surface((grassw, grassh))
  r_image = pygame.Surface((grassw, grassh))
  l_image.fill(dark_green)
  r_image.fill(dark_green)
  gameDisplay.blit(l_image, left_rect)
  gameDisplay.blit(r_image, right_rect)

def street_line(side):
  linew = lineWidth
  lineh = display_height
  if side == 'left':
    rect = pygame.Rect(leftEdge, 0, linew, lineh)
  if side == 'right':
    rect = pygame.Rect(rightEdge, 0, linew, lineh)
  image = pygame.Surface((linew, lineh))
  image.fill(white)
  gameDisplay.blit(image, rect)

def text_objects(text, font, color):
  textSurface = font.render(text, True, color)
  return textSurface, textSurface.get_rect()

def message_display(text):
  largeText = pygame.font.Font('freesansbold.ttf', 115)
  textSurf, textRect = text_objects(text, largeText, c_blue)
  textRect.center = ((display_width/2), (display_height/2))
  gameDisplay.blit(textSurf, textRect)
  pygame.display.update()
  time.sleep(2)
  game_loop()

def crash():
  message_display('You Crashed!')

def obs_passed(count):
  font = pygame.font.SysFont(None, 25)
  text = font.render("Passed: " + str(count), True, white)
  gameDisplay.blit(text, (3,3))

def z51_speed(count):
  font = pygame.font.SysFont(None, 25)
  text = font.render("Stingray Speed: " + str(count), True, green)
  gameDisplay.blit(text, (3,20))

def game_intro():
  intro = True
  while intro:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    gameDisplay.fill(red)
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    textSurf, textRect = text_objects("Z51 Bandit", largeText, c_blue)
    textRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    clock.tick(15)

def game_loop():
  x = (display_width * 0.43)
  y = (display_height * 0.80)
  x_change = 0
  myObs = obs_list[random.randrange(0, 3)]
  obs_startx = random.randrange(obsLeft, obsRight)
  obs_starty = -800
  obs_speed = 15
  obs_width = 80
  obs_height = 189
  game_exit = False
  passed = 0
  c7Speed = 65
#  game_intro()
  while not game_exit:
    for event in pygame.event.get():
      if event == pygame.QUIT:
        pygame.quit()
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          x_change = -10
        elif event.key == pygame.K_RIGHT:
          x_change = 10
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
          x_change = 0
    x += x_change
    gameDisplay.fill(grey)
# ^redraw
    grass()
    street_line('left')
    street_line('right')
    car(x,y)
    obs_passed(passed)
    z51_speed(c7Speed)
    obsticles(myObs, obs_startx, obs_starty, obs_width, obs_height)
    obs_starty += obs_speed
    if obs_starty > display_height + obs_height:
      passed += 1
      myObs = obs_list[random.randrange(0, 3)]
      if c7Speed < 200:
        c7Speed += 5
        obs_speed += 1
      obs_starty = 0 - obs_height
      obs_startx = random.randrange(obsLeft, obsRight)
# crash detection
    #if x > display_width - car_width or x < 0:
    if x > obsRight or x < obsLeft:
      crash()
    if y < obs_starty + obs_height - 10:
      x_right = x + car_width
      if x >= obs_startx and x <= obs_startx + obs_width or \
      x_right >= obs_startx and x_right <= obs_startx + obs_width:
        crash()
# redraw next line down
    pygame.display.update()
    clock.tick(60)

game_loop()
pygame.quit()
quit()

