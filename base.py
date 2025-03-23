import pygame
import random
import os
import time
import BaseWindow
import animations

SIZE = WIDTH, HEIGHT = 600, 600

all_sprites = pygame.sprite.Group()
main_ = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
water_tiles_group = pygame.sprite.Group()
remain = pygame.sprite.Group()
alien = pygame.sprite.Group()
base = pygame.sprite.Group()
base_window = pygame.sprite.Group()
base_button_w = pygame.sprite.Group()
remains_sprites = [pygame.image.load(f'sprites\\remains\\{file}') for file in os.listdir("sprites\\remains")]
rock_sprites = [pygame.image.load(f'sprites\\rocks\\{file}') for file in os.listdir("sprites\\rocks")]
Level = BaseWindow.LEVEL
REQUIREMENT = BaseWindow.REQUIREMENT
WORLD_SIZE = 200
FPS = 140
Base_Activated = False
Remains_amount = 50
In_Base = False
HERO_SPEED = 2


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, sizes, texture, x, y, c_a, *group):
        if c_a:
            super().__init__(*group, tiles_group)
        else:
            super().__init__(*group, tiles_group, water_tiles_group)
        self.surface = pygame.Surface(sizes)
        self.image = pygame.transform.scale(texture, sizes)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class WORLD:
    def __init__(self):
        self.world = 'Savings1'
        self.tile = 50
        self.tiles = [pygame.image.load("sprites\\floor_tile.png")]
        self.rock_tiles = rock_sprites
        self.Base_Activated = False

    def create_world(self):
        with open(self.world, 'w') as file:
            arr = [([str(random.randint(0, 6)) for _ in range(WORLD_SIZE)])
                   for row in range(WORLD_SIZE)]
            arr = list(map(lambda x: ';'.join(x), arr))
            file.write('\n'.join(arr))

    def load_world(self):
        filename = os.path.abspath(self.world)
        with open(filename, 'r') as file:
            level_map = [line.strip() for line in file]
        self.max_width = len(level_map[0])
        self.height = len(level_map)
        self.level = list(map(lambda x: list(map(int, x.split(';'))), level_map))

    def render(self):
        global player
        self.x, self.y = 0, 0
        for line in self.level:
            for row in line:
                if row:
                    Tile((self.tile, self.tile), self.tiles[0], self.x, self.y, True, all_sprites)
                    if row == 5:
                        if random.randint(0, 15) == 5:
                            remains = Remains(self.x + 10, self.y + 10)
                        if random.randint(0, 10) == 5:
                            npc = NPC(self.x, self.y, player)
                    self.x += self.tile
                else:
                    Tile((self.tile, self.tile), random.choice(self.rock_tiles), self.x, self.y, False, all_sprites)
                    self.x += self.tile
            self.x = 0
            self.y += self.tile


class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, hero):
        super().__init__(alien)
        self.image = pygame.image.load("sprites\\walk_left\\1_left.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.hero = hero
        self.hp = 0  # dfghj

    def move(self):
        if self.rect.x < self.hero.rect.x - 20:
            self.rect.x += self.speed
        if self.rect.x > self.hero.rect.x - 20:
            self.rect.x -= self.speed
        if self.rect.y < self.hero.rect.y - 20:
            self.rect.y += self.speed
        if self.rect.y > self.hero.rect.y - 20:
            self.rect.y -= self.speed

    def check(self):
        if abs(self.rect.x - self.hero.rect.x) < 75 and abs(self.rect.x - self.hero.rect.x) < 75:
            self.move()
        if pygame.sprite.spritecollideany(self, main_):
            self.hero.hp -= 1


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, size, world, hp, *group):
        super().__init__(*group)
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.image = None
        self.rect = self.surface.get_rect()
        pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(self.rect.x, self.rect.y, *size))
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.speed = HERO_SPEED
        self.world = world
        self.attack = False
        self.running = False
        self.animations = {
            'walk_right': animations.Animation(x, y, 'sprites\\walk_right', size),
            'walk_left': animations.Animation(x, y, 'sprites\\walk_left', size),
            'attack_left': animations.Animation(x, y, 'sprites\\attack_left', size),
            'attack_right': animations.Animation(x, y, 'sprites\\attack_right', size)
        }
        self.direction = "left"

    def input(self):
        global In_Base
        keys_pressed = pygame.key.get_pressed()
        v_x, v_y = 0, 0
        if keys_pressed[pygame.K_SPACE]:
            self.attack = True
            self.image = self.animations[f'attack_{self.direction}']
        else:
            self.attack = False
        if keys_pressed[pygame.K_LSHIFT]:
            self.speed = HERO_SPEED * 1.5
            self.running = True
        else:
            self.speed = HERO_SPEED
            self.running = False
        if keys_pressed[pygame.K_w]:
            v_y = -1 * self.speed
        if keys_pressed[pygame.K_s]:
            v_y = 1 * self.speed
        if keys_pressed[pygame.K_d]:
            v_x = 1 * self.speed
            self.direction = 'right'
        if keys_pressed[pygame.K_a]:
            v_x = -1 * self.speed
            self.direction = 'left'
        if keys_pressed[pygame.K_e] and not self.world.Base_Activated:
            self.base = Base(self.rect.x, self.rect.y)
            self.world.Base_Activated = True
        if pygame.sprite.spritecollideany(self, base) and keys_pressed[pygame.K_e]:
            In_Base = True
        if (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s] or
                keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d]):
            self.animations[f'walk_{self.direction}'].is_on = True
        else:
            self.animations[f'walk_{self.direction}'].is_on = False
        return v_x, v_y

    def move(self, v_x, v_y):
        self.rect = self.rect.move(v_x * self.speed, v_y * self.speed)
        # if pygame.sprite.spritecollideany(self, tiles_group):
        #     while not pygame.sprite.spritecollideany(self, tiles_group):
        #         self.rect = self.rect.move(-1 * v_x, -1 * v_y)
        # else:
        #     self.rect = self.rect.move(-2 * v_x * self.speed, -2 * v_y * self.speed)
        if pygame.sprite.spritecollideany(self, water_tiles_group):
            while pygame.sprite.spritecollideany(self, water_tiles_group):
                self.rect = self.rect.move(-1 * v_x, -1 * v_y)

    def update(self):
        v_x, v_y = self.input()
        self.move(v_x, v_y)
        if self.attack:
            self.animations[f'attack_{self.direction}'].update()
            self.image = self.animations[f"attack_{self.direction}"].image
        else:
            self.animations[f"walk_{self.direction}"].update()
            self.image = self.animations[f"walk_{self.direction}"].image


Amount = 0


class Remains(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(remain)
        self.image = pygame.Surface([20, 20])
        self.image = pygame.transform.scale(random.choice(remains_sprites), [35, 35])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.k = False

    def update(self, screen):
        global Amount
        if pygame.sprite.spritecollideany(self, main_):
            if Amount < (Level - 1) + REQUIREMENT:
                Amount += 1
                self.kill()
            else:
                f1 = pygame.font.Font(None, 52)
                screen.blit(f1.render("The Storage is full!", False, '#9e0808'), (250, 100))


class Base(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, base)
        self.image = pygame.Surface([50, 50])
        self.image.fill('#ba3c06')  # pygame.transform.scale(изображение, (размер x, размер_y))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Air:
    def __init__(self):
        self.oxygen = 200
        self.h = 200
        self.m_oxygen = self.oxygen

    def render(self, screen):
        if self.oxygen > 0:
            if self.oxygen <= self.h:
                pygame.draw.rect(screen, '#00e1ff', pygame.Rect(10, 380, 40, self.oxygen))
            else:
                pygame.draw.rect(screen, '#00e1ff', pygame.Rect(10, 380, 40, self.h))
            pygame.draw.rect(screen, '#058787', pygame.Rect(10, 380 + self.oxygen, 40,
                                                            self.h - self.oxygen))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 380, 40, self.h), 7)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 380, 40, self.h))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 380, 40, self.h), 7)
        if self.oxygen > self.m_oxygen:
            self.m_oxygen = self.oxygen


class HP:
    def __init__(self):
        self.hp = 200
        self.h = 200
        self.m_hp = self.hp

    def __sub__(self, other):
        self.hp -= other * 100
        return self.hp

    def render(self, screen):
        if self.hp > 0:
            if self.hp <= self.h:
                pygame.draw.rect(screen, '#07db0e', pygame.Rect(70, 380, 40, self.hp))
            else:
                pygame.draw.rect(screen, '#07db0e', pygame.Rect(70, 380, 40, self.h))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(70, 380, 40, self.h), 7)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(70, 380, 40, self.h))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(70, 380, 40, self.h), 7)
        if self.hp > self.m_hp:
            self.m_hp = self.hp


def main():
    global In_Base
    global Level
    global REQUIREMENT
    global Amount
    A = WORLD()
    camera = Camera()

    A.create_world()
    A.load_world()

    pygame.init()
    pygame.display.set_caption('*****')
    screen = pygame.display.set_mode(SIZE)
    hp = HP()
    hero = Hero(300, 300, (30, 40), A, hp, all_sprites, main_)
    global player
    player = hero
    Base = BaseWindow.Window(base_window)
    a = Air()

    A.render()
    run = True
    timer = pygame.time.Clock()
    n_time = time.time()
    while run:
        Level = BaseWindow.LEVEL
        REQUIREMENT = BaseWindow.REQUIREMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not In_Base:
            screen.fill((255, 255, 255))
            cur_time = time.time()

            if cur_time - n_time > 1:
                a.oxygen -= 10
                n_time = time.time()
            if a.oxygen <= 0:
                hp.hp -= 1
            if hp.hp <= 0:
                run = False
            main_.update()
            camera.update(hero)

            for sprite in all_sprites:
                camera.apply(sprite)
            for sprite in remain:
                camera.apply(sprite)
            for sprite in alien:
                camera.apply(sprite)
                sprite.check()
            all_sprites.draw(screen)
            main_.draw(screen)
            remain.draw(screen)
            remain.update(screen)
            alien.draw(screen)
            alien.update(screen)

            a.render(screen)
            hp.render(screen)

        if In_Base:
            Base.appear()
            B_UP = BaseWindow.Button((100, 70), 390, 250, base_button_w)
            Final_Button = BaseWindow.RedButton(70, 380, screen, base_button_w)
            AirBar = BaseWindow.Horizontal_Bar(70, 140, screen, a.m_oxygen, a.oxygen, '#00e1ff',
                                               base_button_w)
            HpBar = BaseWindow.Horizontal_Bar(70, 190, screen, hp.m_hp, hp.hp, '#07db0e',
                                              base_button_w)
            RemBar = BaseWindow.Vertical_Bar(280, 230, screen,
                                             pygame.Color('white'), Amount, base_button_w)
            B_A = BaseWindow.Button_A((100, 140), 70, 230, base_button_w)
            B_UP.update(a.oxygen, hp.hp, Amount)
            B_A.update(a.oxygen, a.m_oxygen)
            if B_A.u:
                a.oxygen += B_A.u
            if B_UP.up:
                a.oxygen += 15
                Amount -= REQUIREMENT + (Level - 1)
                hp.hp += 15
            base_window.draw(screen)
            base_button_w.draw(screen)
            Final_Button.update(Amount)
            if Final_Button.p:
                run = False
            AirBar.update()
            HpBar.update()
            RemBar.update()
            In_Base = Base.Exit()
        pygame.display.flip()
        timer.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
