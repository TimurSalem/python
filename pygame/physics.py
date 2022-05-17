import pygame

pygame.init()
HW = 740
WW = 1200
win = pygame.display.set_mode((WW, HW))

pygame.display.set_caption("physic")

x = 200
y = 200

r = 40

width = r
height = r

vel = 10

taped = False

mousex = 0
mousey = 0

hr = 255
hg = 0
hb = 0

run = True

rs = False

xnext = 0
ynext = 0

gravity = 2

rebound_force = 0.6
environment_density = 10

while run:
	pygame.time.delay(10)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	keys = pygame.key.get_pressed()
	#
	# if keys[pygame.key.key_code('a')] and x > width:
	#     x -= vel
	#
	# if keys[pygame.key.key_code('d')] and x < WW - width:
	#     x += vel
	#
	# if keys[pygame.key.key_code('w')] and y > height / 1:
	#     y -= vel
	#
	if keys[pygame.key.key_code(' ')]:
		y = 350
		x = 500
		xnext = 0
		ynext = 0
	
	color = (255, 0, 0)
	#
	# speed_color_change = 1
	#
	# if hr == 255 and hb < 255 and hg == 0:
	#     hb += speed_color_change
	# elif hb == 255 and hr > 0:
	#     hr -= speed_color_change
	# elif hb == 255 and hr == 0 and hg < 255:
	#     hg += speed_color_change
	# elif hg == 255 and hb > 0:
	#     hb -= speed_color_change
	# elif hr < 255 and hg == 255 and hb == 0:
	#     hr += speed_color_change
	# elif hr == 255 and hg > 0:
	#     hg -= speed_color_change
	#
	# win.fill((hr // 3 + 150, hg // 3 + 150, hb // 3 + 150))
	#
	# color = (350 - (hr // 3 + 150), 350 - (hg // 3 + 150), 350 - (hb // 3 + 150))
	
	if (pygame.mouse.get_pressed()[0]
			and x - width < pygame.mouse.get_pos()[0] < x + width
			and y - height < pygame.mouse.get_pos()[1] < y + height):
		taped = True
	
	if not pygame.mouse.get_pressed()[0]:
		if taped:
			new_cursors_coords = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
			xnext = (new_cursors_coords[0] - old_cursor_coords[0]) * 8
			ynext = (new_cursors_coords[1] - old_cursor_coords[1]) * 8
		
		rs = False
		
		taped = False
	
	if taped:
		xnext = 0
		ynext = 0
		mousex = pygame.mouse.get_pos()[0]
		mousey = pygame.mouse.get_pos()[1]
		if not rs:
			
			rastx = (mousex - (x - width))
			rasty = (mousey - (y - height))
			rs = True
		
		else:
			x = mousex - rastx + width
			y = mousey - rasty + height
			
	'''Гравитация'''
	if y + height < HW and not taped:
		print(gravity)

		gravity = gravity + ((1 / gravity) * 10)
		print(gravity)
		ynext += gravity
	else:
		gravity = 2
		
	'''Гравитация'''

	if xnext:
		x += xnext / 10
		xnext -= xnext / (3 * environment_density)
	
	if ynext:
		y += ynext / 10
		ynext -= ynext / (3 * environment_density)
	
	if x + width >= WW:
		xnext = -xnext
		x = WW - width
		ynext *= rebound_force
		xnext *= rebound_force
	if y + height >= HW:
		ynext = -ynext
		y = HW - height
		ynext *= rebound_force
		xnext *= rebound_force
	if x - width <= 0:
		xnext = -xnext
		x = width
		ynext *= rebound_force
		xnext *= rebound_force
	if y - height <= 0:
		ynext = -ynext
		y = height
		ynext *= rebound_force
		xnext *= rebound_force
	
	win.fill((0, 0, 0))
	
	old_cursor_coords = (mousex, mousey)
	
	timer = pygame.time.Clock()
	timer.tick(60000000)
	
	# pygame.draw.circle(win, (10, 10, 10), (x, y), height + 5)
	pygame.draw.circle(win, (250, 250, 250), (x, y), height)
	pygame.display.update()

pygame.quit()
