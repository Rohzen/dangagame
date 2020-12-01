import pygame

import constants
import levels

from player import *
from enemies import Enemy
from enemies import EnemyShot
from enemies import Explosion
from npc import Npc

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
font_name = pygame.font.match_font('arial')

BAR_LENGTH = 100
BAR_HEIGHT = 10

pygame.init()

player_img = pygame.image.load('img\hamster.png').convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(constants.WHITE)

player_die_sound = pygame.mixer.Sound('sounds/rumble1.ogg')

def main_menu():
    global screen

    #menu_song = pygame.mixer.music.load('sounds/menu.ogg')
    #pygame.mixer.music.play(-1)

    title = pygame.image.load('img/main_menu.png').convert()
    title = pygame.transform.scale(title, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), screen)

    #screen.blit(title, (0,0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                main()
                #break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
        else:
            draw_text(screen, "Press [ENTER] To Begin", 30, constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2+100)
            draw_text(screen, "or [Q] To Quit", 30, constants.SCREEN_WIDTH/2, (constants.SCREEN_HEIGHT/2)+140)
            pygame.display.update()

    #pygame.mixer.music.stop()
    # ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    # ready.play()
    screen.fill(constants.BLACK)
    draw_text(screen, "GET READY!", 40, constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)
    pygame.display.update()
    

def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, constants.WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    # if pct < 0:
    #     pct = 0
    pct = max(pct, 0) 
    ## moving them to top
    # BAR_LENGTH = 100
    # BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, constants.BLUE, fill_rect)
    pygame.draw.rect(surf, constants.WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def game_over():
    global screen

    #menu_song = pygame.mixer.music.load('sounds/menu.ogg')
    #pygame.mixer.music.play(-1)

    #title = pygame.image.load('img/main_menu.png').convert()
    #title = pygame.transform.scale(title, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), screen)
    screen.fill(constants.BLACK)
    #screen.blit(title, (0,0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                main_menu()
                #break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
        else:
            draw_text(screen, "GAME OVER", 30, constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)
            draw_text(screen, "Press [ENTER] To MENU", 30, constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2+100)
            draw_text(screen, "or [Q] To Quit", 30, constants.SCREEN_WIDTH/2, (constants.SCREEN_HEIGHT/2)+140)
            pygame.display.update()

    #pygame.mixer.music.stop()
    # ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    # ready.play()
    
    #draw_text(screen, "GET READY!", 40, constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)
    #pygame.display.update()



def main():
    """ Main Program """
    #pygame.init()
    #main_menu()
    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Danga")

    ### Main score song we pause for debug
    song = pygame.mixer.Sound("sounds/danga.wav")
    song.play(-1)

    score = 0
    # Create the player
    player = Player()
    player_shot = None
    # Create the enemy
    enemy = Enemy()
    enemies  = pygame.sprite.Group()
    npcs  = pygame.sprite.Group()

    #Prepare for enemy_shots
    enemy_shots  = pygame.sprite.Group()

    npc = Npc()

    # Create all the levels
    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    enemy.level = current_level
    npc.level = current_level

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    enemy.rect.x = constants.SCREEN_WIDTH - enemy.rect.width
    enemy.rect.y = 0 #constants.SCREEN_HEIGHT - enemy.rect.height

    active_sprite_list.add(enemy)
    enemies.add(enemy)

    npc.rect.x = constants.SCREEN_WIDTH - enemy.rect.width
    npc.rect.y = 0 #constants.SCREEN_HEIGHT - enemy.rect.height

    #aggiungiano un NPC ?
    #active_sprite_list.add(npc)
    #npcs.add(npc)

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    player.yell()
                if event.key == pygame.K_LCTRL:
                    #shots.append(Shot(player.rect.center, player.direction))
                    player_shot = Shot(player.rect.center, player.direction)
                    active_sprite_list.add(player_shot)
                #if event.key == pygame.K_RCTRL:
                    #shots.append(EnemyShot(enemy.rect.center))
                    #active_sprite_list.add(EnemyShot(enemy.rect.center, player))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        ### ENEMY SHOTS
        time_now = pygame.time.get_ticks()
        #print (str(time_now - enemy.last_shot))
        if time_now - enemy.last_shot > 1500:
            current_shot = EnemyShot(enemy.rect.center, player)
            enemy_shots.add(current_shot)
            active_sprite_list.add(current_shot)
            enemy.last_shot = time_now
            #draw_text('COLLIDE!', font40, constants.WHITE, int( constants.SCREEN_WIDTH / 2 - 100), int( constants.SCREEN_HEIGHT / 2 + 50))

        ### MAIN COLLISION (Player Shot)
        if player_shot:
            if pygame.sprite.collide_rect(player_shot, enemy):
               #print("COLLIDE")
               explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, 4)
               active_sprite_list.add(explosion)
               score += 10

        ### MAIN COLLISION (Enemy Shot)
        if pygame.sprite.collide_rect(current_shot, player):
           #print("COLLIDE")
           explosion = DeathExplosion(player.rect.centerx, player.rect.centery, 4)
           active_sprite_list.add(explosion)
           player.shield = player.shield -3

        ### SHIELD, DEATH, LIVES AND GAME OVER
        if player.shield <= 0: 
            player_die_sound.play()
            death_explosion = DeathExplosion(player.rect.centerx, player.rect.centery, 4)
            active_sprite_list.add(death_explosion)
            # running = False     ## GAME OVER 3:D
            player.hide()
            player.lives -= 1
            player.shield = 100

        ## if player died and the explosion has finished, end game
        if player.lives == 0 and not death_explosion.alive():
            done = True
            #draw_text(screen, "GAME OVER", 30, constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)

        ### SPRITE UPDATES
        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        ### PLAYER SCREEN LIMITS

        # print ('x:'+str(player.rect.x))
        # print ('y:'+str(player.rect.y))
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.x <= 120:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        ### DRAWS

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        draw_text(screen, str(score), 18, constants.SCREEN_WIDTH / 2, 10) ## 10px down from the screen
        #draw_shield_bar(screen, 5, 5, 100)
        draw_shield_bar(screen, 5, 5, player.shield)

        # Draw lives
        draw_lives(screen, constants.SCREEN_WIDTH - 100, 5, player.lives, player_mini_img)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    game_over()
    main_menu()
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    #pygame.quit()



if __name__ == "__main__":
    main_menu()
    #main()
