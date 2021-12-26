import pygame as pg
import random as rnd

GREEN = (0, 255,   0)

figure_matrices = {
    "I": [
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]],

        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],

        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],

        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]]
    ],

    "O": [
        [[1, 1],
         [1, 1]]
    ],

    "S": [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],

        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]],

        [[0, 0, 0],
         [0, 1, 1],
         [1, 1, 0]],

        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],

    "Z": [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],

        [[0, 0, 1],
         [0, 1, 1],
         [0, 1, 0]],

        [[0, 0, 0],
         [1, 1, 0],
         [0, 1, 1]],

        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]]

    ],

    "L": [
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],

        [[0, 0, 0],
         [1, 1, 1],
         [1, 0, 0]],

        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]],

        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
    ],

    "J": [
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]],

        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],

        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 1]]

    ],

    "T": [
        [[0, 0, 0],
         [1, 1, 1],
         [0, 1, 0]],

        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]],

        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 1, 0],
         [0, 1, 1],
         [0, 1, 0]],
    ]
}


class Figures:
    def __init__(self) -> None:
        self.finished_figures = []
        self.current_letter = ''
        self.next_letter = rnd.choice(list(figure_matrices.keys()))
        self.current_rot = 0

    def select_figure(self):
        self.current_letter = self.next_letter
        self.next_letter = rnd.choice(list(figure_matrices.keys()))
        self.current_rot = 0
        return 0, 5, figure_matrices[self.current_letter][self.current_rot]

    def rotate(self):
        self.current_rot += 1
        self.current_rot %= len(figure_matrices[self.current_letter])
        return figure_matrices[self.current_letter][self.current_rot]

    def get_next_fig_mat(self):
        return figure_matrices[self.current_letter][(self.current_rot + 1) % len(figure_matrices[self.current_letter])]

    def get_next_fig(self):
        return figure_matrices[self.next_letter][0]