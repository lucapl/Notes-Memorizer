import logging
from .application import NotesApp

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    NotesApp().run()