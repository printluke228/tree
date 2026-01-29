def is_win(board, player):
    """判定某个玩家是否获胜"""
    # 检查行、列、两条对角线
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # 行获胜
            return True
        if all(board[j][i] == player for j in range(3)):  # 列获胜
            return True
    # 对角线获胜
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def get_empty_cells(board):
    """获取棋盘上所有空位置的坐标"""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]

def simulate_game(board, current_player):
    """
    递归模拟对局，返回结果统计：[胜场, 负场, 平局]
    current_player：当前落子的玩家（O=我，X=对手）
    """
    # 先判定当前棋盘状态
    if is_win(board, 'O'):
        return [1, 0, 0]  # 我赢
    if is_win(board, 'X'):
        return [0, 1, 0]  # 对手赢
    empty_cells = get_empty_cells(board)
    if not empty_cells:
        return [0, 0, 1]  # 平局

    total = [0, 0, 0]
    # 枚举所有空位置，递归模拟
    for (i, j) in empty_cells:
        # 深拷贝棋盘，避免修改原棋盘
        new_board = [row.copy() for row in board]
        new_board[i][j] = current_player
        # 切换玩家
        next_player = 'X' if current_player == 'O' else 'O'
        # 递归结果累加
        res = simulate_game(new_board, next_player)
        total = [total[k] + res[k] for k in range(3)]
    return total

def calculate_win_rate(my_first, opp_first):
    """
    计算胜率主函数
    my_first：我的第一步坐标 (行, 列)，如(1,1)
    opp_first：对手的第一步坐标 (行, 列)，如(0,0)
    """
    # 校验坐标合法性
    def is_valid(pos):
        return len(pos) == 2 and all(0 <= x <= 2 for x in pos)
    if not (is_valid(my_first) and is_valid(opp_first)):
        raise ValueError("坐标无效，行和列必须是0/1/2的整数")
    if my_first == opp_first:
        raise ValueError("你和对手不能落子在同一个位置！")

    # 初始化3×3空棋盘
    board = [[None for _ in range(3)] for _ in range(3)]
    # 落子第一步：我先下O，对手后下X
    board[my_first[0]][my_first[1]] = 'O'
    board[opp_first[0]][opp_first[1]] = 'X'

    # 第二步轮到我落子，开始模拟所有对局
    win, lose, draw = simulate_game(board, current_player='O')
    total_games = win + lose + draw
    # 计算胜率（避免除零，实际井字棋第一步后必有后续走法）
    win_rate = (win / total_games) * 100 if total_games > 0 else 0.0

    # 输出详细信息和胜率
    print("="*30)
    print(f"你的第一步：{my_first} | 对手的第一步：{opp_first}")
    print(f"总模拟对局数：{total_games}")
    print(f"胜场：{win} | 负场：{lose} | 平局：{draw}")
    print(f"你的胜率：{win_rate:.2f}%")
    return win_rate
