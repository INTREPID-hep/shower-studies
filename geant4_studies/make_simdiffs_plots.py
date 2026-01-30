import ROOT as r
import utils.root_plot_functions as rpf
from copy import deepcopy

def main():
    folder = "./results"
    print("Plotting")
    graphs_simhits = []
    graphs_digis = []

    with r.TFile.Open(f"{folder}/histograms/histograms_noFilter_simDiffs.root", "READ") as f:
        hist_simhits = deepcopy(f.Get("SimHit_nHits_per_sl"))
        hist_digis = deepcopy(f.Get("Digi_nDigis_per_sl"))
        graphs_simhits.append((hist_simhits, "noFilter"))
        graphs_digis.append((hist_digis, "noFilter"))
    with r.TFile.Open(f"{folder}/histograms/histograms_wallCrossing_simDiffs.root", "READ") as f:
        hist_simhits = deepcopy(f.Get("SimHit_nHits_per_sl"))
        hist_digis = deepcopy(f.Get("Digi_nDigis_per_sl"))
        graphs_simhits.append((hist_simhits, "wallCrossing"))
        graphs_digis.append((hist_digis, "wallCrossing"))
    with r.TFile.Open(f"{folder}/histograms/histograms_wallCrossing_Confinement_simDiffs.root", "READ") as f:
        hist_simhits = deepcopy(f.Get("SimHit_nHits_per_sl"))
        hist_digis = deepcopy(f.Get("Digi_nDigis_per_sl"))
        graphs_simhits.append((hist_simhits, "wallCrossing_Confinement"))
        graphs_digis.append((hist_digis, "wallCrossing_Confinement"))
    with r.TFile.Open(f"{folder}/histograms/histograms_wallCrossing_Confinement_wireCut_simDiffs.root", "READ") as f:
        hist_simhits = deepcopy(f.Get("SimHit_nHits_per_sl"))
        hist_digis = deepcopy(f.Get("Digi_nDigis_per_sl"))
        graphs_simhits.append((hist_simhits, "wallCrossing_Confinement_wireCut"))
        graphs_digis.append((hist_digis, "wallCrossing_Confinement_wireCut"))

    # Plot SimHits
    colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen+2]
    c1 = r.TCanvas("c1", "SimHits", 800, 600)
    for i, (hist, label) in enumerate(graphs_simhits):
        if not hist:
            print(f"Histogram for {label} not found!")
        hist.SetLineColor(colors[i])
        hist.Draw("HIST" + (" SAME" if i > 0 else ""))
    
    leg1 = r.TLegend(0.6, 0.6, 0.9, 0.9)
    for hist, label in graphs_simhits:
        leg1.AddEntry(hist, label, "f")
    leg1.Draw()
    c1.SaveAs(f"{folder}/plots/simhits_comparison.root")
    
    # Plot Digis
    c2 = r.TCanvas("c2", "Digis", 800, 600)
    for i, (hist, label) in enumerate(graphs_digis):
        hist.SetLineColor(colors[i])
        hist.Draw("HIST" + (" SAME" if i > 0 else ""))
    
    leg2 = r.TLegend(0.6, 0.6, 0.9, 0.9)
    for hist, label in graphs_digis:
        leg2.AddEntry(hist, label, "f")
    leg2.Draw()
    c2.SaveAs(f"{folder}/plots/digis_comparison.root")

if __name__ == "__main__":
    main()