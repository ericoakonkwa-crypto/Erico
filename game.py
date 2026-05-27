#!/usr/bin/env python3
"""
Math Quiz Game Logic
Manages game flow, question generation, and scoring
"""

from question_generator import QuestionGenerator
from teacher import MrMath
from scorer import ScoreTracker

class MathQuizGame:
    """Main game class that orchestrates the quiz"""
    
    def __init__(self):
        self.question_generator = QuestionGenerator()
        self.teacher = MrMath()
        self.scorer = ScoreTracker()
        self.current_topic = None
        self.current_difficulty = None
    
    def run(self):
        """Main game loop"""
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self.play_quiz()
            elif choice == "2":
                self.show_scores()
            elif choice == "3":
                self.show_instructions()
            elif choice == "4":
                self.quit_game()
            else:
                print("❌ Invalid choice! Please enter 1-4.")
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "-"*50)
        print("MAIN MENU")
        print("-"*50)
        print("1. Play Quiz")
        print("2. View Scores")
        print("3. Instructions")
        print("4. Quit")
    
    def play_quiz(self):
        """Start a quiz session"""
        print("\n" + "="*50)
        print("CHOOSE A TOPIC")
        print("="*50)
        
        topics = [
            "Addition",
            "Subtraction",
            "Multiplication",
            "Division",
            "BODMAS",
            "Algebra",
            "Calculus"
        ]
        
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic}")
        
        topic_choice = input("\nSelect topic (1-7): ").strip()
        
        try:
            topic_idx = int(topic_choice) - 1
            if 0 <= topic_idx < len(topics):
                self.current_topic = topics[topic_idx]
                self.select_difficulty()
            else:
                print("❌ Invalid topic selection!")
        except ValueError:
            print("❌ Please enter a number!")
    
    def select_difficulty(self):
        """Let player select difficulty level"""
        print("\n" + "-"*50)
        print(f"DIFFICULTY LEVEL - {self.current_topic}")
        print("-"*50)
        print("1. Easy (5 questions)")
        print("2. Medium (10 questions)")
        print("3. Hard (15 questions)")
        
        difficulty_choice = input("\nSelect difficulty (1-3): ").strip()
        
        difficulties = {"1": "easy", "2": "medium", "3": "hard"}
        
        if difficulty_choice in difficulties:
            self.current_difficulty = difficulties[difficulty_choice]
            self.run_quiz_session()
        else:
            print("❌ Invalid difficulty selection!")
    
    def run_quiz_session(self):
        """Run the actual quiz"""
        num_questions = {"easy": 5, "medium": 10, "hard": 15}
        questions_count = num_questions[self.current_difficulty]
        
        print(f"\n{'='*50}")
        print(f"Starting {self.current_difficulty.upper()} quiz on {self.current_topic}")
        print(f"Total Questions: {questions_count}")
        print(f"Type 'hint' to get help from Mr. Math")
        print(f"{'='*50}\n")
        
        correct_count = 0
        
        for question_num in range(1, questions_count + 1):
            question = self.question_generator.generate_question(
                self.current_topic,
                self.current_difficulty
            )
            
            print(f"Question {question_num}/{questions_count}:")
            print(f"  {question['question']}")
            
            answered_correctly = False
            attempts = 0
            max_attempts = 3
            
            while attempts < max_attempts and not answered_correctly:
                user_input = input("\nYour answer (or 'hint'): ").strip()
                
                if user_input.lower() == "hint":
                    hint = self.teacher.provide_hint(question)
                    print(f"\n💡 Mr. Math says: {hint}\n")
                    attempts += 1
                    continue
                
                try:
                    user_answer = float(user_input)
                    
                    if abs(user_answer - question['answer']) < 0.001:
                        print("✅ Correct!")
                        correct_count += 1
                        answered_correctly = True
                        self.scorer.add_points(1, self.current_difficulty)
                    else:
                        attempts += 1
                        if attempts < max_attempts:
                            remaining = max_attempts - attempts
                            print(f"❌ Incorrect. You have {remaining} attempt(s) left.")
                        else:
                            print(f"❌ Wrong! The correct answer is: {question['answer']}")
                            self.teacher.provide_encouragement()
                
                except ValueError:
                    print("❌ Please enter a valid number or 'hint'!")
                    attempts += 1
            
            print("-" * 50)
        
        self.show_quiz_summary(correct_count, questions_count)
    
    def show_quiz_summary(self, correct, total):
        """Show quiz results"""
        percentage = (correct / total) * 100
        
        print(f"\n{'='*50}")
        print("QUIZ COMPLETED!")
        print(f"{'='*50}")
        print(f"Score: {correct}/{total} ({percentage:.1f}%)")
        print(f"Topic: {self.current_topic}")
        print(f"Difficulty: {self.current_difficulty.upper()}")
        
        if percentage == 100:
            print("🌟 Perfect Score! Outstanding work!")
        elif percentage >= 80:
            print("⭐ Excellent! Great job!")
        elif percentage >= 60:
            print("👍 Good effort! Keep practicing!")
        else:
            print("💪 Don't worry! Practice makes perfect!")
        
        print(f"{'='*50}\n")
    
    def show_scores(self):
        """Display score statistics"""
        print("\n" + "="*50)
        print("YOUR SCORES")
        print("="*50)
        self.scorer.display_stats()
    
    def show_instructions(self):
        """Show game instructions"""
        print("\n" + "="*50)
        print("HOW TO PLAY")
        print("="*50)
        print("""
1. Select a math topic you want to practice
2. Choose your difficulty level:
   - Easy: 5 questions
   - Medium: 10 questions
   - Hard: 15 questions

3. Answer each question by typing your answer

4. If you're stuck, type 'hint' to get help from Mr. Math

5. You have 3 attempts per question before the answer is revealed

6. Your score is tracked based on correct answers and difficulty level

7. Topics include:
   • Addition & Subtraction
   • Multiplication & Division
   • BODMAS (Order of Operations)
   • Algebra (Solving equations)
   • Calculus (Derivatives & Integrals)
        """)
        print("="*50)
    
    def quit_game(self):
        """Exit the game"""
        print("\n" + "="*50)
        print("Thanks for playing Math Quiz Game!")
        self.scorer.display_stats()
        print("Goodbye! 👋")
        print("="*50 + "\n")
        exit()
