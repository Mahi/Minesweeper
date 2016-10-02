#!/usr/bin/env python3

"""An implementation of the minesweeper game with pygame."""

import argparse

import pygame

import utilities


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-w', '--width', type=int, help='Width of the game window.')
    parser.add_argument('-h', '--height', type=int, help='Height of the game window.')
    parser.add_argument('--fps', type=int, help='Framerate of the game window.')
    return parser.parse_args()




class Scene:

    def __init__(self, fps, font=None, bg_color=(0, 0, 0), fg_color=(255, 255, 255)):
        self.screen = pygame.display.get_surface()
        self.fps = fps
        self.running = False
        self.font = font if font is not None else pygame.font.Font(None, 64)
        self._render_cache = utilities.KeyDefaultDict(self._font_renderer)
        self.bg_color = bg_color
        self.fg_color = fg_color

    def _font_renderer(self, text):
        return self.font.render(text, 1, self.fg_color)

    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.screen.fill(self.bg_color)
            self.draw()
            pygame.display.update()
            for event in pygame.event.get():
                self.handle_event(event)
            clock.tick(self.fps)
def main(win_size, fps):
    pygame.init()
    pygame.display.set_mode(win_size)
    pygame.display.set_caption('Pygame Minesweeper')
    pygame.quit()

if __name__ == '__main__':
    args = parse_args()
    main((args.width, args.height), args.fps)
