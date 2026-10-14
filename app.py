import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

st.set_page_config(page_title="Transistor to Qubit Lab", page_icon="⚛️", layout="wide")

st.markdown("""
<style>
.stApp {background: #081321; color: #edf5ff;}
[data-testid="stHeader"] {background: rgba(8,19,33,0.9);}
.block-container {padding-top: 1.8rem; max-width: 1200px;}
h1,h2,h3 {color: #eaf5ff;}
div[data-testid="stMetric"] {background:#122238;padding:14px;border:1px solid #29415d;border-radius:12px;}
div.stButton>button {border-radius:9px;font-weight:650;}
</style>
""", unsafe_allow_html=True)

st.title("⚛️ From Transistors to Qubits")
st.caption("EDC Assignment #2 · Interactive Transistor-to-Qubit Learning Framework")
st.markdown("Explore how transistor switching and digital logic relate to qubits, quantum gates, measurement, and noise.")

tab_a, tab_b, tab_c, tab_d, tab_noise = st.tabs([
    "A · Transistor", "B · Logic gates", "C · Quantum simulator", "D · Compare", "Noise & errors"
])

with tab_a:
    st.header("Module A — Transistor switching simulator")
    st.write("An idealized educational NPN-switch model. It illustrates switching; it is not a SPICE-accurate transistor simulation.")
    left, right = st.columns(2)
    with left:
        vin = st.slider("Base input voltage (V)", 0.0, 5.0, 0.0, 0.1)
        threshold = st.slider("Switching threshold (V)", 0.2, 1.5, 0.7, 0.1)
        resistance = st.slider("Load resistance (Ω)", 100, 1000, 330, 10)
    on = vin >= threshold
    current_ma = max(0.0, (5.0 - 2.0) / resistance * 1000) if on else 0.0
    with right:
        st.metric("Switch state", "ON" if on else "OFF")
        st.metric("LED output", "ON 🟢" if on else "OFF ⚫")
        st.metric("Classical output bit", "1" if on else "0")
        st.metric("Estimated load current", f"{current_ma:.2f} mA")
        st.progress(min(current_ma / 30.0, 1.0))
    st.info("Model assumption: 5 V supply, 2 V LED drop, and an ideal saturated switch. Real current depends on the actual circuit and transistor.")

with tab_b:
    st.header("Module B — Logic-gate simulator")
    gate = st.selectbox("Choose a logic gate", ["NOT", "AND", "OR", "NAND", "NOR", "XOR"])
    c1, c2, c3 = st.columns(3)
    with c1:
        a = st.radio("Input A", [0, 1], horizontal=True, key="logic_a")
    with c2:
        b = st.radio("Input B", [0, 1], horizontal=True, disabled=(gate == "NOT"), key="logic_b")
    def gate_output(name, x, y):
        if name == "NOT": return 1-x
        if name == "AND": return x & y
        if name == "OR": return x | y
        if name == "NAND": return 1-(x & y)
        if name == "NOR": return 1-(x | y)
        return x ^ y
    output = gate_output(gate, a, b)
    with c3:
        st.metric("Output", str(output))
    st.subheader(f"{gate} truth table")
    rows = []
    combos = [(0, 0), (1, 0)] if gate == "NOT" else [(0,0),(0,1),(1,0),(1,1)]
    for x, y in combos:
        rows.append({"A": x, **({} if gate == "NOT" else {"B": y}), "Output": gate_output(gate, x, y)})
    st.dataframe(rows, use_container_width=True, hide_index=True)
    explanations = {
        "NOT":"NOT reverses input A.", "AND":"AND is 1 only when both inputs are 1.",
        "OR":"OR is 1 when at least one input is 1.", "NAND":"NAND is the inverse of AND.",
        "NOR":"NOR is the inverse of OR.", "XOR":"XOR is 1 when the inputs are different."
    }
    st.caption(explanations[gate])

with tab_c:
    st.header("Module C — Quantum simulator using Qiskit")
    st.write("Apply quantum gates to a single qubit, inspect its statevector, and simulate measurements.")
    if "quantum_gates" not in st.session_state:
        st.session_state.quantum_gates = []
    q1, q2, q3 = st.columns([1,1,2])
    with q1:
        if st.button("Reset to |0⟩", use_container_width=True):
            st.session_state.quantum_gates = []
    with q2:
        if st.button("Prepare |1⟩", use_container_width=True):
            st.session_state.quantum_gates = ["X"]
    with q3:
        st.caption("Gate sequence: " + (" → ".join(st.session_state.quantum_gates) if st.session_state.quantum_gates else "none (initial |0⟩)"))
    g1, g2, g3 = st.columns(3)
    with g1:
        if st.button("Apply X gate", use_container_width=True):
            st.session_state.quantum_gates.append("X")
    with g2:
        if st.button("Apply H gate", use_container_width=True):
            st.session_state.quantum_gates.append("H")
    with g3:
        if st.button("Apply Z gate", use_container_width=True):
            st.session_state.quantum_gates.append("Z")

    qc = QuantumCircuit(1)
    for gate_name in st.session_state.quantum_gates:
        getattr(qc, gate_name.lower())(0)
    state = Statevector.from_instruction(qc)
    amplitudes = state.data
    p0, p1 = float(abs(amplitudes[0])**2), float(abs(amplitudes[1])**2)
    st.code(qc.draw(output="text"), language="text")
    st.latex(r"|\psi\rangle = \alpha|0\rangle + \beta|1\rangle")
    st.write(f"**Statevector:** α = `{amplitudes[0]:.3f}`, β = `{amplitudes[1]:.3f}`")
    m1, m2 = st.columns(2)
    m1.metric("P(0)", f"{p0*100:.1f}%")
    m2.metric("P(1)", f"{p1*100:.1f}%")
    st.progress(p0, text="Probability of measuring 0")
    st.progress(p1, text="Probability of measuring 1")
    shots = st.selectbox("Measurement shots", [10, 100, 500, 1000], index=1)
    if st.button("Measure / run shots"):
        outcomes = np.random.choice([0, 1], size=shots, p=[p0, p1])
        n0, n1 = int(np.sum(outcomes == 0)), int(np.sum(outcomes == 1))
        st.success(f"Completed {shots} simulated measurements: 0 = {n0} ({n0/shots*100:.1f}%), 1 = {n1} ({n1/shots*100:.1f}%).")
        st.bar_chart({"Observed counts": {"0": n0, "1": n1}})

    st.subheader("Two-qubit CNOT basis-state demonstration")
    c1, c2 = st.columns(2)
    with c1:
        control = st.selectbox("Control qubit", [0, 1], key="control")
    with c2:
        target = st.selectbox("Target qubit", [0, 1], key="target")
    if st.button("Apply CNOT"):
        cnot = QuantumCircuit(2)
        if control == 1: cnot.x(1)
        if target == 1: cnot.x(0)
        cnot.cx(1, 0)
        # Qiskit uses little-endian display ordering; this demo labels control and target explicitly.
        result_control = control
        result_target = target ^ control
        st.success(f"Control = {result_control}, target = {result_target} → basis output |{result_control}{result_target}⟩")
        st.code(cnot.draw(output="text"), language="text")
    st.info("This is a local Qiskit simulator, not a connection to IBM quantum hardware. It demonstrates ideal state evolution and measurement sampling.")

with tab_d:
    st.header("Module D — Classical vs quantum comparison")
    comparison = [
        {"Classical electronics": "Bit: logical value 0 or 1", "Quantum computing": "Qubit: α|0⟩ + β|1⟩"},
        {"Classical electronics": "Transistor can act as an electronic switch", "Quantum computing": "Qubit carries quantum information"},
        {"Classical electronics": "NOT gate flips a bit", "Quantum computing": "X gate flips computational basis states"},
        {"Classical electronics": "Logic gates operate on binary values", "Quantum computing": "Quantum gates transform quantum states"},
        {"Classical electronics": "Read output as a logic level", "Quantum computing": "Measurement returns a classical result"},
        {"Classical electronics": "Electrical noise can disturb voltage", "Quantum computing": "Quantum noise can cause errors; decoherence degrades coherence"},
        {"Classical electronics": "Ideal Boolean logic gives a definite output for fixed inputs", "Quantum computing": "Measurement may be probabilistic, depending on state and basis"},
    ]
    st.dataframe(comparison, use_container_width=True, hide_index=True)
    st.warning("The analogy has limits: a qubit is not simply a transistor or a classical bit. Quantum amplitudes, interference, and entanglement have no direct classical-bit equivalent.")

with tab_noise:
    st.header("Noise and quantum errors")
    st.subheader("Classical signal noise")
    noise = st.slider("Illustrative noise amplitude (V)", 0.0, 2.0, 0.3, 0.1)
    st.latex(r"V_{out}=V_{ideal}+n(t)")
    st.write(f"If the ideal output is 5.0 V, an illustrative range is {5-noise:.1f}–{5+noise:.1f} V.")
    st.subheader("Quantum error concepts")
    st.markdown("""
    - **Bit-flip error:** flips the computational basis value.
    - **Phase-flip error:** changes the relative phase of amplitudes.
    - **Depolarizing noise:** a model that randomly applies Pauli errors (X, Y, or Z).
    - **Quantum error correction:** encodes quantum information across multiple physical qubits to detect and correct errors.
    """)
    st.caption("The voltage range is illustrative, not a real measurement. Classical voltage noise and quantum decoherence are different physical phenomena.")

st.divider()
st.caption("EDC Assignment #2 · Transistor-to-Qubit Learning Framework · Python + Streamlit + NumPy + Qiskit")
