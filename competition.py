#!/usr/bin/env python3
"""
Competition System for Math Quiz Game
Manages competitions and sends report cards to winners on December 1st
"""

import json
import os
from datetime import datetime


class Competition:
    """Manages math quiz competitions and winner selection"""
    
    COMPETITION_DATE = datetime(2026, 12, 1)
    COMPETITIONS_FILE = "competitions.json"
    
    def __init__(self):
        self.participants = {}
        self.load_competitions()
    
    def load_competitions(self):
        """Load existing competition data"""
        if os.path.exists(self.COMPETITIONS_FILE):
            with open(self.COMPETITIONS_FILE, 'r') as f:
                self.participants = json.load(f)
    
    def save_competitions(self):
        """Save competition data"""
        with open(self.COMPETITIONS_FILE, 'w') as f:
            json.dump(self.participants, f, indent=2)
    
    def register_participant(self, username, email):
        """Register a participant for the competition"""
        if username not in self.participants:
            self.participants[username] = {
                "email": email,
                "scores": [],
                "total_score": 0,
                "report_card_sent": False
            }
            self.save_competitions()
            return True
        return False
    
    def add_score(self, username, topic, difficulty, score, total_questions):
        """Add a score for a participant"""
        if username in self.participants:
            self.participants[username]["scores"].append({
                "topic": topic,
                "difficulty": difficulty,
                "score": score,
                "total_questions": total_questions,
                "percentage": (score / total_questions) * 100
            })
            self._update_total_score(username)
            self.save_competitions()
    
    def _update_total_score(self, username):
        """Update total score with difficulty multipliers"""
        scores = self.participants[username]["scores"]
        difficulty_mult = {"easy": 1, "medium": 2, "hard": 3}
        total = 0
        for s in scores:
            mult = difficulty_mult.get(s["difficulty"], 1)
            total += s["score"] * mult
        self.participants[username]["total_score"] = total
    
    def get_leaderboard(self, limit=10):
        """Get top performers"""
        sorted_p = sorted(
            self.participants.items(),
            key=lambda x: x[1]["total_score"],
            reverse=True
        )
        return sorted_p[:limit]
    
    def get_winners(self):
        """Get top 10 winners"""
        return self.get_leaderboard(10)
    
    def is_competition_day(self):
        """Check if today is December 1st"""
        today = datetime.now()
        return today.month == 12 and today.day == 1
    
    def generate_report_cards(self):
        """Generate and send report cards to winners on Dec 1st"""
        if not self.is_competition_day():
            return []
        
        cards = []
        for rank, (username, data) in enumerate(self.get_winners(), 1):
            card = self._create_report_card(username, data, rank)
            cards.append(card)
            self.participants[username]["report_card_sent"] = True
        
        self.save_competitions()
        return cards
    
    def _create_report_card(self, username, participant_data, rank):
        """Create a report card for a winner"""
        scores = participant_data["scores"]
        avg_accuracy = sum(s["percentage"] for s in scores) / len(scores) if scores else 0
        
        status_map = {
            1: "GOLD WINNER - 1st Place",
            2: "SILVER WINNER - 2nd Place",
            3: "BRONZE WINNER - 3rd Place"
        }
        status = status_map.get(rank, f"WINNER - Top {rank}" if rank <= 10 else "Participant")
        
        return {
            "rank": rank,
            "username": username,
            "email": participant_data["email"],
            "total_score": participant_data["total_score"],
            "quizzes_completed": len(scores),
            "average_accuracy": round(avg_accuracy, 2),
            "status": status,
            "generated_date": datetime.now().isoformat(),
            "competition_date": "2026-12-01"
        }


class ReportCard:
    """Generates and manages report cards for winners"""
    
    def __init__(self):
        self.report_cards_dir = "report_cards"
        if not os.path.exists(self.report_cards_dir):
            os.makedirs(self.report_cards_dir)
    
    def save_report_card(self, report_card_data):
        """Save report card as JSON"""
        username = report_card_data["username"]
        filename = f"{self.report_cards_dir}/{username}_report_card_dec_2026.json"
        
        with open(filename, 'w') as f:
            json.dump(report_card_data, f, indent=2)
        
        return filename
    
    def generate_html_report_card(self, report_card_data):
        """Generate beautiful HTML report card"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Report Card - {report_card_data['username']}</title>
    <style>
        body {{ font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
        .card {{ background: white; border-radius: 15px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); max-width: 800px; padding: 40px; }}
        .header {{ text-align: center; border-bottom: 3px solid #667eea; padding-bottom: 20px; margin-bottom: 30px; }}
        .title {{ font-size: 28px; color: #333; margin: 0; }}
        .badge {{ font-size: 24px; font-weight: bold; color: #667eea; text-align: center; margin: 20px 0; }}
        .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0; }}
        .stat {{ background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea; }}
        .label {{ font-size: 12px; color: #999; text-transform: uppercase; margin-bottom: 5px; }}
        .value {{ font-size: 24px; font-weight: bold; color: #333; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h1 class="title">🏆 Math Quiz Competition Report Card</h1>
            <p>December 1st, 2026</p>
        </div>
        
        <div style="text-align: center; margin: 20px 0; padding: 15px; background: #f0f4ff; border-radius: 8px;">
            <div style="font-weight: bold; color: #667eea; font-size: 16px;">{report_card_data['username']}</div>
            <div style="color: #999; font-size: 12px;">{report_card_data['email']}</div>
        </div>
        
        <div class="badge">{report_card_data['status']}</div>
        
        <div class="stats">
            <div class="stat">
                <div class="label">Ranking</div>
                <div class="value">#{report_card_data['rank']}</div>
            </div>
            <div class="stat">
                <div class="label">Total Score</div>
                <div class="value">{report_card_data['total_score']}</div>
            </div>
            <div class="stat">
                <div class="label">Quizzes</div>
                <div class="value">{report_card_data['quizzes_completed']}</div>
            </div>
            <div class="stat">
                <div class="label">Accuracy</div>
                <div class="value">{report_card_data['average_accuracy']}%</div>
            </div>
        </div>
        
        <div class="footer">
            <p>🎓 Congratulations on being a winner!</p>
            <p>This report card has been sent to {report_card_data['email']}</p>
            <p>Generated: {report_card_data['generated_date']}</p>
        </div>
    </div>
</body>
</html>
"""
    
    def save_html_report_card(self, report_card_data):
        """Save HTML report card"""
        username = report_card_data["username"]
        html = self.generate_html_report_card(report_card_data)
        filename = f"{self.report_cards_dir}/{username}_report_card_dec_2026.html"
        
        with open(filename, 'w') as f:
            f.write(html)
        
        return filename
    
    def send_report_card(self, email, report_card_data):
        """Send report card to winner's email"""
        print(f"\n{'='*50}")
        print(f"📧 REPORT CARD EMAIL NOTIFICATION")
        print(f"{'='*50}")
        print(f"To: {email}")
        print(f"Subject: 🏆 Your Math Quiz Competition Report Card - {report_card_data['status']}")
        print(f"\nDear {report_card_data['username']},")
        print(f"\nCongratulations! You are a WINNER in the Math Quiz Competition!")
        print(f"\n✅ Ranking: #{report_card_data['rank']}")
        print(f"✅ Status: {report_card_data['status']}")
        print(f"✅ Total Score: {report_card_data['total_score']} points")
        print(f"✅ Average Accuracy: {report_card_data['average_accuracy']}%")
        print(f"✅ Quizzes Completed: {report_card_data['quizzes_completed']}")
        print(f"\nYour detailed report card has been attached and saved to your account.")
        print(f"\nBest regards,")
        print(f"Mr. Math & The Math Quiz Team")
        print(f"{'='*50}\n")
        return True
