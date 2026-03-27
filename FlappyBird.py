import pygame
import random


RES = 800
SIZE = 50


pygame.init()
window = pygame.display.set_mode([RES, RES])
pygame.display.set_caption('FlappyBird')
clock = pygame.time.Clock()


front_score = pygame.font.SysFont("Arial", 26, bold=True)
front_end = pygame.font.SysFont("Arial", 66, bold=True)
front_start = pygame.font.SysFont("Arial", 46, bold=True)
front_restart = pygame.font.SysFont("Arial", 36, bold=True)


img_background = pygame.image.load("Image/background_free.png").convert_alpha()
img_bird_up = pygame.image.load("Image/bird_up.png").convert_alpha()
img_bird_down = pygame.image.load("Image/bird_down.png").convert_alpha()
img_post_up_head = pygame.image.load("Image/post_up_head.png").convert_alpha()
img_post_up_body = pygame.image.load("Image/post_up_body.png").convert_alpha()
img_post_down_head = pygame.image.load("Image/post_down_head.png").convert_alpha()
img_post_down_body = pygame.image.load("Image/post_down_body.png").convert_alpha()
img_clout= pygame.image.load("Image/cloud.png").convert_alpha()
img_solar= pygame.image.load("Image/solar_2.png").convert_alpha()
img_moon= pygame.image.load("Image/moon.png").convert_alpha()
img_solar_many= pygame.image.load("Image/solar_many.png").convert_alpha()


def start():
    global x, y, dx, dy, post, score, total, cloud, rgb, flag_day, solar, moon
    x, y = 100, 350
    dx, dy = 1, 0
    post = [[RES, 0, random.randrange(0, 300, SIZE)]]
    post.append([RES, post[-1][2]+300, RES])
    score = 0
    total = 100
    cloud = [[RES, random.randrange(0,400)]]
    rgb = [75, 75, 175]
    flag_day =  1
    solar = [RES, RES//3]
    moon = [2*RES+70,RES//3-10]


def first_start():
    windows_print()
    while True:
        
        pygame.display.flip()

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            break
        
        render_start = front_start.render(f"PRESS 'SPACE' TO START", 1, pygame.Color("black"))
        window.blit(render_start, (RES // 2 - 300, RES // 3))

        exit_game()
        clock.tick(10)


def windows_print():
    global x, y, dy, score, rgb, solar

    window.fill(rgb)
    img_solar_many.set_alpha(200-rgb[2])
    window.blit(img_solar_many, (0, 0))
    window.blit(img_solar_many, (0, 400))
    window.blit(img_background, (0, 0))

    window.blit(img_solar, (solar[0], solar[1]))
    window.blit(img_moon, (moon[0], moon[1]))

    for i in cloud:
        window.blit(img_clout, (i[0], i[1]))

    for i in post:
        if i[2]==RES:
            window.blit(img_post_up_head, (i[0], i[1]))
            for yy in range(i[1]+SIZE,i[2],SIZE):
                window.blit(img_post_up_body, (i[0], yy))
        else:
            window.blit(img_post_down_head, (i[0], i[2]))
            for yy in range(i[1],i[2],SIZE):
                window.blit(img_post_down_body, (i[0], yy))

    render_score = front_score.render(f"SCORE: {score}", 1, pygame.Color("black"))
    window.blit(render_score, (5, 5))

    if dy>=0:
        window.blit(img_bird_up, (x, y))
    else:
        window.blit(img_bird_down, (x, y))


def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    

def key_pr():
    global dy
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] and dy<-5:
        dy = 15
        return 'play'
    if key[pygame.K_r]:
        start()
        return 'restart'
    if key[pygame.K_ESCAPE]:
        exit()



def main():
    global x, y, dx, dy, post, score, total, rgb, flag_day, solar, moon
    
    start()
    first_start()

    while True:
        key_pr()
        windows_print()
        pygame.display.flip()

        if rgb[0]<1 or rgb[0]>150:
            flag_day*=-1
        rgb[0]+=0.05*flag_day
        rgb[1]+=0.05*flag_day
        rgb[2]+=0.05*flag_day
        solar[0]-=0.3
        solar[1]-=0.10*flag_day
        moon[0]-=0.3
        moon[1]+=0.10*flag_day
        if solar[0]<-70:
            solar = [2*RES+70,RES//3-10]
        if moon[0]<-70:
            moon = [2*RES+70,RES//3-10]
        

        if y+SIZE>RES-SIZE or y<0 or (
        post[0][0]-SIZE+10<=x<=post[0][0]+SIZE-20 and post[0][1]<=y-SIZE+5<=post[0][2]) or (
        post[1][0]-SIZE+10<=x<=post[1][0]+SIZE-20 and post[1][1]<=y+SIZE-5<=post[1][2]):
            while True:
                render_end = front_end.render(f"GAME OWER", 1, pygame.Color("red"))
                window.blit(render_end, (RES // 2 - 200, RES // 3))

                render_restart = front_restart.render(f"PRESS 'R' TO RESTART", 1, pygame.Color("grey"))
                window.blit(render_restart, (RES // 2 - 200, RES // 3 + 75))

                if key_pr()=='restart':
                    break
                pygame.display.flip()
                exit_game()

        key_pr()
        y-=dy
        dy-=1

        for i in range(len(cloud)):
            cloud[i][0] -= 1
        if len(cloud)>0 and cloud[0][0]==-400:
            cloud.pop(0)

        for i in range(len(post)):
            post[i][0]-=5

        if post[0][0]==-SIZE:
            dist = 950 - total
            post.append([post[-1][0]+dist, 0, random.randrange(0, 300, SIZE)])
            post.append([post[-2][0]+dist, post[-1][2]+300, RES])
            if score>=total and total != 700:
                total += 100
                post.append([post[-1][0]+dist, 0, random.randrange(0, 300, SIZE)])
                post.append([post[-2][0]+dist, post[-1][2]+300, RES])
            post.pop(0)
            post.pop(0)
            if random.randint(0,5)==0 :
                cloud.append([RES, random.randrange(0,400)])

        if post[0][0]-SIZE<=x<post[0][0]+SIZE and post[0][2]<=y<=post[1][1]:
            score += 1

        key_pr()
        clock.tick(50)
        exit_game()
    

if __name__=="__main__":
    main()