import pygame

# music and sounds
mixer.init()
#mixer.music.set_volume(0.5)
mixer.music.load("music/oyho.ogg")
jump_sound = mixer.Sound("music/jump.wav")
throw_sound = mixer.Sound("music/throw.wav")
hurt_sound = mixer.Sound("music/hurt.wav")
break_sound = mixer.Sound("music/break.wav")
death_sound = mixer.Sound("music/death.wav")
build_sound = mixer.Sound("music/build.wav")

# player images
player_image1 = pygame.image.load("images/player1.png").convert()
player_image2 = pygame.image.load("images/player2.png").convert()
player_image1.set_colorkey(GREEN)
player_image2.set_colorkey(GREEN)
player_images = [player_image1, player_image2]

# tile images
grasstile = pygame.image.load("images/tiles/grass.png").convert()
snowy_grass = pygame.image.load("images/tiles/snowy_grass.png").convert()
rocktile = pygame.image.load("images/tiles/rock.png").convert()
stonetile = pygame.image.load("images/tiles/stone.png").convert()
dirttile = pygame.image.load("images/tiles/dirt.png").convert()
planktile = pygame.image.load("images/tiles/plank.png").convert()
coaltile = pygame.image.load("images/tiles/coaltile.png").convert()
plank_wall = pygame.image.load("images/tiles/plank_wall.png").convert()
plant_image = pygame.image.load("images/tiles/plant.png").convert()
plant_image.set_colorkey((255, 255, 255))

# tools
hammer_image = pygame.image.load("images/hammer.png").convert()
hammer_image.set_colorkey(WHITE)
pick_image = pygame.image.load("images/pickaxe.png").convert()
pick_image.set_colorkey(WHITE)
shovel_image = pygame.image.load("images/spade.png").convert()
shovel_image.set_colorkey(WHITE)
axe_image = pygame.image.load("images/axe.png").convert()
axe_image.set_colorkey(WHITE)
hoe_image = pygame.image.load("images/hoe.png").convert()
hoe_image.set_colorkey(WHITE)


# others
select_arrow = pygame.image.load("images/select_arrow.png")
select_arrow.set_colorkey(WHITE)
sapling_image = pygame.image.load("images/sapling.png").convert()
sapling_image.set_colorkey(WHITE)
slab_image = pygame.image.load("images/slab.png").convert()
slab_image.set_colorkey(WHITE)
coal_item = pygame.image.load("images/coal.png").convert()
coal_item.set_colorkey(WHITE)
arrow_image = pygame.image.load("images/arrow.png").convert()
arrow_image.set_colorkey(WHITE)
torch_image = pygame.image.load("images/torch.png").convert()
torch_image.set_colorkey(WHITE)
heart_image = pygame.image.load("images/heart.png").convert()
heart_image.set_colorkey(WHITE)
meat_image = pygame.image.load("images/meat.png").convert()
meat_image.set_colorkey(GREEN)
worm_head = pygame.image.load("images/worm/head.png").convert()
worm_head.set_colorkey(WHITE)
worm_body = pygame.image.load("images/worm/body.png").convert()
worm_body.set_colorkey(WHITE)
worm_tail = pygame.image.load("images/worm/tail.png").convert()
worm_tail.set_colorkey(WHITE)
background_image = pygame.transform.scale(pygame.image.load("images/background.png").convert(), (W, H))
night_background_image = pygame.transform.scale(pygame.image.load("images/background_night.png").convert(), (W, H))

polarbear_images = []
for i in range(0, 12):
    polarbear_image = pygame.transform.scale(pygame.image.load("images/polarbear/{}.png".format(i)), (32, 32))
    polarbear_images.append(polarbear_image)

skeleton_images = []
for i in range(1, 3):
    image = pygame.image.load("images/skeleton/skeleton{}.png".format(str(i)))
    image.set_colorkey(GREEN)
    skeleton_images.append(image)

crow_images = []
for i in range(1, 4):
    crow = pygame.transform.scale(pygame.image.load("images/crow/{}.png".format(i)), (16, 16))
    crow_images.append(crow)

tree_images = []
for i in range(1,5):
    tree_image = pygame.image.load("images/trees/tree{}.png".format(i)).convert()
    tree_image.set_colorkey((255, 255, 255))
    tree_images.append(tree_image)

explosion_images = []
for i in range(0, 9):

    explosion_image = pygame.image.load("images/explosion/{}.png".format(i)).convert()
    explosion_image.set_colorkey((229, 229, 229))
    explosion_images.append(explosion_image)
