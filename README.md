# Dance of Fire and Ice AI

## Overview
This project consists of creating an AI that can play the game [The Dance of Fire and Ice](https://store.steampowered.com/app/977950/A_Dance_of_Fire_and_Ice/).

The game revolves around 2 spinning circles that move within a track made of tiles that can only go Up, Down, Left or Right.
However, the game's objective consists of timing keyboard presses so the circles anchor in the respective tile.

A human can easily play the game if they have a basic idea of rhythm, but will an AI be able to perform as well?

## Limitations and problems
Since the original games revolves about timing, then creating an AI to watch the game real time may not be the best answer.
That solution requires to watch in real time the state of the game then do extra processing so the computer can understand what do the pixels mean and how to interpret them.
A Convolutional Neural Network can help in this problem, but the extra time that it required to process each frame may slow down things and since the game is about music, the window to send an input is very tight.
And lets not add the fact that the original game sometimes has some tracks that overalp with themselves and the tracks may contain flashy animations or assets that just add noise and consequently, add more processing time.

## Best Approach
The best solution to simulate the game is to create it from scratch. The project has implemented the game using [Python](https://www.python.org/downloads/) and the tool called [Processing](https://processing.org/download).

Processing is a framework that facilitates the bond between programming and user interface. It makes it easier to paint shapes and create visual behaviour with programming.
Currently, Processing is supported for Python and Javascript, but Python was the winner of the project due to the compatibility of the most AI libraries found today.

## The problem
The game made from scratch in processing is not a 1-to-1 mapping from the original game; it only mimicks the basic mechanics.
As the player plays the game, they will notice that there are a few factors to consider while playing in order to reach the end of the track.

Consider the next situation:

<Insert image here>

There are 3 variables to consider:
- The current angle of the ball spinning
- The direction of the next tile
- The window to press an input in order to anchor the spinning ball

The first variable is a real number that ranges from 0 to approximately 2π (slightly above due to the implementation with processing). It is the most straightforward variable to understand because it basically tells the current angle of the spinning ball.

The second variable is a integer that can range from 1 to 4 and tells the direction of the next tile. The current implementation has:
- Up = 1
- Down = 2
- Right = 3
- Left = 4

And the last variable is the range, window or threshold that the user is allowed to anchor the spinning ball. This variable depends of the distance between the balls and the size of the tiles.

In order to move on to the next tile, the user has to press any key and the game will check the current spinning ball's angle and will compare if said angle is within the threshold or window. If so, then the player will move on to the next tile and this repeats until they beat the track.

If you want to try the game by yourself, run the file called **game_human.py** located under the directory *dance_fire_ice/games*.

## Artificial Intelligence
The main model used to tackle this problem is the Neural Networks.
Neural Networks were selected because the inputs have a real number and it is crutial to generalize a function that can take a range of numbers and map out to actions.
For the NNs, the selected inputs are:
- The current angle of the spinning ball
- The direction of the next tile

However, since the direction is just a discrete number with 4 possible options, they will be split into 4 different inputs and each one will represent a direction and will take a value of 0 or 1 where 1 means its the correct direction.
So in total, the NN will have 5 inputs to deal with.

The architecture of the Neural Network will be very simple with just a input layer, then a hidden layer of 4 neurons and an output layer of 2 neurons (one neuron represents 'anchor now' action and 'wait' action, just like the player does in the game).

In order to train the NN and have robust results, 2 approaches were attempted: Genetic Algorithms and Deep-Q Learning.

The first approach consists of taking the idea of Charles Darwin's Evolution theory and apply it to the algorithm.
There will be a generation made of a population of multiple and diverse agents (the spinning circles) and each one will try to achieve the goal, which is complete the track.
However, all the agents will be given the same amount of time or tries and the ones who perform better, will be selected to pass down their features so the next generation can improve even more.
In this case, the weights of the layers will be the features that will be passed on.

The second approach consists of taking the concept of Q-Learning and expand it to the real numbers. Instead of using a Q table that maps a finite amount of possibilities to a finite amount of actions, a Neural Network will be used in order to map infinitie inputs to a finite amount of actions.
The neural network will process the current inputs and will generate Q values in its output neurons. The neuron with the highest Q value is going to be the action that the AI will take.

## Reward System
This is a problem of Reinforcement Learning, so rewards are necessary in order to guide better the AI of what it must do.
There will be 4 types of rewards:
- Successful Anchoring: It incentives of anchoring the spinning ball within the threshold
- Failed Waiting: It punishes the AI by taking the decision of anchoring outside of the threshold
- Succesful Waiting: It rewards the AI by waiting when the spinning ball is not in the threshold
- Failed Anchoring: It punishes the AI when it decides to not anchor whithin the allowed threshold

## Evaluation Time
The agents were given a total amount of mistakes that they can commit. Once they have reached the limit, the reach the 'game over' state and can no longer play.

The following actions contribute to the definition of 'making a mistake' in this context:
- Attempting to anchor 

The current number of mistakes allowed are 512

## Results

### Genetic Algorithms
The first approach attempted was using Genetic Algorithms.
The results were not the ones expected because the algorithm takes a lot of time to converge to solve just 10-20% of the tracks used for training.

It is guaranteed that the algorithm will land on a optimal solution that can complete all the tracks but it will take a lot of time which isn't a good result at all.

There were also a few issues with this approach:
- The frame rate drops heavily when drawing more than 10 agents in the screen
- Sometimes the algorithm gets stuck in a corner and takes a lot of time to get out of that situation. There were a couple of attempts where the agent does not mutate to generate a solution.
- The breeding mechanism inserts too much randomness and contributes to the huge time consumption of finding an feasable solution

### Deep-Q Learning
This approach is the best one so far because it synergizes well with the AI implemented in the agent to make the decision process.

Instead of creating a population of agents, only one single agent will be trained and it will get better as time goes on. Also, all the issues stated above no longer exist with this solution so the time consumed to land on a feasable solution is more acceptable and manageable.












