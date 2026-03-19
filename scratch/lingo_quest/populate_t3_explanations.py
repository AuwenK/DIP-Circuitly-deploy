import csv

INPUT = 'questions/QuestionBank.csv'

EXPLANATIONS = {
    '301': (
        "The time constant of an RC circuit is τ = R × C. "
        "Here R = 10 kΩ = 10,000 Ω and C = 10 μF = 10×10⁻⁶ F. "
        "τ = 10,000 × 10×10⁻⁶ = 0.1 s. Answer: B."
    ),
    '302': (
        "A fundamental rule for capacitors: the voltage across a capacitor cannot change instantaneously. "
        "Therefore v_C(0⁺) = v_C(0⁻) = 5 V. The capacitor maintains its stored charge at the instant of switching. Answer: C."
    ),
    '303': (
        "In a charging RC circuit with a DC source V_s, the capacitor voltage follows: "
        "v_C(t) = V_s(1 - e^{-t/τ}). This is an exponential approach toward V_s — "
        "the voltage increases and gradually levels off (not linearly, not oscillating). Answer: B."
    ),
    '304': (
        "The time constant of an RL circuit is τ = L / R. "
        "Here L = 2 H and R = 5 Ω. "
        "τ = 2 / 5 = 0.4 s. Answer: D."
    ),
    '305': (
        "An ideal inductor obeys v = L(di/dt). The inductor current cannot change instantaneously "
        "because that would require infinite voltage. Therefore current is always continuous through an inductor. "
        "Voltage across an inductor CAN change instantaneously. Answer: B."
    ),
    '306': (
        "Just like capacitor voltage, inductor current cannot change instantaneously. "
        "At the moment of switching (t = 0⁺), the inductor current must equal its value just before switching (t = 0⁻): "
        "i_L(0⁺) = i_L(0⁻). This is the inductor continuity condition. Answer: C."
    ),
    '307': (
        "For a series RLC circuit, the damping condition depends on the discriminant R² - 4L/C. "
        "Underdamped: R² < 4L/C (complex roots → oscillatory response). "
        "Critically damped: R² = 4L/C. Overdamped: R² > 4L/C. "
        "Underdamped means R² < 4L/C. Answer: C."
    ),
    '308': (
        "The natural response is the circuit's behaviour due to energy initially stored in capacitors and inductors, "
        "with NO external sources applied. It depends only on initial conditions (stored energy), "
        "not on any external input. Answer: B."
    ),
    '309': (
        "A second-order circuit requires two independent energy-storage elements. "
        "Both an inductor (L) and a capacitor (C) are needed to produce a second-order differential equation "
        "and the characteristic transient response (exponential, oscillatory, or critically damped). Answer: C."
    ),
    '310': (
        "The transient component of any response decays as e^{-t/τ}. "
        "After 5τ, the exponential term e^{-5} ≈ 0.0067, which is less than 1% of its original value. "
        "Engineering convention: the transient is considered negligible after 5 time constants. Answer: C."
    ),
    '311': (
        "In sinusoidal steady-state (also called AC steady-state), all sources are sinusoidal at frequency ω. "
        "After all transients die out, every voltage and current in a linear circuit oscillates at exactly "
        "the same frequency as the source — only amplitude and phase differ. Answer: C."
    ),
    '312': (
        "For v(t) = V_m cos(ωt + φ), the phasor representation is V = V_m∠φ. "
        "Here v(t) = 10cos(100t + 30°), so V_m = 10 and φ = 30°. "
        "The phasor is 10∠30°. Answer: D."
    ),
    '313': (
        "The impedance of a capacitor in the frequency domain is Z_C = 1/(jωC). "
        "This comes from the capacitor's v-i relationship: i = C(dv/dt). "
        "In phasor form: I = jωC·V, so Z = V/I = 1/(jωC). Answer: B."
    ),
    '314': (
        "The impedance of an inductor in the frequency domain is Z_L = jωL. "
        "This comes from the inductor's v-i relationship: v = L(di/dt). "
        "In phasor form: V = jωL·I, so Z = V/I = jωL. Answer: C."
    ),
    '315': (
        "In a purely capacitive circuit, the current i = C(dv/dt). "
        "If v = V_m cos(ωt), then i = -ωCV_m sin(ωt) = ωCV_m cos(ωt + 90°). "
        "The current leads the voltage by 90°. Answer: B."
    ),
    '316': (
        "The instantaneous power in a pure inductor is p(t) = v·i. "
        "Averaged over a full cycle, the positive and negative half-cycles cancel exactly. "
        "A pure inductor stores and releases energy each cycle but dissipates zero average (real) power. Answer: C."
    ),
    '317': (
        "Power factor (pf) is defined as the cosine of the phase angle θ between voltage and current: "
        "pf = cos(θ). It represents the ratio of real power P to apparent power S: "
        "pf = P/S = cos(θ). The ratio V_rms/I_rms gives impedance magnitude |Z|, not pf. Answer: B."
    ),
    '318': (
        "Frequency response analysis studies how a circuit's output (gain and phase) varies as the "
        "input signal frequency is swept across a range. It reveals filter cutoff frequencies, "
        "resonance, and bandwidth — all as a function of frequency. Answer: D."
    ),
    '319': (
        "In an RC low-pass filter with R in series and C in parallel with the output: "
        "at low frequencies, the capacitor impedance 1/(jωC) is large → most voltage appears across C → pass. "
        "At high frequencies, the capacitor impedance is small → voltage across C drops → attenuate. "
        "The output is taken across the capacitor. Answer: B."
    ),
    '320': (
        "The complete (total) response of a linear circuit to any excitation is the sum of two components: "
        "1) The transient (natural) response: dies away with time, depends on initial conditions. "
        "2) The steady-state (forced) response: persists indefinitely, driven by the source. "
        "Total response = Transient + Steady-state. Answer: C."
    ),
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

print(f"Done. Wrote {count} explanations for Topic 3.")
