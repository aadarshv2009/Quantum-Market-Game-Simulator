# Quantum-Market-Game-Simulator
## App Link
The app is linked here:
[Streamlit App](https://quantum-game-simulator.streamlit.app/)

# Project Documentation: Quantum Market Game Theory Simulator

## Introduction
**The Quantum Market Game Theory Simulator** is a trading game theory scenario with a quantum twist. The project uses Qiskit to utilize superposition and entanglement to create an immersive learning experience through the simulation of a simple market scenario. Two traders are given a choice to buy or sell an asset. Instead of classical buy or sell mechanics, the traders are put into a superposition of buy and sell using rotation angles that determine the probability of each decision. This simulation demonstrates the core principles of quantum mechanics - superposition and entanglement - in a simple trading game.

## How It Works
The simulation represents two traders as qubits that are initialized within a quantum state using rotations. The angles of rotation, which determine the probability of buying or selling, are either randomized or selected by the user.  

**|0⟩ causes the trader to sell the asset and |1⟩ causes the trader to buy the asset.**

Each round of the game goes through the following steps:

### 1. State Preparation
Each trader's decision is determined by a **RY** rotation, which puts the traders into a superposition state.

### 2. Entanglement
Toggled on or off by the user, there is an optional controlled-NOT gate that is applied to the circuit. This gate creates a correlation between the traders.

### 3. Measurement
The quantum state is measured and collapses into a classical outcome (00, 01, 10, 11). This outcome determines the real decision made by each trader after the market is "opened".

### 4. Outcome Evaluation
A payoff matrix determines the outcome of the trade and assigns gains or losses to each trader.

### 5. Expected Value
Instead of evaluating one outcome of the game, the simulator calculates the expected value of the payoffs across all of the measurement probabilities.

## Features

### Superposition Representation
Each trader is in a probabilistic superposition until the final measurement, showing superposition in real world scenarios.

### Entanglement Representation
When entanglement is enabled, the decisions of the traders are correlated with one another, allowing the user to view the effect of entanglement between two agents.

### Multiple Game Modes
The game has 3 game modes, allowing flexibility in the learning experience.

- **Mode 0:** Both angles are chosen randomly by the simulation  
- **Mode 1:** Trader 1's angle is chosen by the user while Trader 2's angle is chosen by the simulation  
- **Mode 2:** Both angles are chosen by the user  

### Results Visualization
The user is able to see graphs and tables that represent the qualities of superposition and entanglement.

## Technology

- **Quantum Circuits:** Qiskit  
- **Quantum Backend:** Qiskit Aer Simulator and IonQ Quantum backend  
- **Programming Language:** Python  

## Educational Value
The Quantum Market Game Theory Simulator is a technical project as well as a learning tool that helps users understand:
- **Superposition:** Decisions are represented as probability distributions rather than fixed decisions.
- **Measurement:** Measuring the system or "opening the market" makes the decisions collapse into a singular outcome.
- **Entanglement:** The action of one trader can affect the probability distribution of the other trader.


