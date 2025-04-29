import gymnasium as gym

env = gym.make("CliffWalking-v0", render_mode="human")
observation, info = env.reset()
env.render()