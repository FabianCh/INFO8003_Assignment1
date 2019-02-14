import numpy as np
import random as rdm
import Policy


class Domain:
    # Class to create a determinist domain (Beta=0) or a stochastique domain (beta!=0)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    UP = (0, -1)
    ACTION_SPACE = [RIGHT, LEFT, DOWN, UP]

    def __init__(self, x, y, board, beta=0):
        self.board = board
        self.n = len(board[0])
        self.m = len(board)
        self.state = [x, y]
        self.B = np.max(self.board)
        self.gamma = 0.99
        self.beta = beta
        self.w = rdm.uniform(0, 1)


    def moves(self, action):
        if action in self.ACTION_SPACE:
            if self.w <= 1 - self.beta:
                if action in self.ACTION_SPACE:
                    self.state[0] = min(max(self.state[0] + action[0], 0), self.n - 1)
                    self.state[1] = min(max(self.state[1] + action[1], 0), self.m - 1)
            else:
                self.state[0] = 0
                self.state[1] = 0
            self.w = rdm.uniform(0, 1)

    def reward(self, state, action):
        if action in self.ACTION_SPACE:
            xa, ya = action
            xr = min(max(state[0] + xa, 0), self.n - 1)
            yr = min(max(state[1] + ya, 0), self.m - 1)
            return (1 - self.beta)*self.g(xr, yr) + self.beta * self.g(0, 0)

    def g(self, x, y):
        return self.board[y][x]


def JN(domain: Domain, policy: Policy.Policy, N):
    # method to return the Expected value after N turn with a policy in a domain
    if N == 0:
        return 0
    else:
        R = domain.reward(domain.state, policy.action())
        domain.moves(policy.action())
        return R + domain.gamma * JN(domain, policy, N-1)


def ExpectedCumulativeRewardSignal(domain, policy):
    # method to return the Expected Cumulative Reward Signal with a policy in a domain
    state = domain.state
    S = JN(domain, policy, 10)
    domain.state = state
    return S


def MatrixJN(domain: Domain, policy: Policy.Policy, N):
    # method to return the list of Matrix of Expected value after N turn with a policy in a domain
    L = [np.array([[0. for k in range(domain.n)] for l in range(domain.m)])]
    for h in range(1, N):
        L.append(np.array([[0. for k in range(domain.n)] for l in range(domain.m)]))
        for i in range(domain.n):
            for j in range(domain.m):
                L[-1][j][i] = domain.reward([i, j], policy.action())
                L[-1][j][i] += domain.gamma * (1 - domain.beta) * L[-2][min(max(j + policy.action()[1], 0), domain.n - 1)][min(max(i + policy.action()[0], 0), domain.m - 1)]
                L[-1][j][i] += domain.gamma * domain.beta * L[-2][0][0]
    return L
