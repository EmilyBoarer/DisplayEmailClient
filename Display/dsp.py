import pygame

W, H = 480, 320

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
running = True


message = """
look at these ducks!
""" ## TODO get from email
textcol = (0,0,0)
bgcol = (255,255,255)
gap = 10
fontsize = 30


font = pygame.font.SysFont("chilanka", 30)

screen.fill(bgcol)

lines = message.split("\n")
y = gap
while len(lines) > 0:
    line = lines.pop(0)
    if len(line) == 0: continue
    width, height = font.size(line)
    excess = []
    while width > W - 2*gap:
        l = line.split(" ")
        excess.insert(0, l[-1])
        line = " ".join(l[:-1])
        width, height = font.size(line)
    if len(excess) > 0: lines.insert(0," ".join(excess))
    t = font.render(line, True, textcol)
    screen.blit(t, ((W-width) // 2,y))
    y += height + gap

img = "test_img.JPG" ## TODO get from email, blank if nothing

if len(img) > 0:
    i = pygame.image.load(img)
    r = i.get_rect()
    h = H - y - gap
    ratio = h / r.height
    w = r.width * ratio
    screen.blit(pygame.transform.scale(i, (w, h)), ((W-w) // 2, y))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    # RENDER YOUR GAME HERE

    pygame.display.flip()
    clock.tick(10)
pygame.quit()