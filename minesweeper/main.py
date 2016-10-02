#!/usr/bin/env python3

"""An implementation of the minesweeper game with pygame."""

import argparse
import collections

import pygame

import utilities


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-w', '--width', type=int, help='Width of the game window.')
    parser.add_argument('-h', '--height', type=int, help='Height of the game window.')
    parser.add_argument('--fps', type=int, help='Framerate of the game window.')
    return parser.parse_args()


MOUSE1 = 1
MOUSE2 = 3


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


MenuOption = collections.namedtuple('MenuOption', ['text', 'game'])


class Menu(Scene):

    def __init__(self, fps, options):
        super().__init__(fps)
        self.options = options

    def _vertical_distance_between_options(self):
        height = self.screen.get_size()[1]
        return height // len(self.options)

    def draw(self):
        step = self._vertical_distance_between_options()
        offset = (step - self.font.get_height()) // 2
        for i, option in enumerate(self.options):
            pos = (20, i * step + offset)
            text = self._render_cache[option.text]
            self.screen.blit(text, pos)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == MOUSE1:
            step = self._vertical_distance_between_options()
            option_index = event.pos[1] // step
            self.running = False
            self.options[option_index].game.run()


class Game(Scene):

    def __init__(self, fps, minefield):
        super().__init__(fps)
        self.minefield = minefield

    def draw(self):
        screenw, screenh = self.screen.get_size()
        cellw, cellh = screenw / self.minefield.width, screenh / self.minefield.height
        for x in range(self.minefield.width):
            for y in range(self.minefield.height):
                cell = self.minefield[x, y]
                text = self._render_cache[str(cell)]
                px, py = x * cellw, y * cellh
                self.screen.blit(text, (px, py))
                pygame.draw.line(self.screen, self.fg_color, (px, 0), (px, screenh))
                pygame.draw.line(self.screen, self.fg_color, (0, py), (screenw, py))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
def main(win_size, fps):
    pygame.init()
    pygame.display.set_mode(win_size)
    pygame.display.set_caption('Pygame Minesweeper')
    pygame.quit()

if __name__ == '__main__':
    args = parse_args()
    main((args.width, args.height), args.fps)
