import pygame
import os
from eclient import update_saved_content

# temp for debugging:
# def update_saved_content():
#     pass

W, H = 480, 320

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
running = True

textcol = (0,0,0)
bgcol = (255,255,255)
gap = 10
fontsize = 30

font = pygame.font.SysFont("chilanka", fontsize)

def render_message():
    message = open("curr_message.txt").read()
    img = "" ## hacky by works:
    if os.path.exists("curr_img.JPG"):
        img = "curr_img.JPG"
    if os.path.exists("curr_img.jpg"):
        img = "curr_img.jpg"
    if os.path.exists("curr_img.jpeg"):
        img = "curr_img.jpeg"
    if os.path.exists("curr_img.png"):
        img = "curr_img.png"

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

    if len(img) > 0:
        i = pygame.image.load(img)
        r = i.get_rect()
        h = H - y - gap
        ratio = h / r.height
        w = r.width * ratio
        screen.blit(pygame.transform.scale(i, (w, h)), ((W-w) // 2, y))

def render_opts():
    screen.blit(font.render("Force Refresh", True, textcol), (50, 50))
    screen.blit(font.render("Shutdown Device", True, textcol), (50, 50+(50+fontsize)*1))

print("updating...")
update_saved_content()  # connect to email server
render_message()
print("updated")

counter = 0
fps = 10
checking_interval = 30  # seconds
state = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if state == 0:  # normal / display
                state = 1
                counter = 0  # reset timer
                screen.fill(bgcol)
                render_opts()

            elif state == 1:  # options menu
                if y < 50+30+25: # Force Refresh
                    print("force refreshing")
                    update_saved_content() ## connect to email server
                    state = 0
                    screen.fill(bgcol)
                    render_message()
                elif y < 50+30+50+30+25:
                    print("TODO: shutdown device")


    counter += 1
    if counter > checking_interval*fps:
        state = 0
        counter = 0
        print("updating...")
        update_saved_content() ## connect to email server
        screen.fill(bgcol)
        render_message()
        print("updated")

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()