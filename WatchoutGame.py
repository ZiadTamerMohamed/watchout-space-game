import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800 # Set the window size to 1000x800 for better visibility and gameplay experience.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Watchout!")

BG = pygame.transform.scale(pygame.image.load("images.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_VEL = 5
DIS_WIDTH = 10
DIS_HEIGHT = 20
DIS_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)
LARGE_FONT = pygame.font.SysFont("comicsans", 50)

def draw(player, elapsed_time, disabilities, player_name):
    WIN.blit(BG, (0, 0))
    
    # Render the time and player name
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    name_text = FONT.render(f"Player: {player_name}", 1, "white")
    
    WIN.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))
    WIN.blit(name_text, (10, 10))
    
    pygame.draw.rect(WIN, "red", player)
    
    for dis in disabilities:
        pygame.draw.rect(WIN, "white", dis)
    
    pygame.display.update()

def get_player_name():
    player_name = ""
    input_active = True
    
    while input_active:
        WIN.blit(BG, (0, 0))
        title_text = LARGE_FONT.render("Enter Your Name:", 1, "white")
        name_text = FONT.render(player_name, 1, "white")
        
        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, HEIGHT/2 - 50))
        pygame.draw.rect(WIN, "white", (WIDTH/2 - 150, HEIGHT/2, 300, 40), 2)
        WIN.blit(name_text, (WIDTH/2 - name_text.get_width()/2, HEIGHT/2 + 10))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 15 and event.unicode.isalnum():
                        player_name += event.unicode
    
    return player_name

def save_score(player_name, score):
    with open("scores.txt", "a") as f:
        f.write(f"{player_name}: {score}\n")

def show_game_over(score):
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        
        game_over_text = LARGE_FONT.render("Game Over!", 1, "white")
        score_text = FONT.render(f"Your Score: {round(score)} seconds", 1, "white")
        restart_text = FONT.render("Press R to restart or Q to quit", 1, "white")
        
        WIN.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - 100))
        WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2))
        WIN.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2 + 100))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run = False
                    main()  # Restart the game
                elif event.key == pygame.K_q:
                    run = False
    
    pygame.quit()

def main():
    player_name = get_player_name() # Get player name
    if not player_name:
        return
    
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    
    dis_add_increment = 2000
    dis_count = 0
    disabilities = []
    hit = False
    
    while run:
        dis_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        if dis_count > dis_add_increment:
            for _ in range(3):
                dis_x = random.randint(0, WIDTH - DIS_WIDTH)
                dis = pygame.Rect(dis_x, -DIS_HEIGHT, DIS_WIDTH, DIS_HEIGHT)
                disabilities.append(dis)
            
            dis_add_increment = max(200, dis_add_increment - 50)
            dis_count = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL
        
        for dis in disabilities[:]:
            dis.y += DIS_VEL
            if dis.y > HEIGHT:
                disabilities.remove(dis)
            elif dis.y + DIS_HEIGHT >= player.y and dis.colliderect(player):
                hit = True
                break
        
        if hit:
            save_score(player_name, elapsed_time)
            show_game_over(elapsed_time)
            break
        
        draw(player, elapsed_time, disabilities, player_name)
    
    pygame.quit()

if __name__ == "__main__":
    main()