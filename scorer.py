#!/usr/bin/env python3
"""
Score Tracker
Tracks player scores and statistics
"""

class ScoreTracker:
    """Tracks player scores across all quiz sessions"""
    
    def __init__(self):
        self.total_questions = 0
        self.total_correct = 0
        self.easy_score = 0
        self.medium_score = 0
        self.hard_score = 0
        self.total_sessions = 0
    
    def add_points(self, points, difficulty):
        """Add points based on question and difficulty"""
        multiplier = {"easy": 1, "medium": 2, "hard": 3}
        actual_points = points * multiplier.get(difficulty, 1)
        
        self.total_correct += points
        self.total_questions += 1
        
        if difficulty == "easy":
            self.easy_score += actual_points
        elif difficulty == "medium":
            self.medium_score += actual_points
        elif difficulty == "hard":
            self.hard_score += actual_points
    
    def end_session(self):
        """Mark end of a quiz session"""
        self.total_sessions += 1
    
    def display_stats(self):
        """Display current statistics"""
        if self.total_questions == 0:
            print("\nNo quiz data yet. Play some quizzes to see your stats!")
            return
        
        accuracy = (self.total_correct / self.total_questions) * 100
        total_score = self.easy_score + self.medium_score + self.hard_score
        
        print(f"""
        Total Questions: {self.total_questions}
        Correct Answers: {self.total_correct}
        Accuracy: {accuracy:.1f}%
        
        Score Breakdown:
          Easy Questions: {self.easy_score} points
          Medium Questions: {self.medium_score} points
          Hard Questions: {self.hard_score} points
        
        TOTAL SCORE: {total_score} points
        """)
