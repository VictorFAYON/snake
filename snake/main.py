import abc  # Module pour les classes abstraites
import argparse  # Pour traiter les arguments de ligne de commande
import enum  # Pour créer des énumérations
import random as rd  # Pour les opérations aléatoires
import re #Pour les regular expression
from typing import List, Tuple, Iterator,  Any  # Types utilisés pour annoter le code

import pygame  # Bibliothèque pour créer des jeux en 2D
class SnakeException(Exception):
    def __init__(self,message : str) -> None:
        super().__init__(message)

class Gameover(SnakeException):
    def __init__(self,message : str) -> None:
        super().__init__(message)

class SnakeError(SnakeException):
    def __init__(self,message : str) -> None:
        super().__init__(message)

class IntRangeError(SnakeError):
    def __init__(self,name:str,value:int,Vmin:int,Vmax:int) -> None:
        super().__init__(f"Value {value} of {name} is out of allowed range[{Vmin}-{Vmax}]")   

class ColorError(SnakeError):
    def __init__(self,color:str,name:str) -> None:
        super().__init__(f"Wrong {name} : {color}]")

class Observer(abc.ABC):
    def __init__(self,l,w) -> None:
        super().__init__()
        self._objects: list[GameObject]=[]
        self.l=l
        self.w=w
        self.stay=True
    def notify_object_moved(self, obj: "GameObject") -> "GameObject":
        for o in self._objects:
            if isinstance(o, Subject):
                pos=[]
                for ti in o.tiles:
                    pos.append(ti)
                if o == obj:
                    if pos[0].x > self.w or pos[0].x < 0 or pos[0].y > self.l or pos[0].y < 0 or [pos[0].x,pos[0].y] in [[ti.x,ti.y] for ti in pos[1:]]:
                        self.notify_limite()
                else:
                    if obj in o:
                        self.notify_collision(obj,o)

        return obj

    def notify_object_eaten(self, obj: "Serpent") -> None:
        if isinstance(self,Apple):
            self.new(obj.position, self.w,self.l)
        if isinstance(self,Serpent):
            self.eaten=True
        if isinstance(self,Point):
            self.win()


    def notify_collision(self, obj: "GameObject",o: "GameObject") -> None:
        if isinstance(obj, Serpent) and isinstance(o, Apple):
            if isinstance(self,Subject):
                for obs in self._observers:
                    obs.notify_object_eaten(obj)
    def notify_limite(self):
        raise Gameover
class Subject(abc.ABC):

    def __init__(self) -> None:
        super().__init__()
        self._observers: list[Observer] = []

    @property
    def observers(self) -> list[Observer]:
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        print(f"Attach {obs} as observer of {self}.")
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        print(f"Detach observer {obs} from {self}.")
        self._observers.remove(obs)

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
class Board(Observer, Subject):
    def __init__(self, screen: pygame.Surface, size: int,l,w) -> None:
        super().__init__(l,w)
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

    def __contains__(self, obj: object) -> bool:
        if isinstance(obj, GameObject):
            for ti in self.tiles:
                for autre in obj.tiles:
                    if [ti.x,ti.y]==[autre.x,autre.y]:
                        return True
            return False
        raise TypeError("Can contain GameObject")

    @property
    @abc.abstractmethod
    def tiles(self) -> (Iterator[Any]):
        # Doit être implémentée par les classes dérivées pour fournir les cases occupées
        raise NotImplementedError

# Classe pour représenter une case du jeu


# Classe représentant le serpent
class Serpent(Observer, Subject, GameObject):
    def __init__(
        self,
        dir: Dir,
        color: Tuple[int, int, int],
        position: List[List[int]],
        l: int,
        w: int,
    ) -> None:
        super().__init__(l,w)
        self.colorserpent: Tuple[int, int, int] = color  # Couleur du serpent
        self.position: List[Tile] = [
            Tile(self.colorserpent, vertebre[0], vertebre[1]) for vertebre in position
        ]  # Liste des cases constituant le serpent
        self._direction: Dir = dir  # Direction initiale
        self.l: int = l  # Longueur du plateau
        self.w: int = w  # Largeur du plateau
        self.stay: bool = True  # Indique si le jeu continue
        self.eaten: bool = False

    @property
    def dir(self) -> Dir:
        return self._direction  # Renvoit la direction actuelle

    @dir.setter
    def dir(self, new_direction: Dir) -> None:
        self._direction = new_direction  # Met à jour la direction

    def avancer(self) -> None:
        # Fait grandir le serpent
        self.position.append(self.position[-1])
        for i in range(1,len(self.position)):
            self.position[len(self.position) - i] = self.position[len(self.position) - 1 - i] #fait avancer le corps
        self.position[0] = self.position[0] + self._direction # Avance la tête
        for obs in self.observers:
            obs.notify_object_moved(self)
        if not self.eaten: #fait rétrécir le sermment si non mangé
            self.position.pop()
        self.eaten=False

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
        for ligne in range(self.w):
            for colonne in range(self.l):
                if (colonne + ligne) % 2 == 0:
                    yield Tile(self._color1, ligne, colonne)
                else:
                    yield Tile(self._color2, ligne, colonne)

# Classe pour représenter une pomme
class Apple(Observer, Subject, GameObject):
    def __init__(
        self, color: Tuple[int, int, int], serp: List[Tile], w: int, l: int
    ) -> None:
        super().__init__(l,w)
        self.color: Tuple[int, int, int] = color  # Couleur de la pomme
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
class Point(Observer):
    def __init__(self,l,w) -> None:
        super().__init__(l,w)
        self.pt: int = 0  # Score initial

    def win(self) -> None:
        # Incrémente le score
        self.pt += 1

# Classe principale pour le jeu Snake
class Snake:
    def boardsize(self) -> argparse.Namespace:
        # Configure la taille du plateau via des arguments
        MIN_WIDTH, MIN_LENTH, FPS_MIN, FPS_MAX= 200, 200, 1, 10
        DEFAULT_WIDTH,DEFAULT_LENTH,DEFAULT_FPS=300,300,3

        parser = argparse.ArgumentParser(description="Set the resolution")
        parser.add_argument("-w", type=int, default=DEFAULT_WIDTH, help="width")
        parser.add_argument("-l", type=int, default=DEFAULT_LENTH, help="length")
        parser.add_argument("-fps", type=int, default=DEFAULT_FPS, help="frame per second")
        parser.add_argument('-fruit_color', type=str,default='#', help="Fruit's color")
        args = parser.parse_args()

        if not re.match(r'#[0-9A-Fa-f]{6}$', args.fruit_color):
            raise ColorError(args.fruit_color,"fruit color")

        if args.w < MIN_WIDTH:
            raise ValueError(f"The size (-w argument) must be \u2265 {MIN_WIDTH}.")
        if args.l < MIN_LENTH:
            raise ValueError(f"The size (-l argument) must be \u2265 {MIN_LENTH}.")
        if args.fps < FPS_MIN or args.fps > FPS_MAX:
            raise IntRangeError("FPS", args.fps,FPS_MIN, FPS_MAX)

        args.w = (args.w // 20) * 20  # Ajuste à un multiple de 20
        args.l = (args.l // 20) * 20
        return args

    def endgame(self) -> None:
        # Termine le jeu
        self.stay = False

    def game(self) -> None:
        pygame.init()
        try:
            # Logique principale du jeu
            args = self.boardsize()
            lenth, width = args.l // 20, args.w // 20
            screen = pygame.display.set_mode((args.w, args.l))
            clock = pygame.time.Clock()
            score = Point(lenth,width)
            pygame.display.set_caption(f"SNAKE Score: {score.pt}")

            board = Board(screen, 20,lenth,width)  # Crée le plateau
            black, white = (0, 0, 0), (255, 255, 255)
            check = CheckerBoard(width, lenth, black, white)
            board.newobject(check)  # Ajoute le damier au plateau
            board.attach_obs(score)

            dir = Dir.RIGHT
            colorserpent = (9, 82, 40)
            initialsserpent = [[10, 7], [10, 6], [10, 5]]
            serp = Serpent(dir, colorserpent, initialsserpent, lenth, width)
            board.newobject(serp)  # Ajoute le serpent au plateau
            serp.attach_obs(board)
            board.attach_obs(serp)

            colorapple = (228, 124, 110)
            pom = Apple(colorapple, serp.position, width, lenth)
            board.newobject(pom)  # Ajoute une pomme au plateau
            pom.attach_obs(board)
            board.attach_obs(pom)

            while board.stay:
                board.draw()  # Dessine le plateau
                clock.tick(args.fps)  # Gère la vitesse du jeu
                pygame.display.set_caption(f"SNAKE Score: {score.pt}")
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        board.stay=False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            board.stay=False
                        elif event.key == pygame.K_UP:
                            dir = Dir.UP
                        elif event.key == pygame.K_DOWN:
                            dir = Dir.DOWN
                        elif event.key == pygame.K_LEFT:
                            dir = Dir.LEFT
                        elif event.key == pygame.K_RIGHT:
                            dir = Dir.RIGHT

                serp.dir=dir
                serp.avancer()
        except Gameover:
                print("You loose.")
        pygame.quit()  # Quitte le jeu

# Fonction principale pour démarrer le jeu

def snakegame() -> None:
    Snake().game()
