#!/usr/bin/env python3
"""
Question Generator
Generates math questions based on topic and difficulty
"""

import random
import math

class QuestionGenerator:
    """Generates math questions for different topics and difficulties"""
    
    def generate_question(self, topic, difficulty):
        """Generate a question based on topic and difficulty"""
        topic_lower = topic.lower()
        
        if topic_lower == "addition":
            return self._generate_addition(difficulty)
        elif topic_lower == "subtraction":
            return self._generate_subtraction(difficulty)
        elif topic_lower == "multiplication":
            return self._generate_multiplication(difficulty)
        elif topic_lower == "division":
            return self._generate_division(difficulty)
        elif topic_lower == "bodmas":
            return self._generate_bodmas(difficulty)
        elif topic_lower == "algebra":
            return self._generate_algebra(difficulty)
        elif topic_lower == "calculus":
            return self._generate_calculus(difficulty)
        else:
            return self._generate_addition(difficulty)
    
    def _generate_addition(self, difficulty):
        """Generate addition questions"""
        if difficulty == "easy":
            a, b = random.randint(1, 20), random.randint(1, 20)
        elif difficulty == "medium":
            a, b = random.randint(1, 100), random.randint(1, 100)
        else:  # hard
            a, b = random.randint(1, 1000), random.randint(1, 1000)
        
        return {
            "question": f"{a} + {b} = ?",
            "answer": a + b
        }
    
    def _generate_subtraction(self, difficulty):
        """Generate subtraction questions"""
        if difficulty == "easy":
            a, b = random.randint(1, 20), random.randint(1, 20)
            a, b = max(a, b), min(a, b)  # Ensure a > b for positive result
        elif difficulty == "medium":
            a, b = random.randint(1, 100), random.randint(1, 100)
            a, b = max(a, b), min(a, b)
        else:  # hard
            a, b = random.randint(1, 1000), random.randint(1, 1000)
            a, b = max(a, b), min(a, b)
        
        return {
            "question": f"{a} - {b} = ?",
            "answer": a - b
        }
    
    def _generate_multiplication(self, difficulty):
        """Generate multiplication questions"""
        if difficulty == "easy":
            a, b = random.randint(1, 12), random.randint(1, 12)
        elif difficulty == "medium":
            a, b = random.randint(1, 50), random.randint(1, 50)
        else:  # hard
            a, b = random.randint(10, 99), random.randint(10, 99)
        
        return {
            "question": f"{a} × {b} = ?",
            "answer": a * b
        }
    
    def _generate_division(self, difficulty):
        """Generate division questions"""
        if difficulty == "easy":
            divisor = random.randint(2, 12)
            quotient = random.randint(1, 12)
            dividend = divisor * quotient
        elif difficulty == "medium":
            divisor = random.randint(2, 50)
            quotient = random.randint(1, 20)
            dividend = divisor * quotient
        else:  # hard
            divisor = random.randint(10, 99)
            quotient = random.randint(5, 50)
            dividend = divisor * quotient
        
        return {
            "question": f"{dividend} ÷ {divisor} = ?",
            "answer": dividend / divisor
        }
    
    def _generate_bodmas(self, difficulty):
        """Generate BODMAS (Order of Operations) questions"""
        if difficulty == "easy":
            # a + b * c
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            c = random.randint(1, 10)
            answer = a + (b * c)
            question = f"{a} + {b} × {c} = ?"
        elif difficulty == "medium":
            # (a + b) * c - d
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            c = random.randint(1, 10)
            d = random.randint(1, 50)
            answer = ((a + b) * c) - d
            question = f"({a} + {b}) × {c} - {d} = ?"
        else:  # hard
            # a * b + c / d - e
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            c = random.randint(10, 100)
            d = random.randint(2, 10)
            e = random.randint(1, 20)
            # Ensure division works
            c = c - (c % d)  # Make c divisible by d
            answer = (a * b) + (c // d) - e
            question = f"{a} × {b} + {c} ÷ {d} - {e} = ?"
        
        return {
            "question": question,
            "answer": answer
        }
    
    def _generate_algebra(self, difficulty):
        """Generate algebra questions (solving for x)"""
        if difficulty == "easy":
            # x + a = b, solve for x
            a = random.randint(1, 20)
            x = random.randint(1, 20)
            b = a + x
            answer = x
            question = f"Solve for x: x + {a} = {b}"
        elif difficulty == "medium":
            # ax + b = c, solve for x
            a = random.randint(2, 10)
            b = random.randint(1, 20)
            x = random.randint(1, 10)
            c = (a * x) + b
            answer = x
            question = f"Solve for x: {a}x + {b} = {c}"
        else:  # hard
            # ax + b = cx + d
            a = random.randint(2, 5)
            b = random.randint(5, 20)
            c = random.randint(2, 5)
            while c == a:
                c = random.randint(2, 5)
            x = random.randint(5, 15)
            left = (a * x) + b
            d = (c * x)
            answer = x
            question = f"Solve for x: {a}x + {b} = {c}x + {d}"
        
        return {
            "question": question,
            "answer": answer
        }
    
    def _generate_calculus(self, difficulty):
        """Generate calculus questions (derivatives)"""
        if difficulty == "easy":
            # Derivative of ax^2 at a point
            # f(x) = ax^2, f'(x) = 2ax
            a = random.randint(1, 5)
            x = random.randint(1, 5)
            answer = 2 * a * x
            question = f"Find f'({x}) if f(x) = {a}x²"
        elif difficulty == "medium":
            # Derivative of ax^3 + bx at a point
            # f(x) = ax^3 + bx, f'(x) = 3ax^2 + b
            a = random.randint(1, 3)
            b = random.randint(1, 10)
            x = random.randint(1, 5)
            answer = (3 * a * (x ** 2)) + b
            question = f"Find f'({x}) if f(x) = {a}x³ + {b}x"
        else:  # hard
            # Derivative of ax^n at a point
            # f(x) = ax^4 + bx^2 + c, f'(x) = 4ax^3 + 2bx
            a = random.randint(1, 2)
            b = random.randint(1, 5)
            x = random.randint(1, 3)
            answer = (4 * a * (x ** 3)) + (2 * b * x)
            question = f"Find f'({x}) if f(x) = {a}x⁴ + {b}x²"
        
        return {
            "question": question,
            "answer": answer
        }
