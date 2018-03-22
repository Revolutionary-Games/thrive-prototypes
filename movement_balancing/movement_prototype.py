import pygame
pygame.init()
import numpy as np
from pygame.locals import *
import math

''' THINGS STILL TO DO
snap to hex grid when placing new elements
'''
#Constants
hex_size=15
#global_top_speed=10
#cytoplasm_mass=1
#nucleus_mass=7
#mitochondria_mass=2
#vacuole_mass=1
#ribosome_mass=3
#flagella_mass=0.5
#FPS=60
#force_flagella=0.1

#Hex moving
Up_0=np.array([0,-1*math.sqrt(3)*hex_size])
Down_0=np.array([0,math.sqrt(3)*hex_size])
Up_Right_0=np.array([math.sqrt(9)*hex_size/2,-1*math.sqrt(3)*hex_size/2])
Up_Left_0=np.array([-1*math.sqrt(9)*hex_size/2,-1*math.sqrt(3)*hex_size/2])
Down_Right_0=np.array([math.sqrt(9)*hex_size/2,math.sqrt(3)*hex_size/2])
Down_Left_0=np.array([-1*math.sqrt(9)*hex_size/2,math.sqrt(3)*hex_size/2])

Up=np.array([0,-1*math.sqrt(3)*hex_size])
Down=np.array([0,math.sqrt(3)*hex_size])
Up_Right=np.array([math.sqrt(9)*hex_size/2,-1*math.sqrt(3)*hex_size/2])
Up_Left=np.array([-1*math.sqrt(9)*hex_size/2,-1*math.sqrt(3)*hex_size/2])
Down_Right=np.array([math.sqrt(9)*hex_size/2,math.sqrt(3)*hex_size/2])
Down_Left=np.array([-1*math.sqrt(9)*hex_size/2,math.sqrt(3)*hex_size/2])

cell_angle = 0

#window setup
background_color = (0,0,0)
black = background_color
white = (255,255,255)
editor_background_color = (55,55,55)
(width, height) = (1000, 600)
screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_color)

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
  
def sigmoid(x):
	return 1/(1+np.exp(-x))

font=pygame.font.SysFont(None, 25)	

def message_to_screen(msg,color,position):
	screen_text = font.render(msg, True, color)
	screen.blit(screen_text,position)
	
def text_to_button(msg,color,x,y,width,height):
	button_text = font.render(msg, True, color)
	screen.blit(button_text,[x,y+height/4])
	
def draw_hex(color, position):
	pi2 = 2 * 3.14
	for i in range(0, 6):
		pygame.draw.line(screen, color, position, (math.cos(i / 6 * pi2) * hex_size + position[0], 
				math.sin(i / 6 * pi2) * hex_size + position[1]))
	return pygame.draw.lines(screen,color,True,[(math.cos(i / 6 * pi2) * hex_size + position[0], 
					math.sin(i / 6 * pi2) * hex_size + position[1]) for i in range(0, 6)])
	
def draw_nucleus(position):
	color = [128,0,128]
	draw_hex(color, position)
	draw_hex(color, position+Up)
	draw_hex(color, position+Down)
	draw_hex(color, position+Up_Left)
	draw_hex(color, position+Up_Right)
	draw_hex(color, position+Down_Left)
	draw_hex(color, position+Down_Right)

def draw_vacuole(position):
	color=[0,128,128]
	draw_hex(color, position)

def draw_cytoplasm(position):
	color=[40,128,40]
	draw_hex(color, position)

def draw_mitochondria(position,tilt):
	color=[255,20,147]
	draw_hex(color,position)
	if tilt==0:
		draw_hex(color,position+Up)
	elif tilt==60:
		draw_hex(color,position+Up_Right)
	elif tilt==120:
		draw_hex(color,position+Down_Right)

def draw_ribosomes(position):
	color = [255,140,0]
	draw_hex(color,position)
	draw_hex(color,position+Up_Left)
	draw_hex(color,position+Up_Right)

def draw_flagella(position):
	color = [255,255,255]
	draw_hex(color,position)
	
def adjust_tilt(tilt):
	if tilt==0:
		return 60
	elif tilt==60:
		return 120
	else:
		return 0

def draw_element(string, position, click):
	if string=='Flagella':
		draw_flagella(position)
	elif string=='Vacuole':
		draw_vacuole(position)
	elif string=='Cytoplasm':
		draw_cytoplasm(position)
	elif string=='Mitochondria':
		tilt=0
		if click[2]:
			tilt=adjust_tilt(tilt)
		draw_mitochondria(position,tilt)
		return tilt
	elif string=='Nucleus':
		draw_nucleus(position)
	elif string=='Ribosomes':
		draw_ribosomes(position)
		
def org_button(color1, color2, x, y, width, height,msg):
	cur=pygame.mouse.get_pos()
	click=pygame.mouse.get_pressed()
	if x<cur[0]<x+width and y<cur[1]<y+height:
		pygame.draw.rect(screen,color1,(x,y,width,height))
		if click[0]:
			return True
	else:
		pygame.draw.rect(screen,color2,(x,y,width,height))
	text_to_button(msg,black,x,y,width,height)
	
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
	
def draw_cell(organelle_list,position):
	pygame.draw.circle(screen, [0,0,255], (int(position[0]), int(position[1])), 3)
	for organelle in organelle_list:
		rel_pos = np.array([math.cos(cell_angle)*organelle[1][0]  - math.sin(cell_angle)*organelle[1][1],
							math.sin(cell_angle)*organelle[1][0] + math.cos(cell_angle)*organelle[1][1]])
		if organelle[0]=='Nucleus':
			draw_nucleus(position+rel_pos)
		elif organelle[0]=='Ribosomes':
			draw_ribosomes(position+rel_pos)
		elif organelle[0]=='Flagella':
			draw_flagella(position+rel_pos)
		elif organelle[0]=='Vacuole':
			draw_vacuole(position+rel_pos)
		elif organelle[0]=='Cytoplasm':
			draw_cytoplasm(position+rel_pos)
		elif organelle[0]=='Mitochondria':
			draw_mitochondria(position+rel_pos,organelle[2])

def v_lines(dx,height,width,step):
	for x in range(0,width,step):
		x += dx
		x = x % width
		pygame.draw.line(screen, (0,191,255), (x,0), (x,height))

def h_lines(dy,height,width,step):
	for y in range(0,height,step):
		y += dy
		y = y % height
		pygame.draw.line(screen, (0,191,255), (0,y), (width,y))

organelle_list =[]
#[['Nucleus', [0, 0]],['Ribosomes', 2*Down],['Vacuole',2*Down+Down_Right],
#['Mitochondria',2*Down+Down_Left,120],['Flagella',3*Down+Down_Left],['Flagella',3*Down+Down_Right]]

flagella_list = []
#[organelle_list[-1][1],organelle_list[-2][1]]

clock = pygame.time.Clock()

def gameloop():
	global Up, Down, Up_Right, Up_Left, Down_Right, Down_Left, cell_angle
	cell_position = np.array([0.5*width, 0.5*height])
	#Constants
	hex_size=15
	global_top_speed=8
	cytoplasm_mass=1
	nucleus_mass=7
	mitochondria_mass=2
	vacuole_mass=1
	ribosome_mass=3
	flagella_mass=0.5
	FPS=60
	force_flagella=2.2 #force of each flagella
<<<<<<< HEAD
	rate_of_turn = 0.5 #how fast should the cell turn?
=======
	rate_of_turn = 0.07 #how fast should the cell turn?
>>>>>>> 3be665d2d8a7142a938857ffee2a8b62502afaf8
	x_unit = math.sqrt(9)*hex_size/2
	y_unit = math.sqrt(3)*hex_size/2
	(center_mass_x,center_mass_y)=(0,0)
	(dx, dy) = (0, 0)
	
	running=True
	editor=True
	while running:	
		while editor:
			screen.fill(black)
			message_to_screen("Press ESC to leave editor",(255,0,0),(0,0))
			button_pressed=False
			cell_position=np.array([0.5*width, 0.5*height])
			button_pressed = org_button((0,255,0), white, 10, height-250, 120, 50, "Mitochondria")
			while button_pressed:
				screen.fill(black)
				message_to_screen("Press ESC to leave editor",(255,0,0),(0,0))
				message_to_screen("Press ENTER to place organelle",(255,0,0),(width-280,0))
				draw_cell(organelle_list,cell_position)
				cur=pygame.mouse.get_pos()-cell_position
				org_pos=(round(cur[0]/x_unit)*x_unit+cell_position[0],round(cur[1]/y_unit)*y_unit+cell_position[1])
				tilt=draw_element("Mitochondria",org_pos,pygame.mouse.get_pressed())
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == KEYDOWN:
						if event.key == pygame.K_RETURN:
							organelle_list.append(["Mitochondria",org_pos-cell_position,tilt])
							button_pressed=False
						elif event.key == pygame.K_ESCAPE:
							button_pressed = False
							
			button_pressed=org_button((0,255,0), white, 10, height-70, 120, 50, "Vacuole")
			while button_pressed:
				screen.fill(black)
				message_to_screen("Press ESC to leave editor",(255,0,0),(0,0))
				message_to_screen("Press ENTER to place organelle",(255,0,0),(width-280,0))
				draw_cell(organelle_list,cell_position)
				cur=pygame.mouse.get_pos()-cell_position
				org_pos=(round(cur[0]/x_unit)*x_unit+cell_position[0],round(cur[1]/y_unit)*y_unit+cell_position[1])
				draw_element("Vacuole",org_pos,pygame.mouse.get_pressed())
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == KEYDOWN:
						if event.key == pygame.K_RETURN:
							organelle_list.append(["Vacuole",org_pos-cell_position])
							button_pressed=False
						elif event.key == pygame.K_ESCAPE:
							button_pressed = False
							
			button_pressed=org_button((0,255,0), white, 10, height-130, 120, 50, "Flagella")
			while button_pressed:
				screen.fill(black)
				message_to_screen("Press ESC to leave editor",(255,0,0),(0,0))
				message_to_screen("Press ENTER to place organelle",(255,0,0),(width-280,0))
				draw_cell(organelle_list,cell_position)
				cur=pygame.mouse.get_pos()-cell_position
				org_pos=(round(cur[0]/x_unit)*x_unit+cell_position[0],round(cur[1]/y_unit)*y_unit+cell_position[1])
				draw_element("Flagella",org_pos,pygame.mouse.get_pressed())
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == KEYDOWN:
						if event.key == pygame.K_RETURN:
							organelle_list.append(["Flagella",org_pos-cell_position])
							flagella_list.append(org_pos-cell_position)
							button_pressed=False
						elif event.key == pygame.K_ESCAPE:
							button_pressed = False
							
			button_pressed=org_button((0,255,0), white, 10, height-190, 120, 50, "Cytoplasm")
			while button_pressed:
				screen.fill(black)
				message_to_screen("Press ESC to leave editor",(255,0,0),(0,0))
				draw_cell(organelle_list,cell_position)
				cur=pygame.mouse.get_pos()-cell_position
				org_pos=(round(cur[0]/x_unit)*x_unit+cell_position[0],round(cur[1]/y_unit)*y_unit+cell_position[1])
				draw_element("Cytoplasm",org_pos,pygame.mouse.get_pressed())
				message_to_screen("Press ENTER to place organelle",(255,0,0),(width-280,0))
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == KEYDOWN:
						if event.key == pygame.K_RETURN:
							organelle_list.append(["Cytoplasm",org_pos-cell_position])
							button_pressed=False
						elif event.key == pygame.K_ESCAPE:
							button_pressed = False
							
			button_pressed=org_button((0,255,0), white, 10, height-370, 120, 50, "Nucleus")
			while button_pressed:
				screen.fill(black)
				message_to_screen("Press ESC to leave editor",(255,0,0),(0,0))
				draw_cell(organelle_list,cell_position)
				cur=pygame.mouse.get_pos()-cell_position
				org_pos=(round(cur[0]/x_unit)*x_unit+cell_position[0],round(cur[1]/y_unit)*y_unit+cell_position[1])
				draw_element("Nucleus",org_pos,pygame.mouse.get_pressed())
				message_to_screen("Press ENTER to place organelle",(255,0,0),(width-280,0))
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == KEYDOWN:
						if event.key == pygame.K_RETURN:
							organelle_list.append(["Nucleus",org_pos-cell_position])
							button_pressed=False
						elif event.key == pygame.K_ESCAPE:
							button_pressed = False
			
			button_pressed=org_button((0,255,0), white, 10, height-310, 120, 50, "Ribosomes")
			while button_pressed:
				screen.fill(black)
				message_to_screen("Press ESC to leave editor",(255,0,0),(0,0))
				draw_cell(organelle_list,cell_position)
				cur=pygame.mouse.get_pos()-cell_position
				org_pos=(round(cur[0]/x_unit)*x_unit+cell_position[0],round(cur[1]/y_unit)*y_unit+cell_position[1])
				draw_element("Ribosomes",org_pos,pygame.mouse.get_pressed())
				message_to_screen("Press ENTER to place organelle",(255,0,0),(width-280,0))
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == KEYDOWN:
						if event.key == pygame.K_RETURN:
							organelle_list.append(["Ribosomes",org_pos-cell_position])
							button_pressed=False
						elif event.key == pygame.K_ESCAPE:
							button_pressed = False
							
			button_pressed = num_button((0,255,0),white,width-230,height-120,200,50,force_flagella,"force_flagella")
			while button_pressed:
				force_flagella=ask(screen,"force_flagella")
				button_pressed=False
			button_pressed = num_button((0,255,0),white,width-230,height-60,200,50,global_top_speed,"global_top_speed")
			while button_pressed:
				global_top_speed=ask(screen,"global_top_speed")
				button_pressed=False
			button_pressed = num_button((0,255,0),white,width-230,height-180,200,50,vacuole_mass,"vacuole_mass")
			while button_pressed:
				vacuole_mass=ask(screen,"vacuole_mass")
				button_pressed=False
			button_pressed = num_button((0,255,0),white,width-230,height-240,200,50,nucleus_mass,"nucleus_mass")
			while button_pressed:
				nucleus_mass=ask(screen,"nucleus_mass")
				button_pressed=False
			button_pressed = num_button((0,255,0),white,width-230,height-300,200,50,ribosome_mass,"ribosome_mass")
			while button_pressed:
				ribosome_mass=ask(screen,"ribosome_mass")
				button_pressed=False
			button_pressed = num_button((0,255,0),white,width-230,height-360,200,50,mitochondria_mass,"mitochondria_mass")
			while button_pressed:
				mitochondria_mass=ask(screen,"mitochondria_mass")
				button_pressed=False
			button_pressed = num_button((0,255,0),white,width-230,height-420,200,50,cytoplasm_mass,"cytoplasm_mass")
			while button_pressed:
				cytoplasm_mass=ask(screen,"cytoplasm_mass")
				button_pressed=False
			button_pressed = num_button((0,255,0),white,width-230,height-480,200,50,flagella_mass,"flagella_mass")
			while button_pressed:
				flagella_mass=ask(screen,"flagella_mass")
				button_pressed=False
			button_pressed = num_button((0,255,0),white,width-230,height-540,200,50,rate_of_turn,"rate_of_turn")
			while button_pressed:
				rate_of_turn=ask(screen,"rate_of_turn")
				button_pressed=False
			
			draw_cell(organelle_list,[0.5*width, 0.5*height])
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running=False
				elif event.type == KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						cell_position = np.array([0.5*width, 0.5*height])
						num_flagella=0
						weight=0
						size=0
						inertia=0
						for organelle in organelle_list:
							if organelle[0]=='Nucleus':
								size+=7
								weight+=nucleus_mass
								center_mass_x+=organelle[1][0]*nucleus_mass
								center_mass_y+=organelle[1][1]*nucleus_mass
							elif organelle[0]=='Ribosomes':
								size+=3
								weight+=ribosome_mass
								center_mass_x+=organelle[1][0]*ribosome_mass/3
								center_mass_y+=organelle[1][1]*ribosome_mass/3
								center_mass_x+=(organelle[1]+Up_Left)[0]*ribosome_mass/3
								center_mass_y+=(organelle[1]+Up_Left)[1]*ribosome_mass/3
								center_mass_x+=(organelle[1]+Up_Right)[0]*ribosome_mass/3
								center_mass_y+=(organelle[1]+Up_Right)[1]*ribosome_mass/3
							elif organelle[0]=='Flagella':
								num_flagella+=1
								weight+=flagella_mass
								center_mass_x+=organelle[1][0]*flagella_mass
								center_mass_y+=organelle[1][1]*flagella_mass
							elif organelle[0]=='Vacuole':
								size+=1
								weight+=vacuole_mass
								center_mass_x+=organelle[1][0]*vacuole_mass
								center_mass_y+=organelle[1][1]*vacuole_mass
							elif organelle[0]=='Cytoplasm':
								size+=1
								weight+=cytoplasm_mass
								center_mass_x+=organelle[1][0]*cytoplasm_mass
								center_mass_y+=organelle[1][1]*cytoplasm_mass
							elif organelle[0]=='Mitochondria':
								size+=2
								weight+=mitochondria_mass
								center_mass_x+=organelle[1][0]*mitochondria_mass
								center_mass_y+=organelle[1][1]*mitochondria_mass
						center_mass_x=center_mass_x/weight
						center_mass_y=center_mass_y/weight
<<<<<<< HEAD
						#Calculate inertia
						for organelle in organelle_list:
							if organelle[0]=='Nucleus':
								inertia+=nucleus_mass*((organelle[1][0]-center_mass_x)**2+(organelle[1][1]-center_mass_y)**2)
							elif organelle[0]=='Ribosomes':
								inertia+=ribosome_mass*((organelle[1][0]-center_mass_x)**2+(organelle[1][1]-center_mass_y)**2)/3
								inertia+=ribosome_mass*((organelle[1][0]+Up_Left[0]-center_mass_x)**2+(organelle[1][1]+Up_Left[1]-center_mass_y)**2)/3
								inertia+=ribosome_mass*((organelle[1][0]+Up_Right[0]-center_mass_x)**2+(organelle[1][1]+Up_Right[1]-center_mass_y)**2)/3
							elif organelle[0]=='Flagella':
								inertia+=flagella_mass*((organelle[1][0]-center_mass_x)**2+(organelle[1][1]-center_mass_y)**2)
							elif organelle[0]=='Vacuole':
								inertia+=vacuole_mass*((organelle[1][0]-center_mass_x)**2+(organelle[1][1]-center_mass_y)**2)
							elif organelle[0]=='Cytoplasm':
								inertia+=cytoplasm_mass*((organelle[1][0]-center_mass_x)**2+(organelle[1][1]-center_mass_y)**2)
							elif organelle[0]=='Mitochondria':
								inertia+=mitochondria_mass*((organelle[1][0]-center_mass_x)**2+(organelle[1][1]-center_mass_y)**2)
=======
>>>>>>> 3be665d2d8a7142a938857ffee2a8b62502afaf8
						#y = 0.5/(1+size)
						y = 0.1
						x_w=0
						x_a=0
						x_d=0
						x_s=0
						torque=0
						for flagella in flagella_list:
							#normalised flagella forces, otherwise flagella further away add more force
							flag_loc = np.array([center_mass_x,center_mass_y])-flagella
							flag_loc_normalised = flag_loc/(math.sqrt(flag_loc[0]**2 + flag_loc[1]**2))
							force_dir = force_flagella*(flag_loc_normalised)/weight
							x_w+=np.abs(min(float(force_dir[1]),0))
							x_s+=np.abs(max(float(force_dir[1]),0))
							x_a+=np.abs(min(float(force_dir[0]),0))
							x_d+=np.abs(max(float(force_dir[0]),0))
							torque+=np.sqrt((flag_loc[0]**2+flag_loc[1]**2))*force_flagella
						
						speed_w=global_top_speed*((1-y)*sigmoid(15*(x_w-0.33))+y)
						speed_a=global_top_speed*((1-y)*sigmoid(15*(x_a-0.33))+y)
						speed_d=global_top_speed*((1-y)*sigmoid(15*(x_d-0.33))+y)
						speed_s=global_top_speed*((1-y)*sigmoid(15*(x_s-0.33))+y)

						editor=False
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running=False
			elif event.type == KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running=False
				if event.key == pygame.K_e:
					cell_angle = 0
					editor = True
		
		mouse_pos = pygame.mouse.get_pos()
		mouse_angle = math.atan2(mouse_pos[1] - cell_position[1], mouse_pos[0] - cell_position[0]) + math.pi/2
		#added smooth turning code
		turn = mouse_angle - cell_angle
		#keep all angles in [-pi, pi]
		if turn < -math.pi:
			turn += math.pi*2
		if turn > math.pi:
			turn -= math.pi*2
		#add some amount of the turn
		if editor == False:
<<<<<<< HEAD
			cell_angle += rate_of_turn*(turn)*torque/inertia
=======
			cell_angle += rate_of_turn*(turn)
>>>>>>> 3be665d2d8a7142a938857ffee2a8b62502afaf8

		#keep angle in the right range
		if cell_angle < -math.pi:
			cell_angle += math.pi*2
		if cell_angle > math.pi:
			cell_angle -= math.pi*2


		#update the draw directions
		rotation = np.array([[math.cos(cell_angle), -math.sin(cell_angle)], 
							[math.sin(cell_angle), math.cos(cell_angle)]])

		
		Up=rotation.dot(Up_0)
		Down=rotation.dot(Down_0)
		Up_Right=rotation.dot(Up_Right_0)
		Up_Left=rotation.dot(Up_Left_0)
		Down_Right=rotation.dot(Down_Right_0)
		Down_Left=rotation.dot(Down_Left_0)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			dy+=math.cos(cell_angle)*speed_w
			dx-=math.sin(cell_angle)*speed_w 
		if keys[pygame.K_s]:
			dy-=math.cos(cell_angle)*speed_s
			dx+=math.sin(cell_angle)*speed_s 
		if keys[pygame.K_d]:
			dx-=math.cos(cell_angle)*speed_d
			dy-=math.sin(cell_angle)*speed_d
		if keys[pygame.K_a]:
			dx+=math.cos(cell_angle)*speed_a
			dy+=math.sin(cell_angle)*speed_a
			
		(dx,dy)=(dx % width, dy % height)
		
		'''I decided to move the background instead of the cell'''
		#if((cell_position[0]>width and dx>0) or (cell_position[0]<0 and dx<0)):
		#	dx=0
		#if((cell_position[1]>height and dy>0) or (cell_position[1]<0 and dy<0)):
		#	dy=0
		#cell_position = cell_position +np.array([dx, dy])
		
		speed_w_str = "speed_w = " + str(speed_w)
		speed_a_str = "speed_a = " + str(speed_a)
		speed_s_str = "speed_s = " + str(speed_s)
		speed_d_str = "speed_d = " + str(speed_d)
		cell_mass_str = "cell_mass = " + str(weight)
		cell_size_str = "cell_size = " + str(size)
		
		screen.fill(background_color)
		v_lines(dx,height,width,int(6*y_unit))
		h_lines(dy,height,width,int(6*y_unit))
		
		message_to_screen("Press ESC to leave test drive",(255,0,0),(0,0))
		message_to_screen("Press E to enter editor",(255,0,0),(width-250,0))
		message_to_screen(speed_w_str,(255,0,0),(0,height-20))
		message_to_screen(speed_a_str,(255,0,0),(0,height-50))
		message_to_screen(speed_s_str,(255,0,0),(0,height-80))
		message_to_screen(speed_d_str,(255,0,0),(0,height-110))
		message_to_screen(cell_mass_str,(255,0,0),(0,height-140))
		message_to_screen(cell_size_str,(255,0,0),(0,height-170))
		
		draw_cell(organelle_list,cell_position)
		pygame.display.update()
		clock.tick(FPS)

	pygame.quit()
	quit()
gameloop()