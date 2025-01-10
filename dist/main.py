import pygame
import math,sys,os
from board import Board
from board import Game
import random

def resource_path(relative_path):
    """Obtenir le chemin absolu pour les ressources"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialisation de pygame
pygame.init()
pygame.mixer.init()
# Couleurs
blanc = (255, 255, 255)
largeur, hauteur = 650, 650



pygame.display.set_caption("ECHECS")
ecran = pygame.display.set_mode((650, 650))
background = pygame.image.load("chess1 (2).jpg")

# Notre bannière
banner = pygame.image.load("sdeco-1962066712.jpg")
banner = pygame.transform.scale(banner, (300, 90))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(ecran.get_width() / 3.3)
banner_rect.y = math.ceil(ecran.get_height() / 2.8)

# icone de musique
banner2 = pygame.image.load("la-musique(2).png")
banner2 = pygame.transform.scale(banner2, (60, 60))
banner_rect2 = banner2.get_rect()
banner_rect2.x = math.ceil(ecran.get_width() / 22)
banner_rect2.y = math.ceil(ecran.get_height() / 1.2)

# Importe le bouton
play_button = pygame.image.load("bouton-219749262.jpg")
play_button = pygame.transform.scale(play_button, (250, 60))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(ecran.get_width() / 2.9)
play_button_rect.y = math.ceil(ecran.get_height() / 2)
board = Board()

# chargrenment du son
click_sound = pygame.mixer.Sound("bruit2.wav")
# Classe pour représenter un flocon de neige
class Flocon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill(blanc)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largeur)
        self.rect.y = random.randint(0, hauteur)

    def update(self):
        self.rect.y += 1
        if self.rect.y > hauteur:
            self.rect.y = 0
            self.rect.x = random.randint(0, largeur)


# Groupe de sprites pour tous les flocons de neige
tous_les_flocons = pygame.sprite.Group()

# Création de quelques flocons au début
for _ in range(60):
    flocon = Flocon()
    tous_les_flocons.add(flocon)

# boucle principale
music_playing = True
game = Game()
running = True
music_file = "Chess-Music-Enhance-Your-Playing-Experience.mp3"
pygame.mixer.music.load(music_file)
pygame.mixer.music.play(-1)
try:

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if banner_rect2.collidepoint(mouse_x, mouse_y):  # Si le clic est sur banner2
                    if music_playing:  # Si la musique est en cours
                        pygame.mixer.music.pause()  # Mettre en pause la musique
                    else:
                        pygame.mixer.music.unpause()  # Reprendre la musique
                    music_playing = not music_playing  # Inverser l'état de la musique
                elif play_button_rect.collidepoint(mouse_x, mouse_y):
                    click_sound.play()
                    game.is_playing = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                game.Board.handle_piece_selection(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                game.Board.handle_piece_movement(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                game.Board.handle_mouse_up(ecran)
        ecran.blit(background, (0, 0))
        if game.is_playing:
            game.update()

        else:
            ecran.blit(banner, banner_rect)
            ecran.blit(play_button, play_button_rect)
            ecran.blit(banner2, banner_rect2)

            horloge = pygame.time.Clock()
            tous_les_flocons.update()
            tous_les_flocons.draw(ecran)
            horloge.tick(65)
            pygame.display.flip()

except Exception as e:
    print(f"Une erreur est survenue : {e}")

pygame.quit()