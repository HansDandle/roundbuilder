# TriviaMaster

An intelligent trivia round analyzer and generator. Load your existing trivia rounds, learn your style, and automatically generate new rounds matching your style from a database of pre-written questions.

## Features

- **Style Analysis**: Analyze your existing trivia rounds to learn your question patterns
- **Question Matching**: Score questions from external sources based on how well they match your learned style
- **Round Generation**: Automatically generate complete trivia rounds with matched questions
- **Manual Builder**: Manually construct rounds by selecting and ordering questions
- **DOCX Export**: Export generated rounds as formatted Word documents

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download NLTK data (one-time setup):
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

## Quick Start

1. **Analyze Your Style**:
   - Place all your trivia round DOCX files in a folder
   - Open TriviaMaster and go to the "Analyze Style" tab
   - Browse to your rounds folder and click "Analyze Rounds"
   - The app will learn your trivia style

2. **Load Questions**:
   - Go to "Match Questions" tab
   - Select a CSV file containing questions to match
   - The app will score each question based on your style

3. **Generate Rounds**:
   - Go to "Generate Round" tab
   - Set round name, number of questions, and optional category filter
   - Click "Generate Round"
   - Review the generated round and click "Export to DOCX" to save

4. **Manual Building** (Optional):
   - Use the "Build Round" tab to manually select specific questions
   - Add/remove questions as needed
   - Export when satisfied

## CSV Format

Your CSV file should have the following columns:
- `question`: The trivia question
- `answer`: The answer to the question
- `category`: Category of the question (optional)
- `difficulty`: Difficulty level - easy, medium, hard (optional)
- `type`: Question type - multiple_choice, short_answer, etc. (optional)

## Project Structure

```
TriviaMaster/
├── trivia_master/
│   ├── core/
│   │   ├── docx_parser.py      # Parse DOCX files
│   │   ├── style_analyzer.py   # Analyze trivia style
│   │   ├── question_matcher.py # Match questions to style
│   │   └── round_generator.py  # Generate rounds
│   ├── gui/
│   │   └── main_window.py      # PyQt6 GUI
│   ├── utils/
│   │   └── docx_exporter.py    # Export to DOCX
│   ├── config.py               # Configuration
│   └── __init__.py
├── data/                        # Your input data
├── output/                      # Generated rounds
├── requirements.txt
├── run_trivia_master.py         # Entry point
└── README.md
```

## Running the Application

```bash
python run_trivia_master.py
```

## How It Works

1. **Analysis Phase**: The app parses all your DOCX files and builds a style profile that captures:
   - Average question/answer lengths
   - Difficulty distribution
   - Question types and patterns
   - Common keywords and themes
   - Question/answer formatting preferences

2. **Matching Phase**: When given a CSV of questions, each question is scored (0-100) based on:
   - How similar the length is to your typical questions
   - How many of your common keywords appear
   - How well it matches your question patterns
   - Overall style similarity

3. **Generation Phase**: The app selects from matched questions to create a complete round that:
   - Meets your size requirements
   - Has diverse categories
   - Maintains difficulty balance
   - Matches your overall style

## Settings

- **Matching Threshold**: Minimum score (0-100) for a question to be considered a match (default: 60)
- **Round Size**: Number of questions per round (5-50)
- **Category Filter**: Optionally filter questions by category

## Tips for Best Results

1. Use a large number of your trivia rounds for analysis (10+) for better style learning
2. Ensure your CSV has complete data for all questions
3. Adjust the matching threshold up for stricter matching, down for more lenient matching
4. Use category filters to create themed rounds
5. Review generated rounds before exporting and make manual adjustments if needed

## Output

Generated rounds are saved as formatted DOCX files in the `output/` folder with:
- Clear numbering
- Question text in bold
- Answer text in italics
- Category information
- Proper spacing for readability

## License

MIT
