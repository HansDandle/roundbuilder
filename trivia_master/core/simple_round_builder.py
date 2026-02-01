"""Simple random round builder with filtering"""
import logging
import random
from typing import List, Dict, Any
import pandas as pd

logger = logging.getLogger(__name__)


class SimpleRoundBuilder:
    """Build trivia rounds with simple filtering"""
    
    def load_csv(self, filepath: str) -> List[Dict[str, str]]:
        """Load CSV and return questions"""
        try:
            logger.info(f"Loading CSV from: {filepath}")
            df = pd.read_csv(filepath)
            
            # Normalize column names to lowercase
            df.columns = df.columns.str.lower()
            logger.info(f"Columns found: {df.columns.tolist()}")
            
            questions = []
            for _, row in df.iterrows():
                question_text = str(row.get('question', '')).strip()
                answer_text = str(row.get('answer', '')).strip()
                
                if not question_text or not answer_text:
                    continue
                
                questions.append({
                    'question': question_text,
                    'answer': answer_text,
                    'category': str(row.get('category', 'General')).strip(),
                    'difficulty': str(row.get('difficulty', 'medium')).strip(),
                })
            
            logger.info(f"Loaded {len(questions)} questions")
            return questions
        except Exception as e:
            logger.error(f"Error loading CSV: {e}", exc_info=True)
            return []
    
    def get_categories(self, questions: List[Dict[str, str]]) -> List[str]:
        """Get unique categories"""
        categories = set()
        for q in questions:
            if q.get('category'):
                categories.add(q['category'])
        return sorted(list(categories))
    
    def get_difficulties(self, questions: List[Dict[str, str]]) -> List[str]:
        """Get unique difficulties"""
        difficulties = set()
        for q in questions:
            if q.get('difficulty'):
                difficulties.add(q['difficulty'])
        return sorted(list(difficulties))
    
    def filter_questions(self,
                        questions: List[Dict[str, str]],
                        category: str = None,
                        difficulty: str = None,
                        keyword: str = None) -> List[Dict[str, str]]:
        """Filter questions by category, difficulty, and/or keyword"""
        filtered = questions
        
        # Category filter
        if category and category != "All Categories":
            filtered = [q for q in filtered if q.get('category', '').lower() == category.lower()]
            logger.info(f"After category filter '{category}': {len(filtered)} questions")
        
        # Difficulty filter
        if difficulty and difficulty != "All Difficulties":
            filtered = [q for q in filtered if q.get('difficulty', '').lower() == difficulty.lower()]
            logger.info(f"After difficulty filter '{difficulty}': {len(filtered)} questions")
        
        # Keyword filter
        if keyword and keyword.strip():
            keyword_lower = keyword.lower()
            filtered = [q for q in filtered 
                       if keyword_lower in q['question'].lower() or keyword_lower in q['answer'].lower()]
            logger.info(f"After keyword filter '{keyword}': {len(filtered)} questions")
        
        return filtered
    
    def build_round(self,
                   questions: List[Dict[str, str]],
                   round_name: str = "Random Round",
                   round_size: int = 10,
                   category: str = None,
                   difficulty: str = None,
                   keyword: str = None) -> Dict[str, Any]:
        """Build a round by randomly selecting from filtered questions"""
        
        logger.info(f"Building round: {round_name}, size: {round_size}")
        
        # Filter questions
        filtered = self.filter_questions(questions, category, difficulty, keyword)
        
        if not filtered:
            logger.warning("No questions matched filters")
            return {
                'name': round_name,
                'questions': [],
                'question_count': 0,
                'categories': [],
                'error': 'No questions match your filters'
            }
        
        # Randomly select from filtered questions
        selected = random.sample(filtered, min(round_size, len(filtered)))
        
        # Get categories in this round
        categories = sorted(list(set(q.get('category', 'Unknown') for q in selected)))
        
        logger.info(f"Selected {len(selected)} random questions from {len(filtered)} filtered")
        
        return {
            'name': round_name,
            'questions': selected,
            'question_count': len(selected),
            'categories': categories,
        }
