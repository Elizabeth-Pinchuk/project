import pygame, os


class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, path, size):
        super().__init__()
        self.sprites = []
        self.is_on = False
        self.now_sprite = 0
        self.load_sprites(path)
        for i in range (len(self.sprites)):
            self.sprites[i] = pygame.transform.scale(self.sprites[i], size)
        self.image = self.sprites[self.now_sprite]

    def update(self, speed=1):
        if self.is_on:
            self.now_sprite += speed
            if int(self.now_sprite) >= len(self.sprites):
                self.now_sprite = 0
        self.image = self.sprites[self.now_sprite]

    def load_sprites(self, path):
        for file in os.listdir(path):
            self.sprites.append(pygame.image.load(path + '\\' + file))
