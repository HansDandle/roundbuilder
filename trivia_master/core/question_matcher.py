"""Match questions from external sources to learned style"""
from typing import List, Dict, Any
import logging
import pandas as pd
from .style_analyzer import StyleAnalyzer

logger = logging.getLogger(__name__)


class QuestionMatcher:
    """Match questions to learned style patterns"""
    
    def __init__(self, style_analyzer: StyleAnalyzer):
        self.analyzer = style_analyzer
        self.threshold = 40.0  # Minimum score to match (lowered from 60 to allow more matches)
    
    def load_questions_from_csv(self, filepath: str) -> List[Dict[str, str]]:
        """Load questions from CSV file"""
        try:
            logger.info(f"Loading CSV from: {filepath}")
            df = pd.read_csv(filepath)
            logger.info(f"CSV loaded with {len(df)} rows")
            logger.info(f"Columns: {df.columns.tolist()}")
            
            # Normalize column names to lowercase for consistency
            df.columns = df.columns.str.lower()
            questions = []
            
            for _, row in df.iterrows():
                question_text = str(row.get('question', '')).strip()
                answer_text = str(row.get('answer', '')).strip()
                
                if not question_text or not answer_text:
                    logger.debug(f"Skipping empty question/answer: q={bool(question_text)}, a={bool(answer_text)}")
                    continue
                
                question_dict = {
                    'question': question_text,
                    'answer': answer_text,
                    'category': str(row.get('category', 'General')).strip(),
                    'difficulty': str(row.get('difficulty', 'medium')).strip(),
                    'type': str(row.get('type', 'multiple_choice')).strip(),
                }
                questions.append(question_dict)
            
            logger.info(f"Loaded {len(questions)} valid questions from CSV")
            return questions
        except Exception as e:
            logger.error(f"Error loading CSV: {e}", exc_info=True)
            return []
    
    def find_matching_questions(self, 
                               questions: List[Dict[str, str]], 
                               category: str = None,
                               limit: int = 10) -> List[tuple]:
        """Find questions matching the learned style
        
        Returns list of (question_dict, score) tuples sorted by score
        If no style profile exists, returns random questions.
        """
        import random
        
        logger.info(f"Finding matching questions: category={category}, limit={limit}")
        logger.info(f"Style profile exists: {bool(self.analyzer.style_profile)}")
        logger.info(f"Threshold: {self.threshold}")
        
        # If no style profile, return random questions (no scoring)
        if not self.analyzer.style_profile:
            logger.info("No style profile found - using random selection instead of scoring")
            
            # Filter by category if specified
            filtered = questions
            if category:
                filtered = [q for q in questions 
                           if q.get('category', '').lower() == category.lower()]
                logger.info(f"Category filter '{category}': {len(filtered)} questions matched")
            
            # Random selection
            if len(filtered) <= limit:
                selected = filtered
            else:
                selected = random.sample(filtered, limit)
            
            logger.info(f"Returning {len(selected)} random questions")
            return [(q, 50.0) for q in selected]  # Return with neutral score
        
        # Normal scoring-based matching
        scored_questions = []
        category_count = 0
        threshold_count = 0
        
        for question in questions:
            # Category filter
            if category:
                q_category = question.get('category', '').lower()
                if q_category != category.lower():
                    continue
                category_count += 1
            
            # Score the question
            score = self.analyzer.score_question(question)
            
            if score >= self.threshold:
                threshold_count += 1
                scored_questions.append((question, score))
        
        # Log filtering results
        if category:
            logger.info(f"Category filter '{category}': {category_count} questions matched category")
        logger.info(f"Threshold filter: {threshold_count} questions scored >= {self.threshold}")
        
        # Sort by score descending
        scored_questions.sort(key=lambda x: x[1], reverse=True)
        logger.info(f"Returning top {min(limit, len(scored_questions))} of {len(scored_questions)} scored questions")
        
        return scored_questions[:limit]
    
    def set_threshold(self, threshold: float):
        """Set minimum score threshold for matching"""
        self.threshold = max(0, min(threshold, 100))
    
    def batch_score_questions(self, questions: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Score all questions and return with scores"""
        results = []
        for question in questions:
            score = self.analyzer.score_question(question)
            results.append({
                'question': question['question'],
                'answer': question['answer'],
                'category': question.get('category', 'Unknown'),
                'score': score,
                'matches_style': score >= self.threshold
            })
        
        return sorted(results, key=lambda x: x['score'], reverse=True)
