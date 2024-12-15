import pytest
from pygame import Surface

from snake.main import Dir, Tile, Serpent, Point, Apple, Board

def test_dir_enum():
    assert Dir.UP.value == [0, -1]
    assert Dir.DOWN.value == [0, 1]
    assert Dir.LEFT.value == [-1, 0]
    assert Dir.RIGHT.value == [1, 0]

def test_tile_addition():
    tile = Tile((255, 255, 255), 5, 5)
    new_tile = tile + Dir.UP
    assert new_tile.x == 5
    assert new_tile.y == 4

    new_tile = tile + Dir.RIGHT
    assert new_tile.x == 6
    assert new_tile.y == 5

    with pytest.raises(TypeError):
        tile + "invalid"

def test_serpent_initialization():
    serpent = Serpent(Dir.RIGHT, (0, 255, 0), [[5, 5], [5, 4], [5, 3]], 20, 20)
    assert len(serpent.position) == 3
    assert serpent.position[0].x == 5
    assert serpent.position[0].y == 5

def test_serpent_movement():
    serpent = Serpent(Dir.RIGHT, (0, 255, 0), [[5, 5], [5, 4], [5, 3]], 20, 20)
    serpent.avancer()
    assert serpent.position[0].x == 6
    assert serpent.position[0].y == 5

def test_serpent_collision_with_apple():
    serpent = Serpent(Dir.RIGHT, (0, 255, 0), [[5, 5], [5, 4], [5, 3]], 20, 20)
    apple = Apple((255, 0, 0), serpent.position, 20, 20)
    apple.position = Tile((255, 0, 0), 6, 5)  
    serpent.avancer() 
    assert serpent.eaten is True  

def test_apple_new_position():
    serpent = Serpent(Dir.RIGHT, (0, 255, 0), [[5, 5], [5, 4], [5, 3]], 20, 20)
    apple = Apple((255, 0, 0), serpent.position, 20, 20)
    old_position = apple.position
    apple.new(serpent.position, 20, 20)
    assert apple.position != old_position  

def test_point_system():
    point = Point()
    assert point.pt == 0
    point.win()
    assert point.pt == 1

def test_board_creation():
    screen = Surface((400, 400))
    board = Board(screen, 20)
    assert board._size == 20
    assert len(board._objects) == 0
