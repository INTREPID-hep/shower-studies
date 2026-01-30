import utils.root_plot_functions as rpf
import ROOT as r

def main():
    folder = "./results"
    print("Plotting")
    graphs = []

    with r.TFile.Open(f"{folder}/histograms/histograms_bigsample_130126_no_parallel.root", "READ") as f:
        eff_ = r.TEfficiency(f.Get("muonshowered_vs_pt_num"), f.Get("muonshowered_vs_pt_total"))
        graph = eff_.CreateGraph()
        for ibin in range(graph.GetN()):
            graph.SetPointEXhigh(ibin, 0)
            graph.SetPointEXlow(ibin, 0)

        graphs.append((graph, "Geant4 Data"))
    
    # with r.TFile.Open(f"{folder}/histograms/histograms_wallCrossing.root", "READ") as f:
    #     eff_ = r.TEfficiency(f.Get("muonshowered_vs_pt_num"), f.Get("muonshowered_vs_pt_total"))
    #     graph = eff_.CreateGraph()
    #     for ibin in range(graph.GetN()):
    #         graph.SetPointEXhigh(ibin, 0)
    #         graph.SetPointEXlow(ibin, 0)

    #     graphs.append((graph, "wallCrossing"))
    
    # with r.TFile.Open(f"{folder}/histograms/histograms_wallCrossing_Confinement.root", "READ") as f:
    #     eff_ = r.TEfficiency(f.Get("muonshowered_vs_pt_num"), f.Get("muonshowered_vs_pt_total"))
    #     graph = eff_.CreateGraph()
    #     for ibin in range(graph.GetN()):
    #         graph.SetPointEXhigh(ibin, 0)
    #         graph.SetPointEXlow(ibin, 0)

    #     graphs.append((graph, "wallCrossing_Confinement"))

    # with r.TFile.Open(f"{folder}/histograms/histograms_wallCrossing_Confinement_wireCut.root", "READ") as f:
    #     eff_ = r.TEfficiency(f.Get("muonshowered_vs_pt_num"), f.Get("muonshowered_vs_pt_total"))
    #     graph = eff_.CreateGraph()
    #     for ibin in range(graph.GetN()):
    #         graph.SetPointEXhigh(ibin, 0)
    #         graph.SetPointEXlow(ibin, 0)

    #     graphs.append((graph, "wallCrossing_Confinement_wireCut"))

    nBins = 10
    binFirst = 0
    binLast = 2000

    # Now plot the graphs
    rpf.plot_graphs(
        graphs = graphs, 
        name = "pt_trend_bigsample_130126",
        nBins = nBins, 
        firstBin = binFirst, 
        lastBin = binLast,
        maxY = 1.1,
        # notes =  [
        #     ("Private work (#bf{CMS} Phase-2 Simulation)", (.08, .90, .5, .95), 0.03)
        # ],
        legend_pos=(0.3, 0.68, 0.44, 0.78),
        drawOption="pe1 same",
        titleX = "p_{T} [GeV]", 
        titleY = "Shower probability",
        outfolder = f"{folder}/plots",
    )

if __name__ == "__main__":
    main()