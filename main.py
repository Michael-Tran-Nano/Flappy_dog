import pygame
from sys import exit

# Spyd 32 px bred, 91 px høj

# Settings
window_size = (400, 500)
jump = -8
gravity = 0.38
floor_height = 419
speed = 3

class Dog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        dog_1 = pygame.image.load('graphics/dog_1.png').convert_alpha()
        dog_2 = pygame.image.load('graphics/dog_2.png').convert_alpha()
        self.dogs = [dog_1, dog_2] # List of animations
        self.dog_index = 0

        self.image = self.dogs[self.dog_index] # Shift between different dogs
        self.rect = self.image.get_rect(bottomleft=(100, 100)) ### THINK ABOUT THE DIFFERENT SIZES!!!
        self.gravity = 0

    def space_bar(self):
        self.gravity = jump

    def apply_gravity(self):
        self.gravity += gravity
        self.rect.y += self.gravity
        if self.rect.bottom > floor_height:
            self.rect.bottom = floor_height # Change later
    
    def animation_state(self):
        if self.gravity < 0:
            self.dog_index = 1
        else:
            self.dog_index = 0
        self.image = self.dogs[self.dog_index]
        self.rect = self.image.get_rect(center=(self.rect.center))

    def update(self):
        #self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'top':
            pole = pygame.Surface(size=(32, 100))
            y_pos = 0
        elif type == 'bot':
            pole = pygame.Surface(size=(32, 100))
            y_pos = 200

        self.image = pole
        self.rect = self.image.get_rect(topleft=(window_size[1], y_pos))

    def update(self):
        self.rect.x -= speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

pygame.init()
screen = pygame.display.set_mode(size=window_size)
pygame.display.set_caption('Flappy Dog')
clock = pygame.time.Clock()
game_active = True

# Plater
dog = pygame.sprite.GroupSingle()
dog.add(Dog())
dog_sprite = dog.sprite # To call Class functions
# Obstacles
obstacle_group = pygame.sprite.Group()

# Background
background_surface = pygame.image.load('graphics/background.png').convert()
background_x = 0
background_x_max = 1000

# Distance count
dist = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    dog_sprite.space_bar()

    if game_active:

        # Background
        screen.blit(source=background_surface, dest=(background_x, 0))
        background_x -= speed
        if background_x < -background_x_max:
            background_x = 0

        # Player
        dog.draw(screen)
        dog.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        dist += speed

        if dist > 175:
            dist -= 175
            obstacle_group.add(Obstacle('top'))
            obstacle_group.add(Obstacle('bot'))

    pygame.display.update()
    clock.tick(60)