"""Parse DOCX files containing trivia rounds"""
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from docx import Document
import re


class TriviaRound:
    """Represents a single trivia round"""
    
    def __init__(self, name: str, questions: List[Dict[str, str]], metadata: Dict[str, Any] = None):
        self.name = name
        self.questions = questions
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert round to dictionary"""
        return {
            'name': self.name,
            'questions': self.questions,
            'metadata': self.metadata,
            'question_count': len(self.questions)
        }


class DocxParser:
    """Parse DOCX files to extract trivia questions"""
    
    def __init__(self):
        self.rounds = []
    
    def parse_file(self, filepath: str) -> Optional[TriviaRound]:
        """Parse a single DOCX file and extract questions"""
        try:
            doc = Document(filepath)
            questions = self._extract_questions(doc)
            round_name = Path(filepath).stem
            
            round_obj = TriviaRound(round_name, questions)
            self.rounds.append(round_obj)
            return round_obj
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None
    
    def parse_directory(self, directory: str) -> List[TriviaRound]:
        """Parse all DOCX files in a directory"""
        docx_files = Path(directory).glob("*.docx")
        parsed_rounds = []
        
        for docx_file in docx_files:
            round_obj = self.parse_file(str(docx_file))
            if round_obj:
                parsed_rounds.append(round_obj)
        
        return parsed_rounds
    
    def _extract_questions(self, doc: Document) -> List[Dict[str, str]]:
        """Extract questions from DOCX document"""
        questions = []
        current_question = None
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            
            # Look for question patterns (usually starts with number or Q:)
            if self._is_question_start(text):
                if current_question:
                    questions.append(current_question)
                current_question = {
                    'question': text,
                    'answer': '',
                    'category': '',
                    'difficulty': 'medium',
                    'type': 'multiple_choice'
                }
            elif current_question and self._is_answer_start(text):
                current_question['answer'] = text
            elif current_question:
                # Accumulate additional content
                if current_question['answer']:
                    current_question['answer'] += '\n' + text
                else:
                    current_question['question'] += '\n' + text
        
        # Add the last question
        if current_question:
            questions.append(current_question)
        
        return questions
    
    def _is_question_start(self, text: str) -> bool:
        """Detect if text is the start of a question"""
        # Look for patterns like "1.", "Q:", "Question:", etc.
        patterns = [
            r'^\d+\.',
            r'^[A-Z]\.',
            r'^Q:',
            r'^Question:',
        ]
        return any(re.match(pattern, text) for pattern in patterns)
    
    def _is_answer_start(self, text: str) -> bool:
        """Detect if text is the start of an answer"""
        patterns = [
            r'^A:',
            r'^Answer:',
            r'^ANSWER:',
        ]
        return any(re.match(pattern, text) for pattern in patterns)
    
    def get_all_questions(self) -> List[Dict[str, str]]:
        """Get all questions from all parsed rounds"""
        all_questions = []
        for round_obj in self.rounds:
            all_questions.extend(round_obj.questions)
        return all_questions
