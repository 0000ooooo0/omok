import pygame
import numpy as np
from typing import Tuple, Optional

class Board:
    def __init__(self, size: int = 15):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.cell_size = 40
        self.margin = 50
        self.board_width = size * self.cell_size
        self.board_height = size * self.cell_size
        self.screen_width = self.board_width + 2 * self.margin
        self.screen_height = self.board_height + 2 * self.margin
        
        # 3D 효과를 위한 색상
        self.board_color = (139, 69, 19)  # 나무색
        self.grid_color = (0, 0, 0)
        self.stone_colors = {
            1: (0, 0, 0),      # 검은 돌
            2: (255, 255, 255) # 흰 돌
        }
        self.stone_shadow_color = (100, 100, 100)
        
    def get_cell_from_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """마우스 위치를 보드 좌표로 변환 - 격자선 교차점 기준"""
        x, y = pos
        if (self.margin <= x <= self.margin + self.board_width and 
            self.margin <= y <= self.margin + self.board_height):
            # 격자선 교차점을 기준으로 계산
            col = round((x - self.margin) / self.cell_size)
            row = round((y - self.margin) / self.cell_size)
            if 0 <= row < self.size and 0 <= col < self.size:
                return (row, col)
        return None
    
    def get_stone_center(self, row: int, col: int) -> Tuple[int, int]:
        """돌의 중심 좌표 계산 - 격자선 교차점"""
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        return (x, y)
    
    def place_stone(self, row: int, col: int, player: int) -> bool:
        """돌을 놓기"""
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row, col] == 0:
            self.board[row, col] = player
            return True
        return False
    
    def check_winner(self, row: int, col: int, player: int) -> bool:
        """승리 조건 확인"""
        directions = [
            (0, 1),   # 가로
            (1, 0),   # 세로
            (1, 1),   # 대각선 ↘
            (1, -1)   # 대각선 ↙
        ]
        
        for dr, dc in directions:
            count = 1
            
            # 정방향 확인
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r, c] == player:
                count += 1
                r += dr
                c += dc
            
            # 역방향 확인
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r, c] == player:
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        
        return False
    
    def is_full(self) -> bool:
        """보드가 가득 찼는지 확인"""
        return np.all(self.board != 0)
    
    def draw(self, screen: pygame.Surface):
        """3D 효과가 있는 보드 그리기"""
        # 배경
        screen.fill((34, 139, 34))  # 초록색 배경
        
        # 3D 보드판 그리기
        board_rect = pygame.Rect(
            self.margin - 5, 
            self.margin - 5, 
            self.board_width + 10, 
            self.board_height + 10
        )
        
        # 보드 그림자
        shadow_rect = pygame.Rect(
            self.margin + 3, 
            self.margin + 3, 
            self.board_width + 10, 
            self.board_height + 10
        )
        pygame.draw.rect(screen, (100, 100, 100), shadow_rect)
        
        # 보드판
        pygame.draw.rect(screen, self.board_color, board_rect)
        
        # 격자 그리기
        for i in range(self.size + 1):
            # 세로선
            start_pos = (self.margin + i * self.cell_size, self.margin)
            end_pos = (self.margin + i * self.cell_size, self.margin + self.board_height)
            pygame.draw.line(screen, self.grid_color, start_pos, end_pos, 2)
            
            # 가로선
            start_pos = (self.margin, self.margin + i * self.cell_size)
            end_pos = (self.margin + self.board_width, self.margin + i * self.cell_size)
            pygame.draw.line(screen, self.grid_color, start_pos, end_pos, 2)
        
        # 돌 그리기
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row, col] != 0:
                    self.draw_stone(screen, row, col, self.board[row, col])
    
    def draw_stone(self, screen: pygame.Surface, row: int, col: int, player: int):
        """3D 효과가 있는 돌 그리기 - 격자선 교차점에 놓기"""
        # 돌을 격자선 교차점에 놓기
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        radius = self.cell_size // 2 - 2
        
        # 돌 그림자
        shadow_radius = radius + 2
        pygame.draw.circle(screen, self.stone_shadow_color, (x + 2, y + 2), shadow_radius)
        
        # 돌 그라데이션 효과
        color = self.stone_colors[player]
        for i in range(3):
            current_radius = radius - i * 2
            if current_radius > 0:
                # 밝기 조절로 그라데이션 효과
                if player == 1:  # 검은 돌
                    brightness = max(0, 50 - i * 15)
                    current_color = (brightness, brightness, brightness)
                else:  # 흰 돌
                    brightness = max(200, 255 - i * 15)
                    current_color = (brightness, brightness, brightness)
                
                pygame.draw.circle(screen, current_color, (x, y), current_radius)
        
        # 돌 하이라이트
        highlight_radius = radius // 3
        highlight_offset = radius // 4
        if player == 1:  # 검은 돌
            highlight_color = (100, 100, 100)
        else:  # 흰 돌
            highlight_color = (200, 200, 200)
        
        pygame.draw.circle(screen, highlight_color, 
                         (x - highlight_offset, y - highlight_offset), highlight_radius)
    
    def reset(self):
        """보드 초기화"""
        self.board = np.zeros((self.size, self.size), dtype=int) 