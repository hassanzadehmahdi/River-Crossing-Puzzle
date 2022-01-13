import copy
import time
from os import system, name

# place in state for each character
FATHER = 0
MOTHER = 1
SON_1 = 2
SON_2 = 3
DAUGHTER_1 = 4
DAUGHTER_2 = 5
THIEF = 6
POLICE = 7
BOAT = 8

# initial state
START_STATE = ["L", "L", "L", "L", "L", "L", "L", "L", "L"]

# define thief rule
def thiefRule(state):
    return state[POLICE] == state[THIEF] or (
        state[THIEF] != state[FATHER]
        and state[THIEF] != state[MOTHER]
        and state[THIEF] != state[SON_1]
        and state[THIEF] != state[SON_2]
        and state[THIEF] != state[DAUGHTER_1]
        and state[THIEF] != state[DAUGHTER_2]
    )


# define daughter rule
def daughterRule(state):
    return (
        state[DAUGHTER_1] == state[MOTHER] or state[DAUGHTER_1] != state[FATHER]
    ) and (state[DAUGHTER_2] == state[MOTHER] or state[DAUGHTER_2] != state[FATHER])


# define son rule
def sonRule(state):
    return (state[SON_1] == state[FATHER] or state[SON_1] != state[MOTHER]) and (
        state[SON_2] == state[FATHER] or state[SON_2] != state[MOTHER]
    )


# We have defined each rule and in this function we check whether the given state is valid or not
def isValid(state):
    return thiefRule(state) and daughterRule(state) and sonRule(state)


# checking for goal state
def isGoal(state):
    return state == ["R", "R", "R", "R", "R", "R", "R", "R", "R"]


# generates all possible moves
def generateMoves(state):
    for other in [FATHER, MOTHER, DAUGHTER_1, DAUGHTER_2, SON_1, SON_2, THIEF, POLICE]:
        if state[FATHER] == state[other] == state[BOAT]:
            move = copy.deepcopy(state)
            move[FATHER] = "L" if state[FATHER] == "R" else "R"
            move[other] = "L" if state[other] == "R" else "R"
            move[BOAT] = "L" if state[BOAT] == "R" else "R"
            yield move

        if state[MOTHER] == state[other] == state[BOAT]:
            move = copy.deepcopy(state)
            move[MOTHER] = "L" if state[MOTHER] == "R" else "R"
            move[other] = "L" if state[other] == "R" else "R"
            move[BOAT] = "L" if state[BOAT] == "R" else "R"
            yield move

        if state[POLICE] == state[other] == state[BOAT]:
            move = copy.deepcopy(state)
            move[POLICE] = "L" if state[POLICE] == "R" else "R"
            move[other] = "L" if state[other] == "R" else "R"
            move[BOAT] = "L" if state[BOAT] == "R" else "R"
            yield move


# filter out only the valid moves
def validMoves(state_list):
    validList = []
    for state in state_list:
        if isValid(state) and state not in validList:
            validList.append(state)
    return validList


# we do a depth limited search, using a previous_states list to keep track of where we have been. This function only returns a winning answer.
def depthLimitedSearch(state, previous_states, maxDepth):
    previous_states.append(state)

    if isGoal(state):
        return previous_states

    if maxDepth <= 0:
        return None

    for move in validMoves(generateMoves(state)):
        if move not in previous_states:
            result = depthLimitedSearch(move, previous_states, maxDepth - 1)
            if result is not None:
                return result
            previous_states.pop()

    return None


# print one state in the terminal
def show(state):
    CHARACTERSNAME = [
        "FATHER",
        "MOTHER",
        "SON_1",
        "SON_2",
        "DAUGHTER_1",
        "DAUGHTER_2",
        "THIEF",
        "POLICE",
    ]
    space = " " * 10
    plainText = "|| {} |                | {} ||"

    print("=" * 46)
    print(plainText.format(space, space))

    for i in range(0, 8):
        characterName = CHARACTERSNAME[i] + " " * (10 - len(CHARACTERSNAME[i]))

        if state[i] == "L":
            print(plainText.format(characterName, space))
        else:
            print(plainText.format(space, characterName))

        if i == 3:
            if state[8] == "R":
                print("||", space, "|           \\___/|", space, "||")
            else:
                print("||", space, "|\\___/           |", space, "||")

    print(plainText.format(space, space))
    print("=" * 46)


# print path in the terminal with help of show() function
def pathShow(state_list, delay):
    for state in state_list:
        show(state)
        time.sleep(delay)
        clear()


# clear the terminal
def clear():

    # for windows
    if name == "nt":
        _ = system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


# main function
def main():

    state_list = depthLimitedSearch(
        ["L", "L", "L", "L", "L", "L", "L", "L", "L"], [], 30
    )

    userInput = input(
        "please enter number of the state that you want to print (0 to 17) or enter 'path' for showing path or enter 'exit' for exiting: "
    )

    while userInput != "exit":
        try:

            if userInput == "path":
                clear()
                pathShow(state_list, 1.5)

            else:
                show(state_list[int(userInput)])

            userInput = input(
                "please enter number of the state that you want to print (0 to 17) or enter 'path' for showing path or enter 'exit' for exiting: "
            )
        except:
            print("please enter a valid value.")
            userInput = input(
                "please enter number of the state that you want to print (0 to 17) or enter 'path' for showing path or enter 'exit' for exiting: "
            )
            continue


main()
