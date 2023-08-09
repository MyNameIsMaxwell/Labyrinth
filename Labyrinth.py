import sys
import pygame
from pygame.color import THECOLORS


LABYRINTH_MAP = [
    '#######@#####',
    '#  K#     #K#',
    '# ### # # # #',
    '# #   # #   #',
    '# # # #######',
    '# # #       #',
    '# # ####### #',
    '# #     #K# #',
    '# ##### # # #',
    '#   #   # # #',
    '### # ### # #',
    '#     #     #',
    '#X###########',
]

BLOCK_SIDE = 60
CELL_SIDE = 60
WIDTH = len(LABYRINTH_MAP[0])
HEIGHT = len(LABYRINTH_MAP)

SCREEN_WIDTH = WIDTH * BLOCK_SIDE
SCREEN_HEIGHT = HEIGHT * BLOCK_SIDE

wall_textures = pygame.image.load(f'Wall_Block_Tall.png')


key_texture = pygame.image.load(f'Star.png')
door_textures = []
for i in range(4):
    door_textures.append(pygame.image.load(f'door{i}.png'))
player_texture = pygame.image.load(f'catgirl.png')

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('Comic Sans MS', 60)
text = font.render('You Win!', True, THECOLORS['lawngreen'])


class Wall:
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.texture = texture

    def draw(self):
        screen.blit(self.texture, (self.x, self.y))


class Key:
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.texture = texture
        self.is_taken = False

    def draw(self):
        if not self.is_taken:
            screen.blit(self.texture, (self.x, self.y))


class Exit:
    def __init__(self, x, y, textures):
        self.x = x
        self.y = y
        self.textures = textures
        self.keys_collected = 0

    def draw(self):
        door_texture_index = min(self.keys_collected, len(self.textures) - 1)
        screen.blit(self.textures[door_texture_index], (self.x, self.y))


class Labyrinth:
    def __init__(self):
        self.walls = []
        self.keys = []
        self.exits = []
        self.player = None

        for y in range(HEIGHT):
            for x in range(WIDTH):
                cell = LABYRINTH_MAP[y][x]
                if cell == '#':
                    self.walls.append(Wall(x * BLOCK_SIDE, y * BLOCK_SIDE, wall_textures))
                elif cell == '@':
                    self.player = Player(x * BLOCK_SIDE, y * BLOCK_SIDE)
                elif cell == 'X':
                    self.exits.append(Exit(x * BLOCK_SIDE, y * BLOCK_SIDE, door_textures))
                elif cell == 'K':
                    self.keys.append(Key(x * BLOCK_SIDE, y * BLOCK_SIDE, key_texture))

    def move_player(self):
        self.set_player_direction(self.player.direction)
        self.player.move()
        for key in self.keys:
            if not key.is_taken and (key.x, key.y) == (self.player.x, self.player.y):
                key.is_taken = True
                for exit in self.exits:
                    exit.keys_collected += 1
                break

    def set_player_direction(self, direction):
        if self.player_can_move(direction):
            self.player.direction = direction
        else:
            self.player.direction = Direction.NONE

    def player_can_move(self, direction):
        pcx, pcy = self.get_player_cell()
        if direction == Direction.UP:
            return pcy > 0 and LABYRINTH_MAP[pcy - 1][pcx] != '#'
        elif direction == Direction.DOWN:
            return pcy < HEIGHT - 1 and LABYRINTH_MAP[pcy + 1][pcx] != '#'
        elif direction == Direction.LEFT:
            return pcx > 0 and LABYRINTH_MAP[pcy][pcx - 1] != '#'
        elif direction == Direction.RIGHT:
            return pcx < WIDTH - 1 and LABYRINTH_MAP[pcy][pcx + 1] != '#'
        return False

    def draw(self):
        for wall in self.walls:
            wall.draw()
        for exit in self.exits:
            exit.draw()
        for key in self.keys:
            key.draw()
        self.player.draw()

    def win(self):
        for exit in self.exits:
            if (exit.x, exit.y) == (self.player.x, self.player.y) and exit.keys_collected == len(self.keys):
                return True
        return False

    def get_player_cell(self):
        return self.player.x // CELL_SIDE, self.player.y // CELL_SIDE


class Direction:
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.texture = player_texture
        self.step = CELL_SIDE
        self.direction = Direction.NONE

    def draw(self):
        screen.blit(self.texture, (self.x, self.y))

    def move(self):
        if self.direction == Direction.UP:
            self.y -= self.step
        elif self.direction == Direction.DOWN:
            self.y += self.step
        elif self.direction == Direction.LEFT:
            self.x -= self.step
        elif self.direction == Direction.RIGHT:
            self.x += self.step


def start_level():
    labyrinth = Labyrinth()

    while True:
        if labyrinth.win():
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    labyrinth.set_player_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    labyrinth.set_player_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    labyrinth.set_player_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    labyrinth.set_player_direction(Direction.RIGHT)
                elif event.key == pygame.K_f:
                    screen.blit(font.render('Hey, Pasha:*', True, THECOLORS['darkviolet']), (SCREEN_WIDTH - 600, SCREEN_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.wait(1000)
            elif event.type == pygame.KEYUP:
                labyrinth.set_player_direction(Direction.NONE)

        labyrinth.move_player()

        screen.fill((255, 218, 185))
        labyrinth.draw()

        pygame.display.flip()
        pygame.time.wait(60)


def show_win_message():
    screen.blit(text, (CELL_SIDE * 2, SCREEN_HEIGHT - CELL_SIDE - 60))
    pygame.display.flip()
    pygame.time.wait(1000)


if __name__ == "__main__":
    while True:
        start_level()
        show_win_message()
