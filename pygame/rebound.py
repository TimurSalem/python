import pygame

pygame.init()
HW = 740
WW = 1200
win = pygame.display.set_mode((WW, HW))

pygame.display.set_caption("rebound")

x = 200
y = 200

r = 40

width = r
height = r

vel = 10

taped = False

hr = 255
hg = 0
hb = 0

run = True

xmove = 0
ymove = 0

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
        xmove = 0
        ymove = 0

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
            xmove += (x - pygame.mouse.get_pos()[0])
            ymove += (y - pygame.mouse.get_pos()[1])
        taped = False
        
    if xmove != 0:
        x += xmove / 10
        xmove -= xmove / 30
        
    if ymove != 0:
        y += ymove / 10
        ymove -= ymove / 30
        
    if x + width >= WW:
        xmove = -xmove
        x = WW - width
        ymove *= 0.8
        xmove *= 0.8
        
    if y + height >= HW:
        ymove = -ymove
        y = HW - height
        ymove *= 0.8
        xmove *= 0.8
    if x - width <= 0:
        xmove = -xmove
        x = width
        ymove *= 0.8
        xmove *= 0.8
    if y - height <= 0:
        ymove = -ymove
        y = height
        ymove *= 0.8
        xmove *= 0.8
        
    win.fill((0, 0, 0))

    # pygame.draw.circle(win, (10, 10, 10), (x, y), height + 5)

    if taped:
        color = (320 - (hr // 3 + 150), 330 - (hg // 3 + 150), 320 - (hb // 3 + 150))
        pygame.draw.line(win, (250, 250, 250), (x, y), pygame.mouse.get_pos(), width=7)
        
    pygame.draw.circle(win, (250, 250, 250), (x, y), height)
    pygame.display.update()

pygame.quit()
