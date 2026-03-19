import csv
import os

explanations = {
    # TOPIC 1
    '101': "1. Count essential nodes where 3+ elements meet. 2. Count branches (components). 3. Apply the network topology equation: l = b - n + 1.",
    '102': "1. Redraw the circuit for switch position 1. 2. Calculate equivalent resistance and source current via Ohm's Law (I=V/R). 3. Repeat for switch position 2.",
    '103': "1. Determine total loop voltage and series current. 2. Apply Ohm's Law (R = V/I) to find the unknown resistance.",
    '104': "According to Ohm's Law (I = V/R), current is inversely proportional to resistance. If resistance doubles while voltage is constant, the current is halved.",
    '105': "Kirchhoff's Current Law (KCL) states that the total current entering a node equals the current leaving it. This is a direct consequence of the Conservation of Charge.",
    '106': "Kirchhoff's Voltage Law (KVL) states that the sum of electrical potential differences (voltages) around any closed circuit loop is zero.",
    '107': "Under the passive sign convention, power P = VI. If P is positive, power is absorbed. If P is negative, power is being supplied by the component.",
    '108': "A Thevenin equivalent circuit simplifies any linear circuit to a single independent voltage source (Vth) in series with a single resistor (Rth).",
    '109': "The Superposition Principle relies on linearity. It can only be applied to linear circuits, allowing you to consider independent sources one at a time.",
    '110': "The Norton resistance (Rn) is calculated in the exact same manner as Thevenin resistance (Rth) by turning off independent sources. Thus, Rn = Rth.",
    '111': "The Maximum Power Transfer Theorem states that maximum power is delivered to a load when its resistance (RL) equals the Thevenin resistance (Rth) of the source network.",
    '112': "1. Identify the meshes in the circuit. 2. Apply Kirchhoff's Voltage Law (KVL) around each mesh. 3. Solve the system of linear equations for i1, i2, and i3.",
    '113': "1. Select a reference node (ground). 2. Apply Kirchhoff's Current Law (KCL) at the essential nodes. 3. Solve the simultaneous equations for the node voltages V1-V4.",
    '114': "1. Use Nodal Analysis at node 1. 2. Write the KCL equation: sum of currents leaving = 0. 3. Solve algebraically for V1.",
    '115': "1. Define the variables v and ix. 2. Express the dependent source in terms of ix. 3. Use KVL or Nodal Analysis to solve for the exact values.",
    '116': "1. Apply Nodal Analysis. 2. If a voltage source connects two non-reference nodes, treat them as a supernode. 3. Solve the resulting equations for v1, v2, v3.",
    '117': "1. Simplify parallel/series resistors where appropriate. 2. Use Voltage Divider Rule or Nodal Analysis to calculate Vx explicitly.",
    '118': "1. Start from the far end opposite to the terminals. 2. Add resistors in series (R1+R2). 3. Combine resistors in parallel (R1*R2)/(R1+R2).",
    '119': "1. Try combining trivial series/parallel pairs first. 2. If blocked by a bridge structure, perform a Delta-Wye (or Wye-Delta) transformation, then reduce.",
    '120': "1. Identify the node containing Vx. 2. Apply KCL or Mesh Analysis around the dependent source to solve for Vx.",
    '121': "1. Find the voltage or current for the 25kOhm resistor explicitly using circuit analysis. 2. Apply Power equation: P = V^2 / R or P = I^2 * R.",
    '122': "1. Set up a nodal equation at the output node. 2. Account for dependent or independent sources. 3. Evaluate the equation to reveal Vo.",
    '123': "1. Combine parallel and series elements on the right. 2. Iteratively simplify backwards to terminals a-b. (Use Wye-Delta if applicable).",
    '124': "1. Determine Vo via Nodal Analysis. 2. Find the current flowing through the dependent source. 3. Power = Voltage drop * Current.",
    '125': "1. Assign mesh currents i1 to i4. 2. Write KVL for all four loops, being careful of shared branch currents. 3. Solve the 4x4 system.",
    '126': "1. Simplify the circuit using Thevenin's theorem or source transformations. 2. Solve for terminal voltage Vo and resulting current Io.",
    '127': "1. Use Superposition: turn off one source, analyze V and I. 2. Turn off the other, analyze V and I. 3. Sum the partial responses.",
    '128': "1. Recognize repeating identical patterns or symmetry. 2. Reduce Delta to Wye formations if it's a bridge, recognizing balanced nodes will have zero potential difference.",

    # TOPIC 2
    '201': "1. Parallel inductors combine like resistors: 1/L_eq = 1/L1 + 1/L2. 2. Series inductors combine like resistors: L_eq = L1 + L2.",
    '202': "In DC steady state, the voltage across a capacitor becomes constant (dV/dt = 0). Since I = C(dV/dt), current is 0, so it acts as an Open Circuit.",
    '203': "Energy stored in an inductor: E = 0.5 * L * I^2. 1. E = 0.5 * (4 * 10^-3) * (5)^2. 2. E = 0.5 * 0.004 * 25 = 0.05 Joules.",
    '204': "Capacitors in series combine like resistors in parallel: 1/Ceq = 1/C1 + 1/C2. Ceq = (10*10) / (10+10) = 5 uF.",
    '205': "An inductor's current cannot change instantaneously because its voltage v = L(di/dt) would be infinite. Thus, current just before toggling equals current just after.",
    '206': "1. Find Current: I_total = I_R + I_C = (V/R) + C(dV/dt). 2. Power = V * I_total. 3. Substitute V=45e^-2000t and compute derivative.",
    '207': "1. V(t) = 1/C * Int(i dt). Calculate integral from 0 to 3 of 8(2-e^-t). 2. Power at t=3: P = V(3) * I(3).",
    '208': "1. Parallel capacitors add together directly: Ceq = C1 + C2. 2. Series capacitors use the reciprocal sum: 1/Ceq = 1/C1 + 1/C2.",
    '209': "1. Inductor Voltage: v = L*(di/dt). 2. di/dt = (120mA - 40mA) / 3ms = 80mA / 3ms = 80/3 A/s. 3. 0.150V = L * (80/3). L = 5.625 mH.",
    '210': "1. Identify DC steady state: the capacitor acts as an open circuit. 2. Calculate the voltage drop across its terminals using Voltage Divider. 3. E = 0.5 * C * V^2.",
    '211': "1. Start away from terminals a-b. 2. Add series inductors (L=L1+L2). 3. Add parallel inductors (1/L = 1/L1+1/L2). 4. Simplify step-by-step to the terminals.",
    '212': "1. Coupling coefficient: k = M / sqrt(L1*L2). 2. Max value of M occurs when k is 1.0 (perfect coupling), so Max_M = sqrt(20 * 80) = 40 mH.",
    '213': "1. V(t) = V(0) + 1/C * Int(i dt). 2. V = 15 + (1/0.03) * (0.006 * 3). 3. V = 15 + (33.33 * 0.018) = 15.6 V.",
    '214': "1. DC Steady State: Capacitor is an open circuit; Inductor is a short circuit. 2. Solve for Vc and iL sequentially. 3. Energy = 0.5*C*Vc^2 + 0.5*L*iL^2.",
    '215': "1. Current i = C(dV/dt). 2. Use product rule to differentiate V = 5t e^-6t. 3. Substitute t=2 into V and i. 4. Compute Power = V * i.",
    '216': "1. Inductor voltage V = L(di/dt). 2. Differentiate 20e^-t/3. 3. Evaluate V and i at t=4. 4. Power = V * i.",
    '217': "1. i(t) = i(0) + 1/L * Int(V dt). 2. Integrate 40(1-e^-4t) from 0 to t=2. 3. Add initial 0.5A. 4. Calculate Energy E = 0.5 * L * i(2)^2."
}

filename = 'questions/QuestionBank.csv'
temp_file = 'questions/QuestionBank_temp.csv'

with open(filename, 'r', encoding='utf-8-sig', errors='replace') as infile, open(temp_file, 'w', encoding='utf-8-sig', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    if 'explanation' not in fieldnames:
        fieldnames.append('explanation')
        
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    count = 0
    for row in reader:
        if row['id'] in explanations:
            row['explanation'] = explanations[row['id']]
            count += 1
        writer.writerow(row)

print(f"Updated {count} explanations for Topics 1 and 2.")
import os
try:
    os.replace(temp_file, filename)
    print("Done! CSV successfully updated.")
except Exception as e:
    print(f"Failed to replace original file due to lock: {e}")
    print("Saved as QuestionBank_temp.csv instead.")
