import pygame
import sys
import sqlite3
from database import init_db # type: ignore
from authentication import register_user, login_user # type: ignore

pygame.init()

# Screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mystic Realms: Collector's Edition")

# Load assets
background = pygame.image.load('assets/ui/background.png')
button_image = pygame.image.load('assets/ui/button.png')

# Fonts and colors
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
white = (255, 255, 255)
black = (0, 0, 0)

# Global variables
current_user = None
coins = 0

# Helper functions
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def get_user_cards(username):
    conn = sqlite3.connect('mystic_realms.db')
    c = conn.cursor()
    c.execute('SELECT card_id FROM user_cards WHERE username = ?', (username,))
    user_cards = c.fetchall()
    conn.close()
    return user_cards

def get_user_coins(username):
    conn = sqlite3.connect('mystic_realms.db')
    c = conn.cursor()
    c.execute('SELECT coins FROM users WHERE username = ?', (username,))
    coins = c.fetchone()[0]
    conn.close()
    return coins

def update_user_coins(username, amount):
    conn = sqlite3.connect('mystic_realms.db')
    c = conn.cursor()
    c.execute('UPDATE users SET coins = ? WHERE username = ?', (amount, username))
    conn.commit()
    conn.close()

def give_daily_pack(username):
    daily_reward = 100
    current_coins = get_user_coins(username)
    update_user_coins(username, current_coins + daily_reward)

def purchase_pack(username, cost):
    current_coins = get_user_coins(username)
    if current_coins >= cost:
        update_user_coins(username, current_coins - cost)
        return True
    return False

def pawn_card(username, card_id):
    conn = sqlite3.connect('mystic_realms.db')
    c = conn.cursor()
    c.execute('SELECT value FROM cards WHERE id = ?', (username, card_id))
    card_value = c.fetchone()[0]
    pawn_value = int(card_value * 0.8)

    current_coins = get_user_coins(username)
    update_user_coins(username, current_coins + pawn_value)

    c.execute('DELETE FROM user_cards WHERE username = ? AND card_id = ?', (username, card_id))
    conn.commit()
    conn.close()

# Main game functions
def main_menu():
    while True:
        screen.blit(background, (0, 0))
        draw_text('Mystic Realms: Collector\'s Edition', font, white, screen, 20, 20)
        draw_text('Register', font, white, screen, 20, 100)
        draw_text('Login', font, white, screen, 20, 150)
        draw_text('Exit', font, white, screen, 20, 200)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    register_screen()
                elif event.key == pygame.K_2:
                    login_screen()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()
            

def register_screen():
    global current_user, coins
    username = input("Enter new username: ")
    password = input("Enter new password: ")

    success, message = register_user(username, password)
    if success:
        print(message)
        current_user = username
        coins = get_user_coins(current_user)
        game_menu()

def login_screen():
    global current_user, coins
    username = input("Enter username: ")
    password = input("Enter password: ")

    success, message = login_user(username, password)
    print(message)
    if success:
        current_user = username
        coins = get_user_coins(current_user)
        give_daily_pack(current_user)
        game_menu()

def game_menu():
    while True:
        screen.blit(background, (0, 0))
        draw_text(f'Logged in as: {current_user}', font, white, screen, 20, 20)
        draw_text(f'Coins: {coins}', font, white, screen, 20, 60)
        draw_text('View cards', font, white, screen, 20, 100)
        draw_text('Shop', font, white, screen, 20, 150)
        draw_text('Pawn', font, white, screen, 20, 200)
        draw_text('Logout', font, white, screen, 20, 250)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    view_cards()
                elif event.key == pygame.K_2:
                    shop_screen()
                elif event.key == pygame.K_3:
                    pawn_screen()
                elif event.key == pygame.K_4:
                    main_menu()

def view_cards():
    user_cards = get_user_cards(current_user)
    while True:
        screen.blit(background, (0, 0))
        draw_text('Your Cards:', font, white, screen, 20, 20)
        y_offset = 60
        for card in user_cards:
            draw_text(f"Card ID: {card[0]}", font, white, screen, 20, y_offset)
            y_offset += 40
        draw_text('Press ESC to return to menu', small_font, white, screen, 20, y_offset)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def shop_screen():
    global coins
    while True:
        screen.blit(background, (0, 0))
        draw_text('Shop:', font, white, screen, 20, 20)
        draw_text('[1] Buy Card Pack (100 coins)', font, white, screen, 20, 60)
        draw_text('Press ESC to return to menu', small_font, white, screen, 20, 100)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    cost = 100
                    if purchase_pack(current_user, cost):
                        print ("Purchsed a card pack!")
                    else:
                        print ("Not enough coins!")
                elif event.key == pygame.K_ESCAPE:
                    return


def pawn_screen():
    global coins
    user_cards = get_user_cards(current_user)
    while True:
        screen.blit(background, (0, 0))
        draw_text('Pawn Shop:', font, white, screen, 20, 20)
        y_offset = 60
        for card in user_cards:
            draw_text(f"Card ID: {card[0]}", font, white, screen, 20, y_offset)
            y_offset += 40
        draw_text('Enter Card ID to Pawn:', small_font, white, screen, 20, y_offset)
        draw_text('Press ESC to return to menu', small_font, white, screen, 20, 500)

        pygame.display.update()

        card_id = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    card_id = input ("Card ID: ")
                    if card_id:
                        pawn_card(current_user, card_id)
                        coins = get_user_coins(current_user)
                        print ("Selled card!")
                        return

if __name__ == "__main__":
    init_db()
    main_menu()
