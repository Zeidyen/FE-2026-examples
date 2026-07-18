"""
plot_InsetChart.py

Python version of plot_InsetChart.Rmd. Reads the All_Age_InsetChart.csv produced
by the InsetChart analyzer (analyzer_W1.py) and saves four faceted figures
(infections, prevalence, climate & vectors, population) as PNG + PDF next to the
CSV. Channels are averaged over simulations at each Time step.

Run from anywhere:  python plot_InsetChart.py
"""

import os
import math
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # no display needed on the cluster
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Input location (edit these to point at your experiment's analyzer output)
# ---------------------------------------------------------------------------
root = os.path.expanduser("~/FE-2026-examples/experiments/my_outputs")
subfolder = "example_basic"
filename = "All_Age_InsetChart.csv"

# Groups of channels to plot, matching the R version. (label, [channels], ncol)
PLOT_GROUPS = [
    ("infections", [
        "30-day Avg Infection Duration", "Avg Num Infections", "Disease Deaths",
        "Infected", "New Clinical Cases", "New Infections", "New Severe Cases",
        "Newly Symptomatic", "Variant Fraction-PfEMP1 Major",
    ], 3),
    ("prevalence", [
        "Blood Smear Gametocyte Prevalence", "Blood Smear Parasite Prevalence",
        "Fever Prevalence", "Log Prevalence", "Mean Parasitemia",
        "PCR Gametocyte Prevalence", "PCR Parasite Prevalence",
        "PfHRP2 Prevalence", "True Prevalence",
    ], 3),
    ("climate_vectors", [
        "Adult Vectors", "Daily Bites per Human", "Daily EIR",
        "Human Infectious Reservoir", "Infectious Vectors", "Air Temperature",
        "Rainfall", "Relative Humidity",
    ], 2),
    ("population", [
        "Births", "Campaign Cost", "Statistical Population",
        "Symptomatic Population",
    ], 2),
]


def plot_group(df, channels, ncol, out_dir, out_base):
    """Faceted line plots (one panel per channel, free y-axis), mean over Time."""
    channels = [c for c in channels if c in df.columns]
    if not channels:
        print(f"  [skip] {out_base}: none of its channels are in the CSV")
        return

    # average across simulations at each Time step
    means = df.groupby("Time")[channels].mean().reset_index()

    nrow = math.ceil(len(channels) / ncol)
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.4 * ncol, 2.3 * nrow),
                             squeeze=False)
    colors = plt.get_cmap("tab10").colors

    for i, ch in enumerate(channels):
        ax = axes[i // ncol][i % ncol]
        ax.plot(means["Time"], means[ch], color=colors[i % len(colors)])
        ax.set_title(ch, fontsize=10)
        ax.tick_params(labelsize=8)
        ax.margins(x=0)

    # hide any unused panels
    for j in range(len(channels), nrow * ncol):
        axes[j // ncol][j % ncol].axis("off")

    fig.tight_layout()
    for ext in ("png", "pdf"):
        path = os.path.join(out_dir, f"All_Age_InsetChart_{out_base}.{ext}")
        fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [ok] All_Age_InsetChart_{out_base}.png / .pdf")


def main():
    out_dir = os.path.join(root, subfolder)
    csv_path = os.path.join(out_dir, filename)
    if not os.path.exists(csv_path):
        raise SystemExit(f"CSV not found: {csv_path}\n"
                         "Run the InsetChart analyzer (analyzer_W1.py) first, or "
                         "edit `root`/`subfolder` at the top of this script.")

    df = pd.read_csv(csv_path)
    print(f"Loaded {csv_path} ({len(df)} rows). Writing figures to {out_dir}")
    for label, channels, ncol in PLOT_GROUPS:
        plot_group(df, channels, ncol, out_dir, label)


if __name__ == "__main__":
    main()
