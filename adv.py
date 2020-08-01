from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []



# TRAVERSAL TEST - DO NOT MODIFY
print("STARTING")
# initiate graph to dict and visited to set 
my_room_graph = {}
visited_rooms = set()
# path to go back to the last unexplored room
return_sequence = []
# bool for when we've finished and dict of directions to get opposites 
visitedBool = False
opposite_directions = {
    "n": "s",
    "s": "n",
    "w": "e",
    "e": "w"
} # (for return sequence back tracking)
# function to add initial room and unexplored neighbors later on
def add_unexplored_room_neighbors(room_id, exit_options, prev_r=None, prev_r_direction=None):
    # initate this index to dict
    my_room_graph[room_id] = {}
    # loop over exits
    for exit_option in exit_options:
        # this option matches the direction we just moved ## not going to run for initiation
        if exit_option == prev_r_direction:
            # append the previous room at this index
            my_room_graph[room_id][exit_option] = prev_r
        else:
            # otherwise, put a ? here
            my_room_graph[room_id][exit_option] = "?" # {0: {'n': '?'}}


# add first room to graph
add_unexplored_room_neighbors(player.current_room.id, player.current_room.get_exits())
print(my_room_graph) # {0: {'n': '?'}}
# while we're not done
while not visitedBool:
    # get exits and current room id
    current_exits = player.current_room.get_exits()
    room_id = player.current_room.id
    # print something pretty
    print("-"*10)
    print(f"Current room: {room_id} - Current exits: {current_exits}")
    print(f"Current return moves: {return_sequence}")
    # print(my_room_graph)

    # the moves I can to go
    my_moves = []
    # loop over exits
    for exit_option in current_exits:
        # if my graph doesn't have this room, let's explore it
        if my_room_graph[room_id][exit_option] == "?":
            my_moves.append(exit_option)
    # if we reach a dead end
    if len(my_moves) == 0:
        # and return sequence was reset( happens when we reach the beginning )
        if len(return_sequence) == 0:
            # we're done!
            visitedBool = True
        else:
            # grab the next move to start going back
            my_move = return_sequence.pop(-1)
            # print, add to final path, and move player
            print(f"moving {my_move}")
            traversal_path.append(my_move)
            player.travel(my_move)
            # if at starting room, reset return_sequence
            if player.current_room.id == world.starting_room:
                return_sequence = []
    # as long as it's not a dead end,
    else:
        # grab next move, add to final path
        my_move = my_moves[0]
        print(f"moving {my_move}")
        traversal_path.append(my_move)
        # add the opposite to the return sequence, in case we need to go back
        return_sequence.append(opposite_directions[my_move])
        # move player and set new room id
        player.travel(my_move)
        new_room_id = player.current_room.id

        # add new_room_id to graph at prev id with move I took
        my_room_graph[room_id][my_move] = new_room_id
        # if new room isn't visited
        if new_room_id not in visited_rooms:
            # add new room to visited
            visited_rooms.add(new_room_id)
            # add new_room_id neighbors to graph
            add_unexplored_room_neighbors(new_room_id, player.current_room.get_exits(), room_id, opposite_directions[my_move])
    print()
    # time.sleep(.5)
# TRAVERSAL TEST - DO NOT MODIFY
visited = set()
player.current_room = world.starting_room
visited.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited.add(player.current_room)

if len(visited) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
