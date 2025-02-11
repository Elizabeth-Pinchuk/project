class Character:
    max_hp = 100
    min_hp = 1

    def __init__(self, pos, name):
        self.name = name
        self.pos = pos
        self.hp = self.max_hp

    def is_dead(self):
        if self.hp < self.min_hp:
            return True
        return False

    def get_info(self):
        print(f'My name is {self.name}!')
        print(f'My hp is {self.hp}/{self.max_hp}.')
        print(f'My cords {self.pos}.')

    def move(self, x, y):
        self.pos = [self.pos[0] + x, self.pos[1] + y]

    def heal(self, amount=15):
        self.hp += amount
        self.check_limit()

    def check_limit(self):
        if self.hp > self.max_hp:
            self.hp = self.max_hp

class Player(Character):
    max_oxygen = 10

    def __init__(self, pos, name):
        super().__init__(pos, name)
        self.oxygen = self.max_oxygen

    def move(self, x, y):
        super().move(x, y)
        self.breath()

    def breath(self, value=1):
        self.oxygen -= value

    def get_info(self):
        print(f'My name is {self.name}!')
        print(f'My hp is {self.hp}/{self.max_hp}.')
        print(f'My oxygen is {self.oxygen}/{self.max_oxygen}.')
        print(f'My cords {self.pos}.')

class Alien(Character):
    def __init__(self, pos, name, spot_range, attack_range):
        super().__init__(pos, name)
        self.player = None
        self.spot_range = spot_range
        self.attack_range = attack_range


    def wait(self):
        ...

    def chasing(self):
        ...

    def attack(self, object):
        object.hp -= 1

    def manager(self, pos):
        deltax = abs(pos[0] - self.pos[0])
        deltay = abs(pos[1] - self.pos[1])
        distance = (deltax ** 2 + deltay ** 2) ** 0.5
        if distance > self.spot_range:
            self.wait()
        elif distance <= self.spot_range:
            self.chasing()
        if distance <= self.attack_range:
            self.attack(self.player)
class Object:
    def __init__(self, pos, name, size):
        self.name = name
        self.pos = pos
        self.size = size

player1 = Player([0, 0], 'player 1')