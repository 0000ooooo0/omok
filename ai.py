import numpy as np
from typing import Tuple, List
import random

class AI:
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.opponent_id = 3 - player_id  # 1이면 2, 2이면 1
    
    def evaluate_position(self, board: np.ndarray, row: int, col: int, player: int) -> int:
        """특정 위치의 가치를 평가"""
        if board[row, col] != 0:
            return -1000  # 이미 돌이 놓인 위치
        
        # 임시로 돌을 놓아서 평가
        board[row, col] = player
        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        total_score = 0
        
        for dr, dc in directions:
            count = 1
            blocked = 0
            
            # 정방향 확인
            r, c = row + dr, col + dc
            while 0 <= r < board.shape[0] and 0 <= c < board.shape[1] and board[r, c] == player:
                count += 1
                r += dr
                c += dc
            if not (0 <= r < board.shape[0] and 0 <= c < board.shape[1]) or board[r, c] != 0:
                blocked += 1
            
            # 역방향 확인
            r, c = row - dr, col - dc
            while 0 <= r < board.shape[0] and 0 <= c < board.shape[1] and board[r, c] == player:
                count += 1
                r -= dr
                c -= dc
            if not (0 <= r < board.shape[0] and 0 <= c < board.shape[1]) or board[r, c] != 0:
                blocked += 1
            
            # 점수 계산
            if count >= 5:
                total_score += 10000
            elif count == 4 and blocked == 0:
                total_score += 1000
            elif count == 3 and blocked == 0:
                total_score += 100
            elif count == 2 and blocked == 0:
                total_score += 10
        
        # 임시로 놓은 돌 제거
        board[row, col] = 0
        
        return total_score
    
    def get_available_moves(self, board: np.ndarray) -> List[Tuple[int, int]]:
        """가능한 수를 찾기"""
        moves = []
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row, col] == 0:
                    # 주변에 돌이 있는 위치만 고려 (성능 최적화)
                    has_neighbor = False
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            r, c = row + dr, col + dc
                            if (0 <= r < board.shape[0] and 0 <= c < board.shape[1] and 
                                board[r, c] != 0):
                                has_neighbor = True
                                break
                        if has_neighbor:
                            break
                    
                    if has_neighbor or board.shape[0] * board.shape[1] < 50:  # 작은 보드면 모든 위치 고려
                        moves.append((row, col))
        
        return moves if moves else [(row, col) for row in range(board.shape[0]) 
                                  for col in range(board.shape[1]) if board[row, col] == 0]
    
    def make_move(self, board: np.ndarray) -> Tuple[int, int]:
        """AI의 수를 결정"""
        available_moves = self.get_available_moves(board)
        
        if not available_moves:
            return (0, 0)
        
        best_score = float('-inf')
        best_moves = []
        
        for row, col in available_moves:
            # 내 수의 가치
            my_score = self.evaluate_position(board, row, col, self.player_id)
            
            # 상대방이 이 위치에 놓았을 때의 가치 (방어)
            opponent_score = self.evaluate_position(board, row, col, self.opponent_id)
            
            # 종합 점수 (공격과 방어를 모두 고려)
            total_score = my_score + opponent_score * 0.8
            
            if total_score > best_score:
                best_score = total_score
                best_moves = [(row, col)]
            elif total_score == best_score:
                best_moves.append((row, col))
        
        # 최고 점수의 수들 중에서 랜덤 선택
        return random.choice(best_moves)
    
    def get_move_with_difficulty(self, board: np.ndarray, difficulty: str = "medium") -> Tuple[int, int]:
        """난이도에 따른 AI 수 결정"""
        if difficulty == "easy":
            # 쉬운 난이도: 랜덤 수
            available_moves = self.get_available_moves(board)
            return random.choice(available_moves) if available_moves else (0, 0)
        
        elif difficulty == "hard":
            # 어려운 난이도: 더 깊은 탐색
            return self.make_move(board)
        
        else:  # medium
            # 중간 난이도: 70% 확률로 좋은 수, 30% 확률로 랜덤 수
            if random.random() < 0.7:
                return self.make_move(board)
            else:
                available_moves = self.get_available_moves(board)
                return random.choice(available_moves) if available_moves else (0, 0) 