import noise
import random
import pygame
from settings import BLACK, BLUE, BROWN, GRAY, BROWN, GRASSGREEN, FONT, TILE_SIZE, CHUNK_SIZE
from resources import ITEMS, break_sound, build_sound

# modifiers for how fast the algorythm goes through the noise pattern
noise_speed = 0.05
cave_noise_speed = 0.07
cave_noise_multiplier = 30

def generate_chunk(x,y,seed):
    """
    Generates a list of tiles with their coordinates and types using
    the perlin noise algorythm.

    Args:
        x: x chunk coord
        y: y chunk coord
        seed: offset to the noise x coord
    Returns:
        [[[tilex, tiley], tiletype], [[tilex, tiley], tiletype]]

    """

    # variation in the height differences through an other noise map
    noise_multiplier = (noise.pnoise1((x + seed) * 0.01, repeat=99999999) + 1) * 20
    # heat map for biome generation
    heat_map = int(round(noise.pnoise1((x + seed) * 0.01, repeat=99999999) * noise_multiplier))
    # setting biome based on heat map
    # 1: Forest, 2: Tundra, 3: Underground
    if heat_map < 0:
        biome = 2
    else:
        biome = 1

    chunk_data = [[], biome]
    for x_pos in range(CHUNK_SIZE):
        for y_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0

            plant_map = noise.pnoise1((target_x + seed) * 0.4, 
                                       repeat=99999999, persistence=2) * noise_multiplier
            caveheight = int(round(noise.pnoise2((target_x + seed) * cave_noise_speed, 
                                                 (target_y) * cave_noise_speed, 
                                                 repeatx=99999999, repeaty=99999999
                                                 ) * cave_noise_multiplier))
            height = int(round(noise.pnoise1((target_x + seed) * noise_speed, repeat=99999999
                                             ) * noise_multiplier))

            # cave generation
            if target_y > 29 - height:
                chunk_data[1] = 3
                if caveheight < 3:
                    tile_type = "stone"
                    if caveheight < -15:
                        tile_type = "coal block"

            # dirt
            if target_y > 8 - height and target_y < 30 - height:
                tile_type = "dirt"
            # grass
            elif target_y == 8 - height:
                if biome == 1:
                    tile_type = "grass"
                elif biome == 2:
                    tile_type = "snowy grass"

            elif target_y == 7 - height:
                # plants
                    if plant_map < 0:
                        if biome == 1:
                            tile_type = "plant"
                    # trees
                    if plant_map > 0:
                        if biome == 1:
                            if plant_map < 3:
                                tile_type = "tree1"
                            elif plant_map < 6:
                                tile_type = "tree2"
                            elif plant_map < 10:
                                tile_type = "tree3"
                        elif biome == 2:
                            if 5 < plant_map < 10:
                                tile_type = "tree4"
            if tile_type != 0:
                chunk_data[0].append([[target_x,target_y],tile_type])
    return chunk_data

def print_text(text, x, y, display, allignment=0, size=32, color=BLACK):
    """
    Prints text onto the screen
    allignments: 0=left, 1=center, 2=right
    Args:
        text, x, y, display, allignment=0, size=32, color=BLACK
    """
    font = pygame.font.SysFont(FONT, size)
    surf = font.render(text, False, color)
    if allignment == 1:
        x = x - surf.get_width() / 2
    elif allignment == 2:
        x = x - surf.get_width()
    display.blit(surf, (x, y))

def move(rect, dx, dy, tiles, slabs=[], entities=[]):
    """Moves a pygame rectangle

    Args:
        rect, tiles, dx, dy, slabs=[], entities=[]
    Returns:
        rect, collisions

    """

    collisions = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            }
    rect.x += dx
    for tile in tiles:
        if rect.colliderect(tile):
            if not tile in slabs:
                if dx > 0:
                    rect.right = tile.left
                    collisions["right"] = True
                if dx < 0:
                    rect.left = tile.right
                    collisions["left"] = True
    for entity in entities:
        if rect.colliderect(entity):
            if dx > 0:
                rect.x -= dx
            if dx < 0:
                rect.y += dx

    rect.y += dy
    for tile in tiles:
        if rect.colliderect(tile):
            if dy > 0:
                rect.bottom = tile.top
                collisions["down"] = True
            if dy < 0:
                if not tile in slabs:
                    rect.top = tile.bottom
                    collisions["up"] = True

    return rect, collisions

def get_next_tiles(pos, buildables, scrollx, scrolly):
    """
    Detects if buildable tiles are adjacent to the mouse

    Args:
        pos: (x,y), buidables: (list), scrollx, scrolly
    Returns:
        boolean
    """
    trueposx = pos[0] + scrollx
    trueposy = pos[1] + scrolly

    testrect = pygame.Rect(0, 0, TILE_SIZE*2, TILE_SIZE*2)
    testrect.centerx = trueposx
    testrect.centery = trueposy
    color = BLUE
    for tile in buildables:
        if tile.colliderect(testrect):
            return True
    return False

def remove_tile(pos, game_map, particles, drops, tiles, scrollx, scrolly, player, nodrops=False, nodistance=False):
    """
    Removes a tile and by default spawns a drop and particles

    Args:
        pos,
        game_map,
        particles,
        drops,
        tiles,
        scrollx,
        scrolly,
        player,
        nodrops=False,
        nodistance=False
    Returns:
        game_map, particles, drops

    """
    # for some stupid fucking reason this is necessary to do in here
    # otherwise the player object breaks
    from entities import DroppedItem, Particle

    # get true position from graphical coordinates
    posx = pos[0] + scrollx
    posy = pos[1] + scrolly
    # proceed if the distance between the player and pos is at most 5 tiles
    # or if the nodistance flag is enabled
    if abs(posx - player.rect.centerx) < 5*TILE_SIZE or nodistance and abs(posy - player.rect.centery) < 5*TILE_SIZE or nodistance:
        # get chunk
        chunk = get_chunk(pos, game_map, scrollx, scrolly)
        if chunk != None:
            # loop throught tile in the chunk
            for tile in game_map[chunk][0]:
                tilerect = pygame.Rect(tile[0][0]*TILE_SIZE, tile[0][1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                # if a tile exists at pos remove it
                if tilerect.collidepoint(posx, posy):
                    game_map[chunk][0].remove(tile)
                    # spawn drops if the nodrops flag isn't enabled
                    if not nodrops:
                        if tilerect in tiles:
                            tiles.remove(tilerect)
                        if tile[1] in ["dirt", "grass", "snowy grass"]:
                            drops.append(DroppedItem(tilerect.x + 5, tilerect.y + 5, 0, 0, "dirt"))
                        elif tile[1] in ["stone", "rock"]:
                            drops.append(DroppedItem(tilerect.x + 5, tilerect.y + 5, 0, 0, "rock"))
                        elif tile[1] in ["tree1", "tree2", "tree3", "tree4"]:
                            drops.append(DroppedItem(tilerect.x + 5, tilerect.y + 5, 0, 0, "plank", random.randint(5, 15)))
                            if tile[1] != "tree4" and random.randint(0, 1) == 1:
                                drops.append(DroppedItem(tilerect.x + 5, tilerect.y + 5, 0, 0, "oak sapling", 1))
                        elif tile[1] == "coal block":
                            drops.append(DroppedItem(tilerect.x + 5, tilerect.y + 5, 0, 0, "coal"))
                        else:
                            drops.append(DroppedItem(tilerect.x + 5, tilerect.y + 5, 0, 0, tile[1]))
                        
                        # spawn particles with the color defaulting to brown
                        particle_color = BROWN
                        if tile[1] in ["stone", "rock", "coal block"]:
                            particle_color = GRAY
                        elif tile[1] in ["plant", "grass"]:
                            particle_color = GRASSGREEN
                        for i in range(10):
                            particles.append(Particle(tilerect.centerx, tilerect.centery, particle_color))
                        # play the breaking sound
                        break_sound.play()
                    break
    return game_map, particles, drops

def get_chunk(pos, game_map, scrollx, scrolly):
    """
    Get chunk based on coordinates (pos)
    
    Args:
        pos, game_map, scrollx, scrolly
    Returns:
        chunk or None if no chunk exists
    """
    mousex = pos[0] + scrollx
    mousey = pos[1] + scrolly
    for chunk in game_map.keys():
        # get chunk coordinates from the game_map keys (e.g. 0;0)
        chunkx, chunky = chunk.split(";")
        chunkx = int(chunkx) * TILE_SIZE * CHUNK_SIZE
        chunky = int(chunky) * TILE_SIZE * CHUNK_SIZE
        # create a rect object for the chunk and test for collisions with the mouse
        chunkrect = pygame.Rect(chunkx, chunky, 8*TILE_SIZE, 8*TILE_SIZE)
        if chunkrect.collidepoint(mousex, mousey):
            return chunk

def tile_exists(chunk, game_map, x, y):
    """
    Check if tile exists in the game map
    Args:
        chunk, game_map, x, y
    Returns:
        tiles or None
    """
    tiles = []
    for tile in game_map[chunk][0]:
        if tile[0][0] == x and tile[0][1] == y:
            tiles.append(tile)
    if tiles:
        return tiles

def place_tile(pos, blocktype, equipped, game_map, inventory, player, scrollx, scrolly, item_cost=True):
    """
    Places into a tile based on coordinates
    Args (yeah there's a few):
        pos, blocktype, equipped, game_map, inventory, player, scrollx, scrolly, item_cost=True
    Returns:
        game_map
    """
    
    targettile = get_tile(pos, game_map, scrollx, scrolly)
    furniture = False
    if targettile != None:
        # if the target tile is a plant, just remove it and place the tile
        if targettile[1] == "plant":
            pass
            #remove_tile(pos)
        # if the target tile is furniture e.g. a wall, torches and other stuff
        # can be placed on it
        elif ITEMS[targettile[1]]["furniture"] == True:
            furniture = True
        # if a tile already exists in the target location, do nothing
        else:
            return game_map
    posx = pos[0] + scrollx
    posy = pos[1] + scrolly
    if abs(posx - player.rect.centerx) < 5*TILE_SIZE and abs(posy - player.rect.centery) < 5*TILE_SIZE:
        chunk = get_chunk(pos, game_map, scrollx, scrolly)
        chunkx, chunky = chunk.split(";")
        # iterate through the chunk and generate rects for collision testing
        for y_pos in range(CHUNK_SIZE):
            for x_pos in range(CHUNK_SIZE):
                target_x = int(chunkx) * CHUNK_SIZE * TILE_SIZE + x_pos * TILE_SIZE
                target_y = int(chunky) * CHUNK_SIZE * TILE_SIZE + y_pos * TILE_SIZE
                tilerect = pygame.Rect(target_x, target_y, TILE_SIZE, TILE_SIZE)
                
                if tilerect.collidepoint(posx, posy):
                    target_block = [[target_x // TILE_SIZE, target_y // TILE_SIZE], blocktype]
                    if tile_exists(chunk, game_map, target_x // TILE_SIZE, target_y // TILE_SIZE) == None:
                        if not tilerect.colliderect(player.rect) or furniture == True:
                            game_map[chunk][0].append(target_block)
                            build_sound.play()
                            if item_cost:
                                remove_inventory_item(inventory, equipped, equipped, 1)
                    else:
                        if ITEMS[equipped]["furniture"] == True:
                            existing_tiles = tile_exists(chunk, game_map, target_x // TILE_SIZE, target_y // TILE_SIZE)
                            if len(existing_tiles) == 1:
                                blockname = existing_tiles[0][1]
                                if equipped != blockname:
                                    if blockname == "plank wall":
                                        game_map[chunk][0].append(target_block)
                                        build_sound.play()
                                        if item_cost:
                                            remove_inventory_item(equipped, 1)
    return game_map

def get_tile(pos, game_map, scrollx, scrolly):
    """
    Gets a tile based on coordinates
    Args:
        pos, game_map
    Returns:
        tile or None if no tile is found
    """
    posx = pos[0] + scrollx
    posy = pos[1] + scrolly
    chunk = get_chunk(pos, game_map, scrollx, scrolly)
    for tile in game_map[chunk][0]:
        tilerect = pygame.Rect(tile[0][0]*TILE_SIZE, tile[0][1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if tilerect.collidepoint(posx, posy):
            return tile

def draw_tile_outline(pos, equipped, game_map, buildables, display,
                      player, scrollx, scrolly):
    posx = pos[0] + scrollx
    posy = pos[1] + scrolly
    if abs(posx - player.rect.centerx) < 5*TILE_SIZE and abs(posy - player.rect.centery) < 5*TILE_SIZE and equipped != None and equipped != "":
        if ITEMS[equipped]["tool"]:
            tile = get_tile(pos, game_map, scrollx, scrolly)
            if tile != None:
                color = BLACK
                drawrect = pygame.Rect(tile[0][0]*TILE_SIZE-scrollx, tile[0][1]*TILE_SIZE-scrolly, TILE_SIZE, TILE_SIZE)
                #if current_biome == 3 or is_night and color == BLACK:
                #    color = WHITE
                pygame.draw.rect(display, color, drawrect, 1)
        elif ITEMS[equipped]["build"]:
            if get_next_tiles(pos, buildables, scrollx, scrolly) == True:
                chunk = get_chunk(pos, game_map, scrollx, scrolly)
                chunkx, chunky = chunk.split(";")
                for y_pos in range(CHUNK_SIZE):
                    for x_pos in range(CHUNK_SIZE):
                        target_x = int(chunkx) * CHUNK_SIZE * TILE_SIZE + x_pos * TILE_SIZE
                        target_y = int(chunky) * CHUNK_SIZE * TILE_SIZE + y_pos * TILE_SIZE
                        tilerect = pygame.Rect(target_x, target_y, TILE_SIZE, TILE_SIZE)
                        if tilerect.collidepoint(posx, posy):
                            tilerect.x -= scrollx
                            tilerect.y -= scrolly
                            #if current_biome == 3 or is_night:
                            #    color = WHITE
                            #else:
                            color = BLACK
                            pygame.draw.rect(display, color, tilerect, 1)
