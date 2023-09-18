from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def generate_circuits_plus():
    # Initialize a quantum circuit with 1 qubit and 1 classical bit
    qc_plus = QuantumCircuit(1, 1)

    # |0> is the initial default state, to get the |+> state
    # we need to apply the Hadamard gate
    qc_plus.h(0) # H gate on qubit 0 = |+> state

    return qc_plus

def generate_circuits_minus():
    # To get a |-> state, we need to apply the Z gate on the |+> state
    qc_minus = generate_circuits_plus()
    qc_minus.z(0) # Z gate on qubit 0 = |-> state

    return qc_minus

def measure_in_plus_minus_basis(qc, qubit):
    """
    Adds gates to 'qc' to measure 'qubit' in the |+> and |-> basis.
    
    Parameters:
    qc (QuantumCircuit): The quantum circuit to modify.
    qubit (int): The index of the qubit to measure.
    """
    qc.h(qubit)  # Apply Hadamard gate
    qc.measure(qubit, qubit)  # Perform standard Z-basis measurement


def measure_in_Y_basis(qc, qubit):
    """
    Adds gates to 'qc' to measure 'qubit' in the Y-basis.
    
    Parameters:
    qc (QuantumCircuit): The quantum circuit to modify.
    qubit (int): The index of the qubit to measure.
    """
    qc.sdg(qubit)  # Apply S-dagger gate
    qc.h(qubit)    # Apply Hadamard gate
    qc.measure(qubit, qubit)  # Perform standard Z-basis measurement

def simulate(qc_list:list, label, legends, image_path=None):
    # Simulate the circuit
    simulator = Aer.get_backend('qasm_simulator')
    total_counts = []
    for qc in qc_list:
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit).result()
        counts = result.get_counts()
        total_counts.append(counts)

    # Plot the results
    plot_histogram(total_counts, legend=legends)
    plt.title(label)

    if image_path is None:
        plt.show()
        return
    
    plt.savefig(image_path)

def main(image_paths:list):
    # Excercice 1
    # Generate the circuits
    qc_plus = generate_circuits_plus()

    measure_in_plus_minus_basis(qc_plus, 0)

    image_path = image_paths[0] if len(image_paths) > 0 else None
    simulate([qc_plus], "Ejercicio 1", ["|+>"], image_path)

    # Excercice 2
    qc_plus = generate_circuits_plus()
    qc_minus = generate_circuits_minus()

    # Perform standard Z-basis measurement
    qc_plus.measure(0, 0)
    qc_minus.measure(0, 0)

    image_path = image_paths[1] if len(image_paths) > 1 else None
    simulate([qc_plus, qc_minus], "Medicion en Z", ["|+>", "|->"], image_path)

    # Excercice 3
    qc_plus = generate_circuits_plus()
    qc_minus = generate_circuits_minus()

    # Perform standard Z-basis measurement
    measure_in_Y_basis(qc_plus, 0)
    measure_in_Y_basis(qc_minus, 0)

    image_path = image_paths[1] if len(image_paths) > 1 else None
    simulate([qc_plus, qc_minus], "Mediciones en Y", ["|+>", "|->"], image_path)

if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
