# NESGym

An EXPERIMENTAL [openai-gym](https://gym.openai.com/) wrapper for NES games.

# Installation
- Install the `fceux` NES emulator and make sure `fceux` is in your `$PATH`. In Debian/Ubuntu, simple use `sudo apt install fceux`.
- Copy state files from `roms/fcs/*` to your `~/.fceux/fcs/` (faster loading for the beginning of the game).

# Example usage
For instance:
```python
# import nesgym to register environments to gym
import nesgym
env = gym.make('nesgym/NekketsuSoccerPK-v0')
obs = env.reset()

for step in range(10000):
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    ... # your awesome reinforcement learning algorithm is here
```

# Examples for training dqn
An implementation of dqn is in [`src/dqn`](src/dqn), using [keras](https://keras.io/).

You can train dqn model for Atari with [`run-atari.py`](src/run-atari.py) and for NES with [`run-soccer.py`](src/run-soccer.py) or [`run-mario.py`](src/run-mario.py).

# Integrating new NES games?
You need to write two files:
1. a lua interface file,
2. and an openai gym environment class(python) file.

The lua file needs to get the reward from emulator(typically extracting from a memory location), and the python file defines the game specific environment.

For an example of lua file, see [`src/lua/soccer.lua`](src/lua/soccer.lua); for an example of gym env file, see [`src/nesgym/nekketsu_soccer_env.py`](src/nesgym/nekketsu_soccer_env.py).

> [This website](http://datacrystal.romhacking.net/wiki/Category:NES_games) gives RAM mapping for the most well-known NES games, this is very useful to extract easily the score or lives directly from the NES RAM memory, to use it as a reward for the reinforcement learning loop. See for instance [for Mario Bros.](http://datacrystal.romhacking.net/wiki/Mario_Bros.:RAM_map).

# Gallery
## Training Atari games
![atari](images/atari.png)

## Training NES games
![fc-soccer](images/soccer.png)


---

### :scroll: License ? [![GitHub license](https://img.shields.io/github/license/Naereen/gym-nes-mario-bros.svg)](https://github.com/Naereen/gym-nes-mario-bros/blob/master/LICENSE)
This (small) repository are published under the terms of the [MIT license](http://lbesson.mit-license.org/) (file [LICENSE](LICENSE)).
© [Lilian Besson](https://GitHub.com/Naereen), 2018.

[![Maintenance](https://img.shields.io/badge/Maintenu%3F-oui-green.svg)](https://GitHub.com/Naereen/gym-nes-mario-bros/graphs/commit-activity)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Naereen/gym-nes-mario-bros)
[![Analytics](https://ga-beacon.appspot.com/UA-38514290-17/github.com/Naereen/gym-nes-mario-bros/README.md?pixel)](https://GitHub.com/Naereen/gym-nes-mario-bros/)

[![made-with-OpenAIGym](https://img.shields.io/badge/Made%20with-OpenAI%20Gym-1f425f.svg)](https://gym.openai.com/)
[![made-with-Fceux](https://img.shields.io/badge/Made%20with-Fceux-1f425f.svg)](http://www.fceux.com/web/home.html)
[![made-with-Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-Lua](https://img.shields.io/badge/Made%20with-Lua-1f425f.svg)](https://www.Lua.org/)
[![made-with-Keras](https://img.shields.io/badge/Made%20with-Keras-1f425f.svg)](https://Keras.io/)
[![made-with-TensorFlow](https://img.shields.io/badge/Made%20with-TensorFlow-1f425f.svg)](https://www.tensorflow.org/)
[![made-with-OpenCV](https://img.shields.io/badge/Made%20with-OpenCV-1f425f.svg)](https://opencv.org/)

[![ForTheBadge built-with-swag](http://ForTheBadge.com/images/badges/built-with-swag.svg)](https://GitHub.com/Naereen/)
[![ForTheBadge uses-badges](http://ForTheBadge.com/images/badges/uses-badges.svg)](http://ForTheBadge.com)
[![ForTheBadge uses-git](http://ForTheBadge.com/images/badges/uses-git.svg)](https://GitHub.com/)
