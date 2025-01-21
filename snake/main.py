# ruff: noqa: D100,S311

# Standard
import sys
import logging

# First party
from .cmd_line import read_args
from .exceptions import SnakeError
from .game import Game
from .logger_setting import logger_settings

def main() -> None: # noqa: D103

    try:
        # Read command line arguments
        args = read_args()
        logger_level=args.logger_set_level
        logger_settings()
        if logger_level=="info":
            logger.setLevel(logging.INFO)
        if logger_level=="debug":
            logger.setLevel(logging.DEBUG)
        if logger_level=="warning":
            logger.setLevel(logging.WARNING)

        # Start game
        Game(width = args.width, height = args.height,
             tile_size = args.tile_size, fps = args.fps,
             fruit_color = args.fruit_color,
             snake_head_color = args.snake_head_color,
             snake_body_color = args.snake_body_color,
             gameover_on_exit = args.gameover_on_exit,
             scores_file=args.scores_file,).start()

    except SnakeError as e:
        print(f"Error: {e}") # noqa: T201
        sys.exit(1)
