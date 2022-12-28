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
        pygame.draw.rect(
            self.win, WHITE, (self.x, self.y, self.width, self.height))

    def command(self, keys) -> None:
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

    def update(self, keys):
        self.command(keys)
        self.draw()


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
            self.y_vel = 0

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

    def update(self, win):
        self.draw(win)
        self.move()


class Game:

    def __init__(self, width: int, height: int):
        self.win_width, self.win_height = width, height
        self.WIN_SIZE: tuple = (self.win_width, self.win_height)
        self.win = pygame.display.set_mode(self.WIN_SIZE)

        self.player1 = Player(self.win, 10, self.win_width // 2 - 100 * 1.5, 1)
        self.player2 = Player(
            self.win, 785, self.win_width // 2 - 100 * 1.5, 2)

        self.ball = Ball(self.win_width//2, self.win_height//2, 7)

        self.left_point = 0
        self.right_point = 0

    def point_system(self):

        if self.ball.x > win_width:
            self.left_point += 1
        elif self.ball.x < 0:
            self.right_point += 1

        fnt = pygame.font.SysFont("Arial", 40, bold=True)

        t1 = fnt.render(str(self.left_point), True, "white")
        t2 = fnt.render(str(self.right_point), True, "white")

        self.win.blit(t1, (200, 0))
        self.win.blit(t2, (600, 0))

    def collision(self):
        if self.ball.y + self.ball.radius >= self.win_height:
            self.ball.y_vel *= -1

        elif self.ball.y - self.ball.radius <= 0:
            self.ball.y_vel *= -1

        if self.ball.x_vel < 0:
            if self.ball.y >= self.player1.y and self.ball.y <= self.player1.y + self.player1.height:
                if self.ball.x - self.ball.radius <= self.player1.x + self.player1.width:
                    self.ball.x_vel *= -1

                    middle_y = self.player1.y + self.player1.height / 2
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = (
                        self.player1.height / 2) / self.ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    self.ball.y_vel = -1 * y_vel

        else:
            if self.ball.y >= self.player2.y and self.ball.y <= self.player2.y + self.player2.height:
                if self.ball.x + self.ball.radius >= self.player2.x:
                    self.ball.x_vel *= -1

                    middle_y = self.player2.y + self.player2.height / 2
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = (
                        self.player2.height / 2) / self.ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    self.ball.y_vel = -1 * y_vel

    def render(self):
        pygame.init()
        run: bool = True
        clock = pygame.time.Clock()

        while run:
            self.win.fill((0, 0, 0))
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            clock.tick(80)

            self.player1.update(keys)
            self.player2.update(keys)

            self.ball.update(self.win)

            self.point_system()
            self.collision()

            pygame.display.update()


if __name__ == "__main__":
    WHITE: tuple = (255, 255, 255)
    win_width, win_height = 800, 600
    g = Game(win_width, win_height)
    g.render()
