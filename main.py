import pygame
import random


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.jumpCount = 10
        self.vel = 8
        self.hitbox = pygame.Rect(self.x + 10, self.y, width, height)

    def draw(self, window):
        window.blit(char, (self.x, self.y))
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def hit(self):
        self.x = 178
        self.y = screenHeight - 100
        font1 = pygame.font.SysFont('comicsans', 60)
        text = font1.render('Game Over', 1, (0, 0, 0))
        win.blit(text, (50, 160))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1



class Ball(object):
    def __init__(self, x, y, width, height, dx, dy):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hit_box = pygame.Rect(self.x, self.y, width, height)
        self.health = 10
        self.visible = True
        self.spawn_timer = 0
        self.spawn_frequency = 500
        self.dx = dx
        self.dy = dy

    def draw(self, window):
        if self.visible:
            window.blit(enemy, (self.x, self.y))
            self.move()
            self.hit_box.x = self.x
            self.hit_box.y = self.y

        if not self.visible:
            self.hit_box = (1000, 1000, 5, 5)

    def move(self):
        if self.hit_box[1] < 0 or self.hit_box[1] + 160 > screenHeight:
            self.dy *= -1
        if self.hit_box[0] < 0 or self.hit_box[0] + self.hit_box[3] > screenWidth:
            self.dx *= -1

        self.x += self.dx
        self.y += self.dy
        self.dy += GRAVITY

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

    def hit_player(self):
        self.x = random.randint(0, screenWidth - 140)
        self.y = random.randint(0, (screenWidth // 2) - 140)


def redraw_game_window(projectiles, balls):
    win.blit(bg, (0, 0))
    cannon.draw(win)
    for projectile in projectiles:
        projectile.draw(win)
    for ball in balls:
        ball.draw(win)
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (screenWidth // 2 - 55, 10))
    pygame.display.update()


class Projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = -10

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


pygame.init()

screenWidth = 400
screenHeight = 430

pygame.display.set_caption("My_game")
win = pygame.display.set_mode((screenWidth, screenHeight))

char = pygame.image.load("img/cannon.png")
bg = pygame.image.load("img/background.jpg")
enemy = pygame.image.load("img/ball.png")
score = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 30, True)
GRAVITY = .2

cannon = Player(178, screenHeight - 100, char.get_width(), char.get_height())
bullets = []
targets = [Ball(random.randint(0, screenWidth - 140),
                random.randint(0, (screenWidth // 2) - 140),
                enemy.get_width(), enemy.get_height(),
                random.randint(1, 2), 1)]
run = True
new_ball_timer = 10.0
while run:
    time_delta = clock.tick(30)/1000.0
    if new_ball_timer > 0.0:
        new_ball_timer -= time_delta
    else:
        new_ball_timer = 5.0
        targets.append(Ball(random.randint(0, screenWidth - 140),
                            random.randint(0, (screenWidth // 2) - 140),
                            enemy.get_width(), enemy.get_height(),
                            random.randint(1, 2), 1))

    for target in targets:
        if cannon.hitbox.colliderect(target.hit_box):
            cannon.hit()
            target.hit_player()
            score = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        for target in targets:
            if bullet.y - bullet.radius < target.hit_box[1] + target.hit_box[3] and bullet.y + bullet.radius > target.hit_box[1]:
                if bullet.x + bullet.radius > target.hit_box[0] and bullet.x - bullet.radius < target.hit_box[0] + target.hit_box[2]:
                    target.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    targets.remove(target)
        if 0 < bullet.y < 430:
            bullet.y += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if len(bullets) < 50:
            bullets.append(Projectile(round(cannon.x + cannon.width // 2), round(cannon.y), 6, (0, 0, 0)))
    if keys[pygame.K_LEFT] and cannon.x > cannon.vel:
        cannon.x -= cannon.vel
    if keys[pygame.K_RIGHT] and cannon.x < screenWidth - cannon.width:
        cannon.x += cannon.vel

    redraw_game_window(bullets, targets)

pygame.quit()
