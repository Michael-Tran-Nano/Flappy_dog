import pygame
from sys import exit
from random import randint

# Settings
window_size = (400, 500)
jump = -8
gravity = 0.38
floor_height = 419
initial_speed = 3
speed = initial_speed
block_dist = 225
block_gap = 110

class Dog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        dog_1 = pygame.image.load('graphics/dog_1.png').convert_alpha()
        dog_2 = pygame.image.load('graphics/dog_2.png').convert_alpha()
        self.dogs = [dog_1, dog_2] # List of animations
        self.dog_index = 0

        self.image = self.dogs[self.dog_index] # Shift between different dogs
        self.rect = self.image.get_rect(bottomleft=(100, 100)) ### THINK ABOUT THE DIFFERENT SIZES!!!
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0

        # Rotation when dead
        self.rotation_count = 0

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
        self.rect = self.image.get_rect(center=(self.rect.center)) # Changing the hit_box
        self.mask = pygame.mask.from_surface(self.image)

    def death(self):
        self.space_bar()
        self.dog_index = 0
        self.image = self.dogs[self.dog_index]

    def rotate(self):
        # Rotate when you have not touched the floor yet
        if self.rect.bottom < floor_height:

            self.rotation_count += 0.5
            if self.rotation_count > 1:
                self.rotation_count = 0
                self.image = pygame.transform.rotate(self.image, 90)
            self.rect.x += initial_speed

    def update(self):
        self.apply_gravity()
        if alive:
            self.animation_state()
        else:
            self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, height):
        super().__init__()

        self.image = pygame.image.load('graphics/pole.png').convert()

        if type == 'top':
            y_pos = height - block_gap//2
            self.rect = self.image.get_rect(midbottom=(window_size[0]*1.1, y_pos))
        elif type == 'bot':
            y_pos = height + block_gap//2
            self.rect = self.image.get_rect(midtop=(window_size[0]*1.1, y_pos))

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Obstacle_attachment(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'top':
            self.image = pygame.image.load('graphics/top.png').convert_alpha()
            self.rect = self.image.get_rect(midtop=(window_size[0]*1.1, 0))
        elif type == 'bot':
            self.image = pygame.image.load('graphics/bottom.png').convert_alpha()
            self.rect = self.image.get_rect(midbottom=(window_size[0]*1.1, window_size[1]))

    def update(self):
        self.rect.x -= speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def collisions_obstacle_test():
    if pygame.sprite.spritecollide(sprite=dog.sprite, 
                                   group=obstacle_group, 
                                   dokill=False):
        print('Rect collision')
        # Only check for mask collision when there is rect collision
        if pygame.sprite.spritecollide(sprite=dog.sprite, 
                                   group=obstacle_group, 
                                   dokill=False,
                                   collided=pygame.sprite.collide_mask):
            print('Real collision')
            dog_sprite.death() # Make the dog jump before spinning
            # obstacle_group.empty()
            # obstacle_attachment_group.empty()
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode(size=window_size)
pygame.display.set_caption('Flappy Dog')
clock = pygame.time.Clock()

# Player
dog = pygame.sprite.GroupSingle()
dog.add(Dog())
dog_sprite = dog.sprite # To call Class functions
# Obstacles
obstacle_group = pygame.sprite.Group()
obstacle_attachment_group = pygame.sprite.Group()

# Background
background_surface = pygame.image.load('graphics/background.png').convert()
background_x = 0
background_x_max = 1000

# Distance count
dist_traversed = 0

# Status
game_active = True
alive = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active and alive:
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
        obstacle_attachment_group.draw(screen)
        obstacle_attachment_group.update()

        # game_active = collisions_obstacle_test()
        if alive:
            alive = collisions_obstacle_test()
        if not alive:
            speed = 0


        dist_traversed += speed

        if dist_traversed > block_dist:
            dist_traversed -= block_dist
            height = randint(100, 340)
            obstacle_group.add(Obstacle('top', height))
            obstacle_group.add(Obstacle('bot', height))
            obstacle_attachment_group.add(Obstacle_attachment('top'))
            obstacle_attachment_group.add(Obstacle_attachment('bot'))

    pygame.display.update()
    clock.tick(60)