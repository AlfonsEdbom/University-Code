# epsilon-greedy example implementation of a multi-armed bandit
import random

WINDOW_SIZE = 100
EPSILON_DECAY = 0.8

class Bandit:
    """
    Generic epsilon-greedy bandit that you need to improve
    """

    def __init__(self, arms, epsilon=0.9):
        """
        Initiates the bandits

        :param arms: List of arms
        :param epsilon: Epsilon value for random exploration
        """
        self.arms = arms
        self.epsilon = epsilon
        self.frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)
        self.expected_values = [0] * len(arms)
        self.history = [[] for _ in range(len(arms))]
        self.window_sum = [0] * len(arms)

    def run(self):
        """
        Asks the bandit to recommend the next arm

        :return: Returns the arm the bandit recommends pulling
        """
        if min(self.frequencies) == 0:
            return self.arms[self.frequencies.index(min(self.frequencies))]
        if random.random() < self.epsilon:
            self.epsilon = self.epsilon * EPSILON_DECAY
            return self.arms[random.randint(0, len(self.arms) - 1)]

        self.epsilon = self.epsilon * EPSILON_DECAY
        return self.arms[self.expected_values.index(max(self.expected_values))]

    def give_feedback(self, arm, reward):
        """
        Sets the bandit's reward for the most recent arm pull

        :param arm: The arm that was pulled to generate the reward
        :param reward: The reward that was generated
        """
        arm_index = self.arms.index(arm)
        window = self.history[arm_index]

        if len(window) == WINDOW_SIZE:
            window.pop(0)
            window.append(reward)
        else:
            window.append(reward)
        self.history[arm_index] = window

        window_sum = sum(self.history[arm_index])
        self.window_sum[arm_index] = window_sum

        expected_value = window_sum / len(window)
        self.expected_values[arm_index] = expected_value

        sum1 = self.sums[arm_index] + reward
        self.sums[arm_index] = sum1

        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency
