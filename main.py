#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 오목 게임
Python과 Pygame을 사용한 3D 효과가 있는 오목 게임
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import Game

def main():
    """메인 함수"""
    print("3D 오목 게임을 시작합니다...")
    print("게임 로딩 중...")
    
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n게임이 중단되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        print("게임을 종료합니다.")
    finally:
        print("게임을 종료합니다.")

if __name__ == "__main__":
    main() 