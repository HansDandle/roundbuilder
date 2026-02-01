"""Generate trivia rounds from matched questions"""
from typing import List, Dict, Any
import logging
import random
from .question_matcher import QuestionMatcher

logger = logging.getLogger(__name__)


class RoundGenerator:
    """Generate complete trivia rounds"""
    
    def __init__(self, matcher: QuestionMatcher):
        self.matcher = matcher
    
    def generate_round(self,
                       questions: List[Dict[str, str]],
                       round_name: str = "Custom Round",
                       round_size: int = 10,
                       category: str = None) -> Dict[str, Any]:
        """Generate a round of matched questions"""
        
        logger.info(f"Generating round: {round_name}, size: {round_size}, category: {category}")
        logger.info(f"Total questions available: {len(questions)}")
        
        # Find matching questions
        matched = self.matcher.find_matching_questions(
            questions,
            category=category,
            limit=round_size * 2  # Get more to choose from
        )
        
        logger.info(f"Matched questions found: {len(matched)}")
        
        if not matched:
            logger.warning(f"No matching questions found for category: {category}")
            return {
                'name': round_name,
                'questions': [],
                'error': 'No matching questions found'
            }
        
        # Select diverse questions
        selected = self._select_diverse_questions([q[0] for q in matched], round_size)
        logger.info(f"Selected {len(selected)} diverse questions")
        
        return {
            'name': round_name,
            'questions': selected,
            'question_count': len(selected),
            'categories': self._get_categories(selected),
            'difficulty_distribution': self._get_difficulty_distribution(selected)
        }
    
    def _select_diverse_questions(self, 
                                   questions: List[Dict[str, str]], 
                                   count: int) -> List[Dict[str, str]]:
        """Select diverse questions (avoid too many from same category)"""
        if len(questions) <= count:
            return questions
        
        selected = []
        category_counts = {}
        
        # Sort to get good coverage
        random.shuffle(questions)
        
        for question in questions:
            if len(selected) >= count:
                break
            
            category = question.get('category', 'General')
            current_count = category_counts.get(category, 0)
            
            # Allow some category overlap but limit it
            max_per_category = max(2, count // 4)
            if current_count < max_per_category or len(selected) < count // 2:
                selected.append(question)
                category_counts[category] = current_count + 1
        
        return selected[:count]
    
    def _get_categories(self, questions: List[Dict[str, str]]) -> List[str]:
        """Get unique categories from questions"""
        categories = set()
        for q in questions:
            if q.get('category'):
                categories.add(q['category'])
        return sorted(list(categories))
    
    def _get_difficulty_distribution(self, questions: List[Dict[str, str]]) -> Dict[str, int]:
        """Get difficulty distribution"""
        distribution = {}
        for q in questions:
            difficulty = q.get('difficulty', 'medium')
            distribution[difficulty] = distribution.get(difficulty, 0) + 1
        return distribution
    
    def generate_themed_round(self,
                             questions: List[Dict[str, str]],
                             theme: str,
                             round_size: int = 10) -> Dict[str, Any]:
        """Generate a themed round"""
        # Filter questions that mention theme
        themed_questions = [
            q for q in questions 
            if theme.lower() in q['question'].lower() or 
               theme.lower() in q['answer'].lower()
        ]
        
        # Score remaining questions
        scored = []
        for q in themed_questions:
            score = self.matcher.analyzer.score_question(q)
            scored.append((q, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        selected = [q[0] for q in scored[:round_size]]
        
        return {
            'name': f"{theme} Round",
            'theme': theme,
            'questions': selected,
            'question_count': len(selected),
            'categories': self._get_categories(selected)
        }
