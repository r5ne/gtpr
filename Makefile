PACMAN := uv
PACMANFLAGS := run streamlit run
SOURCE := main.py

.PHONY: all

all:
	$(PACMAN) $(PACMANFLAGS) $(SOURCE)
