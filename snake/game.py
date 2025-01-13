# ruff: noqa: D100,S311

# Third party
import pygame
import importlib.resources
import time

# First party
from .board import Board
from .checkerboard import Checkerboard
from .dir import Dir
from .exceptions import GameOver
from .fruit import Fruit
from .snake import Snake
from .state import State
from .score import Score
from .scores import Scores


# Constants
SK_START_LENGTH = 3

with importlib.resources.path("mymodule", "myresources/my_resource_file.yml") as myfile:
        with myfile.open("r") as f:
            pass

class Game:
    """The main class of the game."""

    def __init__(self, width: int, height: int, tile_size: int, # noqa: PLR0913
                 fps: int,
                 *,
                 fruit_color: pygame.Color,
                 snake_head_color: pygame.Color,
                 snake_body_color: pygame.Color,
                 gameover_on_exit: bool,
                 ) -> None:
        """Object initialization."""
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._fps = fps
        self._fruit_color = fruit_color
        self._snake_head_color = snake_head_color
        self._snake_body_color = snake_body_color
        self._gameover_on_exit = gameover_on_exit
        self._state=State.SCORES
        self._snake=None


    def _init(self) -> None:
        """Initialize the game."""
        # Create a display screen
        screen_size = (self._width * self._tile_size,
                       self._height * self._tile_size)
        self._screen = pygame.display.set_mode(screen_size)

        # Create the clock
        self._clock = pygame.time.Clock()

        #create scores
        self._score = Scores

        # Create the main board
        self._board = Board(screen = self._screen,
                            nb_lines = self._height,
                            nb_cols = self._width,
                            tile_size = self._tile_size)

        # Create checkerboard
        self._checkerboard = Checkerboard(nb_lines = self._height,
                                          nb_cols = self._width)
        self._board.add_object(self._checkerboard)

        # Create snake
        self._reset_snake()

        self._board.add_object(self._snake)
        self._board.attach_obs(self._snake)

        # Create fruit
        Fruit.color = self._fruit_color
        self._board.create_fruit()
        # Uploading the fonts
        with importlib.resources.path("snake", "DejaVuSansMono-Bold.ttf") as myfile:
            self._font_GAMEOVER=pygame.font.font(myfile,64)
            self._font_SCORES=pygame.font.font(myfile,32)

    def _reset_snake(self):
        if self._snake is not None:
            self._board.remove_object(self._snake)
        self._snake = Snake.create_random(
                nb_lines = self._height,
                nb_cols = self._width,
                length = SK_START_LENGTH,
                head_color = self._snake_head_color,
                body_color = self._snake_body_color,
                gameover_on_exit = self._gameover_on_exit,
                )

    def _process_events(self) -> None:
        """Process pygame events."""
        # Loop on all events
        for event in pygame.event.get():
            match self._state:
                case State.SCORES:
                    match event.key:
                        case pygame.K_SPACE:
                            self._state=State.PLAY
                case State.PLAY:
                    if event.type == pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_q:
                                self.state = State.QUIT
                            case pygame.K_UP:
                                self._snake.dir = Dir.UP
                            case pygame.K_DOWN:
                                self._snake.dir = Dir.DOWN
                            case pygame.K_LEFT:
                                self._snake.dir = Dir.LEFT
                            case pygame.K_RIGHT:
                                self._snake.dir = Dir.RIGHT
            # Closing window (Mouse click on cross icon or OS keyboard shortcut)
            if event.type == pygame.QUIT:
                self._run = False

    def _drawgameover(self) -> None:
        text_surface = self._font_GAMEOVER.render("GAMEOVER",True , pygame.Color("red"))
        x, y = 80, 160 # Define the position where to write text.
        self._screen.blit(text_surface, (x, y))
    
    def process_score(self):
        pass

    def _draw_scores(self):
        x, y = 80, 10 # Define the position where to write text.
        for score in self._scores:
            text_scores= self._font_GAMEOVER.render(f"{score.name}" +f"{score.score:.>8}",True , pygame.Color("red"))
            self._screen.blit(text_surface, (x, y))
            y+=32

    def _displayscores(self) -> None:
        text_surface = self._font_SCORES.render("GAMEOVER",True , pygame.Color("red"))
        x, y = 80, 160 # Define the position where to write text.
        self._screen.blit(text_surface, (x, y))

    def start(self) -> None:
        """Start the game."""
        # Initialize pygame
        pygame.init()
        # Initialize game
        self._init()

        while self._state!=State.QUIT:
            # Wait 1/FPS second
            self._clock.tick(self._fps)

            # Listen for events
            self._process_events()
            # Draw
            self._board.draw()
            try:
                # Wait 1/FPS second
                self._clock.tick(self._fps)

                # Listen for events
                self._process_events()
                # Draw
                self._board.draw()

                # Display
                pygame.display.update()

                self._snake.move()

            except GameOver:  # noqa: PERF203
                self._state=State.GAMEOVER
                countdown=self._fps

            # Draw
            self._board.draw()
            match self._state:
                case State.GAMEOVER:
                    self._drawgameover()
                    countdown-=1
                    if countdown==0:
                        score=self._snake.score
                        if self._scores.is_high_score(score):
                            self._state=State.INPUT_NAME #aller chercher event.unicode pour écrire le nom
                        else:
                            self._state=State.SCORES
                            self._reset_snake()
                case State.SCORES:
                    self._displayscores()
            # Terminate pygame
        pygame.quit()

