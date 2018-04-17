import pygame
pygame.init()
import numpy as np
from pygame.locals import *
import math

base_damage = 10
bar_len = 150
bar_height = 25
dimensionality = 3
max_health = 50
FPS = 30

(WIDTH, HEIGHT) = (1000, 600)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

font=pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, black,
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, white,
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, white),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  pygame.font.init()
  current_string = ""
  display_box(screen, question + ": " + current_string)
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey <= 127:
      current_string+=chr(inkey)
    display_box(screen, question + ": " + current_string)
  return float(current_string)

def message_to_screen(msg,color,position):
	screen_text = font.render(msg, True, color)
	screen.blit(screen_text,position)
	
def text_to_button(msg,color,x,y,width,height):
	button_text = font.render(msg, True, color)
	screen.blit(button_text,[x,y+height/4])
	  
def num_button(color1, color2, x, y, width, height, var, varname):
	cur=pygame.mouse.get_pos()
	click=pygame.mouse.get_pressed()
	if x<cur[0]<x+width and y<cur[1]<y+height:
		pygame.draw.rect(screen,color1,(x,y,width,height))
		if click[0]:
			return True
	else:
		pygame.draw.rect(screen,color2,(x,y,width,height))
	string = varname + " = " + str(var)
	text_to_button(string,black,x,y,width,height)

def calc_damage(t1,t2):
	damage=0
	for i in range(len(t2)):
		damage+=(t2[i]-t1[i])**2
	damage = math.sqrt(damage/2)*base_damage
	return damage

class toxin:
	def __init__(self, tox_type):
		self.tox_type = tox_type
		
class health_bar:
	def __init__(self, hp):
		self.max_health=hp
		self.current_health=hp
		
	def draw(self,screen,p):
		full_len = bar_len*self.current_health/self.max_health
		if p==1:
			if full_len>0:
				pygame.draw.rect(screen, red, [50,30,full_len,bar_height])
				if full_len<bar_len:
					pygame.draw.rect(screen, white, [full_len+50,30,bar_len-full_len,bar_height])
		if p==2:
			if full_len>0:
				pygame.draw.rect(screen, red, [800,30,full_len,bar_height])
				if full_len<bar_len:
					pygame.draw.rect(screen, white, [full_len+800,30,bar_len-full_len,bar_height])
					
class cell:
	def __init__(self,p):
		tox_type = np.random.rand(dimensionality)
		self.color = 255*tox_type
		self.tox_mag = 0
		for t in tox_type:
			self.tox_mag+=t**2
		self.tox_mag=np.sqrt(self.tox_mag)
		tox = tox_type/self.tox_mag
		self.tox = toxin(tox)
		self.HB = health_bar(max_health)
		self.p=p
		if self.p==1:
			self.x = 75
		if self.p ==2:
			self.x = WIDTH-75
		self.y = HEIGHT-75
		
	def attack(self,target):
		damage=calc_damage(self.tox.tox_type,target.tox.tox_type)
		target.HB.current_health-=damage
		
	def normalize_tox(self,fixed):
		bc = 0
		for i in range(dimensionality):
			if i != fixed:
				bc+=self.tox.tox_type[i]**2
			else:
				a=1-self.tox.tox_type[i]**2
		d=a/bc
		for i in range(dimensionality):
			if i != fixed:
				self.tox.tox_type[i]*=np.sqrt(d)
		
	def draw(self,screen):
		pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], 40)
		self.HB.draw(screen,self.p)
				
def gameloop():
	c1 = cell(1)
	c2 = cell(2)
	cells = [c1,c2]
	running = True
	while running:	
		
		new_tox=[c1.tox.tox_type[0]*c1.tox_mag,c1.tox.tox_type[1]*c1.tox_mag,c1.tox.tox_type[2]*c1.tox_mag]
		Editor = False
		
		screen.fill(black)
		message_to_screen('Hit SPACE to attack or E to enter editor',red,(350,0))
		
		for ev in pygame.event.get():
			if ev.type == pygame.QUIT:
				running=False
			elif ev.type == KEYDOWN:
				if ev.key == pygame.K_ESCAPE:
					running=False
				elif ev.key == pygame.K_SPACE:
					c1.attack(c2)
				elif ev.key == pygame.K_e:
					Editor = True
				
		while Editor:
			editor_loop(c1,cells)
			for ev in pygame.event.get():
				if ev.type == pygame.QUIT:
					running=False
				elif ev.type == KEYDOWN:
					if ev.key == pygame.K_ESCAPE:
						c2.HB.current_health=c2.HB.max_health
						Editor=False
					elif ev.key == pygame.K_e:
						c2.HB.current_health=c2.HB.max_health
						Editor = False
			pygame.display.update()
			clock.tick(FPS)
					
		c1.draw(screen)
		c2.draw(screen)
		
		pygame.display.update()
		clock.tick(FPS)
	pygame.quit()
	quit()
	
def editor_loop(cell,cells):
	screen.fill(black)
	axis_len=400
	pygame.draw.rect(screen, red, [50,HEIGHT-50,axis_len,3])
	pygame.draw.rect(screen, red, [50,HEIGHT-(50+axis_len),3,axis_len])
	message_to_screen('X', red, [axis_len+50,HEIGHT-50])
	message_to_screen('Y', red, [55,HEIGHT-(50+axis_len)])
	message_to_screen('Toxin will renormalize after you have made your edit', red, [400,100])
	for c in cells:
		pygame.draw.circle(screen, c.color, [50+int(c.tox.tox_type[0]*axis_len), HEIGHT-(50+int(c.tox.tox_type[1]*axis_len))], 10)
	pygame.draw.circle(screen, white, [50, HEIGHT-50], axis_len, 3)
		
	button_pressed = num_button((0,255,0),white,WIDTH-230,HEIGHT-320,200,50,cell.tox.tox_type[0],"Element X")
	while button_pressed:
		message_to_screen('Enter a value between 0 and 1',red,(0,0))
		cell.tox.tox_type[0]=ask(screen,"Element X")
		cell.normalize_tox(0)
		button_pressed=False
	button_pressed = num_button((0,255,0),white,WIDTH-230,HEIGHT-220,200,50,cell.tox.tox_type[1],"Element Y")
	while button_pressed:
		message_to_screen('Enter a value between 0 and 1',red,(0,0))
		cell.tox.tox_type[1]=ask(screen,"Element Y")
		cell.normalize_tox(1)
		button_pressed=False
	button_pressed = num_button((0,255,0),white,WIDTH-230,HEIGHT-120,200,50,cell.tox.tox_type[2],"Element Z")
	while button_pressed:
		message_to_screen('Enter a value between 0 and 1',red,(0,0))
		cell.tox.tox_type[2]=ask(screen,"Element Z")
		cell.normalize_tox(2)
		button_pressed=False

gameloop()