import os
import sys
sys.path.append(os.path.normpath(os.path.join
                (os.path.dirname(os.path.abspath(__file__)), '..')))

from src.game import Game

WIDTH = 800
HEIGHT = 650
FPS = 30

play = Game(WIDTH, HEIGHT, FPS)

# Test that end_turn actually increases the number of turns done
turn = play.turn
play.end_turn_button.action(play)
assert turn + 1 == play.turn

# Test that reset_map refreshes game stats
play.reset_map_button.action(play)
assert play.turn == 0

for country in play.game_state.countries:
    units = play.game_state.countries[country].get_units()
    capital = play.game_state.countries[country].get_capital()
    capital_is_neighbour = True
    try_attack = dict()
    for unit in units:
        try_attack[unit] = []
        cell = unit.get_cell()
        # in case unit spawned on the capital
        cin = (cell[0], cell[1]) == capital
        neighbours = play.game_state.gamemap.neighbours(cell[0], cell[1])
        for cell in neighbours:
            if (cell.X(), cell.Y()) == capital:
                cin = True
            if cell.vis_cell.get_unit() is not None:
                try_attack[unit].append(cell.vis_cell.get_unit())
        capital_is_neighbour = capital_is_neighbour and cin
    # Test that all units are around capital
    assert capital_is_neighbour
    for unit in try_attack:
        for enemy in try_attack[unit]:
            if unit.country != enemy.get_unit().country:
                # Test that attack on enemies work
                pass
            else:
                # Test that attack on allies doesn't work
                pass
        # Test that attack on townhall doesn't work
        pass

# Tests finished, finalize the game
play.quit()
