"""Analyze trivia style and patterns"""
import re
import logging
from typing import List, Dict, Any
from collections import Counter
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

logger = logging.getLogger(__name__)


class StyleAnalyzer:
    """Analyze the style of trivia questions"""
    
    def __init__(self):
        self.style_profile = {}
        self.stop_words = set(stopwords.words('english'))
    
    def analyze_questions(self, questions: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze a collection of questions and extract style patterns"""
        if not questions:
            return {}
        
        style_profile = {
            'total_questions': len(questions),
            'avg_question_length': self._avg_length([q['question'] for q in questions]),
            'avg_answer_length': self._avg_length([q['answer'] for q in questions]),
            'difficulty_distribution': self._analyze_difficulty([q.get('difficulty', 'medium') for q in questions]),
            'question_types': self._analyze_question_types(questions),
            'categories': self._extract_categories([q.get('category', 'General') for q in questions]),
            'common_keywords': self._extract_keywords(questions),
            'question_patterns': self._analyze_patterns(questions),
            'answer_patterns': self._analyze_answer_patterns(questions),
        }
        
        self.style_profile = style_profile
        return style_profile
    
    def _avg_length(self, texts: List[str]) -> float:
        """Calculate average text length"""
        if not texts:
            return 0
        return sum(len(t.split()) for t in texts) / len(texts)
    
    def _analyze_difficulty(self, difficulties: List[str]) -> Dict[str, float]:
        """Analyze difficulty distribution"""
        counter = Counter(difficulties)
        total = len(difficulties)
        return {
            difficulty: count / total 
            for difficulty, count in counter.items()
        }
    
    def _analyze_question_types(self, questions: List[Dict[str, str]]) -> Dict[str, int]:
        """Identify question types (multiple choice, fill-in-blank, etc.)"""
        types = Counter()
        
        for q in questions:
            question_text = q['question'].lower()
            answer_text = q['answer'].lower()
            
            if 'which' in question_text or 'who' in question_text or 'what' in question_text:
                types['identification'] += 1
            if 'true' in answer_text or 'false' in answer_text:
                types['true_false'] += 1
            if '/' in q['answer'] or ' or ' in q['answer'].lower():
                types['multiple_choice'] += 1
            else:
                types['short_answer'] += 1
        
        return dict(types)
    
    def _extract_categories(self, categories: List[str]) -> Dict[str, int]:
        """Extract category distribution"""
        counter = Counter(categories)
        return dict(counter)
    
    def _extract_keywords(self, questions: List[Dict[str, str]], top_n: int = 20) -> List[tuple]:
        """Extract most common keywords from questions"""
        all_text = ' '.join([q['question'] + ' ' + q['answer'] for q in questions])
        
        # Tokenize and filter
        tokens = word_tokenize(all_text.lower())
        keywords = [t for t in tokens if t.isalnum() and t not in self.stop_words and len(t) > 3]
        
        # Get most common
        counter = Counter(keywords)
        return counter.most_common(top_n)
    
    def _analyze_patterns(self, questions: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze question patterns"""
        patterns = {
            'question_starters': Counter(),
            'avg_options': 0,
            'uses_dates': 0,
            'uses_numbers': 0,
            'uses_quotes': 0,
        }
        
        for q in questions:
            question_text = q['question']
            
            # Get first few words
            words = question_text.split()[:3]
            patterns['question_starters'][' '.join(words)] += 1
            
            # Count various elements
            if re.search(r'\d{4}|\d{1,2}/\d{1,2}', question_text):
                patterns['uses_dates'] += 1
            if re.search(r'\d+', question_text):
                patterns['uses_numbers'] += 1
            if '"' in question_text:
                patterns['uses_quotes'] += 1
        
        patterns['question_starters'] = dict(patterns['question_starters'].most_common(10))
        total = len(questions)
        patterns['uses_dates'] = patterns['uses_dates'] / total if total > 0 else 0
        patterns['uses_numbers'] = patterns['uses_numbers'] / total if total > 0 else 0
        patterns['uses_quotes'] = patterns['uses_quotes'] / total if total > 0 else 0
        
        return patterns
    
    def _analyze_answer_patterns(self, questions: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze answer patterns"""
        patterns = {
            'avg_answer_length': 0,
            'uses_multiple_options': 0,
            'uses_explanations': 0,
        }
        
        total = len(questions)
        for q in questions:
            answer = q['answer']
            patterns['avg_answer_length'] += len(answer.split())
            
            if '/' in answer or ' or ' in answer.lower():
                patterns['uses_multiple_options'] += 1
            
            if '(' in answer and ')' in answer:
                patterns['uses_explanations'] += 1
        
        patterns['avg_answer_length'] = patterns['avg_answer_length'] / total if total > 0 else 0
        patterns['uses_multiple_options'] = patterns['uses_multiple_options'] / total if total > 0 else 0
        patterns['uses_explanations'] = patterns['uses_explanations'] / total if total > 0 else 0
        
        return patterns
    
    def score_question(self, question: Dict[str, str]) -> float:
        """Score a question based on learned style using multiple factors (0-100)"""
        if not self.style_profile:
            logger.debug("No style profile - returning neutral score of 50.0")
            return 50.0
        
        scores = {}
        question_text = question.get('question', '')
        answer_text = question.get('answer', '')
        
        if not question_text or not answer_text:
            logger.debug("Empty question or answer text")
            return 0.0
        
        # ============ LENGTH SIMILARITY (20 points max) ============
        avg_q_len = self.style_profile.get('avg_question_length', 50)
        avg_a_len = self.style_profile.get('avg_answer_length', 5)
        
        q_len = len(question_text.split())
        a_len = len(answer_text.split())
        
        # Question length: prefer within 50% of average
        q_len_diff = abs(q_len - avg_q_len)
        q_len_score = 10.0 * max(0, 1 - (q_len_diff / max(avg_q_len, 1)))
        scores['question_length'] = q_len_score
        
        # Answer length: prefer within 50% of average  
        a_len_diff = abs(a_len - avg_a_len)
        a_len_score = 10.0 * max(0, 1 - (a_len_diff / max(avg_a_len, 1)))
        scores['answer_length'] = a_len_score
        
        # ============ DIFFICULTY MATCH (15 points max) ============
        difficulty_dist = self.style_profile.get('difficulty_distribution', {})
        q_difficulty = question.get('difficulty', 'medium').lower()
        
        if q_difficulty in difficulty_dist:
            difficulty_prob = difficulty_dist[q_difficulty]
            # Score higher if difficulty is common in profile
            difficulty_score = 15.0 * min(difficulty_prob * 2, 1.0)
        else:
            difficulty_score = 5.0  # Small penalty for unknown difficulty
        scores['difficulty'] = difficulty_score
        
        # ============ QUESTION PATTERN MATCH (15 points max) ============
        patterns = self.style_profile.get('question_patterns', {})
        pattern_score = 0.0
        
        # Check question starters
        starters = patterns.get('question_starters', {})
        if starters:
            q_lower = question_text.lower()
            for starter in starters.keys():
                if q_lower.startswith(starter.lower()):
                    pattern_score += 5.0
                    break
        
        # Check for date usage
        if patterns.get('uses_dates', 0) > 0.3:  # If 30%+ of questions have dates
            if re.search(r'\d{4}|\d{1,2}/\d{1,2}', question_text):
                pattern_score += 5.0
        
        # Check for number usage
        if patterns.get('uses_numbers', 0) > 0.5:  # If 50%+ of questions have numbers
            if re.search(r'\d+', question_text):
                pattern_score += 5.0
        
        scores['patterns'] = min(pattern_score, 15.0)
        
        # ============ CONTENT/KEYWORD RELEVANCE (20 points max) ============
        keywords = self.style_profile.get('common_keywords', [])
        if keywords:
            # Extract top meaningful keywords (filter out very common words)
            meaningful_keywords = [k[0].lower() for k in keywords[:20] if len(k[0]) > 4 and k[1] > 5]
            
            q_lower = question_text.lower()
            a_lower = answer_text.lower()
            
            keyword_matches = sum(1 for k in meaningful_keywords if k in q_lower or k in a_lower)
            keyword_score = 20.0 * (keyword_matches / max(len(meaningful_keywords), 1))
        else:
            keyword_score = 10.0  # Default if no keywords
        
        scores['keywords'] = min(keyword_score, 20.0)
        
        # ============ ANSWER PATTERN MATCH (15 points max) ============
        answer_patterns = self.style_profile.get('answer_patterns', {})
        answer_pattern_score = 0.0
        
        # Check if answers have multiple options
        if answer_patterns.get('uses_multiple_options', 0) > 0.3:
            if '/' in answer_text or ' or ' in answer_text.lower():
                answer_pattern_score += 7.5
        
        # Check if answers have explanations
        if answer_patterns.get('uses_explanations', 0) > 0.2:
            if '(' in answer_text and ')' in answer_text:
                answer_pattern_score += 7.5
        
        scores['answer_pattern'] = answer_pattern_score
        
        # ============ CATEGORY MATCH (15 points max) ============
        profile_categories = self.style_profile.get('categories', {})
        q_category = question.get('category', 'General')
        
        if profile_categories and q_category in profile_categories:
            category_score = 15.0
        else:
            category_score = 5.0  # Small score for uncategorized or different category
        
        scores['category'] = category_score
        
        # Calculate total
        total_score = sum(scores.values())
        final_score = min(max(total_score, 0), 100)
        
        logger.debug(f"Question scoring: len_q={q_len_score:.1f}, len_a={a_len_score:.1f}, "
                    f"difficulty={difficulty_score:.1f}, patterns={scores['patterns']:.1f}, "
                    f"keywords={scores['keywords']:.1f}, ans_pattern={answer_pattern_score:.1f}, "
                    f"category={category_score:.1f} => TOTAL: {final_score:.1f}")
        
        return final_score
