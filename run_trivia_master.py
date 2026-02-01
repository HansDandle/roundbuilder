"""TriviaMaster - Run the application"""
import sys
import logging

# Setup logging to console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

from trivia_master.gui.main_window import main

if __name__ == '__main__':
    main()
