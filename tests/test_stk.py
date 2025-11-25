import pygame
import pytest

from stk import Label

@pytest.fixture
def game() -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((1,1))
    return screen

@pytest.fixture
def labels(game:pygame.Surface) -> Label:
    label = Label(game,'',1,1,1,1)
    return label

def test_Label(labels:Label) -> None:
    assert labels is not None
    assert isinstance(labels,Label)
    assert isinstance(labels.rect,pygame.Rect)

def test_Label_goto(labels:Label) -> None:
    assert labels.x == 1
    assert labels.y == 1
    labels.goto((0,0))
    assert labels.x == 0
    assert labels.y == 0
    labels.goto((1,1))