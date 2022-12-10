from math import inf as infinity
from random import choice
import platform
import time
from os import system

# CONSTANTS AND GLOBAL VARS
HUMAN = -1
COMP = +1
board = [
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
]


def evaluate(board):
	"""
	Evaluates the current state of the board.
	@param: the state of the current board
	@return: +1 human wins, -1 human losses, 0 draw
	"""
	if wins(board, COMP):
		score = +1
	elif wins(board, HUMAN):
		score = -1
	else:
		score = 0

	return score


def wins(board, player):
	"""
	Checks if the given player wins.
	Win cases:
	* Three rows    [X X X] or [O O O].
	* Three cols    [X X X] or [O O O].
	* Two diagonals [X X X] or [O O O].
	@param board: the current board
	@param player: the human or computer player
	@return: True if the player wins
	"""
	win_state = [
		[board[0][0], board[0][1], board[0][2]],
		[board[1][0], board[1][1], board[1][2]],
		[board[2][0], board[2][1], board[2][2]],
		[board[0][0], board[1][0], board[2][0]],
		[board[0][1], board[1][1], board[2][1]],
		[board[0][2], board[1][2], board[2][2]],
		[board[0][0], board[1][1], board[2][2]],
		[board[2][0], board[1][1], board[0][2]],
	]
	if [player, player, player] in win_state:
		return True
	else:
		return False

def game_over(state):
	"""
	This function test if the human or computer wins.
	@param: the state of the current board
	@return: True if the human or computer wins
	"""
	return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(board):
	"""
	checks empty cells of the board
	@param: the state of the current board
	@return: a list of the empty cells
	"""
	cells = []

	for x, row in enumerate(board):
		for y, cell in enumerate(row):
			if cell == 0:
				cells.append([x, y])

	return cells


def valid_move(x, y):
	"""
	check if the player moves are valid or not,
	depending on rules and empty cells
	@param x: X coordinate
	@param y: Y coordinate
	@return: True if the board[x][y] is empty
	"""
	if [x, y] in empty_cells(board):
		return True
	else:
		return False


def set_move(x, y, player):
	"""
	Set the move on board, if the move coords are valid
	@param x: X coordinate
	@param y: Y coordinate
	@param player: the current player
	@return: true and move or false if the move was validated
	"""
	if valid_move(x, y):
		board[x][y] = player
		return True
	else:
		return False


def minimax(state, depth, player):
	"""
	AI algorithm that chooses the best move
	@param state: current state of the board
	@param depth: node index in the tree (0 <= depth <= 9),
	but never nine (see iaturn() function)
	@param player: the current player
	@return: a list with [the best row, best col, best score]
	"""

	if player == COMP:
		best = [-1, -1, -infinity]
	else:
		best = [-1, -1, +infinity]

	if depth == 0 or game_over(state):
		score = evaluate(state)
		return [-1, -1, score]

	for cell in empty_cells(state):
		x, y = cell[0], cell[1]
		state[x][y] = player
		# maybe number of recursion could be limited
		if difficulty == 1:
			# limit recursion to 3 levels
			score = lim_minimax(state, depth - 1, -player, 0)
		elif difficulty == 2:
			# limit recursion to 5 levels
			score = lim_minimax(state, depth - 1, -player, 0)
		elif difficulty == 3:
			# full level recursion
			score = minimax(state, depth - 1, -player)

		state[x][y] = 0
		score[0], score[1] = x, y

		if player == COMP:
			if score[2] > best[2]:
				best = score  # max value
		else:
			if score[2] < best[2]:
				best = score  # min value
	return best


def lim_minimax(state, depth, player, diff_counter):
	"""
	Same as minimax function but used for limited recursion.
	Limits recursion by diff_counter param.
	"""
	# DIFFICULTY VALIDATION TO LIMIT RECURSION
	if difficulty == 1:
		if diff_counter < 3:
			if player == COMP:
				best = [-1, -1, -infinity]
			else:
				best = [-1, -1, +infinity]

			if depth == 0 or game_over(state):
				score = evaluate(state)
				return [-1, -1, score]

			for cell in empty_cells(state):
				x, y = cell[0], cell[1]
				state[x][y] = player

				# limit recursion to 3 levels
				score = lim_minimax(state, depth - 1, -player, diff_counter + 1)

				state[x][y] = 0
				score[0], score[1] = x, y

				if player == COMP:
					if score[2] > best[2]:
						best = score  # max value
				else:
					if score[2] < best[2]:
						best = score  # min value
		else:
			# score = lim_minimax(state, 0, -player, diff_counter)
			score = eval_funct(state, depth, player)
			best = score

	elif difficulty == 2:
		# limit recursion to 5 levels
		if diff_counter < 5:
			if player == COMP:
				best = [-1, -1, -infinity]
			else:
				best = [-1, -1, +infinity]

			if depth == 0 or game_over(state):
				score = evaluate(state)
				return [-1, -1, score]

			for cell in empty_cells(state):
				x, y = cell[0], cell[1]
				state[x][y] = player
				score = lim_minimax(state, depth - 1, -player, diff_counter + 1)
				state[x][y] = 0
				score[0], score[1] = x, y
				if player == COMP:
					if score[2] > best[2]:
						best = score  # max value
				else:
					if score[2] < best[2]:
						best = score  # min value
		else:
			# score = lim_minimax(state, 0, -player, diff_counter)
			score = eval_funct(state, depth, player)
			best = score

	elif difficulty == 3:
		# full level recursion
		if player == COMP:
			best = [-1, -1, -infinity]
		else:
			best = [-1, -1, +infinity]

		if depth == 0 or game_over(state):
			score = evaluate(state)
			return [-1, -1, score]

		for cell in empty_cells(state):
			x, y = cell[0], cell[1]
			state[x][y] = player

			# full level recursion
			score = minimax(state, depth - 1, -player)

			state[x][y] = 0
			score[0], score[1] = x, y

			if player == COMP:
				if score[2] > best[2]:
					best = score  # max value
			else:
				if score[2] < best[2]:
					best = score  # min value

	return best

def eval_funct(state, depth, player):
	"""
	Euristic evaluation function. Iterates over
	each empty cell to count near opponent
	and same player cells.
	@param state: current board state
	@param depth: node index in the tree
	@param player: current player
	@return: list with [best row, best col, best score]
	"""

	if player == COMP:
		best = [-1, -1, -infinity]
	else:
		best = [-1, -1, +infinity]

	if depth == 0 or game_over(state):
		score = evaluate(state)
		return [-1, -1, score]

	player_count = 0
	opponent_count = 0
	for cell in empty_cells(state):
		x, y = cell[0], cell[1]
		state[x][y] = player

		# check previous cell to left
		if (x-1) >= 0 and (x-1) <= 2:
			if state[x-1][y] == player:
				player_count += 1
			elif state[x-1][y] == -player:
				opponent_count += 1

		# check previous cell above
		if (y-1) >= 0 and (y-1) <= 2:
			if state[x][y-1] == player:
				player_count += 1
			elif state[x][y-1] == -player:
				opponent_count += 1

		# check next cell to right
		if (x+1) >= 0 and (x+1) <= 2:
			if state[x+1][y] == player:
				player_count += 1
			elif state[x+1][y] == -player:
				opponent_count += 1

		# check next cell below
		if (y+1) >= 0 and (y+1) <= 2:
			if state[x][y+1] == player:
				player_count += 1
			elif state[x][y+1] == -player:
				opponent_count += 1

		# check previous cell left and up
		if ((x-1) >= 0 and (x-1) <= 2) and ((y-1) >= 0 and (y-1) <= 2):
			if state[x-1][y-1] == player:
				player_count += 1
			elif state[x-1][y-1] == -player:
				opponent_count += 1

		# check next cell left and down
		if ((x-1) >= 0 and (x-1) <= 2) and ((y+1) >= 0 and (y+1) <= 2):
			if state[x-1][y+1] == player:
				player_count += 1
			elif state[x-1][y+1] == -player:
				opponent_count += 1

		# check next cell right and up
		if ((x+1) >= 0 and (x+1) <= 2) and ((y+1) >= 0 and (y+1) <= 2):
			if state[x+1][y+1] == player:
				player_count += 1
			elif state[x+1][y+1] == -player:
				opponent_count += 1

		# check previous cell right and down
		if ((x+1) >= 0 and (x+1) <= 2) and ((y-1) >= 0 and (y-1) <= 2):
			if state[x+1][y-1] == player:
				player_count += 1
			elif state[x+1][y-1] == -player:
				opponent_count += 1

		state[x][y] = 0
		best[0], best[1] = x, y

	if player_count > opponent_count:
		score = 1
	elif player_count < opponent_count:
		score = -1
	else:
		score = 0

	if player == COMP:
		if score > best[2]:
			best[2] = score  # max value
	else:
		if score < best[2]:
			best[2] = score  # min value

	return best


def clean():
	"""
	Clears the console
	"""
	os_name = platform.system().lower()
	if 'windows' in os_name:
		system('cls')
	else:
		system('clear')


def render(state, c_choice, h_choice):
	"""
	Prints the board on console
	@param state: current state of the board
	@param c_choice: computer choice
	@param h_choice: human choice
	"""

	chars = {
		-1: h_choice,
		+1: c_choice,
		0: ' '
	}
	str_line = '---------------'

	print('\n' + str_line)
	for row in state:
		for cell in row:
			symbol = chars[cell]
			print(f'| {symbol} |', end='')
		print('\n' + str_line)


def ai_turn(c_choice, h_choice):
	"""
	Calls the minimax function if the depth < 9,
	else, choices a random coordinate
	@param c_choice: computer's choice X or O
	@param h_choice: human's choice X or O
	@return: none
	"""
	depth = len(empty_cells(board))

	if depth == 0 or game_over(board):
		return

	clean()
	print(f'Computer turn [{c_choice}]')
	render(board, c_choice, h_choice)

	move = minimax(board, depth, COMP)
	x, y = move[0], move[1]

	set_move(x, y, COMP)
	time.sleep(1)


def human_turn(c_choice, h_choice):
	"""
	The Human plays choosing a valid move.
	@param c_choice: computer's choice X or O
	@param h_choice: human's choice X or O
	@return: none
	"""
	depth = len(empty_cells(board))
	if depth == 0 or game_over(board):
		return

	# Dictionary of valid movement coordinates
	move = -1
	moves = {
		1: [0, 0], 2: [0, 1], 3: [0, 2],
		4: [1, 0], 5: [1, 1], 6: [1, 2],
		7: [2, 0], 8: [2, 1], 9: [2, 2],
	}

	clean()
	print(f'Human turn [{h_choice}]')
	render(board, c_choice, h_choice)

	while move < 1 or move > 9:
		try:
			move = int(input('Choose cell (1..9): '))
			coord = moves[move]
			can_move = set_move(coord[0], coord[1], HUMAN)

			if not can_move:
				print('Bad move!')
				move = -1
		except (EOFError, KeyboardInterrupt):
			print("\nBye\n")
			time.sleep(1)
			system("exit")
			exit()
		except (KeyError, ValueError):
			print('Bad choice!')


def main():
	"""
	Main function of program flow
	"""
	clean()
	h_choice = ''  # X or O
	c_choice = ''  # X or O
	first = ''  # if human is the first

	# Human chooses X or O to play
	while h_choice != 'O' and h_choice != 'X':
		try:
			print('')
			h_choice = input('Choose X or O: ').upper()
		except (EOFError, KeyboardInterrupt):
			print("\nBye\n")
			time.sleep(1)
			system("exit")
			exit()
		except (KeyError, ValueError):
			print('Bad choice')

	# Setting computers choice
	if h_choice == 'X':
		first = 'Y'
		c_choice = 'O'
	else:
		first = 'N'
		c_choice = 'X'

	clean()

	global difficulty
	difficulty = 0

	while difficulty <= 0 or difficulty > 3:
		try:
			print('')
			difficulty = int(input('Choose difficulty (1,2,3): '))
		except (EOFError, KeyboardInterrupt):
			print("\nBye\n")
			time.sleep(1)
			system("exit")
			exit()
		except (KeyError, ValueError):
			print('Bad choice')

	# Main loop of the game
	while len(empty_cells(board)) > 0 and not game_over(board):
		if first == 'N':
			# computer begins with a random choice
			ai_turn(c_choice, h_choice)
			first = ''

		human_turn(c_choice, h_choice)
		ai_turn(c_choice, h_choice)

	# Game over message
	if wins(board, HUMAN):
		clean()
		print(f'Human turn [{h_choice}]')
		render(board, c_choice, h_choice)
		print('YOU WIN!')
	elif wins(board, COMP):
		clean()
		print(f'Computer turn [{c_choice}]')
		render(board, c_choice, h_choice)
		print('YOU LOSE!')
	else:
		clean()
		render(board, c_choice, h_choice)
		print('DRAW!')

	# exit automaticlly after 5 seconds
	time.sleep(5)
	exit()


if __name__ == '__main__':
	main()
