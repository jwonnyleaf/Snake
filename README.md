
# Snake Game

This is a Python implementation of the classic Snake game along with an AI agent that learns to play the game using Reinforcement Learning. The Reinforcement Learning half is based on a tutorial by [Patrick Loeber](https://www.youtube.com/watch?v=VGkcmBaeAGM&list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV&index=4)



## Requirements

- Python 3.x
- Pygame
- Torch
- Numpy
- Matplot


## Installation

1. Clone the repository
2. Install the required packages using pip:

```bash
  pip install -r requirements.txt
```


    
## Usage
To run the game normally, simply run the 'snake.py' script inside the Snake Folder
```python
cd Snake
python snake.py
```

Running the AI will require running 'agent.py' inside the SnakeAI Folder
```python
cd SnakeAI
python agent.py
```



## How it Works
The AI agent learns to play the game using a form of Reinforcement Learning called Q-Learning. The agent is represented by a neural network that takes in the current state of the game (e.g. the positions of the snake and the food) as input, and outputs a Q-value for each possible action (e.g. move left, move right, etc.). The Q-value represents the expected reward for taking that action in that state.

During training, the agent plays the game multiple times, and updates its neural network based on the rewards it receives. The goal is to maximize the total reward (i.e. the score) over time. The agent uses an epsilon-greedy policy to balance exploration (trying new actions) and exploitation (taking the action with the highest Q-value).
## Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, please create an issue or submit a pull request.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

