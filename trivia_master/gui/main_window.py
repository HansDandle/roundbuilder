"""Simplified TriviaMaster GUI - Random Round Builder"""
import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QFileDialog,
    QListWidget, QListWidgetItem, QSpinBox, QComboBox,
    QStatusBar, QMessageBox, QTextEdit, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..core.simple_round_builder import SimpleRoundBuilder
from ..utils.docx_exporter import DocxExporter
from ..config import OUTPUT_DIR

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TriviaMaster - Random Round Builder")
        self.setGeometry(100, 100, 1000, 800)
        
        # Initialize components
        self.builder = SimpleRoundBuilder()
        self.exporter = DocxExporter()
        self.exporter.set_output_directory(str(OUTPUT_DIR))
        
        self.current_questions = []
        self.current_round = None
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # ============ CSV SELECTION SECTION ============
        csv_section = self.create_csv_section()
        main_layout.addWidget(QLabel("Step 1: Load Questions"))
        main_layout.addLayout(csv_section)
        
        # ============ FILTERING SECTION ============
        filter_section = self.create_filter_section()
        main_layout.addWidget(QLabel("Step 2: Filter & Generate"))
        main_layout.addLayout(filter_section)
        
        # ============ RESULTS SECTION ============
        main_layout.addWidget(QLabel("Step 3: Review Round"))
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        main_layout.addWidget(self.results_text)
        
        # ============ EXPORT BUTTON ============
        export_btn = QPushButton("Export Round to DOCX")
        export_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        export_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        export_btn.clicked.connect(self.export_round)
        main_layout.addWidget(export_btn)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready - Load a CSV file to start")
    
    def create_csv_section(self) -> QHBoxLayout:
        """Create CSV file selection section"""
        layout = QHBoxLayout()
        
        self.csv_path = QLineEdit()
        self.csv_path.setReadOnly(True)
        self.csv_path.setPlaceholderText("Select your CSV file with trivia questions...")
        layout.addWidget(self.csv_path)
        
        browse_btn = QPushButton("Browse CSV")
        browse_btn.clicked.connect(self.browse_csv)
        layout.addWidget(browse_btn)
        
        load_btn = QPushButton("Load")
        load_btn.clicked.connect(self.load_csv)
        layout.addWidget(load_btn)
        
        return layout
    
    def create_filter_section(self) -> QVBoxLayout:
        """Create filtering section"""
        layout = QVBoxLayout()
        
        # Filters form
        form = QFormLayout()
        
        # Category filter
        self.category_combo = QComboBox()
        self.category_combo.addItem("All Categories")
        form.addRow("Category:", self.category_combo)
        
        # Difficulty filter
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItem("All Difficulties")
        form.addRow("Difficulty:", self.difficulty_combo)
        
        # Keyword search
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Optional: search for keyword in question or answer")
        form.addRow("Keyword Search:", self.keyword_input)
        
        # Round size
        self.round_size_spin = QSpinBox()
        self.round_size_spin.setRange(1, 100)
        self.round_size_spin.setValue(10)
        form.addRow("Number of Questions:", self.round_size_spin)
        
        # Round name
        self.round_name_input = QLineEdit("My Random Round")
        form.addRow("Round Name:", self.round_name_input)
        
        layout.addLayout(form)
        
        # Generate button
        gen_btn = QPushButton("Generate Random Round")
        gen_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        gen_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        gen_btn.clicked.connect(self.generate_round)
        layout.addWidget(gen_btn)
        
        return layout
    
    def browse_csv(self):
        """Browse for CSV file"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if filepath:
            self.csv_path.setText(filepath)
    
    def load_csv(self):
        """Load CSV file"""
        if not self.csv_path.text():
            QMessageBox.warning(self, "Error", "Please select a CSV file first")
            return
        
        logger.info(f"Loading CSV: {self.csv_path.text()}")
        self.current_questions = self.builder.load_csv(self.csv_path.text())
        
        if not self.current_questions:
            QMessageBox.warning(self, "Error", "Failed to load CSV file or no valid questions found")
            return
        
        # Populate filter dropdowns
        categories = self.builder.get_categories(self.current_questions)
        difficulties = self.builder.get_difficulties(self.current_questions)
        
        self.category_combo.clear()
        self.category_combo.addItem("All Categories")
        for cat in categories:
            self.category_combo.addItem(cat)
        
        self.difficulty_combo.clear()
        self.difficulty_combo.addItem("All Difficulties")
        for diff in difficulties:
            self.difficulty_combo.addItem(diff)
        
        msg = f"Loaded {len(self.current_questions)} questions\n"
        msg += f"Categories: {', '.join(categories)}\n"
        msg += f"Difficulties: {', '.join(difficulties)}"
        
        QMessageBox.information(self, "Success", msg)
        self.statusBar.showMessage(f"Loaded {len(self.current_questions)} questions")
    
    def generate_round(self):
        """Generate a random round based on filters"""
        if not self.current_questions:
            QMessageBox.warning(self, "Error", "Please load a CSV file first")
            return
        
        round_name = self.round_name_input.text()
        round_size = self.round_size_spin.value()
        
        category = None
        if self.category_combo.currentIndex() > 0:
            category = self.category_combo.currentText()
        
        difficulty = None
        if self.difficulty_combo.currentIndex() > 0:
            difficulty = self.difficulty_combo.currentText()
        
        keyword = self.keyword_input.text().strip() if self.keyword_input.text().strip() else None
        
        logger.info(f"Generating round: name={round_name}, size={round_size}, "
                   f"category={category}, difficulty={difficulty}, keyword={keyword}")
        
        self.statusBar.showMessage("Generating round...")
        
        # Generate round
        self.current_round = self.builder.build_round(
            self.current_questions,
            round_name=round_name,
            round_size=round_size,
            category=category,
            difficulty=difficulty,
            keyword=keyword
        )
        
        # Display results
        results_text = f"Round: {self.current_round['name']}\n"
        results_text += f"Questions: {self.current_round['question_count']}\n"
        results_text += f"Categories: {', '.join(self.current_round['categories'])}\n\n"
        results_text += "=" * 70 + "\n"
        results_text += "QUESTIONS:\n"
        results_text += "=" * 70 + "\n\n"
        
        for i, q in enumerate(self.current_round['questions'], 1):
            results_text += f"{i}. {q['question']}\n"
            results_text += f"   Answer: {q['answer']}\n"
            results_text += f"   Category: {q.get('category', 'Unknown')}\n"
            results_text += f"   Difficulty: {q.get('difficulty', 'Unknown')}\n\n"
        
        self.results_text.setText(results_text)
        
        if self.current_round['question_count'] == 0:
            self.statusBar.showMessage("No questions matched your filters!")
            QMessageBox.warning(self, "No Results", self.current_round.get('error', 'No questions matched filters'))
        else:
            self.statusBar.showMessage(f"Generated round with {self.current_round['question_count']} questions")
    
    def export_round(self):
        """Export round to DOCX"""
        if not self.current_round or self.current_round['question_count'] == 0:
            QMessageBox.warning(self, "Error", "Generate a round first")
            return
        
        logger.info(f"Exporting round: {self.current_round['name']}")
        
        try:
            filepath = self.exporter.export_round(self.current_round, include_answers=True)
            QMessageBox.information(self, "Success", f"Round exported to:\n{filepath}")
            self.statusBar.showMessage(f"Exported to {filepath}")
        except Exception as e:
            logger.error(f"Export failed: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Export failed: {e}")


def main():
    """Main entry point"""
    app = __import__('PyQt6.QtWidgets', fromlist=['QApplication']).QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
