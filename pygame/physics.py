import pygame

pygame.init()
HW = 740
WW = 1200
win = pygame.display.set_mode((WW, HW))

pygame.display.set_caption("physic")

x = 200
y = 200

r = 40

taped = False

mousex = 0
mousey = 0

run = True
rs = False

xnext = 0
ynext = 0

rastx = 0
rasty = 0

gravity = 2

rebound_force = 0.6
environment_density = 10
old_cursor_coords = (0, 0)

while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	keys = pygame.key.get_pressed()
	
	if keys[pygame.key.key_code(' ')]:
		y = 350
		x = 500
		xnext = 0
		ynext = 0
	
	color = (255, 0, 0)
	
	if (
			pygame.mouse.get_pressed()[0]
			and x - r < pygame.mouse.get_pos()[0] < x + r
			and y - r < pygame.mouse.get_pos()[1] < y + r):
		taped = True
	
	if not pygame.mouse.get_pressed()[0]:
		if taped:
			new_cursors_coords = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
			xnext = (
				abs((new_cursors_coords[0] - old_cursor_coords[0])) ** 0.75 * 15
				if new_cursors_coords[0] - old_cursor_coords[0] > 0
				else -abs((new_cursors_coords[0] - old_cursor_coords[0])) ** 0.75 * 15
			)
			ynext = (
				abs((new_cursors_coords[1] - old_cursor_coords[1])) ** 0.75 * 15
				if new_cursors_coords[1] - old_cursor_coords[1] > 0
				else -abs((new_cursors_coords[1] - old_cursor_coords[1])) ** 0.75 * 15
			)
		
		rs = False
		taped = False
	
	if taped:
		xnext = 0
		ynext = 0
		mousex = pygame.mouse.get_pos()[0]
		mousey = pygame.mouse.get_pos()[1]
		if not rs:
			
			rastx = (mousex - (x - r))
			rasty = (mousey - (y - r))
			rs = True
		
		else:
			x = mousex - rastx + r
			y = mousey - rasty + r
	
	'''gravity'''
	if y + r < HW and not taped:
		gravity = gravity + ((1 / gravity) * 10)
		ynext += gravity
	else:
		gravity = 2
	'''gravity'''
	
	if xnext:
		x += xnext / 10
		xnext -= xnext / (3 * environment_density)
	
	if ynext:
		y += ynext / 10
		ynext -= ynext / (3 * environment_density)
	
	if x + r >= WW:
		xnext = -xnext
		x = WW - r
		ynext *= rebound_force
		xnext *= rebound_force
	if y + r >= HW:
		ynext = -ynext
		y = HW - r
		ynext *= rebound_force
		xnext *= rebound_force
	if x - r <= 0:
		xnext = -xnext
		x = r
		ynext *= rebound_force
		xnext *= rebound_force
	if y - r <= 0:
		ynext = -ynext
		y = r
		ynext *= rebound_force
		xnext *= rebound_force
	
	win.fill((0, 0, 0))
	
	old_cursor_coords = (mousex, mousey)
	
	timer = pygame.time.Clock()
	timer.tick(99 ** 3)
	
	pygame.draw.circle(win, (250, 250, 250), (x, y), r)
	pygame.display.update()

pygame.quit()
