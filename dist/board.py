import pygame
import sys
from pieces import Pieces

pygame.init()

# Couleurs
couleur_blanc = (220, 220, 220)
couleur_noir = (130, 130, 130)

class Player:
    def __init__(self):
        pass

class Board:
    def __init__(self):
        self.pieces = Pieces(80, 80)
        self.selected_piece = None
        self.possible_moves = []

    def handle_piece_selection(self, mouse_x, mouse_y):
        row = mouse_y // 80
        col = mouse_x // 80

        clicked_piece = self.pieces.get_piece(row, col)

        if clicked_piece is not None:
            self.selected_piece = clicked_piece
            self.current_row, self.current_col = row, col
            self.possible_moves = self.pieces.get_possible_moves(row, col)
            print(f"Possible moves: {self.possible_moves}")  # Debug
        else:
            self.selected_piece = None
            self.possible_moves = []

    def handle_piece_movement(self, mouse_x, mouse_y):
        if self.selected_piece is not None:
            self.current_row = mouse_y // 80
            self.current_col = mouse_x // 80

    def handle_mouse_up(self, ecran):
        if self.selected_piece is not None:
            end_row, end_col = self.current_row, self.current_col
            move_result = self.pieces.move_piece(self.selected_piece.row, self.selected_piece.col, end_row, end_col)

            # Vérifier si le roi est éliminé
            roi_blanc_position = self.pieces.trouver_roi("white")
            roi_noir_position = self.pieces.trouver_roi("black")

            if roi_blanc_position is not None:
                roi_blanc_present = self.pieces.get_piece(roi_blanc_position[0], roi_blanc_position[1]) is not None
            else:
                roi_blanc_present = False

            if roi_noir_position is not None:
                roi_noir_present = self.pieces.get_piece(roi_noir_position[0], roi_noir_position[1]) is not None
            else:
                roi_noir_present = False

            if not roi_blanc_present:
                print("Le roi blanc est éliminé!")
                self.display_end_message("Échec et mat ! Les Noirs gagnent!", ecran)
            elif not roi_noir_present:
                print("Le roi noir est éliminé!")
                self.display_end_message("Échec et mat ! Les Blancs gagnent!", ecran)
            elif move_result == "echec_et_mat":
                self.highlight_king_in_checkmate(ecran)
                if self.pieces.current_player == "white":
                    print("Les Noirs sont en échec et mat!")
                    self.display_end_message("Échec et mat ! Les Blancs gagnent!", ecran)
                else:
                    print("Les Blancs sont en échec et mat!")
                    self.display_end_message("Échec et mat ! Les Noirs gagnent!", ecran)
            elif move_result == "echec":
                if self.pieces.current_player == "black":
                    print("Les Blancs sont en échec!")
                    self.display_end_message("Échec ! Les Blancs sont en danger.", ecran)
                else:
                    print("Les Noirs sont en échec!")
                    self.display_end_message("Échec ! Les Noirs sont en danger.", ecran)

            self.selected_piece = None
            self.possible_moves = []  # Clear possible moves after a move is made

    def draw_selected_piece_highlight(self, ecran):
        if self.selected_piece is not None:
            pygame.draw.rect(ecran, (0, 255, 0), (self.selected_piece.col * 80, self.selected_piece.row * 80, 80, 80), 3)

    def draw_board(self, ecran):
        for i in range(8):
            for j in range(8):
                couleur_case = couleur_blanc if (i + j) % 2 == 0 else couleur_noir
                pygame.draw.rect(ecran, couleur_case, (i * 80, j * 80, 80, 80))

                piece = self.pieces.get_piece(j, i)
                if piece is not None:
                    ecran.blit(piece.image, (i * self.pieces.largeur_case, j * self.pieces.hauteur_case))

            # Appeler highlight_king_in_checkmate une seule fois après avoir dessiné tout le plateau
        self.highlight_king_in_checkmate(ecran)

        # Draw possible moves
        for move in self.possible_moves:
            row, col = move
            pygame.draw.circle(ecran, (0, 255, 0, 128), (col * 80 + 40, row * 80 + 40), 10)

    def reset_board(self):
        self.pieces = Pieces(80, 80)

    def highlight_king_in_checkmate(self, ecran):
        # Créez une surface avec la même taille que la case
        surface_transparente = pygame.Surface((80, 80), pygame.SRCALPHA)

        # Définir la couleur rouge transparent avec un alpha de 100
        rouge_transparent = (255, 0, 0, 100)
        surface_transparente.fill(rouge_transparent)

        # Déterminez si un roi est en échec et mat
        roi_blanc_en_mat = self.pieces.est_echec_et_mat("white")
        roi_noir_en_mat = self.pieces.est_echec_et_mat("black")

        if roi_blanc_en_mat:
            ligne, colonne = self.pieces.trouver_roi("white")
            ecran.blit(surface_transparente, (colonne * 80, ligne * 80))
        elif roi_noir_en_mat:
            ligne, colonne = self.pieces.trouver_roi("black")
            ecran.blit(surface_transparente, (colonne * 80, ligne * 80))

    def display_end_message(self, message, ecran):
        font = pygame.font.Font(None, 50)
        fonts = pygame.font.Font(None, 57)

        # Charger l'image de fond
        background_image = pygame.image.load('10087525.jpg')
        background_image = pygame.transform.scale(background_image, (ecran.get_width(), ecran.get_height()))

        # Afficher l'image de fond
        ecran.blit(background_image, (0, 0))

        # Afficher le texte
        text = font.render(message, True, (5, 5, 5))
        text_rect = text.get_rect(center=(ecran.get_width() / 2, ecran.get_height() // 2 - 170))
        ecran.blit(text, text_rect)

        # Dessinez les boutons
        replay_rect = pygame.Rect(ecran.get_width() // 2 - 185, ecran.get_height() // 2 - 5, 150, 70)
        quit_rect = pygame.Rect(ecran.get_width() // 2 + 35, ecran.get_height() // 2 - 8, 150, 70)
        pygame.draw.rect(ecran, (5, 5, 5), replay_rect)
        pygame.draw.rect(ecran, (5, 5, 5), quit_rect)
        replay_text = fonts.render("Replay", True, (255, 255, 255))
        quit_text = fonts.render("  Quit", True, (255, 255, 255))
        ecran.blit(replay_text, replay_rect.move(10, 10))
        ecran.blit(quit_text, quit_rect.move(10, 10))

        pygame.display.flip()

        # Attendez que l'utilisateur fasse un choix
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if replay_rect.collidepoint(mouse_x, mouse_y):
                        self.reset_board()  # Réinitialiser le jeu
                        waiting = False
                    elif quit_rect.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        sys.exit()


class Game:
    def __init__(self):
        self.is_playing = False
        self.pressed = {}
        self.player = Player()
        self.Board = Board()
        self.ecran = pygame.display.set_mode((80 * 8, 80 * 8))
        pygame.display.set_caption("PLATEAU d'échecs")

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choix = afficher_boite_dialogue(self.ecran)
                    if choix == "Redémarrer":
                        self.Board.reset_board()
                        return True
                    elif choix == "Quitter":
                        pygame.quit()
                        return False
                    elif choix == "Continuer":
                        return True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    self.Board.handle_piece_selection(mouse_x, mouse_y)
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    self.Board.handle_piece_movement(mouse_x, mouse_y)
                elif event.type == pygame.MOUSEBUTTONUP:
                    move_result = self.Board.handle_mouse_up(self.ecran)
                    if move_result == "echec_et_mat":
                        self.Board.display_end_message("Échec et mat!", self.ecran)
                    elif move_result == "echec":
                        self.Board.display_end_message("Échec!", self.ecran)

            self.Board.draw_board(self.ecran)
            self.Board.draw_selected_piece_highlight(self.ecran)
            pygame.display.flip()

def afficher_boite_dialogue(ecran):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 160 <= mouse_x <= 310 and 210 <= mouse_y <= 280:
                    return "Continuer"
                elif 340 <= mouse_x <= 490 and 210 <= mouse_y <= 280:
                    return "Redémarrer"
                elif 240 <= mouse_x <= 420 and 340 <= mouse_y <= 415:
                    return "Quitter"

        pygame.draw.rect(ecran, (195, 220, 225), (150, 180, 350, 250))
        pygame.draw.rect(ecran, (0, 0, 0), (160, 210, 150, 70))
        pygame.draw.rect(ecran, (0, 0, 0), (340, 210, 150, 70))
        pygame.draw.rect(ecran, (0, 0, 0), (240, 340, 180, 75))

        font = pygame.font.Font(None, 39)
        texte_continuer = font.render(" Continue", True, (255, 255, 255))
        texte_redemarrer = font.render("REPLAY", True, (255, 255, 255))
        texte_quitter = font.render(" QUIT ", True, (255, 255, 255))
        ecran.blit(texte_continuer, (170, 230))
        ecran.blit(texte_redemarrer, (365, 230))
        ecran.blit(texte_quitter, (285, 365))

        pygame.display.flip()


if __name__ == "__main__":
    largeur_case = 80
    hauteur_case = 80
    taille_ecran = (largeur_case * 8, hauteur_case * 8)

    ecran = pygame.display.set_mode(taille_ecran)
    pygame.display.set_caption("PLATEAU d'échecs")

    game = Game()
    game.update(ecran)
