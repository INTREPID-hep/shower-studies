import dtpr.utils.root_plot_functions as rpf
from dtpr.utils.functions import color_msg, create_outfolder
import ROOT as r

in_folder = "."
out_folder = "./plots_sab"

def identify_efficiency_graphs(segv=2, all=False):
    graphs = []
    n_ = ["showered", ""] if not all else ["", "all_"] 
    with r.TFile.Open(f"{in_folder}/histograms/histograms_zprime_segv{segv}.root", "READ") as f:
        # gm showered that matches a shower / gm showered
        eff_ = r.TEfficiency(f.Get(f"shower_{n_[0]}genmuon_tag_eff_pttrend_{n_[1]}num"), f.Get(f"shower_{n_[0]}genmuon_tag_eff_pttrend_{n_[1]}total"))
        graph = eff_.CreateGraph()
        for ibin in range(graph.GetN()):
            graph.SetPointEXhigh(ibin, 0)
            graph.SetPointEXlow(ibin, 0)

        graphs.append((graph, f"SS Method {segv}"))

    return graphs

def main():
    graphs = identify_efficiency_graphs()+ identify_efficiency_graphs(segv=1)
    
    nBins = 50
    binFirst = 0
    binLast = 3335
    maxY = 1.1
    notes =  [
            ("Private work (#bf{CMS} Phase-2 Simulation)", (.08, .90, .5, .95), 0.03),
            ("200 PU", (.75, .90, .89, .95), 0.03),
    ]
    legend_pos=(0.3, 0.68, 0.44, 0.78)
    drawOption="pe1 same"
    titleX = "GenMuon Pt [GeV]"
    titleY = "Identification efficiency #scale[0.5]{#left[#frac{GenMuon showered identified}{GenMuon showered}#right]}"

    # Now plot the graphs
    rpf.plot_graphs(
        graphs = graphs, 
        name = "identify_efficiency",
        nBins = nBins, 
        firstBin = binFirst, 
        lastBin = binLast,
        maxY = maxY,
        notes = notes,
        legend_pos=legend_pos,
        drawOption=drawOption,
        titleX = titleX, 
        titleY = titleY,
        outfolder = out_folder,
        repit_color_each=2,
    )

    graphs_all = identify_efficiency_graphs(all=True) + identify_efficiency_graphs(segv=1, all=True)

    titleY = "Identification efficiency #scale[0.5]{#left[#frac{GenMuon showered identified}{GenMuon}#right]}"


    rpf.plot_graphs(
        graphs = graphs_all, 
        name = "identify_efficiency_all",
        nBins = nBins, 
        firstBin = binFirst, 
        lastBin = binLast,
        maxY = maxY,
        notes = notes,
        legend_pos=legend_pos,
        drawOption=drawOption,
        titleX = titleX,
        titleY = titleY,
        outfolder = out_folder,
        repit_color_each=2,
    )

if __name__ == "__main__":
    create_outfolder(out_folder)
    main()