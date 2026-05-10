import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shooter')
clock = pygame.time.Clock()

font  = pygame.font.Font('ofont.ru_Gnocchi.ttf', 20)
big_font = pygame.font.Font('ofont.ru_Gnocchi.ttf', 60)

player = pygame.Rect(370, 520, 60, 60)
player_image = pygame.image.load("персонаж.png").convert()
player_image = pygame.transform.scale(player_image, (60, 60))
player_speed = 3

bullets = []
bullet_speed = 9

enemies = []
enemy_timer = 0




pygame.mixer.init()
pygame.mixer.music.load("фоноваямузыка.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

try:
    hit_sound = pygame.mixer.Sound('звуквыстрела.wav')
except:
    hit_sound = None


try:
    jump_sound = pygame.mixer.Sound('звукпрыжка.wav')
except:
    jump_sound = None


try:
    death_song = pygame.mixer.Sound('музыкапроигрыша.mp3')
except:
    death_song = None


try:
    victory_song = pygame.mixer.Sound('песняпобеды.mp3')
except:
    victory_song = None




score = 0
game_over = False


player_vel_y = 0
gravity = 0.8
jump_boost = -15
on_ground = True
GROUND_Y = 520


BG = pygame.image.load("экрансамойигры.jpg").convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

VICTORY = pygame.image.load("экранпобеды.jpg").convert()
VICTORY = pygame.transform.scale(VICTORY, (WIDTH, HEIGHT))


DEFEAT = pygame.image.load("экрансмерти.png").convert()
DEFEAT = pygame.transform.scale(DEFEAT, (WIDTH, HEIGHT))

MENU = pygame.image.load("меню.webp").convert()
MENU = pygame.transform.scale(MENU, (WIDTH, HEIGHT))


def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            if MENU: screen.fill((255, 255, 255))
            title1 = big_font.render("The Infinite War", True, (205, 0, 20))
            title2 = big_font.render("PRESS ENTER TO START!", True, (205, 2, 0))

            screen.blit(title1, title1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 140)))
            screen.blit(title2, title2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
            pygame.display.update()
            clock.tick(60)





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
                bullet = pygame.Rect(player.right, player.centery - 5, 20, 20)
                bullet_image = pygame.image.load("пуля.png").convert()
                bullet_image = pygame.transform.scale(bullet_image, (20, 20))
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
            y = random.randint(0, HEIGHT - 60)
            enemy = pygame.Rect(WIDTH, y, 40, 40)
            enemy_image = pygame.image.load("враг.webp").convert()
            enemy_image = pygame.transform.scale(enemy_image, (40, 40))
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
        pygame.draw.rect(screen, (0, 0, 0), (b.x, b.y, 20, 20))
        screen.blit(bullet_image, (b.x, b.y))

    for e in enemies:
        pygame.draw.rect(screen, (128, 0, 0), (e.x, e.y, e.width, e.height))
        screen.blit(enemy_image, (e.x, e.y))

    screen.blit(font.render(f"SCORE: {score}", True, (128, 0, 0)), (100, 100))



    if score >= 15:

        screen.blit(VICTORY, (0, 0))
        hap = big_font.render("YOU WON!", True, (255, 0, 128))
        hap1 = big_font.render("Enough enemies defeated :D", True, (0, 128, 255))
        screen.blit(hap, hap.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200)))
        screen.blit(hap1, hap1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200)))
        if victory_song: victory_song.play()



    if game_over:
        screen.blit(DEFEAT, (0, 0))
        t1 = big_font.render("GAME OVER.", True, (205, 0, 20))
        t2 = big_font.render("PRESS R TO RESTART!", True, (205, 2, 0))

        screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 140)))
        screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        if death_song: death_song.play()


    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()





