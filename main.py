import pygame
from sys import exit
from random import randint

# Settings
window_size = (400, 500)

jump = -8
gravity = 0.38
speed = 3
start_position = (100, 100)

block_dist = 225
block_gap = 120
floor_height = 419

class Dog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        dog_1 = pygame.image.load('graphics/dog_1.png').convert_alpha()
        dog_2 = pygame.image.load('graphics/dog_2.png').convert_alpha()
        self.dogs = [dog_1, dog_2] # List of animations
        self.dog_index = 0

        self.image = self.dogs[self.dog_index] # Shift between different dogs
        self.rect = self.image.get_rect(bottomleft=start_position)
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0

        # Rotation when dead
        self.rotation_count = 0

    def space_bar(self):
        self.gravity = jump
        jump_sound.play()

    def apply_gravity(self):
        self.gravity += gravity
        self.rect.y += self.gravity

        # Floor and ceiling
        if self.rect.bottom > floor_height:
            self.rect.bottom = floor_height
        if self.rect.top < 0:
            self.rect.top = 0
            self.gravity = 0
    
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
            self.rect.x += speed

    def update(self):
        self.apply_gravity()
        if alive:
            self.animation_state()
        elif game_active:
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

class Bone(pygame.sprite.Sprite):
    def __init__(self, height):
        super().__init__()

        self.image = pygame.image.load('graphics/bone.png').convert_alpha()
        self.image_height = self.image.get_height()

        # Position in the gap
        y_pos = randint(height - 0.5*block_gap, height + 0.5*block_gap - self.image_height)
        self.rect = self.image.get_rect(midtop=(window_size[0]*1.1, y_pos))

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
        # Only check for mask collision when there is rect collision
        if pygame.sprite.spritecollide(sprite=dog.sprite, 
                                   group=obstacle_group, 
                                   dokill=False,
                                   collided=pygame.sprite.collide_mask):
            dog_sprite.death() # Make the dog jump before spinning
            crash_sound.play()
        return False
    else:
        return True

def collisions_bone_test():
    if pygame.sprite.spritecollide(sprite=dog.sprite, 
                                   group=bone_group, 
                                   dokill=True):
        ding_sound.play()
        # +1 in score
        return 1
    return 0

# Text functions
def display_score(score):
    score_surf = pixel_font_small.render(f"SCORE: {score}", False, (20, 20, 20))
    score_rect = score_surf.get_rect(center=(window_size[0]/2, window_size[1]/12))
    screen.blit(score_surf, score_rect)
def final_score(score):
    score_surf = pixel_font_small.render(f"FINAL SCORE: {score}", False, (20, 20, 20))
    score_rect = score_surf.get_rect(center=(window_size[0]/2, window_size[1]/3))
    screen.blit(score_surf, score_rect)

pygame.init()
screen = pygame.display.set_mode(size=window_size)
pygame.display.set_caption('Flappy Dog')
clock = pygame.time.Clock()

# Sounds
jump_sound = pygame.mixer.Sound('audio/flap.mp3')
#jump_sound.set_volume(0.1)
crash_sound = pygame.mixer.Sound('audio/collision.mp3')
crash_sound.set_volume(0.3)
ding_sound = pygame.mixer.Sound('audio/ding.mp3')
ding_sound.set_volume(0.2)

# Font
pixel_font_small = pygame.font.Font('fonts/Pixeled.ttf', size=16)
pixel_font_big = pygame.font.Font('fonts/Pixeled.ttf', size=36)
# Text, start
start_text_surf = pixel_font_big.render('FLAPPY DOG', False, (0, 0, 0))
start_text_rect = start_text_surf.get_rect(center=(window_size[0]/2, window_size[1]/3))
space_text_surf = pixel_font_small.render('PRESS SPACE TO START', False, (20, 20, 20))
space_text_rect = space_text_surf.get_rect(center=(window_size[0]/2, window_size[1]/3 + 70))
# Text, respawn
respawn_surf = pixel_font_small.render(f"PRESS SPACEBAR TO RESTART", False, (20, 20, 20))
respawn_rect = respawn_surf.get_rect(center=(window_size[0]/2, window_size[1]/3 + 40))
respawn_background_surf = pygame.Surface((window_size[0], 80), pygame.SRCALPHA) # Also box for final score
respawn_background_surf.fill(color=(255, 255, 255, 100))
respawn_background_rect = respawn_background_surf.get_rect(midtop=(window_size[0]/2, window_size[1]/3 - 16))

# Player
dog = pygame.sprite.GroupSingle()
dog.add(Dog())
dog_sprite = dog.sprite # To call Class functions
# Obstacles
obstacle_group = pygame.sprite.Group()
obstacle_attachment_group = pygame.sprite.Group()
# Bones
bone_group = pygame.sprite.Group()

# Background
background_surface = pygame.image.load('graphics/background.png').convert()
background_x = 0
background_x_max = 1000

# Distance count
dist_traversed = 0

# Status
game_active = False
alive = False
score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # When you are done pressing space bar
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:

                # Playing, press to jump
                if game_active and alive:
                    dog_sprite.space_bar()

                # Press space bar to restart to start screen
                elif (game_active and not alive
                      and dog_sprite.rect.bottom >= floor_height): # You need to touch grass before you can restart
                    game_active = False

                    # Reset dog and obtacles
                    dog_sprite.rect.x, dog_sprite.rect.y = start_position 
                    dog_sprite.image = dog_sprite.dogs[0] # initial sprite
                    obstacle_group.empty()
                    obstacle_attachment_group.empty()
                    bone_group.empty()
                    score = 0
                
                # Press space bar to start the game
                elif not game_active and not alive:
                    game_active = True
                    alive = True
                    dog.sprite.space_bar()

    # Background
    screen.blit(source=background_surface, dest=(background_x, 0))

    if alive or not game_active: # You move when the game is active or when you are at the start screen
        background_x -= speed
        if background_x < -background_x_max:
            background_x = 0

    # Player
    dog.draw(screen)
    dog.update()

    if game_active: # When you are not at the start screen

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_attachment_group.draw(screen)
        # Bones
        bone_group.draw(screen)

        # game_active = collisions_obstacle_test()
        if alive:
            alive = collisions_obstacle_test()
            score += collisions_bone_test()
            dist_traversed += speed
            obstacle_group.update()
            obstacle_attachment_group.update()
            bone_group.update()

            # Spawn obstacles and bones
            if dist_traversed > block_dist:
                dist_traversed -= block_dist
                height = randint(100, 340)
                obstacle_group.add(Obstacle('top', height))
                obstacle_group.add(Obstacle('bot', height))
                obstacle_attachment_group.add(Obstacle_attachment('top'))
                obstacle_attachment_group.add(Obstacle_attachment('bot'))
                bone_group.add(Bone(height))

        else:
            screen.blit(respawn_background_surf, respawn_background_rect)
            screen.blit(respawn_surf, respawn_rect)
            final_score(score)

        display_score(score)  

    else:
        dog_sprite.rect.y = start_position[1] # You stay at a fixed position at the start screen
        screen.blit(source=start_text_surf, dest=start_text_rect)
        screen.blit(source=space_text_surf, dest=space_text_rect)

    pygame.display.update()
    clock.tick(60)