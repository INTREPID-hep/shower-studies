import ROOT as r
import matplotlib.pyplot as plt
from mplhep import style
from dtpr.utils.functions import create_outfolder
from copy import deepcopy

in_folder = "."
out_folder = "./plots_sab"

# plt.style.use(style.CMS)

shower_classes = {
    "tp": 1,
    "tp_matched_amtp": 2,
    "tp_matched_amtp_highpt": 3,
    "tp_matched_amtp_not_highpt": 4,
    "tp_matched_amtp_showeredmuon": 5,
    "tp_matched_amtp_not_showeredmuon": 6,
    "tp_not_matched_amtp": 7,
    "tp_not_matched_amtp_highpt": 8,
    "tp_not_matched_amtp_not_highpt": 9,
    "tp_not_matched_amtp_showeredmuon": 10,
    "tp_not_matched_amtp_not_showeredmuon": 11,
    "fp": 12,
    "fp_matched_amtp": 13,
    "fp_matched_amtp_highpt": 14,
    "fp_matched_amtp_not_highpt": 15,
    "fp_matched_amtp_showeredmuon": 16,
    "fp_matched_amtp_not_showeredmuon": 17,
    "fp_not_matched_amtp": 18,
    "fp_not_matched_amtp_highpt": 19,
    "fp_not_matched_amtp_not_highpt": 20,
    "fp_not_matched_amtp_showeredmuon": 21,
    "fp_not_matched_amtp_not_showeredmuon": 22,
}

def create_shower_AM_pie_chart(hits_name, ax=None, matchtype="highpt"):
    f = r.TFile.Open(f"{in_folder}/histograms/histograms_zprime_segv2.root")
    histo = deepcopy(f.Get(hits_name))
    f.Close()
    size = 0.3

    outer_pie_vals = [histo.GetBinContent(shower_classes["tp"]), histo.GetBinContent(shower_classes["fp"])]
    outer_pie_labels = ["True Positive showers (TPS)", "False Positive showers (FPS)"]
    outer_pie_colors = ["#0088e3", "#e77515"]

    middle_pie_vals = [
        histo.GetBinContent(shower_classes["tp_matched_amtp"]),
        histo.GetBinContent(shower_classes["tp_not_matched_amtp"]),
        histo.GetBinContent(shower_classes["fp_matched_amtp"]),
        histo.GetBinContent(shower_classes["fp_not_matched_amtp"]),
    ]
    middle_pie_labels = [
        "TPS that match an AM TP",
        "TPS don't match to AM TP",
        "FPS that match an AM TP",
        "FPS don't match to AM TP",
    ]
    middle_pie_colors = ["#2196f3", "#7cc1fa", "#ff963b", "#faba81"]

    inner_pie_vals = [
        histo.GetBinContent(shower_classes[f"tp_matched_amtp_{matchtype}"]), histo.GetBinContent(shower_classes[f"tp_matched_amtp_not_{matchtype}"]),
        histo.GetBinContent(shower_classes[f"tp_not_matched_amtp_{matchtype}"]), histo.GetBinContent(shower_classes[f"tp_not_matched_amtp_not_{matchtype}"]),
        histo.GetBinContent(shower_classes[f"fp_matched_amtp_{matchtype}"]), histo.GetBinContent(shower_classes[f"fp_matched_amtp_not_{matchtype}"]),
        histo.GetBinContent(shower_classes[f"fp_not_matched_amtp_{matchtype}"]), histo.GetBinContent(shower_classes[f"fp_not_matched_amtp_not_{matchtype}"]),
    ]
    inner_pie_labels = [
        f"TPS that mathc AM TP and are {matchtype}",
        f"TPS that mathc AM TP and are not {matchtype}",
        f"TPS don't mathc AM TP and are {matchtype}",
        f"TPS don't mathc AM TP and are not {matchtype}",
        f"FPS that mathc AM TP and are {matchtype}",
        f"FPS that mathc AM TP and are not {matchtype}",
        f"FPS don't mathc AM TP and are {matchtype}",
        f"FPS don't mathc AM TP and are not {matchtype}",
        
    ]
    inner_pie_colors = ["#008a1a", "#8dc998", "#008a1a", "#8dc998","#8f0067", "#b68faa", "#8f0067", "#b68faa"]

    make_pie_chart(
        ax, 
        [outer_pie_vals, outer_pie_labels, outer_pie_colors],
        [middle_pie_vals, middle_pie_labels, middle_pie_colors],
        [inner_pie_vals, inner_pie_labels, inner_pie_colors],
        size
    )

def make_pie_chart(ax, outer_pie_info, middle_pie_info, inner_pie_info, size=0.3):
    outer_pie_vals, outer_pie_labels, outer_pie_colors = outer_pie_info
    middle_pie_vals, middle_pie_labels, middle_pie_colors = middle_pie_info
    inner_pie_vals, inner_pie_labels, inner_pie_colors = inner_pie_info

    # Outer pie chart
    _,label_text_out,number_text_out = ax.pie(
        outer_pie_vals, radius=1, colors=outer_pie_colors,
        wedgeprops=dict(width=size, edgecolor='w'), labels=outer_pie_labels,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else "",
        pctdistance=0.85,
    )


    # Middle pie chart
    _,_,number_text_mid = ax.pie(
        middle_pie_vals, radius=1-size, colors=middle_pie_colors,
        wedgeprops=dict(width=size, edgecolor='w'), labels=middle_pie_labels,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else "",
        pctdistance=0.75,
        labeldistance=None,
    )

    # Inner pie chart
    _,_,number_text_in = ax.pie(
        inner_pie_vals, radius=1-2*size, colors=inner_pie_colors,
        wedgeprops=dict(width=size, edgecolor='w'), labels=inner_pie_labels,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else "",
        pctdistance=0.7,
        labeldistance=None,
    )

    for txt in label_text_out:
        txt.set_fontweight('bold')
    for i, txt_obj in enumerate([number_text_out, number_text_mid, number_text_in]):
        for txt in txt_obj:
            txt.set_fontweight('bold')
            txt.set_fontsize(12 -i*1.5)

    ax.legend(
        loc='upper left', bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10, title_fontsize=12
    )
    ax.set(aspect="equal", title='Shower-AM primitives matching')


def main():
    fig, ax = plt.subplots(figsize=(10, 10))
    create_shower_AM_pie_chart("showers_classification", matchtype="highpt", ax=ax)
    fig.tight_layout()
    fig.savefig(f"{out_folder}/pies_2/shower_AM_matching_highpt.svg", dpi=300)
    fig.savefig(f"{out_folder}/pies_2/shower_AM_matching_highpt.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 10))
    create_shower_AM_pie_chart("showers_classification", matchtype="showeredmuon", ax=ax)
    fig.tight_layout()
    fig.savefig(f"{out_folder}/pies_2/shower_AM_matching_showeredmuon.svg", dpi=300)
    fig.savefig(f"{out_folder}/pies_2/shower_AM_matching_showeredmuon.png", dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    create_outfolder(out_folder + "/pies_2")
    main()