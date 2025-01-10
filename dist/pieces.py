import pygame
import os

class Pieces:
    def __init__(self, largeur_case, hauteur_case):
        self.largeur_case = largeur_case
        self.hauteur_case = hauteur_case
        self.current_player = 'white'  # Commencer par les blancs
        self.images = {
            'p': pygame.image.load(os.path.join('chess_images/bP.png')),
            'r': pygame.image.load(os.path.join('chess_images/bR.png')),
            'n': pygame.image.load(os.path.join('chess_images/bKN.png')),
            'b': pygame.image.load(os.path.join('chess_images/bB.png')),
            'q': pygame.image.load(os.path.join('chess_images/bK.png')),
            'k': pygame.image.load(os.path.join('chess_images/bQ.png')),
            'P': pygame.image.load(os.path.join('chess_images/wp.png')),
            'R': pygame.image.load(os.path.join('chess_images/wR.png')),
            'N': pygame.image.load(os.path.join('chess_images/wKN.png')),
            'B': pygame.image.load(os.path.join('chess_images/wB.png')),
            'Q': pygame.image.load(os.path.join('chess_images/wK.png')),
            'K': pygame.image.load(os.path.join('chess_images/wQ.png')),
        }

        for piece, image in self.images.items():
            self.images[piece] = pygame.transform.scale(image, (self.largeur_case, self.hauteur_case))

            # Charger les sons des déplacements
        self.move_sound = pygame.mixer.Sound(os.path.join('bruit2.wav'))

        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def switch_player(self):
        if self.current_player == 'white':
            self.current_player = 'black'
        else:
            self.current_player = 'white'

    def get_piece(self, row, col):
        piece_symbol = self.board[row][col]
        if piece_symbol != ' ':
            return self.Piece(piece_symbol, self.images[piece_symbol], row, col)

    def est_en_echec(self, joueur):
        position_roi = self.trouver_roi(joueur)
        if position_roi is None:
            return False

        adversaire = 'black' if joueur == 'white' else 'white'
        for ligne in range(8):
            for colonne in range(8):
                piece = self.board[ligne][colonne]
                if piece != ' ' and (piece.isupper() if adversaire == 'white' else piece.islower()):
                    if self.is_valid_move(ligne, colonne, position_roi[0], position_roi[1]):
                        return True
        return False

    def est_echec_et_mat(self, joueur):
        if not self.est_en_echec(joueur):
            return False

        for ligne_depart in range(8):
            for colonne_depart in range(8):
                piece = self.board[ligne_depart][colonne_depart]
                if piece != ' ' and (piece.isupper() if joueur == 'white' else piece.islower()):
                    for ligne_arrivee in range(8):
                        for colonne_arrivee in range(8):
                            if self.is_valid_move(ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee):
                                # Essayer le mouvement
                                piece_arrivee_originale = self.board[ligne_arrivee][colonne_arrivee]
                                self.board[ligne_arrivee][colonne_arrivee] = self.board[ligne_depart][colonne_depart]
                                self.board[ligne_depart][colonne_depart] = ' '

                                # Vérifier si le roi est toujours en échec
                                toujours_en_echec = self.est_en_echec(joueur)

                                # Annuler le mouvement
                                self.board[ligne_depart][colonne_depart] = self.board[ligne_arrivee][colonne_arrivee]
                                self.board[ligne_arrivee][colonne_arrivee] = piece_arrivee_originale

                                if not toujours_en_echec:
                                    return False
        return True

    def trouver_roi(self, joueur):
        symbole_roi = 'K' if joueur == 'white' else 'k'
        for ligne in range(8):
            for colonne in range(8):
                if self.board[ligne][colonne] == symbole_roi:
                    return (ligne, colonne)
        return None

    def move_piece(self, start_row, start_col, end_row, end_col):
        if self.is_valid_move(start_row, start_col, end_row, end_col):
            piece_to_move = self.board[start_row][start_col]
            piece_capturee = self.board[end_row][end_col]
            self.board[start_row][start_col] = ' '
            self.board[end_row][end_col] = piece_to_move

            # Jouer le son de déplacement
            self.move_sound.play()

            # Vérifier l'échec et mat
            adversaire = 'black' if self.current_player == 'white' else 'white'
            if self.est_en_echec(self.current_player):
                # Annuler le mouvement si le joueur se met lui-même en échec
                self.board[start_row][start_col] = piece_to_move
                self.board[end_row][end_col] = piece_capturee
                return False

            if self.est_echec_et_mat(adversaire):
                return "echec_et_mat"
            elif self.est_en_echec(adversaire):
                self.switch_player()
                return "echec"

            # Changer de joueur
            self.switch_player()
            return True
        else:
            return False

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        # Vérifier si les coordonnées de départ et d'arrivée sont valides
        if start_row < 0 or start_row > 7 or start_col < 0 or start_col > 7:
            return False
        if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
            return False

        start_piece = self.board[start_row][start_col]
        end_piece = self.board[end_row][end_col]

        # Vérifier si la case de départ contient une pièce et si la case d'arrivée est vide ou contient une pièce adverse
        if start_piece == ' ' or (start_piece.islower() and end_piece.islower()) or (
                start_piece.isupper() and end_piece.isupper()):
            return False

        # Vérifier si la pièce à déplacer appartient au joueur actuel
        if (self.current_player == 'white' and start_piece.islower()) or \
                (self.current_player == 'black' and start_piece.isupper()):
            return False

        # Vérifier le mouvement spécifique à chaque type de pièce
        piece_type = start_piece.lower()
        if piece_type == 'p':  # Pion
            if start_col != end_col:  # Déplacement latéral
                if start_piece.islower() and abs(start_row - end_row) == 1 and abs(
                        start_col - end_col) == 1 and end_piece.isupper():
                    return True
                elif start_piece.isupper() and abs(start_row - end_row) == 1 and abs(
                        start_col - end_col) == 1 and end_piece.islower():
                    return True
                return False
            if start_piece.isupper():  # Pion blanc
                if start_row - end_row == 1:  # Avancer d'une case
                    return end_piece == ' '
                elif start_row == 6 and start_row - end_row == 2 and end_piece == ' ' and self.board[start_row - 1][
                    start_col] == ' ':  # Premier mouvement de deux cases
                    return True
            else:  # Pion noir
                if end_row - start_row == 1:  # Avancer d'une case
                    return end_piece == ' '
                elif start_row == 1 and end_row - start_row == 2 and end_piece == ' ' and self.board[start_row + 1][
                    start_col] == ' ':  # Premier mouvement de deux cases
                    return True

        elif piece_type == 'r':  # Tour
            if start_row == end_row:  # Déplacement horizontal
                step = 1 if end_col > start_col else -1
                for col in range(start_col + step, end_col, step):
                    if self.board[start_row][col] != ' ':
                        return False
                return True
            elif start_col == end_col:  # Déplacement vertical
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if self.board[row][start_col] != ' ':
                        return False
                return True

        elif piece_type == 'n':  # Cavalier
            if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1 or \
                    abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
                return True

        elif piece_type == 'b':  # Fou
            if abs(start_row - end_row) == abs(start_col - end_col):
                step_row = 1 if end_row > start_row else -1
                step_col = 1 if end_col > start_col else -1
                row, col = start_row + step_row, start_col + step_col
                while row != end_row and col != end_col:
                    if self.board[row][col] != ' ':
                        return False
                    row += step_row
                    col += step_col
                return True

        elif piece_type == 'k':  # Roi
            if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
                return True


        elif piece_type == 'q':  # Reine
            if start_row == end_row or start_col == end_col:  # Mouvement en ligne droite (comme une tour)
                if self.is_valid_move_as_rook(start_row, start_col, end_row, end_col):
                    return True
            elif abs(start_row - end_row) == abs(start_col - end_col):  # Mouvement en diagonale (comme un fou)
                if self.is_valid_move_as_bishop(start_row, start_col, end_row, end_col):
                    return True

    def is_valid_move_as_rook(self, start_row, start_col, end_row, end_col):
        if start_row == end_row:  # Déplacement horizontal
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if self.board[start_row][col] != ' ':
                    return False
            return True
        elif start_col == end_col:  # Déplacement vertical
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if self.board[row][start_col] != ' ':
                    return False
            return True
        return False

    def is_valid_move_as_bishop(self, start_row, start_col, end_row, end_col):
        if abs(start_row - end_row) == abs(start_col - end_col):
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
            row, col = start_row + step_row, start_col + step_col
            while row != end_row and col != end_col:
                if self.board[row][col] != ' ':
                    return False
                row += step_row
                col += step_col
            return True
        return False

    def draw_piece(self, surface, row, col):
        piece = self.board[row][col]
        if piece != ' ':
            surface.blit(self.images[piece], (col * self.largeur_case, row * self.hauteur_case))

    def get_possible_moves(self, row, col):
        piece = self.board[row][col]
        possible_moves = []

        if piece.lower() == 'p':  # Vérifie si la pièce est un pion (p ou P)
            direction = -1 if piece.isupper() else 1  # Détermine la direction du mouvement du pion : -1 pour les pièces blanches, 1 pour les pièces noires

            # Déplacement d'un pas en avant (si la case devant est vide)
            if 0 <= row + direction < 8 and self.board[row + direction][col] == ' ':
                possible_moves.append((row + direction,
                                       col))  # Ajoute le mouvement en avant d'une case à la liste des mouvements possibles

            # Déplacement de deux cases en avant (si le pion est encore à sa position de départ et la case de deux cases en avant est vide)
            if (piece.isupper() and row == 6) or (
                    piece.islower() and row == 1):  # Vérifie si le pion est à sa position de départ
                if 0 <= row + 2 * direction < 8 and self.board[row + 2 * direction][col] == ' ':
                    possible_moves.append((row + 2 * direction,
                                           col))  # Ajoute le déplacement de deux cases en avant à la liste des mouvements possibles

            # Déplacement en diagonale à gauche pour capturer (si une pièce ennemie est présente)
            if col > 0 and 0 <= row + direction < 8 and self.board[row + direction][col - 1] != ' ' and \
                    self.board[row + direction][col - 1].isupper() != piece.isupper():
                possible_moves.append((row + direction,
                                       col - 1))  # Ajoute le déplacement en diagonale à gauche à la liste des mouvements possibles

            # Déplacement en diagonale à droite pour capturer (si une pièce ennemie est présente)
            if col < 7 and 0 <= row + direction < 8 and self.board[row + direction][col + 1] != ' ' and \
                    self.board[row + direction][col + 1].isupper() != piece.isupper():
                possible_moves.append((row + direction,
                                       col + 1))  # Ajoute le déplacement en diagonale à droite à la liste des mouvements possibles

        elif piece.lower() == 'r':  # Tour
            for r in range(row + 1, 8):
                if self.is_valid_move(row, col, r, col):
                    possible_moves.append((r, col))
                    if self.board[r][col] != ' ':
                        break
                else:
                    break
            for r in range(row - 1, -1, -1):
                if self.is_valid_move(row, col, r, col):
                    possible_moves.append((r, col))
                    if self.board[r][col] != ' ':
                        break
                else:
                    break
            for c in range(col + 1, 8):
                if self.is_valid_move(row, col, row, c):
                    possible_moves.append((row, c))
                    if self.board[row][c] != ' ':
                        break
                else:
                    break
            for c in range(col - 1, -1, -1):
                if self.is_valid_move(row, col, row, c):
                    possible_moves.append((row, c))
                    if self.board[row][c] != ' ':
                        break
                else:
                    break

        elif piece.lower() == 'n':  # Cavalier
            moves = [(row + 2, col + 1), (row + 2, col - 1), (row - 2, col + 1), (row - 2, col - 1),
                     (row + 1, col + 2), (row + 1, col - 2), (row - 1, col + 2), (row - 1, col - 2)]
            for move in moves:
                r, c = move
                if 0 <= r < 8 and 0 <= c < 8 and self.is_valid_move(row, col, r, c):
                    possible_moves.append((r, c))

        elif piece.lower() == 'b':  # Fou
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row, col
                while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                    r += dr
                    c += dc
                    if self.is_valid_move(row, col, r, c):
                        possible_moves.append((r, c))
                        if self.board[r][c] != ' ':
                            break
                    else:
                        break

        elif piece.lower() == 'q':  # Reine
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.is_valid_move(row, col, r, c):
                        possible_moves.append((r, c))
                        if self.board[r][c] != ' ':  # Arrêter si une pièce est rencontrée
                            break
                    else:
                        break
                    r, c = r + dr, c + dc


        elif piece.lower() == 'k':  # Roi
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if self.is_valid_move(row, col, r, c):
                        possible_moves.append((r, c))

        return possible_moves

    class Piece:
        def __init__(self, symbol, image, row, col):
            self.symbol = symbol
            self.image = image
            self.row = row
            self.col = col
