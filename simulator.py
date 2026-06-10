##start of quantum market game simulator

#imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import RXGate, RZGate, RZZGate
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import QAOAAnsatz
from qiskit_aer import AerSimulator

#### USER CHOOSE MODE
###mode- 0,1,2 




###function for getting user choices
def user_choices():
    mode=int(input("Choose Mode-0,1,2"))
    entanglement=(input("Choose entanglement on or off--> y or n")).lower()=="y"
    shots=int(input("Choose number of shots:"))
    if mode==0:
        angle_1=np.random.uniform(0,np.pi)
        angle_2=np.random.uniform(0,np.pi)
    elif mode==1:
        angle_1=float(input("Choose rotation angle for trader 1- [0,pi]"))
        angle_2=np.random.uniform(0,np.pi)
    elif mode==2:
        angle_1=float(input("Choose rotation angle for trader 1- [0,pi]"))
        angle_2=float(input("Choose rotation angle for trader 2- [0,pi]"))
    return mode, entanglement,shots,angle_1,angle_2


def validate_choices(mode, entanglement,shots,angle_1,angle_2):
    if mode not in(0,1,2):
        raise ValueError("Mode has to be between 0, 1, or 2")
    if not isinstance(entanglement, bool):
        raise ValueError("Entanglement has to be True or False")
    if shots <= 0:
        raise ValueError("Shots have to be above 0")
    if shots>= 10000:
        raise ValueError("Please keep number of shots under 10,000")
    if not (0 <= angle_1 <= np.pi):
        raise ValueError("angle_1 has to be between 0 and pi")

    if not (0 <= angle_2 <= np.pi):
        raise ValueError("angle_2 has to be between 0 and pi")

def circuit(angle_1,angle_2,entanglement):
    qc=QuantumCircuit(2,2)
    qc.ry(angle_1,0)
    qc.ry(angle_2,1)
    if entanglement==True:
        qc.cx(0,1)
    return qc


def compute(qc,shots):
    qc.measure([0,1],[0,1])
    simulator=AerSimulator()
    results=simulator.run(qc,shots=shots).result()
    counts=results.get_counts()
    return counts, results


def shots_to_probs(shots,counts):
    probs={}
    for bitstring, count in counts.items():
        probs[bitstring]=count/shots
    return probs

def most_likely_bitstring(counts):
    bitstring=max(counts,key=counts.get)
    return bitstring

def flip_bitstring(bitstring):
    return bitstring[::-1]

def convert_actions(bitstring):
    actions={"0":"Sell","1":"Buy"}
    trader1_action=actions[bitstring[0]]
    trader2_action=actions[bitstring[1]]
    return trader1_action, trader2_action


payoff_matrix={"00":(-1,-1),"10":(1,3),"01":(3,1),"11":(2,2)}

def payoff(payoff_matrix,bitstring):
    bitstring_flipped=flip_bitstring(bitstring)
    payoff_1, payoff_2 = payoff_matrix[bitstring_flipped]
    return payoff_1,payoff_2



def expected_payoff(counts,payoff_matrix,shots):
    ep_1=0
    ep_2=0
    for bitstring, count in counts.items():
        bitstring_flipped=flip_bitstring(bitstring)
        probability=count/shots
        payoff_1, payoff_2 = payoff_matrix[bitstring_flipped]
        ep_1 += probability * payoff_1
        ep_2 += probability * payoff_2
    return ep_1, ep_2


def winner(payoff_1, payoff_2):
    if payoff_1 > payoff_2:
        return "Trader 1 Wins"
    elif payoff_2 > payoff_1:
        return "Trader 2 Wins"
    else:
        return "Tie"




###create a table
def create_table(counts,payoff_matrix,shots):
    dataset=[]
    for bitstring, count in counts.items():
        real=flip_bitstring(bitstring)
        prob=count/shots
        action1,action2=convert_actions(real)
        p1,p2=payoff_matrix[real]
        dataset.append({
            "Outcome": real,
            "Probability": round(prob, 3),
            "Trader 1's Action": action1,
            "Trader 2's Action": action2,
            "Trader 1's Payoff": p1,
            "Trader 2's Payoff": p2
        })
    table=pd.DataFrame(dataset)
    table=table.sort_values(by="Probability",ascending=False)
    return table
##graph that shows superposition

def graph(counts, shots):
    probs = [count / shots for count in counts.values()]
    labels = [flip_bitstring(bit) for bit in counts.keys()]

    fig, ax = plt.subplots()
    ax.bar(labels, probs)
    ax.set_xlabel("Outcome")
    ax.set_ylabel("Probability")
    ax.set_title("Quantum Outcome")

    return fig

##basic run game function

def run_simulation(angle_1, angle_2, entanglement, shots):
    qc = circuit(angle_1, angle_2, entanglement)
    counts, _ = compute(qc, shots)
    return counts

#### show entanglement

def show_entangle(angle_1, angle_2, shots):
    no_ent = run_simulation(angle_1, angle_2, False, shots)
    yes_ent = run_simulation(angle_1, angle_2, True, shots)

    all_bitstrings = sorted(set(no_ent.keys()) | set(yes_ent.keys()))
    flipped = [flip_bitstring(bit) for bit in all_bitstrings]
    prob_no = [no_ent.get(bit, 0) / shots for bit in all_bitstrings]
    prob_yes = [yes_ent.get(bit, 0) / shots for bit in all_bitstrings]

    x_axis = np.arange(len(flipped))

    fig, ax = plt.subplots()
    ax.bar(x_axis - 0.2, prob_no, width=0.4, label="No Entanglement")
    ax.bar(x_axis + 0.2, prob_yes, width=0.4, label="With Entanglement")
    ax.set_xticks(x_axis)
    ax.set_xticklabels(flipped)
    ax.set_xlabel("Final Outcome")
    ax.set_ylabel("Probability")
    ax.set_title("Entanglement Comparison")
    ax.legend()

    return fig


# def play_game():
#     mode, entanglement,shots,angle_1,angle_2=user_choices()
#     validate_choices(mode, entanglement,shots,angle_1,angle_2)
#     qc=circuit(angle_1,angle_2,entanglement)
#     counts,results=compute(qc,shots)
#     probs=shots_to_probs(shots,counts)
#     bitstring=most_likely_bitstring(counts)
#     flipped_bit=flip_bitstring(bitstring)
#     trader1_action, trader2_action=convert_actions(flipped_bit)
#     payoff_matrix={"00":(-1,-1),"10":(1,3),"01":(3,1),"11":(2,2)}
#     payoff_1,payoff_2=payoff(payoff_matrix,flipped_bit)
#     ep_1,ep_2=expected_payoff(counts,payoff_matrix,shots)
#     game_winner=winner(ep_1,ep_2)

#     print("Trader 1's angle:", angle_1)
#     print("Trader 2's angle:", angle_2)
#     print("Entanglement, yes or no:", entanglement)
#     print("Measurement values:", counts)
#     print("Probabilities:", probs)
#     print("Most likely outcome:", flipped_bit)
#     print("Trader 1's action:", trader1_action)
#     print("Trader 2's action:", trader2_action)
#     print("One round payoff:", payoff_1, payoff_2)
#     print("Expected payoff of trader 1:", ep_1)
#     print("Expected payoff of trader 2:", ep_2)
#     print("Winner based on expected payoff:", game_winner)
#     table=create_table(counts, payoff_matrix, shots)
#     print(table)
#     graph(counts,shots)
#     show_entangle(angle_1,angle_2,shots)
# print("Starting game")



def play_game():
    # Manual hardware result
    angle_1 = 0.000000
    angle_2 = 1.570700
    entanglement = False
    shots = 400

    counts = {'10': 205, '00': 194, '11': 1}
    results = None

    probs = shots_to_probs(shots, counts)
    bitstring = most_likely_bitstring(counts)
    flipped_bit = flip_bitstring(bitstring)
    trader1_action, trader2_action = convert_actions(flipped_bit)

    payoff_matrix = {"00": (-1, -1), "10": (1, 3), "01": (3, 1), "11": (2, 2)}

    payoff_1, payoff_2 = payoff(payoff_matrix, flipped_bit)
    ep_1, ep_2 = expected_payoff(counts, payoff_matrix, shots)
    game_winner = winner(ep_1, ep_2)

    print("\n" + "="*60)
    print("QUANTUM MARKET GAME - HARDWARE RESULTS")
    print("="*60)

    print(f"Trader 1 Angle: {angle_1:.6f} rad")
    print(f"Trader 2 Angle: {angle_2:.6f} rad")
    print(f"Entanglement Enabled: {entanglement}")
    print(f"Shots: {shots}")

    print("\nRAW COUNTS")
    for outcome, count in sorted(counts.items()):
        print(f"{flip_bitstring(outcome)} : {count}")

    print("\nPROBABILITIES")
    for outcome, prob in sorted(probs.items()):
        print(f"{flip_bitstring(outcome)} : {prob:.6f}")

    print("\nMOST LIKELY OUTCOME")
    print(f"Outcome: {flipped_bit}")
    print(f"Trader 1 Action: {trader1_action}")
    print(f"Trader 2 Action: {trader2_action}")

    print("\nSINGLE ROUND PAYOFF")
    print(f"Trader 1: {payoff_1}")
    print(f"Trader 2: {payoff_2}")

    print("\nEXPECTED PAYOFFS")
    print(f"Trader 1 Expected Payoff: {ep_1:.6f}")
    print(f"Trader 2 Expected Payoff: {ep_2:.6f}")

    print("\nWINNER")
    print(game_winner)

    print("\nOUTCOME TABLE")
    table = create_table(counts, payoff_matrix, shots)
    print(table.to_string(index=False))

    print("\nCSV DATA")
    print(f"{angle_1},{angle_2},{entanglement},{shots},{counts},{ep_1},{ep_2}")

    print("="*60)

    print("\nGENERATING GRAPH...")

    fig1 = graph(counts, shots)

    experiment_name = (
        f"a1_{angle_1:.2f}_a2_{angle_2:.2f}_"
        f"{'entangled' if entanglement else 'not_entangled'}"
    )

    fig1.savefig(
        f"hardware_results/{experiment_name}_probabilities.png",
        bbox_inches="tight",
        dpi=300
    )

    plt.show()
play_game()
