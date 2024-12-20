import chess
import chess.engine
import numpy as np
import random
import sys
import time
# Define a dictionary to map pieces to Unicode chess symbols
piece_to_unicode = {
    'r': '\u265C', 'n': '\u265E', 'b': '\u265D', 'q': '\u265B', 'k': '\u265A', 'p': '\u265F',
    'R': '\u2656', 'N': '\u2658', 'B': '\u2657', 'Q': '\u2655', 'K': '\u2654', 'P': '\u2659',
    '.': '\u0020', '\n':'\u0085',' ': '\u0020',  # Using middle dot for empty squares
}

def clear_line():
    sys.stdout.write('\033[1A')  # Clear the entire line
    sys.stdout.write('\033[K')  # Move the cursor to the beginning of the line

def clear_board():
    # Move the cursor up 8 lines (the height of the chess board)
    # sys.stdout.write('\033[AA')
    # Clear each line
    for _ in range(10):
        sys.stdout.write('\033[1A')  # Clear the entire line
        sys.stdout.write('\033[K')  # Move the cursor to the beginning of the line
    # Move the cursor back up to the top of the board
    # sys.stdout.write('\033[AA')

# Print the chess board with Unicode characters
def print_chess_board(board):
    # print(board.__str__().replace(" ", "").split('\n'))
    print("- A B C D E F G H -")  # Column labels
    for i, row in enumerate(board.__str__().replace(" ", "").split('\n')):
        # print(row, end=" ")
        print(f"{8 - i}", end=" ")  # Row labels
        for piece in row:
            print(piece_to_unicode[piece], end=" ")
        print(f" {8 - i}")  # Row labels
    print("- A B C D E F G H -")  # Column labels


def evaluate_board(board, maximizing_color):
    # Simple evaluation function
    # board.piece_map() returns a dictionary Dict[Square, Piece]
    # piece : instance of Piece
    # piece.color is True if WHITE else False
    whiteScore = sum([get_piece_value(piece) for piece in board.piece_map().values() if piece.color])
    blackScore = sum([get_piece_value(piece) for piece in board.piece_map().values() if not piece.color])
    score = whiteScore - blackScore
    if maximizing_color == chess.WHITE:
        return score
    else:
        return -score

def get_piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 10
    elif piece.piece_type == chess.KNIGHT:
        return 20
    elif piece.piece_type == chess.BISHOP:
        return 30
    elif piece.piece_type == chess.ROOK:
        return 40
    elif piece.piece_type == chess.QUEEN:
        return 75
    elif piece.piece_type == chess.KING:
        return 100
    return 0

def minimax(board, depth, alpha, beta, maximizing, maximizing_color):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, maximizing_color)
    
    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False, not maximizing_color)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True, maximizing_color)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move_minimax(board, depth, maximizing_color):
    best_move = None
    best_value = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, float('-inf'), float('inf'), False, maximizing_color)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move = move
    return best_move

if __name__ == '__main__':
    ######################## TOSS ###########################
    try:
        toss_choice = input("Enter your choice: [ H for Heads | T for Tails ] ")
        if toss_choice not in ['Heads', 'Tails', 'H', 'T']:
            raise ValueError
    except ValueError:
        print("Wrong Input. Valid Inputs are || 'Heads' | 'Tails' | 'H' | 'T' ||")
    if toss_choice == 'H':
        toss_choice = 'Heads'
    else:
        toss_choice = 'Tails'
    toss = np.random.choice(['Heads', 'Tails'])
    print("Toss outcome: ", toss)
    ################## PIECE COLOR ASSIGNMENT ###############
    user_moves_first = False
    if toss == toss_choice:
        print("Your piece color is WHITE.")
        maximizing_color = chess.BLACK
        print("You move first.")
        user_moves_first = True
    else:
        print("Your piece color is BLACK.")
        maximizing_color = chess.WHITE
        print("I move first.")
    ############### WINNING RESULT #########################
    winning_result = "1-0" if maximizing_color else "0-1"
    ############### PLAY ###################################
    board = chess.Board()
    ######## Assigning color to bot #######################
    board.turn=maximizing_color
    depth = 5  # Depth of search
    # print board
    print_chess_board(board)
    while not board.is_stalemate() and not board.outcome().winner==winning_result:
        # First move
        move_legal = False
        while not move_legal:
            try:
                # print(board.legal_moves)
                move = chess.Move.from_uci(input("Enter move: ")) if user_moves_first else find_best_move_minimax(board, depth, maximizing_color=chess.WHITE) #
                move_legal = True if board.is_legal(move) else False
                if not move_legal:
                    raise ValueError
            except ValueError:
                print("Move not legal. Try again.")
            except KeyboardInterrupt:
                print("\nResigned!")
                exit()
        # Print move
        print("Move: ", move)
        # Apply move on board
        board.push(move)
        # Print board
        time.sleep(2.0)
        clear_line()
        clear_board()
        print_chess_board(board)
        # Second move
        move_legal = False    
        while not move_legal:
            try:
                move = find_best_move_minimax(board, depth, maximizing_color=chess.BLACK) if user_moves_first else chess.Move.from_uci(input("Enter move: "))
                move_legal = True if board.is_legal(move) else False
                if not move_legal:
                    raise ValueError
            except ValueError:
                print("Move not legal. Try again.")
            except KeyboardInterrupt:
                print("\nResigned!")
                exit()
        # print move
        print("Move: ", move)
        # Apply move
        board.push(move)
        # Print board
        time.sleep(2.0)
        clear_line()
        clear_board()
        print_chess_board(board)
    # Outcome
    if board.outcome().winner==winning_result:
        print("You Win")
    elif board.outcome().result()=="1/2-1/2":
        print("It's a draw! Want a rematch?")
    else:
        print("You Lose")
