import pygame
from sys import exit


# Settings
size = (400, 500)
jump = -20

class Dog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        dog_1 = pygame.image.load('graphics/dog_1.png').convert_alpha()
        #dog_2 = pygame.image.load('graphics/dog_2.png').convert_alpha()
        self.dogs = dog_1 # List of animations

        self.image = self.dogs # Shift between different dogs
        self.rect = self.image.get_rect(center=(100, 100))
        self.gravity = 0
    
    # def player_input(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_SPACE]:
    #         self.gravity = jump

    def space_bar(self):
        self.gravity = jump

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > size[1]:
            self.rect.bottom = size[1] # Change later
    
    def update(self):
        #self.player_input()
        self.apply_gravity()
        # self.animation_state() # Make later

pygame.init()
screen = pygame.display.set_mode(size=size)
pygame.display.set_caption('Flappy Dog')
clock = pygame.time.Clock()
game_active = True

# Objects
dog = pygame.sprite.GroupSingle()
dog.add(Dog())
dog_sprite = dog.sprite # To call Class functions

# Test background
test_surface = pygame.Surface(size=size)
test_surface.fill('Red')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    dog_sprite.space_bar()


    screen.blit(source=test_surface, dest=(0, 0))

    dog.draw(screen)
    dog.update()

    pygame.display.update()
    clock.tick(60)