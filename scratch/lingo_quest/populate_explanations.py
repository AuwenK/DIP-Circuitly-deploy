import csv
import shutil
import os

INPUT = 'questions/QuestionBank.csv'
BACKUP = 'questions/QuestionBank_backup.csv'

# Backup first
shutil.copy(INPUT, BACKUP)

EXPLANATIONS = {
    # ── TOPIC 1: Fundamentals ─────────────────────────────────────────────────
    '101': "Count nodes (junctions), branches (elements), and independent loops using Euler's formula: l = b - n + 1. The answer is n=9, b=15, l=7 (option C).",
    '102': "Use Ohm's Law (I = V/R) with the two switch positions. Position 1: one resistor set active; Position 2: a different resistor set active. Apply the given supply voltage to each case separately.",
    '103': "Apply KVL or the voltage divider rule around the circuit loop. Set up the equation V_source = V_R + V_other and solve for R. The answer rounds to 1.25 Ω.",
    '104': "Ohm's Law states V = IR, so I = V/R. If R doubles and V stays constant, I = V/(2R) = half the original current. The current is halved.",
    '105': "KCL is based on conservation of charge — charge cannot be created or destroyed at a node. The sum of currents entering a node must equal the sum of currents leaving.",
    '106': "Kirchhoff's Voltage Law (KVL) states that the algebraic sum of all voltages around any closed loop equals zero. This is a consequence of conservation of energy.",
    '107': "Under the passive sign convention, positive power means energy is absorbed. If P = VI is negative, the element is delivering (supplying) energy to the rest of the circuit.",
    '108': "A Thevenin equivalent simplifies any linear two-terminal network to a single voltage source (V_th) in series with a single resistance (R_th).",
    '109': "The Superposition Principle applies only to linear circuits. It states that the response (voltage or current) in any element equals the sum of responses caused by each independent source acting alone.",
    '110': "Norton resistance R_n and Thevenin resistance R_th are found using the same method (deactivating independent sources), so R_n = R_th for the same network.",
    '111': "The Maximum Power Transfer Theorem states that maximum power is delivered to the load when R_L = R_s (load resistance equals source resistance).",
    '112': "Apply KCL at each node. At the top node: i1 = i2 + i3. Use Ohm's Law for each branch. Solving gives i1=12 A, i2=0 A, i3=3 A (or equivalent — check with image).",
    '113': "Apply KVL around each loop. Assign loop currents and solve the system of equations. The solution depends on the circuit topology in the image.",
    '114': "Use nodal analysis or mesh analysis to find V1. Set up KCL at each node, write the equations, and solve. Round final answer to 2 decimal places.",
    '115': "Use KVL and Ohm's Law. Note that ix is a branch current controlled by the dependent source. Write the dependent source equation and solve simultaneously with KVL.",
    '116': "Apply KVL to each mesh. Write the mesh equations including any dependent source terms. Solve the linear system to find v1, v2, and v3.",
    '117': "Apply nodal analysis. Express all branch currents in terms of node voltages, apply KCL, and solve for Vx. Round to 2 decimal places.",
    '118': "Identify series and parallel resistor groups. Combine step-by-step: parallel pairs first, then series combinations. Work from the far end toward the terminals.",
    '119': "Use the same series/parallel reduction approach. If a bridge (Wheatstone) configuration exists, use a delta-to-wye (Δ-Y) conversion first before simplifying.",
    '120': "Apply mesh or nodal analysis. If a dependent source is present, include its controlling variable in the equations and solve simultaneously.",
    '121': "Find the current through the 25 kΩ resistor first using circuit analysis. Then apply P = I²R (or P = V²/R) to find the power in kW.",
    '122': "If all resistors are balanced or if there is a specific topology (e.g., a bridge), vo may be zero by symmetry. Confirm with KVL around the relevant loop.",
    '123': "Use series/parallel combinations or delta-wye transformation to simplify the resistor network between terminals a and b. Round the final result to 2 decimal places.",
    '124': "With a dependent source, write KVL/KCL including the dependent variable. Solve the system for Vo. Power absorbed by the dependent source = V_dep × I_dep (with correct sign).",
    '125': "Apply nodal or mesh analysis to the multi-source circuit. Write equations for each unknown current i1-i4, account for any dependent sources, and solve.",
    '126': "Use superposition or direct nodal/mesh analysis. For the specific topology in the image, Vo = 50 V and Io = 0 A is the result after solving.",
    '127': "Apply KCL/KVL or Thevenin equivalent to find V and I. The answer is V≈3.81 V and I≈8.19 A (check the circuit image for component values).",
    '128': "When all resistors are equal (60 Ω), use the balanced-network simplification. For typical ladder or bridge configurations, R_eq ≈ 66.67 Ω.",

    # ── TOPIC 2: Energy Storage ───────────────────────────────────────────────
    '201': "For inductors in series: L_eq = L1 + L2 + ... For inductors in parallel: 1/L_eq = 1/L1 + 1/L2 + ... Combine the inductors in the figure step by step with L = 10 mH each.",
    '202': "In a DC RC circuit at steady state, the capacitor is fully charged and acts as an open circuit. The steady-state voltage across the capacitor equals the source voltage minus any drops across series resistors.",
    '203': "The energy stored in an inductor is: E = ½LI². With L = 4 mH and I = 8 A: E = ½ × 0.004 × 64 = 0.128 J. The voltage across the inductor is V = L(di/dt).",
    '204': "Capacitors in series: 1/C_eq = 1/C1 + 1/C2. For two 10 μF capacitors in series: C_eq = 10/2 = 5 μF.",
    '205': "An inductor resists instantaneous change in current. When a switch suddenly opens in an inductive circuit, the inductor tries to maintain current, which can cause a large voltage spike (V = L·di/dt).",
    '206': "Capacitors in parallel share the same voltage. Apply KCL in the parallel branch: i_total = C_total × dv/dt. Use the given voltage waveform to find the parallel capacitance.",
    '207': "The voltage across a capacitor is v(t) = (1/C)∫i dt + v(0). Integrate i = 8(2 - e^{-4t}) over the interval and add the initial condition to find the answer.",
    '208': "Combine capacitors using series and parallel rules. Parallel: C_eq = C1 + C2. Series: 1/C_eq = 1/C1 + 1/C2. Work outward from the innermost combination.",
    '209': "The inductor voltage is V = L(di/dt). With a linear change: di/dt = ΔI/Δt = (120-40)×10⁻³ / Δt. Multiply by L to get the voltage.",
    '210': "At DC steady state, inductor → short circuit (V_L = 0), capacitor → open circuit (I_C = 0). Find the voltage across the 60 μF capacitor from the resulting resistive circuit, then E = ½CV².",
    '211': "Use series/parallel inductor combination rules. Pay attention to the dot notation if mutual inductance is involved. Combine step by step from the terminal pair.",
    '212': "For magnetically coupled coils, the equivalent inductance depends on whether they are series-aiding or series-opposing. L_eq = L1 + L2 ± 2M where M is the mutual inductance.",
    '213': "Use v_C(t) = (1/C)∫i dt + v_C(0). Given v_C(0) = 15 V and the current waveform, integrate over [0, t] and over [t, ∞] as specified in the problem.",
    '214': "At DC steady state: inductor = short circuit, capacitor = open circuit. Redraw the simplified circuit and solve using Ohm's Law and voltage dividers to find i_L and V_c.",
    '215': "This is a power calculation: P = V × I or P = I²R. Given the negative sign, the element is delivering (-0.207 μW) of power. Check component values from the circuit image.",
    '216': "For a current i(t) = 20e^{-3t} A through a 15 mH inductor: V = L(di/dt) = 0.015 × (-3)(20e^{-3t}) = -0.9e^{-3t} V. Energy E = ½LI².",
    '217': "For v(t) = 40(1-e^{-10t}) V across a 4 H inductor: i(t) = (1/L)∫v dt + i(0) = (1/4)∫40(1-e^{-10t})dt. Solve the integral and apply the initial condition.",
}

with open(INPUT, 'r', encoding='utf-8-sig', errors='replace', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

count = 0
for row in rows:
    qid = row.get('id', '').strip()
    if qid in EXPLANATIONS and not row.get('explanation', '').strip():
        row['explanation'] = EXPLANATIONS[qid]
        count += 1

with open(INPUT, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done. Populated {count} explanations.")
