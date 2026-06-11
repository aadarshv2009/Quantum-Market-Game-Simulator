import streamlit as st
import numpy as np
import pandas as pd
from simulator import run_simulation, create_table, expected_payoff, winner, payoff_matrix,show_entangle,graph,circuit
st.set_page_config(page_title="Quantum Game Theory Simulator",layout="wide")
if "game_started" not in st.session_state:
    st.session_state.game_started = False
with st.sidebar:
    if st.button("Restart Game"):
        st.rerun()
st.info("""This game models two traders that make buy/sell decision using quantum properties.
Each trader chooses an angle θ: θ closer to 0 means mostly sell, θ closer to π means mostly buy, while θ closer to π/2 means mixed strategy.
Quantum entanglement changes how traders interact with each other, correlating their actions.""")
def strategy(angle):
    if angle<(np.pi /2):
        return " a higher probability of selling"
    elif angle>(np.pi/2):
        return " a higher probability of buying"
    else:
        return (" equal Strategy")
st.markdown("""
<style>

.main-title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    text-align: center;
    color: #666;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">Quantum Game Theory Simulator</div>',
    unsafe_allow_html=True
)
if not st.session_state.game_started:
    st.markdown("""
    <div id="setup-screen">
    """, unsafe_allow_html=True)
    with st.expander("Game Rules"):
        st.write("""
        00 = Both traders sell  
        01 = Trader 1 sells, Trader 2 buys  
        10 = Trader 1 buys, Trader 2 sells  
        11 = Both traders buy
        """)

        st.subheader("Payoff Matrix")

        payoffs = pd.DataFrame({
            "Outcome": ["00", "01", "10", "11"],
            "Trader 1 Payoff": [-1, 3, 1, 2],
            "Trader 2 Payoff": [-1, 1, 3, 2]
        })

        st.table(payoffs)

    st.markdown(
        '<div class="subtitle">Explore how superposition and entanglement affect trading decisions and expected market outcomes.</div>',
        unsafe_allow_html=True
    )



    mode=st.sidebar.selectbox("Choose mode", ["Random vs Random","User vs Random","User vs User"])
    Entanglement=st.sidebar.checkbox("Enable Entanglement",help="With entanglement enabled, the actions of one trader affects the other trader's actions.")  
    shots=st.sidebar.slider("Number of shots:", 100,10000,1000,help="More shots increases the accuracy of the measurements")



    if "angle_1" not in st.session_state:
        st.session_state.angle_1 = np.random.uniform(0, np.pi)

    if "angle_2" not in st.session_state:
        st.session_state.angle_2 = np.random.uniform(0, np.pi)
    if st.sidebar.button("New Angles"):
        st.session_state.angle_1 = np.random.uniform(0, np.pi)
        st.session_state.angle_2 = np.random.uniform(0, np.pi)
    if (mode=="Random vs Random"):
        angle_1 = st.session_state.angle_1
        angle_2 = st.session_state.angle_2
    elif (mode=="User vs Random"):
        angle_1=st.sidebar.slider("Trader 1 angle",0.0,3.14159,1.57)
        angle_2=st.session_state.angle_2
    elif(mode=="User vs User"):
        angle_1=st.sidebar.slider("Trader 1 User Chosen Angle",0.0,3.14159,1.57)
        angle_2=st.sidebar.slider("Trader 2 User Chosen Angle",0.0,3.14159,1.57)
    if st.sidebar.button("Start Game"):
        st.session_state.game_started = True
        st.session_state.angle_1_final = angle_1
        st.session_state.angle_2_final = angle_2
        st.session_state.entanglement_final = Entanglement
        st.session_state.shots_final = shots
        st.rerun()
    angle_col1, angle_col2 = st.columns(2)

    with angle_col1:
        st.markdown(
            f"""
            <div style="
                border:1px solid #d1d5db;
                border-radius:12px;
                padding:12px;
                text-align:center;
                font-size:28px;
                font-weight:700;
                color:#2563eb;
                background-color:#f8fafc;
            ">
            Trader 1 Angle: θ = {angle_1:.3f}
            </div>
            """,
            unsafe_allow_html=True
        )

    with angle_col2:
        st.markdown(
            f"""
            <div style="
                border:1px solid #d1d5db;
                border-radius:12px;
                padding:12px;
                text-align:center;
                font-size:28px;
                font-weight:700;
                color:#dc2626;
                background-color:#f8fafc;
            ">
            Trader 2 Angle: θ = {angle_2:.3f}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    col1, col2, col3 = st.columns([1, 0.18, 1])

    with col1:
        with st.container(border=True):



            left1, center1, right1 = st.columns([1,2,1])

            with center1:
                st.image("real_bull.png", width=250)

            st.markdown(
                "<h2 style='text-align:center;'>Trader 1 — Bull</h2>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; color:gray;'>Buy Strategy</p>",
                unsafe_allow_html=True
            )
    with col2:
        st.markdown(
        """
        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            height:100%;
            min-height:520px;
            font-size:70px;
            font-weight:800;
        ">
        VS
        </div>
        """,
        unsafe_allow_html=True
    )

    with col3:
        with st.container(border=True):


            left2, center2, right2 = st.columns([1,2,1])

            with center2:
                st.image("real_bear.png", width=250)

            st.markdown(
                "<h2 style='text-align:center;'>Trader 2 — Bear</h2>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; color:gray;'>Sell Strategy</p>",
                unsafe_allow_html=True
            )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    angle_1 = st.session_state.angle_1_final
    angle_2 = st.session_state.angle_2_final
    Entanglement = st.session_state.entanglement_final
    shots = st.session_state.shots_final
    with st.expander("Game Setup"):
        st.write(f"Trader 1 Angle: {angle_1:.3f}")
        st.write(f"Trader 2 Angle: {angle_2:.3f}")
        st.write(f"Entanglement: {Entanglement}")
        st.write(f"Shots: {shots}")
    st.markdown(
        "<h1 style='text-align:center;'>Results</h1>",
        unsafe_allow_html=True
    )
    angle_1 = st.session_state.angle_1_final
    angle_2 = st.session_state.angle_2_final
    Entanglement = st.session_state.entanglement_final
    shots = st.session_state.shots_final
    tab1,tab2,tab3,tab4=st.tabs(["Results","Graphs", "Explanation","Real Quantum Computing"])
    data=run_simulation(angle_1,angle_2,Entanglement,shots)
    pay_1,pay_2=expected_payoff(data,payoff_matrix,shots)
    game_winner=winner(pay_1,pay_2)
    table = create_table(data, payoff_matrix, shots)
    graph_data=graph(data,shots)
    entanglement_viz=show_entangle(angle_1,angle_2,shots)
    prob_1_sell=np.cos(angle_1/2)**2
    prob_1_buy=np.sin(angle_1/2)**2
    prob_2_sell=np.cos(angle_2/2)**2
    prob_2_buy=np.sin(angle_2/2)**2
   
    with tab1:
        col_pay1,col_pay2,col_win=st.columns(3)
        col_pay1.metric("Trader 1 Expected Payoff:", round(pay_1,4))
        col_pay2.metric("Trader 2 Expected Payoff:", round(pay_2,4))
        col_win.metric("Winner",game_winner)
        if pay_1>pay_2:
            st.success("Trader 1 had a better strategy for this round")
        elif pay_2>pay_1:
            st.success("Trader 2 had a better strategy for this round")

        st.subheader("Data Table")
        st.dataframe(table,use_container_width=True)
        with st.expander("Key"):
            st.markdown("""
            - 00: Both Traders Sell
            - 01: Trader 1 Sells and Trader 2 Buys
            - 10: Trader 1 Buys and Trader 2 Sells
            - 11: Both Traders Buy
            """)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Trader 1 Strategy")
            st.metric("Sell Probability", f"{prob_1_sell:.2%}")
            st.metric("Buy Probability", f"{prob_1_buy:.2%}")

        with col2:
            st.subheader("Trader 2 Strategy")
            st.metric("Sell Probability", f"{prob_2_sell:.2%}")
            st.metric("Buy Probability", f"{prob_2_buy:.2%}")
        st.info(f""" Trader 1 has {strategy(angle_1)}""")
        st.info(f""" Trader 2 has {strategy(angle_2)}""")
    with st.expander("Raw Counts"):
        st.write(data)
    with tab2:
        st.subheader("Circuit Visualization")

        quant = circuit(angle_1, angle_2, Entanglement)

        circuit_text = str(quant.draw(output="text"))

        st.code(circuit_text, language=None)
        st.subheader("Entanglement Visualization")
        st.pyplot(entanglement_viz)
        st.subheader("Data Graph")
        st.pyplot(graph_data)
    

    with tab3:
        st.header("Why Quantum?")
        st.write("""
         In classical game theory, traders make concrete decisions: either buy or sell.
        
        Quantum game theory allows traders to exist in a *superposition* of decisions until the game is ran or "measured".

        Instead of set decisions, traders use probability driven strategies that can lead to multiple different outcomes."""
        )
        with st.expander("What is Superposition?"):
            st.write("Superposition is a quantum state where both the 0 and 1 state exist together. In this game, the traders are in a superposition between buy and sell. The trader is not \"forced\" to pick a state until the circuit is measured or the game is ran. This allows the game to be based on probability distributions rather than solid outcomes. ")
        with st.expander("What is entanglement"):
            st.write("Entanglement is a correlation between two qubits as a result of quantum mechanics. When entanglement is enabled in the game, both traders' actions affect the other's action. This potentially changes the probability distribution of outcomes and affect the expected payoffs.")   
        st.subheader("Classical vs Quantum")
        col1,col2=st.columns(2)
        with col1:
            st.markdown("""
            ### Classical Trader
            - Buy or Sell

            -Fixed decision making process

            -Predictable decisions
            """)
        with col2:
            st.markdown("""
            ### Quantum Trader
            -Buy and sell probabilities

            -Incorporates superposition

            -Incoporates entanglement
            """)
        st.subheader("What is θ?")
        st.write("""
        The angle θ controls the decisions of the traders.

        - θ near 0 means mostly Sell
        - θ near π means mostly Buy
        - θ near π/2 means mixed    
        """)
        st.header('Understanding the Results')
        st.write("The expected payoff is calculated from a weighted average of the probability of a trader picking a certain action and the action's payoff. Even though each action's payoff is a whole number, the weighted average causes the expected payoff to be a decimal.")
        st.subheader("Meaning of Higher Expected Payoff")
        st.write("A higher expected payoff means that over multiple games with the same angles, the winning trader achieved higher rewards than the losing trader")
        st.subheader("Compare Strategies")
        st.write(" Change the traders angles and rerun the simulation. Notice how the outcome probabiltiies change, how the expected payoffs change, and how entanglement affects the results. ")
    with tab4:
        st.header("Real Quantum Computing")

        st.write(
            "We tested the game beyond noiseless simulation by running experiments on IonQ Forte Enterprise hardware."
            " We used 400 shots for each run, meaning that the circuit ran through 400 iterations to calculate the measurement probabilities. Try running the game with the same configurations as the real hardware to see the effect of noise on quantum results. "
        )

        hardware_runs = [
            {
                "Run": 1,
                "Title": "Run 1: Base Angles, No Entanglement",
                "Angle 1": 0.0000,
                "Angle 2": 1.5707,
                "Entanglement": False,
                "Shots": 400,
                "Counts": {"00": 214, "01": 186},
                "Probabilities": {"00": 0.535, "01": 0.465},
                "Most Likely Outcome": "00",
                "Trader 1 Action": "Sell",
                "Trader 2 Action": "Sell",
                "Trader 1 Expected Payoff": 0.8600,
                "Trader 2 Expected Payoff": -0.0700,
                "Winner": "Trader 1 Wins",
                "Graph": "hardware_results/run_1.png",
            },
            {
                "Run": 2,
                "Title": "Run 2: Base Angles, Entanglement",
                "Angle 1": 0.0000,
                "Angle 2": 1.5707,
                "Entanglement": True,
                "Shots": 400,
                "Counts": {"00": 202, "01": 198},
                "Probabilities": {"00": 0.505, "01": 0.495},
                "Most Likely Outcome": "00",
                "Trader 1 Action": "Sell",
                "Trader 2 Action": "Sell",
                "Trader 1 Expected Payoff": 0.9800,
                "Trader 2 Expected Payoff": -0.0100,
                "Winner": "Trader 1 Wins",
                "Graph": "hardware_results/run_2.png",
            },
            {
                "Run": 3,
                "Title": "Run 3: Asymmetric Angles, No Entanglement",
                "Angle 1": 1.2874,
                "Angle 2": 2.5892,
                "Entanglement": False,
                "Shots": 400,
                "Counts": {"00": 20, "10": 8, "01": 234, "11": 138},
                "Probabilities": {"00": 0.050, "10": 0.020, "01": 0.585, "11": 0.345},
                "Most Likely Outcome": "01",
                "Trader 1 Action": "Sell",
                "Trader 2 Action": "Buy",
                "Trader 1 Expected Payoff": 2.4150,
                "Trader 2 Expected Payoff": 1.2850,
                "Winner": "Trader 1 Wins",
                "Graph": "hardware_results/run_3.png",
            },
            {
                "Run": 4,
                "Title": "Run 4: Asymmetric Angles, Entanglement",
                "Angle 1": 1.2874,
                "Angle 2": 2.5892,
                "Entanglement": True,
                "Shots": 400,
                "Counts": {"00": 34, "10": 101, "01": 257, "11": 8},
                "Probabilities": {"00": 0.085, "10": 0.2525, "01": 0.6425, "11": 0.020},
                "Most Likely Outcome": "01",
                "Trader 1 Action": "Sell",
                "Trader 2 Action": "Buy",
                "Trader 1 Expected Payoff": 2.1350,
                "Trader 2 Expected Payoff": 1.3550,
                "Winner": "Trader 1 Wins",
                "Graph": "hardware_results/run_4.png",
            },
            {
                "Run": 5,
                "Title": "Run 5: Balanced Superposition, No Entanglement",
                "Angle 1": 1.5707,
                "Angle 2": 1.5707,
                "Entanglement": False,
                "Shots": 400,
                "Counts": {"00": 89, "10": 103, "01": 113, "11": 95},
                "Probabilities": {"00": 0.2225, "10": 0.2575, "01": 0.2825, "11": 0.2375},
                "Most Likely Outcome": "01",
                "Trader 1 Action": "Sell",
                "Trader 2 Action": "Buy",
                "Trader 1 Expected Payoff": 1.3575,
                "Trader 2 Expected Payoff": 1.3075,
                "Winner": "Trader 1 Wins",
                "Graph": "hardware_results/run_5.png",
            },
            {
                "Run": 6,
                "Title": "Run 6: Balanced Superposition, Entanglement",
                "Angle 1": 1.5707,
                "Angle 2": 1.5707,
                "Entanglement": True,
                "Shots": 400,
                "Counts": {"00": 94, "10": 107, "01": 125, "11": 74},
                "Probabilities": {"00": 0.235, "10": 0.2675, "01": 0.3125, "11": 0.185},
                "Most Likely Outcome": "01",
                "Trader 1 Action": "Sell",
                "Trader 2 Action": "Buy",
                "Trader 1 Expected Payoff": 1.3400,
                "Trader 2 Expected Payoff": 1.2500,
                "Winner": "Trader 1 Wins",
                "Graph": "hardware_results/run_6.png",
            },
        ]

        st.subheader("Hardware Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Backend", "IonQ Forte")
        with col2:
            st.metric("Hardware Type", "Trapped Ion")
        with col3:
            st.metric("Total Runs", "6")
        with col4:
            st.metric("Shots per Run", "400")

        st.subheader("Hardware Run Summary")

        summary_df = pd.DataFrame([
            {
                "Run": run["Run"],
                "θ₁": run["Angle 1"],
                "θ₂": run["Angle 2"],
                "Entanglement": "On" if run["Entanglement"] else "Off",
                "Most Likely Outcome": run["Most Likely Outcome"],
                "Trader 1 EP": run["Trader 1 Expected Payoff"],
                "Trader 2 EP": run["Trader 2 Expected Payoff"],
                "Winner": run["Winner"],
            }
            for run in hardware_runs
        ])

        st.dataframe(summary_df, use_container_width=True)

        st.subheader("Individual Hardware Runs")

        selected_title = st.selectbox(
            "Select a run",
            [run["Title"] for run in hardware_runs]
        )

        selected_run = next(run for run in hardware_runs if run["Title"] == selected_title)

        st.markdown(f"### {selected_run['Title']}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Trader 1 Angle", f"{selected_run['Angle 1']:.4f} rad")
            st.metric("Trader 2 Angle", f"{selected_run['Angle 2']:.4f} rad")

        with col2:
            st.metric("Shots", selected_run["Shots"])
            st.metric("Entanglement", "On" if selected_run["Entanglement"] else "Off")

        with col3:
            st.metric("Most Likely Outcome", selected_run["Most Likely Outcome"])
            st.metric("Winner", selected_run["Winner"])

        st.markdown("### Probability Graph")
        st.image(selected_run["Graph"], use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Raw Counts")
            counts_df = pd.DataFrame([
                {"Outcome": outcome, "Count": count}
                for outcome, count in selected_run["Counts"].items()
            ])
            st.dataframe(counts_df, use_container_width=True)

        with col2:
            st.markdown("### Probabilities")
            prob_df = pd.DataFrame([
                {"Outcome": outcome, "Probability": prob}
                for outcome, prob in selected_run["Probabilities"].items()
            ])
            st.dataframe(prob_df, use_container_width=True)

        st.markdown("### Game Results")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Trader Actions**")
            st.write(f"Trader 1: {selected_run['Trader 1 Action']}")
            st.write(f"Trader 2: {selected_run['Trader 2 Action']}")

        with col2:
            st.write("**Expected Payoffs**")
            st.write(f"Trader 1: {selected_run['Trader 1 Expected Payoff']:.4f}")
            st.write(f"Trader 2: {selected_run['Trader 2 Expected Payoff']:.4f}")

        st.subheader("Entanglement's Impact")

        entanglement_pairs = pd.DataFrame([
            {
                "Circuit Angles": "(0.0000, 1.5707)",
                "No Entanglement EP1": 0.8600,
                "Entanglement EP1": 0.9800,
                "Change in EP1": 0.1200,
                "No Entanglement EP2": -0.0700,
                "Entanglement EP2": -0.0100,
                "Change in EP2": 0.0600,
            },
            {
                "Circuit Angles": "(1.2874, 2.5892)",
                "No Entanglement EP1": 2.4150,
                "Entanglement EP1": 2.1350,
                "Change in EP1": -0.2800,
                "No Entanglement EP2": 1.2850,
                "Entanglement EP2": 1.3550,
                "Change in EP2": 0.0700,
            },
            {
                "Circuit Angles": "(1.5707, 1.5707)",
                "No Entanglement EP1": 1.3575,
                "Entanglement EP1": 1.3400,
                "Change in EP1": -0.0175,
                "No Entanglement EP2": 1.3075,
                "Entanglement EP2": 1.2500,
                "Change in EP2": -0.0575,
            },
        ])

        st.dataframe(entanglement_pairs, use_container_width=True)

        st.write(
            "We tested each angle pair two times: once without entanglement and once with entanglement."
            " This allows users to see the effect of entanglement on real quantum hardware while factoring in noise."
        )
        with st.expander("View full hardware run data"):
            for run in hardware_runs:
                st.markdown(f"### {run['Title']}")
                st.json(run)
            
        
