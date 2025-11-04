PACMAN := uv
PACMANFLAGS := run python
SOURCE := src/gtpr

.PHONY: all

all:
	$(PACMAN) $(PACMANFLAGS) $(SOURCE)
