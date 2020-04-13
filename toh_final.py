import pygame, sys, time

pygame.init()
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

game_done = False
framerate = 60


steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0
tower_list=[0,0,0]


white = (246, 246, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 179, 255)
grey = (170, 170, 170)
green = (77, 206, 145)

def put_text(screen, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    if font is None:
        font = pygame.font.SysFont(font_name, size)
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

def menu_screen():
    global screen, n_disks, game_done
    menu_done = False
    while not menu_done:
        screen.fill(white)
        put_text(screen, 'Towers of Hanoi', (323,72), font_name='sans serif', size=90, color=black)
        put_text(screen, 'Towers of Hanoi', (320,70), font_name='sans serif', size=90, color=blue)
        put_text(screen, 'game and solution', (323,135), font_name='sans serif', size=60, color=black)
        put_text(screen, 'game and solution', (320,133), font_name='sans serif', size=60, color=blue)

        put_text(screen, 'Use arrow keys to select number of disks:', (320, 230), font_name='sans serif', size=30, color=black)
        put_text(screen, str(n_disks), (320, 270), font_name='sans serif', size=40, color=blue)
        put_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans_serif', size=30, color=black)
        pygame.draw.rect(screen, grey, pygame.Rect(0, 450, 640 , 3))
        put_text(screen, 'A: About', (320, 460), font_name='sans serif', size=30, color=black)

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    show_about()
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 7:
                        n_disks = 7
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
        pygame.display.flip()
        clock.tick(60)

def show_about():
    screen.fill(white)
    put_text(screen, 'Towers of Hanoi', (323,72), font_name='sans serif', size=90, color=black)
    put_text(screen, 'Towers of Hanoi', (320,70), font_name='sans serif', size=90, color=blue)
    put_text(screen, 'game and solution', (323,135), font_name='sans serif', size=60, color=black)
    put_text(screen, 'game and solution', (320,133), font_name='sans serif', size=60, color=blue)

    put_text(screen, 'Project by:', (320,220), font_name='sans serif', size=30, color=black)
    put_text(screen, 'Nikith Kumar Shetty', (320,270), font_name='sans serif', size=30, color=black)
    put_text(screen, 'Natesh S', (320,290), font_name='sans serif', size=30, color=black)
    put_text(screen, 'Nithin Kumar', (320,310), font_name='sans serif', size=30, color=black)
    put_text(screen, 'Prasad', (320,330), font_name='sans serif', size=30, color=black)
    put_text(screen, 'Press any key to continue', (320, 400), font_name='mono', size=20, color=black)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                reset()

def make_disks():
    global n_disks, disks, tower_list
    tower_list=[n_disks,0,0]
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 23
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)
        disk['val'] = i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height+3
        width -= 23

def draw_towers():
    global screen
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(screen, green, pygame.Rect(xpos, 400, 160 , 20))
        pygame.draw.rect(screen, grey, pygame.Rect(xpos+75, 200, 10, 200))
    put_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    put_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)

def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, blue, disk['rect'])
    return

def draw_ptr():
    ptr_points = [(towers_midx[pointing_at]-7 ,440), (towers_midx[pointing_at]+7, 440), (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, red, ptr_points)
    return

def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        game_over()

def reset():
    global steps,pointing_at,floating,floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()

def game_over():
    global screen, steps
    screen.fill(white)
    min_steps = 2**n_disks-1
    put_text(screen, 'You Won!', (320, 200), font_name='sans serif', size=72, color=black)
    put_text(screen, 'You Won!', (322, 202), font_name='sans serif', size=72, color=blue)
    put_text(screen, 'Your Steps: '+str(steps), (320, 360), font_name='mono', size=30, color=black)
    put_text(screen, 'Minimum Steps: '+str(min_steps), (320, 390), font_name='mono', size=30, color=red)
    if min_steps==steps:
        put_text(screen, 'You finished in minumum steps!', (320, 300), font_name='mono', size=26, color=blue)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

def show_solution():
    global steps,n_disks
    steps=0
    make_disks()
    display()
    time.sleep(0.5)
    solution(n_disks,0,2,1)
    screen.fill(white)
    put_text(screen, 'Completed in '+str(steps)+' Steps', (318, 18), font_name='sans serif', size=40, color=black)
    put_text(screen, 'Completed in '+str(steps)+' Steps', (320, 20), font_name='sans serif', size=40, color=blue)
    put_text(screen, 'Press any key to continue', (318, 77), font_name='mono', size=20, color=black)
    draw_towers()
    draw_disks()
    pygame.display.flip()
    clock.tick(framerate)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                steps=0
                pointing_at=0
                floater=0
                make_disks()
                return

def solution(disk_number,frm,to,aux):
    if(disk_number==1):
        move(1,frm,to)
    else:
        solution(disk_number-1,frm,aux,to)
        move(disk_number,frm,to)
        solution(disk_number-1,aux,to,frm)
    return

def move(disk_number,source,dest):
    global tower_list,disks,steps
    steps+=1
    disk_number-=1
    # print("moving",disk_number, "from",source,dest)
    disks[::-1][disk_number]['rect'].midtop=(towers_midx[source],100)
    display()
    time.sleep(0.5)
    if(source<dest):
        i=1
        while(source+i<=dest):
            disks[::-1][disk_number]['rect'].midtop=(towers_midx[source+i],100)
            display()
            time.sleep(0.5)
            i+=1
    else:
        i=1
        while(source-i>=dest):
            disks[::-1][disk_number]['rect'].midtop=(towers_midx[source-i],100)
            display()
            time.sleep(0.5)
            i+=1
    disks[::-1][disk_number]['rect'].midtop=(towers_midx[dest],377-(23*tower_list[dest]))
    display()
    time.sleep(0.75)

    tower_list[source]-=1
    tower_list[dest]+=1

def display():
    screen.fill(white)
    put_text(screen, 'Solution ', (318, 18), font_name='sans serif', size=47, color=black)
    put_text(screen, 'Solution ', (320, 20), font_name='sans serif', size=47, color=blue)
    put_text(screen, 'Step: '+str(steps), (320, 50), font_name='mono', size=30, color=black)
    draw_towers()
    draw_disks()
    pygame.display.flip()
    clock.tick(framerate)

menu_screen()
make_disks()

while not game_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset()
            if event.key == pygame.K_q:
                game_done = True
            if event.key == pygame.K_s:
                show_solution()
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at+1)%3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_LEFT:
                pointing_at = (pointing_at-1)%3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_UP and not floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break
            if event.key == pygame.K_DOWN and floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                        if disk['val']<disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                            steps += 1
                        break
                else:
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                    steps += 1
    screen.fill(white)
    draw_towers()
    draw_disks()
    draw_ptr()
    put_text(screen, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
    pygame.draw.rect(screen, grey, pygame.Rect(0, 450, 640 , 3))
    put_text(screen, 'esc: Main Menu        S: Solution', (320, 460), font_name='sans serif', size=30, color=black)
    pygame.display.flip()
    if not floating:check_won()
    clock.tick(framerate)
