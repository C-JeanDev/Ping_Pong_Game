import pygame


class Player():

    def __init__(self, win, x: int, y: int, mode: int) -> None:

        self.win = win
        self.width = 20
        self.height = 100

        self.mode = mode

        self.x = x
        self.y = y

        self.vel = 5

    def draw(self) -> None:
        self.command()
        pygame.draw.rect(
            self.win, WHITE, (self.x, self.y, self.width, self.height))

    def command(self) -> None:
        if self.mode == 1:
            if keys[pygame.K_w] and self.y > 0:
                self.y -= self.vel
            if keys[pygame.K_s] and self.y < win_height - self.height:
                self.y += self.vel
        elif self.mode == 2:
            if keys[pygame.K_UP] and self.y > 0:
                self.y -= self.vel
            if keys[pygame.K_DOWN] and self.y < win_height - self.height:
                self.y += self.vel


class Ball:

    MAX_VEL = 5

    def __init__(self, x: int, y: int, radius: int) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win) -> None:
        if not (self.check()):
            self.x: int = win_width//2
            self.y: int = win_height//2
        
        if self.x == win_width//2 and self.y == win_height//2:
            ball.y_vel = 0        
            
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def check(self) -> bool:
        if self.x > win_width or self.x < 0:
            return False
        if self.y > win_height or self.y < 0:
            return False
        return True

    def point_system(self, win):
        # se la posizione della palla e' maggiore di win_width il punto va al player di sinistra
        # se la posizione della palla e' minore di 0 il punto va al player di destra
        global left_point
        global right_point
        if self.x > win_width:
            left_point += 1
        elif self.x < 0:
            right_point += 1

        fnt = pygame.font.SysFont("Arial", 40, bold=True)

        t1 = fnt.render(str(left_point), True, "white")
        t2 = fnt.render(str(right_point), True, "white")

        win.blit(t1, (200, 0))
        win.blit(t2, (600, 0))


def collision(ball, player1, player2):
    if ball.y + ball.radius >= win_height:
        ball.y_vel *= -1

    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= player1.y and ball.y <= player1.y + player1.height:
            if ball.x - ball.radius <= player1.x + player1.width:
                ball.x_vel *= -1

                middle_y = player1.y + player1.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (player1.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= player2.y and ball.y <= player2.y + player2.height:
            if ball.x + ball.radius >= player2.x:
                ball.x_vel *= -1

                middle_y = player2.y + player2.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (player2.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def main() -> None:

    run: bool = True

    while run:
        win.fill((0, 0, 0))
        global keys
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clock.tick(80)
        player1.draw()
        player2.draw()
        ball.draw(win)
        ball.move()
        ball.point_system(win)
        collision(ball, player1, player2)
        pygame.display.update()


if __name__ == "__main__":

    left_point: int = 0
    right_point: int = 0

    # Color
    WHITE: tuple = (255, 255, 255)

    pygame.init()

    keys = None

    win_width, win_height = 800, 600
    WIN_SIZE: tuple = (win_width, win_height)

    clock = pygame.time.Clock()

    win = pygame.display.set_mode(WIN_SIZE)

    player1 = Player(win, 10, win_width // 2 - 100 * 1.5, 1)
    player2 = Player(win, 785, win_width // 2 - 100 * 1.5, 2)
    ball = Ball(win_width//2, win_height//2, 7)
    ball1 = Ball(0, 0, 15)
    main()
