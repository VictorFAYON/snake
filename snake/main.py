import abc  # Module pour les classes abstraites
import argparse  # Pour traiter les arguments de ligne de commande
import enum  # Pour créer des énumérations
import random as rd  # Pour les opérations aléatoires
from typing import List, Tuple, Iterator, Optional, Any  # Types utilisés pour annoter le code

import pygame  # Bibliothèque pour créer des jeux en 2D

# Enumération pour les directions du serpent
class Dir(enum.Enum):  # Définit les directions possibles
    UP = [0, -1]  # Haut
    DOWN = [0, 1]  # Bas
    LEFT = [-1, 0]  # Gauche
    RIGHT = [1, 0]  # Droite
class Tile:
    def __init__(self, color: Tuple[int, int, int], x: int, y: int) -> None:
        self._color: Tuple[int, int, int] = color  # Couleur de la case
        self.x: int = x  # Position x
        self.y: int = y  # Position y

    def __add__(self, other: Any) -> "Tile":
        # Permet d'ajouter une direction à une case
        if not isinstance(other, Dir):
            raise TypeError("Can only add Dir to Tile")
        return Tile(self._color, self.x + other.value[0], self.y + other.value[1])

    def draw(self, screen: pygame.Surface, size: int) -> None:
        # Dessine la case sur l'écran
        pygame.draw.rect(
            screen,
            self._color,
            pygame.Rect(self.x * size, self.y * size, size, size),
        )
# Classe représentant le plateau du jeu
class Board:
    def __init__(self, screen: pygame.Surface, size: int) -> None:
        self._screen: pygame.Surface = screen  # Surface de dessin
        self._size: int = size  # Taille des cases
        self._objects: List[GameObject] = []  # Liste des objets sur le plateau

    def draw(self) -> None:
        # Dessine tous les objets sur le plateau
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._size)

    def newobject(self, gameobject: "GameObject") -> None:
        # Ajoute un nouvel objet au plateau
        self._objects.append(gameobject)

# Classe abstraite pour représenter les objets du jeu
class GameObject(abc.ABC):
    def __init__(self) -> None:
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self) -> (Iterator[Any]):
        # Doit être implémentée par les classes dérivées pour fournir les cases occupées
        raise NotImplementedError

# Classe pour représenter une case du jeu


# Classe représentant le serpent
class Serpent(GameObject):
    def __init__(
        self,
        dir: Dir,
        color: Tuple[int, int, int],
        position: List[List[int]],
        l: int,
        w: int,
    ) -> None:
        self.colorserpent: Tuple[int, int, int] = color  # Couleur du serpent
        super().__init__()
        self.position: List[Tile] = [
            Tile(self.colorserpent, vertebre[0], vertebre[1]) for vertebre in position
        ]  # Liste des cases constituant le serpent
        self._direction: Dir = dir  # Direction initiale
        self.l: int = l  # Longueur du plateau
        self.w: int = w  # Largeur du plateau
        self.stay: bool = True  # Indique si le jeu continue

    def eat(self) -> None:
        # Le serpent mange une pomme et s'allonge
        self.position.append(self.position[-1])  # Ajoute une case à la fin
        for i in range(1, len(self.position)):
            self.position[len(self.position) - i] = self.position[len(self.position) - 1 - i]
        self.position[0] = self.position[0] + self._direction  # Allonge la tête

    def limite(self) -> bool:
        # Vérifie si le serpent touche les limites ou lui-même
        nexttile: Tile = self.position[0] + self._direction
        return bool(nexttile.x > self.l or nexttile.x < 0 or nexttile.y > self.w or nexttile.y < 0 or [nexttile.x,nexttile.y] in [[ti.x,ti.y] for ti in self.position[:-1]])

    @property
    def dir(self) -> Dir:
        return self._direction  # Renvoit la direction actuelle

    @dir.setter
    def dir(self, new_direction: Dir) -> None:
        self._direction = new_direction  # Met à jour la direction

    def avancer(self, apple: "Apple", score: "Point") -> None:
        # Fait avancer le serpent et gère les interactions
        if self.limite():
            self.stay = False  # Arrête le jeu si collision

        if (self.position[0] + self._direction).x == apple.position.x and (self.position[0] + self._direction).y == apple.position.y:
            self.eat()  # Mange une pomme
            score.win()  # Augmente le score
            apple.new(self.position, self.w, self.l)  # Génère une nouvelle pomme
        else:
            for i in range(1, len(self.position)):
                self.position[len(self.position) - i] = self.position[len(self.position) - 1 - i]
            self.position[0] = self.position[0] + self._direction  # Avance la tête

    @property
    def tiles(self) -> Iterator[Tile]:
        return iter(self.position)  # Renvoit les cases occupées par le serpent

# Classe pour représenter un damier
class CheckerBoard(GameObject):
    def __init__(
        self, w: int, l: int, color1: Tuple[int, int, int], color2: Tuple[int, int, int]
    ) -> None:
        super().__init__()
        self._color1: Tuple[int, int, int] = color1  # Première couleur
        self._color2: Tuple[int, int, int] = color2  # Deuxième couleur
        self.w: int = w  # Largeur du plateau
        self.l: int = l  # Longueur du plateau

    @property
    def tiles(self) -> Iterator[Tile]:
        # Génère les cases alternées pour le damier
        for ligne in range(self.l):
            for colonne in range(self.w):
                if (colonne + ligne) % 2 == 0:
                    yield Tile(self._color1, ligne, colonne)
                else:
                    yield Tile(self._color2, ligne, colonne)

# Classe pour représenter une pomme
class Apple(GameObject):
    def __init__(
        self, color: Tuple[int, int, int], serp: List[Tile], w: int, l: int
    ) -> None:
        self.color: Tuple[int, int, int] = color  # Couleur de la pomme
        super().__init__()
        self.position: Tile = self.new(serp, w, l)  # Position initiale

    def new(self, position: List[Tile], w: int, l: int) -> Tile:
        # Génère une nouvelle position pour la pomme
        x, y = rd.randint(1, w - 1), rd.randint(1, l - 1)
        while [x, y] in [[tile.x, tile.y] for tile in position]:
            x, y = rd.randint(1, w - 1), rd.randint(1, l - 1)
        self.position = Tile(self.color, x, y)
        return self.position

    @property
    def tiles(self) -> Iterator:
        yield self.position  # Renvoit la case de la pomme

# Classe pour gérer le score
class Point:
    def __init__(self) -> None:
        self.pt: int = 0  # Score initial

    def win(self) -> None:
        # Incrémente le score
        self.pt += 1

# Classe principale pour le jeu Snake
class Snake:
    def boardsize(self) -> argparse.Namespace:
        # Configure la taille du plateau via des arguments
        MIN_WIDTH, MIN_LENTH = 300, 300

        parser = argparse.ArgumentParser(description="Set the resolution")
        parser.add_argument("-w", type=int, default=300, help="width")
        parser.add_argument("-l", type=int, default=300, help="length")
        args = parser.parse_args()

        if args.w < MIN_WIDTH:
            raise ValueError(f"The size (-w argument) must be \u2265 {MIN_WIDTH}.")
        if args.l < MIN_LENTH:
            raise ValueError(f"The size (-l argument) must be \u2265 {MIN_LENTH}.")

        args.w = (args.w // 20) * 20  # Ajuste à un multiple de 20
        args.l = (args.l // 20) * 20
        return args

    def endgame(self) -> None:
        # Termine le jeu
        self.stay = False

    def game(self) -> None:
        # Logique principale du jeu
        args = self.boardsize()
        lenth, width = args.l // 20, args.w // 20
        screen = pygame.display.set_mode((args.w, args.l))
        clock = pygame.time.Clock()
        score = Point()
        pygame.display.set_caption(f"SNAKE Score: {score.pt}")

        board = Board(screen, 20)  # Crée le plateau
        black, white = (0, 0, 0), (255, 255, 255)
        check = CheckerBoard(width, lenth, black, white)
        board.newobject(check)  # Ajoute le damier au plateau

        dir = Dir.RIGHT
        colorserpent = (9, 82, 40)
        initialsserpent = [[10, 7], [10, 6], [10, 5]]
        serp = Serpent(dir, colorserpent, initialsserpent, lenth, width)
        board.newobject(serp)  # Ajoute le serpent au plateau

        colorapple = (228, 124, 110)
        pom = Apple(colorapple, serp.position, width, lenth)
        board.newobject(pom)  # Ajoute une pomme au plateau

        while serp.stay:
            board.draw()  # Dessine le plateau
            clock.tick(2)  # Gère la vitesse du jeu
            pygame.display.set_caption(f"SNAKE Score: {score.pt}")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.endgame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.endgame()
                    elif event.key == pygame.K_UP:
                        dir = Dir.UP
                    elif event.key == pygame.K_DOWN:
                        dir = Dir.DOWN
                    elif event.key == pygame.K_LEFT:
                        dir = Dir.LEFT
                    elif event.key == pygame.K_RIGHT:
                        dir = Dir.RIGHT

            serp.dir = dir
            serp.avancer(pom, score)

        pygame.quit()  # Quitte le jeu

# Fonction principale pour démarrer le jeu

def snakegame() -> None:
    Snake().game()
