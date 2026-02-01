"""
TriviaMaster - Streamlit Web App
Simple random trivia round builder with CSV filtering
"""
import streamlit as st
import logging
from io import BytesIO, StringIO
import os
import sys
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trivia_master.core.simple_round_builder import SimpleRoundBuilder
from trivia_master.utils.docx_exporter import DocxExporter
from trivia_master.config import OUTPUT_DIR

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="TriviaMaster",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .stButton > button {
        width: 100%;
        font-size: 16px;
        padding: 10px;
    }
    h1 {
        color: #2196F3;
        text-align: center;
    }
    h2 {
        color: #4CAF50;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🎯 TriviaMaster - Random Round Builder")
st.markdown("Create custom trivia rounds from your question database")

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = None
if 'round' not in st.session_state:
    st.session_state.round = None
if 'builder' not in st.session_state:
    st.session_state.builder = SimpleRoundBuilder()
if 'exporter' not in st.session_state:
    st.session_state.exporter = DocxExporter()
    st.session_state.exporter.set_output_directory(str(OUTPUT_DIR))

# ============ STEP 1: UPLOAD CSV ============
st.markdown("## Step 1: Load Your Questions")

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader("Upload CSV file with trivia questions", type=['csv'])

with col2:
    if uploaded_file is not None:
        # Save uploaded file to system temp directory (cross-platform)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("📥 Load CSV"):
            with st.spinner("Loading questions..."):
                st.session_state.questions = st.session_state.builder.load_csv(temp_path)
            
            if st.session_state.questions:
                st.success(f"✅ Loaded {len(st.session_state.questions)} questions!")
            else:
                st.error("❌ Failed to load CSV")

# Display loaded stats
if st.session_state.questions:
    st.info(f"📊 **{len(st.session_state.questions)} questions loaded**")
    
    categories = st.session_state.builder.get_categories(st.session_state.questions)
    difficulties = st.session_state.builder.get_difficulties(st.session_state.questions)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Categories", len(categories))
    with col2:
        st.metric("Difficulties", len(difficulties))
else:
    st.warning("👆 Upload a CSV file to get started")
    st.stop()

# ============ STEP 2: CONFIGURE FILTERS ============
st.markdown("## Step 2: Configure Your Round")

col1, col2, col3 = st.columns(3)

with col1:
    categories = st.session_state.builder.get_categories(st.session_state.questions)
    category = st.selectbox(
        "Category",
        ["All Categories"] + categories,
        help="Filter questions by category"
    )
    if category == "All Categories":
        category = None

with col2:
    difficulties = st.session_state.builder.get_difficulties(st.session_state.questions)
    difficulty = st.selectbox(
        "Difficulty",
        ["All Difficulties"] + difficulties,
        help="Filter questions by difficulty"
    )
    if difficulty == "All Difficulties":
        difficulty = None

with col3:
    keyword = st.text_input(
        "Keyword (optional)",
        placeholder="Search in question or answer",
        help="Leave blank to skip keyword filtering"
    )
    keyword = keyword.strip() if keyword else None

# Round settings
col1, col2 = st.columns(2)

with col1:
    round_size = st.slider(
        "Number of Questions",
        min_value=1,
        max_value=100,
        value=10,
        step=1,
        help="How many questions in this round?"
    )

with col2:
    round_name = st.text_input(
        "Round Name",
        value="My Random Round",
        placeholder="Give your round a name",
        help="This will appear in the exported DOCX"
    )

# ============ STEP 3: GENERATE ROUND ============
st.markdown("## Step 3: Generate & Review")

if st.button("🎲 Generate Random Round", use_container_width=True, type="primary"):
    with st.spinner("Generating round..."):
        st.session_state.round = st.session_state.builder.build_round(
            st.session_state.questions,
            round_name=round_name,
            round_size=round_size,
            category=category,
            difficulty=difficulty,
            keyword=keyword
        )
    
    if st.session_state.round['question_count'] == 0:
        st.error(f"❌ {st.session_state.round.get('error', 'No questions matched your filters')}")
    else:
        st.success(f"✅ Generated {st.session_state.round['question_count']} questions!")

# Display round if generated
if st.session_state.round and st.session_state.round['question_count'] > 0:
    # Round summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions", st.session_state.round['question_count'])
    with col2:
        st.metric("Categories", len(st.session_state.round['categories']))
    with col3:
        st.metric("Name", round_name)
    
    # Display questions
    st.markdown("### Questions:")
    
    # Expandable questions
    for i, q in enumerate(st.session_state.round['questions'], 1):
        with st.expander(f"**{i}. {q['question'][:80]}...**"):
            st.write(f"**Question:** {q['question']}")
            st.write(f"**Answer:** {q['answer']}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Category:** {q.get('category', 'Unknown')}")
            with col2:
                st.write(f"**Difficulty:** {q.get('difficulty', 'Unknown')}")
    
    # Export button
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("📥 Export to DOCX", use_container_width=True, type="primary"):
            try:
                with st.spinner("Creating DOCX file..."):
                    # Export to BytesIO instead of file
                    docx_buffer = BytesIO()
                    
                    # Use exporter but capture output
                    filepath = st.session_state.exporter.export_round(
                        st.session_state.round, 
                        include_answers=True
                    )
                    
                    # Read the file into memory
                    with open(filepath, 'rb') as f:
                        docx_buffer = BytesIO(f.read())
                    
                    # Generate filename
                    safe_name = "".join(c for c in round_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = f"{safe_name}.docx"
                    
                    st.download_button(
                        label="⬇️ Download DOCX",
                        data=docx_buffer,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    
                    st.success(f"✅ DOCX ready! File: {filename}")
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
                logger.error(f"Export error: {e}", exc_info=True)
    
    with col2:
        if st.button("🔄 Generate New Round", use_container_width=True):
            st.session_state.round = None
            st.rerun()

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("### 📖 About TriviaMaster")
    st.info("""
    **TriviaMaster** is a simple tool to build custom trivia rounds from your question database.
    
    **Features:**
    - 📤 Upload your CSV questions
    - 🔍 Filter by category, difficulty, or keyword
    - 🎲 Generate random rounds
    - 📥 Export to professional DOCX format
    
    **CSV Requirements:**
    - Columns: Question, Answer, Category, Difficulty
    - Any additional columns are ignored
    """)
    
    st.markdown("---")
    st.markdown("### 🚀 How to Use")
    st.markdown("""
    1. **Upload** your CSV file
    2. **Configure** filters and round size
    3. **Generate** a random round
    4. **Export** to DOCX for printing or sharing
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")
