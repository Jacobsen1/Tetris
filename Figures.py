import pygame as pg
import random as rnd
import copy

GREEN = (0, 255,   0)

figure_matrices = {
    "I": [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]],

    "O": [[
        [1, 1],
        [1, 1]]],

    "S": [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]]
    ],

    "Z": [[
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]]],

    "L": [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 1]],

    "J": [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]],

    "T": [
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0]]
}


class Figures:
    def __init__(self) -> None:
        self.finished_figures = []

    def select_figure(self):
        return 0, 5, figure_matrices["S"][0]

    def rotate(self):
        print(self.current_fig)
        fig_mat = []

        for rect, fig in zip(self.current_fig, figure_matrices[self.current_ind]):
            temp = []
            if fig == 1:
                temp.append((rect.x, rect.y))
            else:
                temp.append(0)
            fig_mat.append(temp)

        print(fig_mat)
        '''
        fig_mat = copy.deepcopy(figure_matrices[self.current_ind])
        fig_mat = list(zip(*fig_mat[::-1]))
        fig_mat = [list(ele) for ele in fig_mat]
        print(self.current_fig)
        '''
