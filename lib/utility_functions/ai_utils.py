
import Queue as queue
import sys
from lib.utility_functions.util import Util


class AiUtils:


    @staticmethod
    def dijkstra_on_map(state, source_x, source_y):
        unvisited_tiles = queue.PriorityQueue()
        if state.dijkstra_map_update:
            state.dijkstra_map = [[sys.maxint for col in range(len(state.game_map.game_map[0]))] for row in range(len(state.game_map.game_map))]
            state.dijkstra_map_update = False
        for row in state.game_map.game_map:
            for tile in row:
                if tile.x == source_x and tile.y == source_y:
                    state.dijkstra_map[source_x][source_y] = 0
                    unvisited_tiles.put((0, (tile.x, tile.y)))
                elif tile.blocked:
                    continue
                else:
                    unvisited_tiles.put((sys.maxint, (tile.x, tile.y)))
        while not unvisited_tiles.empty():
            closest_dist, closest_tile = unvisited_tiles.get()
            closest_neighbors = Util.get_adjacent_tiles(state, closest_tile[0], closest_tile[1])
            for neighbor in closest_neighbors:
                if not neighbor.blocked:
                    temp_dist = closest_dist + 1
                    if temp_dist < state.dijkstra_map[neighbor.x][neighbor.y]:
                        state.dijkstra_map[neighbor.x][neighbor.y] = temp_dist
                        unvisited_tiles.put((temp_dist, (neighbor.x, neighbor.y)))
                        neighbor.dist_from_player = temp_dist


        # player_coords = state.player.x, state.player.y



