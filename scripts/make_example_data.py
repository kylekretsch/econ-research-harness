"""Generate the synthetic staggered-DiD panel in data/raw/example/ (true effect = 2.0). Demo only."""

import numpy as np
import pandas as pd

from econ.config import RAW, SEED

rng = np.random.default_rng(SEED)
states, years = 50, range(2000, 2021)
first_treat = rng.choice([0, 2008, 2012, 2016], size=states, p=[0.4, 0.2, 0.2, 0.2])
alpha = rng.normal(0, 2, states)
rows = []
for s in range(states):
    for t in years:
        treated = first_treat[s] > 0 and t >= first_treat[s]
        y = 10 + alpha[s] + 0.1 * (t - 2000) + 2.0 * treated + rng.normal(0, 1)
        rows.append((f"S{s:02d}", t, int(first_treat[s]), round(y, 4)))
out = RAW / "example" / "example_panel.csv"
out.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows, columns=["state", "year", "first_treat", "y"]).to_csv(out, index=False)
print(f"wrote {out}")
