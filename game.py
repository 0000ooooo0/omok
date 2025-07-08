import pygame
import sys
from typing import Optional, Tuple
from board import Board
from ai import AI

class Game:
    def __init__(self):
        pygame.init()
        self.board = Board(15)  # 15x15 오목판
        self.screen = pygame.display.set_mode((self.board.screen_width, self.board.screen_height))
        pygame.display.set_caption("3D 오목 게임")
        
        # 게임 상태
        self.current_player = 1  # 1: 검은 돌, 2: 흰 돌
        self.game_mode = "2player"  # "2player", "ai_easy", "ai_medium", "ai_hard"
        self.game_state = "playing"  # "playing", "game_over", "menu"
        self.winner = None
        
        # AI
        self.ai = AI(2)
        
        # 폰트 - 한글 지원
        try:
            # Windows 시스템 폰트 사용
            self.font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 36)
            self.small_font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 24)
        except:
            try:
                # 대체 폰트
                self.font = pygame.font.Font("C:/Windows/Fonts/gulim.ttc", 36)
                self.small_font = pygame.font.Font("C:/Windows/Fonts/gulim.ttc", 24)
            except:
                # 기본 폰트 사용
                self.font = pygame.font.Font(None, 36)
                self.small_font = pygame.font.Font(None, 24)
        
        # UI 상태
        self.show_menu = True
        self.selected_mode = 0
        self.menu_options = [
            "2인용 게임",
            "AI vs 플레이어 (쉬움)",
            "AI vs 플레이어 (보통)",
            "AI vs 플레이어 (어려움)"
        ]
        

        
        # 색상
        self.menu_bg_color = (50, 50, 50)
        self.menu_text_color = (255, 255, 255)
        self.menu_selected_color = (100, 150, 255)
        
    def handle_menu_events(self, event):
        """메뉴 이벤트 처리"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_mode = (self.selected_mode - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_mode = (self.selected_mode + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    def handle_game_events(self, event):
        """게임 이벤트 처리"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game_state == "playing":
                pos = pygame.mouse.get_pos()
                cell = self.board.get_cell_from_pos(pos)
                if cell:
                    row, col = cell
                    if self.board.place_stone(row, col, self.current_player):
                        if self.board.check_winner(row, col, self.current_player):
                            self.game_state = "game_over"
                            self.winner = self.current_player
                        elif self.board.is_full():
                            self.game_state = "game_over"
                            self.winner = 0  # 무승부
                        else:
                            self.current_player = 3 - self.current_player  # 플레이어 전환
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_m:
                self.show_menu = True
                self.game_state = "menu"
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    def start_game(self):
        """게임 시작"""
        self.show_menu = False
        self.game_state = "playing"
        self.current_player = 1
        self.winner = None
        self.board.reset()
        
        # 게임 모드 설정
        if self.selected_mode == 0:
            self.game_mode = "2player"
        elif self.selected_mode == 1:
            self.game_mode = "ai_easy"
        elif self.selected_mode == 2:
            self.game_mode = "ai_medium"
        elif self.selected_mode == 3:
            self.game_mode = "ai_hard"
    
    def reset_game(self):
        """게임 리셋"""
        self.game_state = "playing"
        self.current_player = 1
        self.winner = None
        self.board.reset()
    
    def ai_move(self):
        """AI 수 두기"""
        if self.game_state == "playing" and self.current_player == 2:
            difficulty = self.game_mode.split("_")[1] if "_" in self.game_mode else "medium"
            row, col = self.ai.get_move_with_difficulty(self.board.board, difficulty)
            
            if self.board.place_stone(row, col, self.current_player):
                if self.board.check_winner(row, col, self.current_player):
                    self.game_state = "game_over"
                    self.winner = self.current_player
                elif self.board.is_full():
                    self.game_state = "game_over"
                    self.winner = 0
                else:
                    self.current_player = 3 - self.current_player
    
    def draw_menu(self):
        """메뉴 그리기"""
        self.screen.fill(self.menu_bg_color)
        
        # 제목
        title = self.font.render("3D 오목 게임", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.board.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # 메뉴 옵션들
        for i, option in enumerate(self.menu_options):
            color = self.menu_selected_color if i == self.selected_mode else self.menu_text_color
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.board.screen_width // 2, 200 + i * 50))
            self.screen.blit(text, text_rect)
        
        # 안내
        instruction = self.small_font.render("↑↓: 선택, Enter: 시작, ESC: 종료", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(center=(self.board.screen_width // 2, 400))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_game_info(self):
        """게임 정보 그리기"""
        # 현재 플레이어 표시
        player_text = f"현재 플레이어: {'검은 돌' if self.current_player == 1 else '흰 돌'}"
        player_surface = self.small_font.render(player_text, True, (255, 255, 255))
        self.screen.blit(player_surface, (10, 10))
        
        # 게임 모드 표시
        mode_text = f"모드: {self.menu_options[self.selected_mode]}"
        mode_surface = self.small_font.render(mode_text, True, (255, 255, 255))
        self.screen.blit(mode_surface, (10, 35))
        
        # 조작법
        controls = [
            "R: 게임 리셋",
            "M: 메뉴로 돌아가기",
            "ESC: 종료"
        ]
        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, (200, 200, 200))
            self.screen.blit(control_surface, (10, 60 + i * 20))
    
    def draw_game_over(self):
        """게임 오버 화면 그리기"""
        # 반투명 오버레이
        overlay = pygame.Surface((self.board.screen_width, self.board.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 결과 메시지
        if self.winner == 0:
            message = "무승부!"
        else:
            winner_name = "검은 돌" if self.winner == 1 else "흰 돌"
            message = f"{winner_name} 승리!"
        
        result_text = self.font.render(message, True, (255, 255, 255))
        result_rect = result_text.get_rect(center=(self.board.screen_width // 2, self.board.screen_height // 2))
        self.screen.blit(result_text, result_rect)
        
        # 재시작 안내
        restart_text = self.small_font.render("R: 재시작, M: 메뉴로 돌아가기", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(self.board.screen_width // 2, self.board.screen_height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """게임 메인 루프"""
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.show_menu:
                    self.handle_menu_events(event)
                else:
                    self.handle_game_events(event)
            
            # AI 수 두기
            if (not self.show_menu and self.game_state == "playing" and 
                self.game_mode != "2player" and self.current_player == 2):
                pygame.time.wait(500)  # AI 생각 시간
                self.ai_move()
            
            # 화면 그리기
            if self.show_menu:
                self.draw_menu()
            else:
                self.board.draw(self.screen)
                self.draw_game_info()
                
                if self.game_state == "game_over":
                    self.draw_game_over()
            
            pygame.display.flip()
            clock.tick(60) 