import ROOT as r
from copy import deepcopy
import matplotlib.pyplot as plt
from mplhep import style
from matplotlib.colors import Normalize
import numpy as np

plt.style.use(style.CMS)
cmap = plt.get_cmap("viridis").copy()
cmap.set_under("#e9e9e9")
norm = Normalize(vmin=0.0001, vmax=1, clip=False)

r.gStyle.SetOptStat(0)

def safe_div(n, d):
    return n / d if d else 0.0


folder = "."
histo_name = "shower_tpfptnfn_MBX"
print(f"Loading histogram {histo_name} from file...")
f = r.TFile.Open("../histograms/histograms.root")
pre, pos = histo_name.split("MB")
histos = [deepcopy(f.Get(f"{pre}MB{ist}{pos[1:]}")) for ist in range(1, 5)]
f.Close()

conf_map = np.zeros((8, 10))
totals = np.zeros((4, 5))
counts = np.zeros((4, 5, 4))  # [station, wheel, (TP, FP, TN, FN)]

# Global totals
TP_sum = 0.0
FP_sum = 0.0
TN_sum = 0.0
FN_sum = 0.0

for st, h in enumerate(histos):
    for iWheel in range(0, 5):
        tp = h.GetBinContent(iWheel + 1, 1)
        fp = h.GetBinContent(iWheel + 1, 2)
        tn = h.GetBinContent(iWheel + 1, 3)
        fn = h.GetBinContent(iWheel + 1, 4)

        # Accumulate global totals
        TP_sum += tp
        FP_sum += fp
        TN_sum += tn
        FN_sum += fn

        total = tp + fp + tn + fn
        conf_map[st * 2, iWheel * 2] = safe_div(tp, total)
        conf_map[(st * 2) + 1, iWheel * 2] = safe_div(fp, total)
        conf_map[st * 2, (iWheel * 2) + 1] = safe_div(tn, total)
        conf_map[(st * 2) + 1, (iWheel * 2) + 1] = safe_div(fn, total)
        totals[st, iWheel] = total
        counts[st, iWheel, 0] = tp
        counts[st, iWheel, 1] = fp
        counts[st, iWheel, 2] = tn
        counts[st, iWheel, 3] = fn

# Aggregate metrics
TOTAL = TP_sum + FP_sum + TN_sum + FN_sum
accuracy = safe_div(TP_sum + TN_sum, TOTAL)
precision = safe_div(TP_sum, TP_sum + FP_sum)
recall = safe_div(TP_sum, TP_sum + FN_sum)           # aka TPR
specificity = safe_div(TN_sum, TN_sum + FP_sum)      # aka TNR
f1 = safe_div(2 * TP_sum, 2 * TP_sum + FP_sum + FN_sum)

fig, ax = plt.subplots()
im = ax.imshow(conf_map, cmap=cmap, norm=norm)
fig.suptitle("Confusion matrices from showers detection")

ax.set_xticks(np.arange(0.5, 10, 2))
ax.set_xticklabels(range(-2, 3))
ax.set_yticks(np.arange(0.5, 8, 2))
ax.set_yticklabels([f"MB{st}" for st in range(1, 5)])
ax.set_xlabel("Wheel")
ax.set_ylabel("Station")

for lh in np.arange(1.5, 8, 2):
    ax.axhline(lh, color="w", lw=2)
for lv in np.arange(1.5, 10, 2):
    ax.axvline(lv, color="w", lw=2)

labels = np.array([["TP", "TN"], ["FP", "FN"]])
for x, y in np.ndindex(conf_map.shape):
    label = labels[x % 2, y % 2]
    color = "w"
    ax.text(y, x, f"{label}={conf_map[x, y]:.2f}", ha="center", va="center",
            color=color, fontsize=9, fontweight="bold")

# Add per wheel/station 'eff=' and 'TPR=' centered labels
for st in range(4):
    for iWheel in range(5):
        tp = counts[st, iWheel, 0]
        fn = counts[st, iWheel, 3]
        # 'eff' as TP fraction + TN fraction within the station-wheel block
        eff_val = conf_map[st * 2, iWheel * 2] + conf_map[st * 2, (iWheel * 2) + 1]
        tpr_val = tp / (tp + fn) if (tp + fn) else 0.0
        cx = iWheel * 2 + 0.5
        cy = st * 2 + 0.5
        ax.text(
            cx, cy,
            f"eff = {eff_val:.2f}\nTPR = {tpr_val:.2f}",
            ha="center", va="center", color="w", fontsize=10,
            bbox=dict(facecolor='black', alpha=0.55, edgecolor='none'), fontweight="bold"
        )

# Remove old duplicate 'eff=' labels block (now included with TPR above)

# Add global totals and metrics on the right side
fig.colorbar(im, ax=ax, orientation="horizontal", pad=0.01, location="top")
fig.tight_layout()
fig.subplots_adjust(right=0.78)  # leave space for the metrics panel

metrics_text = (
    f"Totals (global):\n"
    f"TP = {TP_sum:.0f}\n"
    f"FP = {FP_sum:.0f}\n"
    f"TN = {TN_sum:.0f}\n"
    f"FN = {FN_sum:.0f}\n"
    f"Total = {TOTAL:.0f}\n\n"
    f"Accuracy = {accuracy:.3f}\n"
    f"Precision = {precision:.3f}\n"
    f"Recall (TPR) = {recall:.3f}\n"
    f"Specificity (TNR) = {specificity:.3f}\n"
    f"F1-score = {f1:.3f}"
)

fig.text(0.82, 0.5, metrics_text, va="center", ha="left",
            fontsize=10, bbox=dict(facecolor="#f2f2f2", edgecolor="none", alpha=0.9))

# Print detailed report with numerators and denominators for each combination
print("\n" + "="*80)
print("DETAILED REPORT: Numerators and Denominators for Each Combination")
print("="*80)

for st in range(4):
    for iWheel in range(5):
        wheel_label = iWheel - 2  # Convert to -2, -1, 0, 1, 2
        tp = counts[st, iWheel, 0]
        fp = counts[st, iWheel, 1]
        tn = counts[st, iWheel, 2]
        fn = counts[st, iWheel, 3]
        total = totals[st, iWheel]
        
        eff_num = tp + tn
        eff_denom = total
        eff_val = safe_div(eff_num, eff_denom)
        
        tpr_num = tp
        tpr_denom = tp + fn
        tpr_val = safe_div(tpr_num, tpr_denom)
        
        print(f"\nMB{st+1}, Wheel {wheel_label:+d}:")
        print(f"  TP={tp:.0f}, FP={fp:.0f}, TN={tn:.0f}, FN={fn:.0f}, Total={total:.0f}")
        print(f"  Efficiency: {eff_num:.0f}/{eff_denom:.0f} = {eff_val:.4f}")
        print(f"  TPR (Recall): {tpr_num:.0f}/{tpr_denom:.0f} = {tpr_val:.4f}")

print("\n" + "-"*80)
print("GLOBAL METRICS:")
print("-"*80)
print(f"TP={TP_sum:.0f}, FP={FP_sum:.0f}, TN={TN_sum:.0f}, FN={FN_sum:.0f}, Total={TOTAL:.0f}")
print(f"Accuracy: {TP_sum + TN_sum:.0f}/{TOTAL:.0f} = {accuracy:.4f}")
print(f"Precision: {TP_sum:.0f}/{TP_sum + FP_sum:.0f} = {precision:.4f}")
print(f"Recall (TPR): {TP_sum:.0f}/{TP_sum + FN_sum:.0f} = {recall:.4f}")
print(f"Specificity (TNR): {TN_sum:.0f}/{TN_sum + FP_sum:.0f} = {specificity:.4f}")
print(f"F1-score: {2*TP_sum:.0f}/{2*TP_sum + FP_sum + FN_sum:.0f} = {f1:.4f}")
print("="*80 + "\n")

fig.savefig(folder + "/plots/confusion_maps/conf_map_eff.pdf")
print(f"Confusion matrix plot saved to {folder}/plots/confusion_maps/conf_map_eff.pdf")
fig.savefig(folder + "/plots/confusion_maps/conf_map_eff.svg")

