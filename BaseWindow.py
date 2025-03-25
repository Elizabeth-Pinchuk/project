import pygame

WINDOWSIZE = 450, 360
LEVEL = 1
REQUIREMENT = 3


class Window(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)

    def appear(self):
        self.image = pygame.Surface(WINDOWSIZE)
        self.image.fill('#ba3c06')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 50, 120
        self.In_Base = True

    def Exit(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            self.In_Base = False
        return self.In_Base


class Button(pygame.sprite.Sprite):
    def __init__(self, sizes, x, y, *group):
        super().__init__(*group)
        self.sizes = sizes
        self.image = pygame.Surface(sizes)
        self.image.fill('#f3f707')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.up = 0

    def update(self, ox, hp, a, base):
        global LEVEL
        if self.rect.x <= pygame.mouse.get_pos()[0] <= self.rect.x + self.sizes[0] and\
                self.rect.y <= pygame.mouse.get_pos()[1] <= self.rect.y + self.sizes[1]:
            self.image.fill('#999c08')
            if pygame.mouse.get_pressed()[0] and a == (LEVEL - 1) + REQUIREMENT:
                LEVEL += 1
                self.up = 1
                # base.animation.update()
                # base.image = base.animation.image
                base.level = LEVEL
                base.update()
        else:
            self.image.fill('#f3f707')
            self.up = 0




class RedButton(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, *group):
        super().__init__(*group)
        self.image = pygame.Surface([100, 100], pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, 100, 100)
        self.x, self.y = x, y
        self.screen = screen
        pygame.draw.rect(self.screen, '#eda007', pygame.Rect(self.rect.x, self.rect.y, 100, 100))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.rect.x, self.rect.y, 100, 100), 10)
        pygame.draw.circle(self.screen, '#fc3f26', (x + 50, y + 50), 30)
        pygame.draw.circle(self.screen, (0, 0, 0), (x + 50, y + 50), 30, 6)
        self.p = False

    def update(self, a):
        if ((self.x + 50 - pygame.mouse.get_pos()[0]) ** 2 +
            (self.y + 50 - pygame.mouse.get_pos()[1]) ** 2) ** 0.5 < 30:
            pygame.draw.rect(self.screen, '#eda007', pygame.Rect(self.rect.x, self.rect.y, 100, 100))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.rect.x, self.rect.y, 100, 100), 10)
            pygame.draw.circle(self.screen, '#ad2d1c', (self.x + 50, self.y + 50), 30)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x + 50, self.y + 50), 30, 6)
            if pygame.mouse.get_pressed()[0] or (a >= 1 and LEVEL >= 1):#ПОКА БЕЗ УСЛОВИЯ
                self.p = True
            #надпись YOU WIN!
        else:
            pygame.draw.rect(self.screen, '#eda007', pygame.Rect(self.rect.x, self.rect.y, 100, 100))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.rect.x, self.rect.y, 100, 100), 10)
            pygame.draw.circle(self.screen, '#fc3f26', (self.x + 50, self.y + 50), 30)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x + 50, self.y + 50), 30, 6)



class Horizontal_Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, level, cur_level, color, *group):
        super().__init__(*group)
        self.image = pygame.Surface([420, 30], pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, 420, 30)
        self.x, self.y = x, y
        self.color = color
        self.screen = screen
        if level:
            self.current_level = 420 / level * cur_level
        else:
            self.current_level = 420

    def update(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.rect.x, self.rect.y, self.current_level, 30))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.rect.x, self.rect.y, 420, 30), 10)


class Vertical_Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, color, amount, *group):
        super().__init__(*group)
        self.image = pygame.Surface([70, 240], pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, 70, 240)
        self.x, self.y = x, y
        self.color = color
        self.screen = screen
        if amount:
            self.current_level = 240 / ((LEVEL - 1) * 1 + REQUIREMENT) * amount
        else:
            self.current_level = 0

    def update(self):
        if self.current_level <= 240:
            pygame.draw.rect(self.screen, self.color, pygame.Rect(self.rect.x, 240 + self.rect.y - self.current_level,
                                                              70, self.current_level))
        else:
            pygame.draw.rect(self.screen, self.color, pygame.Rect(self.rect.x, self.rect.y,
                                                                  70, 240))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.rect.x, self.rect.y, 70, 240), 6)


class Button_A(pygame.sprite.Sprite):
    def __init__(self, sizes, x, y, *group):
        super().__init__(*group)
        self.sizes = sizes
        self.image = pygame.Surface(sizes)
        self.image.fill('#160582')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.u = 0

    def update(self, ox, max_ox):
        if self.rect.x <= pygame.mouse.get_pos()[0] <= self.rect.x + self.sizes[0] and\
                self.rect.y <= pygame.mouse.get_pos()[1] <= self.rect.y + self.sizes[1]:
            self.image.fill('#33287f')
            if pygame.mouse.get_pressed()[0]:
                if ox + 15 <= max_ox and ox < max_ox:
                    self.u = 15
                elif ox < max_ox < ox + 15:
                    self.u = max_ox - ox
                else:
                    self.u = 0
        else:
            self.image.fill('#160582')

class Npc_hp(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, level, cur_level, color, *group):
        super().__init__(*group)
        self.image = pygame.Surface([40, 5], pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, 40, 5)
        self.x, self.y = x, y
        self.color = color
        self.screen = screen
        if level:
            self.current_level = 40 / level * cur_level
        else:
            self.current_level = 40

    def update(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.rect.x, self.rect.y, self.current_level, 5))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.rect.x, self.rect.y, 40, 5), 3)