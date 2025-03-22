import pygame
import random
import os
import time
import animations

SIZE = WIDTH, HEIGHT = 600, 600
all_sprites = pygame.sprite.Group()
main_ = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
water_tiles_group = pygame.sprite.Group()
remain = pygame.sprite.Group()
base = pygame.sprite.Group()
WORLD_SIZE = 100
FPS = 200
Remains_amount = 50


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
        self.image = pygame.Surface([sizes, sizes])
        self.image.fill(texture)  # После поменять на фоточку пжпжпжпж
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class WORLD:
    def __init__(self):
        self.world = 'Savings1'
        self.tile = 50
        self.Base_Activated = False

    def create_world(self):
        with open(self.world, 'w') as file:
            arr = [';'.join([str(random.randint(0, 6)) for _ in range(WORLD_SIZE)]) for row in range(WORLD_SIZE)]
            file.write('\n'.join(arr))

    def load_world(self):
        filename = os.path.abspath(self.world)
        with open(filename, 'r') as file:
            level_map = [line.strip() for line in file]
        self.max_width = len(level_map[0])
        self.height = len(level_map)
        self.level = list(map(lambda x: list(map(int, x.split(';'))), level_map))

    def render(self):
        x, y = 0, 0
        for line in self.level:
            for row in line:
                if row:
                    Tile(self.tile, pygame.Color('Green'), x, y, True, all_sprites)
                    x += self.tile
                else:
                    Tile(self.tile, pygame.Color('Blue'), x, y, False, all_sprites)
                    x += self.tile
            x = 0
            y += self.tile


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, size, world, *group):
        super().__init__(*group)
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        # self.image = pygame.image.load('12\\1.png')
        self.image = None
        self.rect = self.surface.get_rect()
        pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(self.rect.x, self.rect.y, *size))
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.world = world
        self.speed = 1.5  # ВЫНЕСТИ В АРГУМЕНТЫ КОНСТРУКТОРА
        self.running = False
        self.anims = {
            'walk': animations.Animation(x, y, '12', size),
            'run': animations.Animation(x, y, '12', size),
            'attack': animations.Animation(x, y, '12', size)
        }
        self.anim = animations.Animation(x, y, '12', size)

    def input(self):
        keys_pressed = pygame.key.get_pressed()
        v_x, v_y = 0, 0
        if keys_pressed[pygame.K_LSHIFT]:
            self.speed = 2.3
            self.running = True
            self.anim.is_on = True
        else:
            self.speed = 1.5
            self.running = False
            self.anim.is_on = False
        if keys_pressed[pygame.K_w] and not keys_pressed[pygame.K_s]:
            v_y = -1 * self.speed
        if not keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]:
            v_y = 1 * self.speed
        if keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a]:
            v_x = 1 * self.speed
        if not keys_pressed[pygame.K_d] and keys_pressed[pygame.K_a]:
            v_x = -1 * self.speed
        if keys_pressed[pygame.K_e] and not self.world.Base_Activated:
            self.world.base = Base(self.rect.x, self.rect.y)
            self.world.Base_Activated = True

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

        self.anim.update()
        self.image = self.anim.image


class Remains(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, remain)
        self.image = pygame.Surface([20, 20])
        self.image.fill('#752908')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


'''
Обломки доделать



'''


class Base(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, base)
        self.image = pygame.Surface([50, 50])
        self.image.fill('#ba3c06')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Air:
    def __init__(self):
        self.oxygen = 200
        self.h = 200

    def render(self, screen):
        if self.oxygen > 0:
            pygame.draw.rect(screen, '#00e1ff', pygame.Rect(40, 380, 40, self.oxygen))
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(40, 380, 40, self.h))


def main():
    A = WORLD()
    camera = Camera()

    A.create_world()
    A.load_world()

    pygame.init()
    pygame.display.set_caption('*****')
    screen = pygame.display.set_mode(SIZE)

    hero = Hero(300, 300, (30, 50), A, all_sprites, main_)
    a = Air()

    A.render()

    run = True
    timer = pygame.time.Clock()
    n_time = time.time()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            cur_time = time.time()

            screen.fill((255, 255, 255))

            if cur_time - n_time > 1:
                a.oxygen -= 10
                n_time = time.time()

            main_.update()
            camera.update(hero)

            for sprite in all_sprites:
                camera.apply(sprite)

            all_sprites.draw(screen)
            main_.draw(screen)

            a.render(screen)

            pygame.display.flip()
            timer.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()

'''if key[pygame.K_w] and not key[pygame.K_s] and not key[pygame.K_d] and not key[pygame.K_a]:
            self.rect.y -= 8
        elif key[pygame.K_s] and not key[pygame.K_w] and not key[pygame.K_d] and not key[pygame.K_a]:
            self.rect.y += 8
        elif key[pygame.K_d] and not key[pygame.K_w] and not key[pygame.K_s] and not key[pygame.K_a]:
            self.rect.x += 8
        elif key[pygame.K_a] and not key[pygame.K_w] and not key[pygame.K_d] and not key[pygame.K_s]:
            self.rect.x -= 8
        elif key[pygame.K_w] and not key[pygame.K_s] and key[pygame.K_d] and not key[pygame.K_a]:
            self.rect.x += 4 * round(2 ** 0.5, 2)
            self.rect.y -= 4 * round(2 ** 0.5, 2)
        elif key[pygame.K_w] and not key[pygame.K_s] and not key[pygame.K_d] and key[pygame.K_a]:
            self.rect.x -= 4 * round(2 ** 0.5, 2)
            self.rect.y -= 4 * round(2 ** 0.5, 2)
        elif not key[pygame.K_w] and key[pygame.K_s] and not key[pygame.K_d] and key[pygame.K_a]:
            self.rect.x -= 4 * round(2 ** 0.5, 2)
            self.rect.y += 4 * round(2 ** 0.5, 2)
        elif not key[pygame.K_w] and key[pygame.K_s] and key[pygame.K_d] and not key[pygame.K_a]:
            self.rect.x += 4 * round(2 ** 0.5, 2)
            self.rect.y += 4 * round(2 ** 0.5, 2)'''
