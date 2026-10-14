TRANSISTOR-TO-QUBIT WEBSITE (PYTHON VERSION)
============================================

This project uses Python, Streamlit, NumPy and Qiskit.

RUN ON WINDOWS
1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/ if Python is not installed.
   During installation, enable "Add Python to PATH".
2. Extract this ZIP.
3. Open the extracted folder.
4. Click the folder address bar in File Explorer, type cmd, and press Enter.
5. Run:
   py -m venv .venv
   .venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   streamlit run app.py
6. Your browser should open the local website. If it does not, open the local URL printed in the terminal (usually http://localhost:8501).

MODULES
A. Simplified transistor switch model (input voltage, threshold, load resistance, LED state, estimated current).
B. NOT, AND, OR, NAND, NOR, XOR gates and truth tables.
C. Qiskit statevector simulation using X, H, Z, measurement shots, and a CNOT basis-state demonstration.
D. Classical-vs-quantum comparison.
Additional noise and quantum-error section.

NOTES
- The transistor section is a simplified educational model, not SPICE or a physical transistor circuit.
- The quantum simulation uses Qiskit's local statevector simulator; it is not connected to IBM Quantum hardware.
- The assignment recommends physically building the classical circuit as well. Follow your instructor's requirements for physical circuit evidence and submission.
- Name the final ZIP using your student ID if required by the assignment.
