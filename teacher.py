#!/usr/bin/env python3
"""
Mr. Math - The Teacher
Provides hints and encouragement to players
"""

import random

class MrMath:
    """Teacher character who provides hints and support"""
    
    def __init__(self):
        self.name = "Mr. Math"
        self.encouragements = [
            "Keep trying, you've got this! 💪",
            "Don't give up! You're doing great! 🌟",
            "Everyone makes mistakes - keep learning! 📚",
            "You're closer than you think! 🎯",
            "Learning is a journey, not a destination! 🚀"
        ]
    
    def provide_hint(self, question):
        """Provide a helpful hint based on the question"""
        q = question['question'].lower()
        
        if '+' in q and '-' not in q and '×' not in q and '÷' not in q:
            return self._hint_addition(question)
        elif '-' in q and '+' not in q and '×' not in q and '÷' not in q:
            return self._hint_subtraction(question)
        elif '×' in q or 'x' in q and 'solve' not in q:
            return self._hint_multiplication(question)
        elif '÷' in q:
            return self._hint_division(question)
        elif '(' in q and '+' in q:
            return self._hint_bodmas(question)
        elif 'solve' in q:
            return self._hint_algebra(question)
        elif 'find f' in q or "f'" in q:
            return self._hint_calculus(question)
        else:
            return "Think about what operation you need to perform!"
    
    def _hint_addition(self, question):
        """Hint for addition"""
        hints = [
            "Remember, addition means combining amounts together.",
            "Start with the first number and count up by the second number.",
            "Try breaking the numbers into tens and ones to make it easier.",
            "Use your fingers or a number line if that helps!"
        ]
        return random.choice(hints)
    
    def _hint_subtraction(self, question):
        """Hint for subtraction"""
        hints = [
            "Subtraction means taking away. Start with the larger number.",
            "Think about how many you need to add to the smaller number to reach the larger one.",
            "Count backwards from the first number by the second number.",
            "Try breaking it into tens to make it simpler."
        ]
        return random.choice(hints)
    
    def _hint_multiplication(self, question):
        """Hint for multiplication"""
        hints = [
            "Multiplication is repeated addition. Think of groups!",
            "For example: 3 × 4 means 3 groups of 4, or 4+4+4.",
            "Try building it step by step using repeated addition.",
            "Remember your times tables - they're very helpful!"
        ]
        return random.choice(hints)
    
    def _hint_division(self, question):
        """Hint for division"""
        hints = [
            "Division is about sharing equally or making groups.",
            "Think: How many times does the divisor fit into the dividend?",
            "You can use multiplication to check your answer!",
            "Try counting up in multiples of the divisor."
        ]
        return random.choice(hints)
    
    def _hint_bodmas(self, question):
        """Hint for BODMAS (Order of Operations)"""
        hints = [
            "Remember BODMAS: Brackets, Orders, Division, Multiplication, Addition, Subtraction.",
            "Do operations in Brackets first, then work left to right for Multiplication/Division.",
            "Handle operations from left to right at the same priority level.",
            "Multiplication and Division come before Addition and Subtraction."
        ]
        return random.choice(hints)
    
    def _hint_algebra(self, question):
        """Hint for algebra"""
        hints = [
            "To solve for x, get x by itself on one side of the equals sign.",
            "What operation was done to x? Do the opposite operation on both sides.",
            "If you added something to x, subtract it from both sides (and vice versa).",
            "Check your answer by substituting it back into the original equation!"
        ]
        return random.choice(hints)
    
    def _hint_calculus(self, question):
        """Hint for calculus"""
        hints = [
            "Remember the power rule: If f(x) = ax^n, then f'(x) = n·a·x^(n-1)",
            "The derivative tells us the rate of change of the function.",
            "Apply the power rule to each term separately.",
            "After finding the derivative formula, substitute in the x value given."
        ]
        return random.choice(hints)
    
    def provide_encouragement(self):
        """Provide encouragement after wrong answer"""
        print(f"\n{self.name} says: {random.choice(self.encouragements)}")
