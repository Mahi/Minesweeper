#!/usr/bin/env python3

"""An implementation of the minesweeper game with pygame."""

import argparse

import pygame


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-w', '--width', type=int, help='Width of the game window.')
    parser.add_argument('-h', '--height', type=int, help='Height of the game window.')
    parser.add_argument('--fps', type=int, help='Framerate of the game window.')
    return parser.parse_args()


def main(win_size, fps):
    pygame.init()
    pygame.display.set_mode(win_size)
    pygame.display.set_caption('Pygame Minesweeper')
    pygame.quit()

if __name__ == '__main__':
    args = parse_args()
    main((args.width, args.height), args.fps)
