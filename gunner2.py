import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shooter')
clock = pygame.time.Clock()

font  = pygame.font.Font('ofont.ru_Gnocchi.ttf', 20)
big_font = pygame.font.Font('ofont.ru_Gnocchi.ttf', 40)

player = pygame.Rect(370, 520, 60, 60)
player_image = pygame.image.load("assset1/images/player.png/500px-Donald_Trump_August_2015.jpg").convert()
player_image = pygame.transform.scale(player_image, (60, 60))
player_speed = 3

bullets = []
bullet_speed = 9

enemies = []
enemy_timer = 0




pygame.mixer.init()
pygame.mixer.music.load("assset1/sound1/bg_music.wav/02. Crazy Dave (Intro Theme).mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

try:
    hit_sound = pygame.mixer.Sound('assset1/sound1/hit.wav/mixkit-metal-hammer-hit-833.wav')
except:
    hit_sound = None


try:
    jump_sound = pygame.mixer.Sound('assset1/sound1/jump.wav/Voicy_Sonic-Jump-Sound.wav')
except:
    jump_sound = None


score = 0
game_over = False


player_vel_y = 0
gravity = 0.8
jump_boost = -15
on_ground = True
GROUND_Y = 520


BG = pygame.image.load("assset1/images/tiles.png/Flag_of_Iran.svg.png").convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

MENU = pygame.image.load("assset1/images/bg.png/mygamemenu.png").convert()
MENU = pygame.transform.scale(MENU, (WIDTH, HEIGHT))


def reset_game():
    global player, score, bullets, enemies, game_over

    bullets = []
    enemies = []
    score = 0
    game_over = False
    player.x = 370
    player.y = 520




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m and not game_over:
                bullet = pygame.Rect(player.right, player.centery - 5, 10, 20)
                bullets.append(bullet)
                if hit_sound: hit_sound.play()

            if event.key == pygame.K_SPACE:
                player_vel_y = jump_boost
                on_ground = False
                if jump_sound: jump_sound.play()


            if event.key == pygame.K_r and game_over == True:
                reset_game()





    if not game_over:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.left -= player_speed
        if keys[pygame.K_RIGHT]:
            player.right += player_speed

        if keys[pygame.K_UP]:
            player.top -= player_speed
        if keys[pygame.K_DOWN]:
            player.bottom += player_speed



        if player.top < 0:
            player.top = 0

        if player.bottom > HEIGHT:
            player.bottom = HEIGHT



        for b in bullets:
            b.x += bullet_speed
            if b.x > WIDTH:
                bullets.remove(b)

        player_vel_y += gravity
        player.y += player_vel_y

        if player.bottom >= GROUND_Y:
            player.bottom = GROUND_Y
            player_vel_y = 0
            on_ground = True




        enemy_timer += 1
        if enemy_timer >= 45:
            enemy_timer = 0
            y = random.randint(0, HEIGHT - 40)
            enemy = pygame.Rect(WIDTH, y, 40, 40)
            enemies.append(enemy)


        for e in enemies:
            e.x -= 4

            if e.colliderect(player):
                game_over = True

            if e.right < 0:
                enemies.remove(e)


        for e in enemies[:]:
            for b in bullets:
                if e.colliderect(b):
                    enemies.remove(e)
                    bullets.remove(b)
                    score += 1
                    break


    screen.blit(BG, (0, 0))

    pygame.draw.rect(screen, (0, 0, 0), (player.x, player.y, player.height, player.width))
    screen.blit(player_image, (player.x, player.y))

    for b in bullets:
        pygame.draw.rect(screen, (0, 0, 0), b)

    for e in enemies:
        pygame.draw.rect(screen, (128, 0, 0), e)

    screen.blit(font.render(f"SCORE: {score}", True, (255, 0, 255)), (100, 100))


    if game_over:
        t1 = big_font.render("GAME OVER", True, (0, 0, 255))
        t2 = big_font.render("PRESS R TO RESTART", True, (205, 2, 205))

        screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))


    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()





