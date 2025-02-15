from kogi_canvas import Canvas
import math
import random
import time

BLACK=1
WHITE=2

board = [
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,1,2,0,0],
        [0,0,2,1,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
]

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 置けるなら True, 置けないなら False
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす

    return False

def can_place(board, stone):
    """
    石を置ける場所を調べる関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

def random_place(board, stone):
    """
    石をランダムに置く関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    while True:
        x = random.randint(0, len(board[0]) - 1)
        y = random.randint(0, len(board) - 1)
        if can_place_x_y(board, stone, x, y):
            return x, y

def copy(board):
    """
    盤面をコピーする関数。
    board: 2次元配列のオセロボード
    """
    return [row[:] for row in board]


def move_stone(board, stone, x, y):
    """
    石を置き、ひっくり返す関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return:
    """
    moves = [copy(board)]*3
    if not can_place_x_y(board, stone, x, y):
        return moves  # 置けない場合は何もしない

    board[y][x] = stone  # 石を置く
    moves.append(copy(board))
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    flipped_count = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        stones_to_flip = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        if stones_to_flip and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            for flip_x, flip_y in stones_to_flip:
                board[flip_y][flip_x] = stone
                moves.append(copy(board))
                flipped_count += 1

    return moves


class hiyokoAI(object):

    def face(self):
        return "🐣"

    def place(self, board, stone):
        # 角の位置
        corners = [(0, 0), (0, 5), (5, 0), (5, 5)]
        valid_moves = []

        # 有効な手をすべて調べる
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    valid_moves.append((x, y))

        # 角が取れる場合は優先して選ぶ
        for move in valid_moves:
            if move in corners:
                return move

        # 角が取れない場合は評価関数を使って選ぶ
        def evaluate(move):
            x, y = move
            # 角に近い位置や、相手にとって有利な位置を避ける
            if (x, y) in [(0, 1), (1, 0), (1, 1), (0, 4), (1, 4), (1, 5), (4, 0), (4, 1), (5, 1), (4, 4), (4, 5), (5, 4)]:
                return -10  # マイナスのスコアを付ける
            return sum([1 for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                        if 0 <= x + dx < len(board[0]) and 0 <= y + dy < len(board) and board[y + dy][x + dx] == stone])

        # 評価が最も高い手を選ぶ
        best_move = max(valid_moves, key=evaluate)
        return best_move



def draw_board(canvas, board):
    ctx = canvas.getContext("2d")
    grid = width // len(board)
    for y, line in enumerate(board):
        for x, stone in enumerate(line):
            cx = x * grid + grid // 2
            cy = y * grid + grid // 2
            if stone != 0:
                ctx.beginPath()
                ctx.arc(cx, cy, grid//2, 0, 2 * math.pi) # 円の描画
                ctx.fillStyle = "black" if stone == 1 else "white"
                ctx.fill()

width=300

def draw_board_moves(canvas, moves):
    for board in moves:
        draw_board(canvas, board)

def play_othello(ai=None, board=None):
    if board is None:
        board = [
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,1,2,0,0],
            [0,0,2,1,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
        ]
    if ai is None:
        ai = PandaAI()

    def redraw(canvas, x, y):
        nonlocal board, ai
        N = len(board)
        grid = width // N
        x = x // grid
        y = y // grid
        if not can_place_x_y(board, BLACK, x, y):
            print('そこに置けません', (x, y))
            return

        moves = []
        moves.extend(move_stone(board, BLACK, x, y))

        if can_place(board, WHITE):
            x, y = ai.place(board, WHITE)
            if not can_place_x_y(board, WHITE, x, y):
                print(f'{ai.face()}は、置けないところに置こうとしました', (x, y))
                print('反則負けです')
                return
            print(f'{ai.face()}は', (x, y), 'におきました。')
            moves.extend(move_stone(board, WHITE, x, y))
        else:
            print(f'{ai.face()}はどこにも置けないのでスキップします')

        while not can_place(board, BLACK):
            if can_place(board, WHITE):
                print(f'あなたはどこにも置けないのでスキップします')
                x, y = ai.place(board, WHITE)
                print(f'{ai.face()}は', (x, y), 'におきました。')
                moves.extend(move_stone(board, WHITE, x, y))
            else:
                black = sum(row.count(BLACK) for row in board)
                white = sum(row.count(WHITE) for row in board)
                print(f'黒: {black}, 白: {white}', end=' ')
                if black > white:
                    print('黒の勝ち')
                elif black < white:
                    print('白の勝ち')
                else:
                    print('引き分け')
                break
        draw_board_moves(canvas, moves)


    canvas = Canvas(background='green', grid=width//6, width=width, height=width, onclick=redraw)
    draw_board(canvas, board)

    display(canvas)


def count_stone(board):
    black = sum(row.count(BLACK) for row in board)
    white = sum(row.count(WHITE) for row in board)
    return black, white

def run_othello(blackai=None, whiteai=None, board=None):
    if board is None:
        board = [
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [0,0,1,2,0,0],
            [0,0,2,1,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
        ]
    if blackai is None:
        blackai = PandaAI()

    if whiteai is None:
        whiteai = PandaAI()
        print(f'{whiteai.face()}が相手するよ！覚悟しな！')

    black_time = 0
    white_time = 0
    moved = True
    while moved and can_place(board, BLACK) and can_place(board, WHITE):
        moved = False
        if can_place(board, BLACK):
            start = time.time()
            x, y = blackai.place(copy(board), BLACK)
            black_time += time.time() - start
            if not can_place_x_y(board, BLACK, x, y):
                print(f'{blackai.face()}は、置けないところに置こうとしました', (x, y))
                print('反則負けです')
                return
            move_stone(board, BLACK, x, y)
            black, white = count_stone(board)
            print(f'{blackai.face()}は{(x, y)}におきました。黒: {black}, 白: {white}')
            moved = True
        else:
            print(f'{blackai.face()}は、どこにも置けないのでスキップします')

        if can_place(board, WHITE):
            start = time.time()
            x, y = whiteai.place(copy(board), WHITE)
            white_time += time.time() - start
            if not can_place_x_y(board, WHITE, x, y):
                print(f'{whiteai.face()}は、置けないところに置こうとしました', (x, y))
                print('反則負けです')
                return
            move_stone(board, WHITE, x, y)
            black, white = count_stone(board)
            print(f'{whiteai.face()}は{(x, y)}におきました。黒: {black}, 白: {white}')
            moved = True
        else:
            print(f'{whiteai.face()}は、どこにも置けないのでスキップします')

    black, white = count_stone(board)
    print(f'最終結果: 黒: {black}, 白: {white}', end=' ')
    if black > white:
        print(f'黒{blackai.face()}の勝ち')
    elif black < white:
        print(f'白{whiteai.face()}の勝ち')
    else:
        print('引き分け')
    print(f'思考時間: 黒: {black_time:.5f}秒, 白: {white_time:.5f}秒')
