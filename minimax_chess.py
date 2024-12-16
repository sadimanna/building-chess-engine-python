import chess
import chess.engine

# Function to check if the game has ended
def check_game_end(board):
    if board.is_checkmate():
        print("Checkmate!")
        return True
    if board.is_stalemate():
        print("Stalemate!")
        return True
    if board.is_insufficient_material():
        print("Insufficient material!")
        return True
    if board.is_seventyfive_moves():
        print("Seventy-five moves rule!")
        return True
    if board.is_fivefold_repetition():
        print("Fivefold repetition!")
        return True
    if board.is_variant_draw():
        print("Draw by variant-specific rules!")
        return True
    return False

def evaluate_board(board):
    # Simple evaluation function
    material = sum([get_piece_value(piece) for piece in board.piece_map().values()])
    return material

def get_piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 2
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 4
    elif piece.piece_type == chess.QUEEN:
        return 5
    elif piece.piece_type == chess.KING:
        return 6
    return 0

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
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
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):
    best_move = None
    best_value = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move = move
    return best_move

if __name__ == '__main__':
    board = chess.Board()
    depth = 5  # Depth of search
    while not board.can_claim_draw() or not board.is_stalemate() or not board.outcome().winner:
        move = find_best_move(board, depth) #input("Enter move: ")
        board.push(move) #chess.Move.from_uci(move))
        best_move = find_best_move(board, depth)
        print(f"Best move: {best_move}")
        board.push(best_move) #chess.Move.from_uci(best_move))
        print(board)
    
   # Check if the game has ended
   if check_game_end(board):
      print("The game has ended.")
      if board.outcome().winner:
          print('You Win')
