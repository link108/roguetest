
import Queue as queue
import sys
from lib.utility_functions.util import Util


class AiUtils:


    @staticmethod
    def dijkstra_on_map(state, x, y):
        unvisited_tiles = queue.PriorityQueue()
        # unvisited_tiles = []
        all_tiles = [[sys.maxint for col in range(len(state.game_map.game_map[0]))] for row in range(len(state.game_map.game_map))]
        for row in state.game_map.game_map:
            for tile in row:
                if tile.x == x and tile.y == y:
                    all_tiles[x][y] = 0
                    unvisited_tiles.put((0, (tile.x, tile.y)))
                else:
                    unvisited_tiles.put((sys.maxint, (tile.x, tile.y)))
        while not unvisited_tiles.empty():
            closest_dist, closest_tile = unvisited_tiles.get()
            closest_neighbors = Util.get_adjacent_tiles(state, closest_tile[0], closest_tile[1])
            for neighbor in closest_neighbors:
                temp_dist = closest_dist + 1
                if temp_dist < all_tiles[neighbor.x][neighbor.y]:
                    all_tiles[neighbor.x][neighbor.y] = temp_dist
                    unvisited_tiles.put((temp_dist, (neighbor.x, neighbor.y)))
                    neighbor.dist_from_player = temp_dist
        print 'hii'


        # player_coords = state.player.x, state.player.y



