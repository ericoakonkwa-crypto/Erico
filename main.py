#!/usr/bin/env python3
"""
Math Quiz Game - Main Entry Point
A fun and interactive math quiz game with Mr. Math as your teacher!
"""

from game import MathQuizGame

def main():
    """Main function to run the Math Quiz Game"""
    print("\n" + "="*50)
    print("  WELCOME TO THE MATH QUIZ GAME!  🎓")
    print("="*50)
    print("\nYour teacher Mr. Math is here to help!\n")
    
    game = MathQuizGame()
    game.run()

if __name__ == "__main__":
    main()
