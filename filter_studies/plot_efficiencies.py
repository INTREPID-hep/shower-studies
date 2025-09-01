import utils.root_plot_functions as rpf
from dtpr.utils.functions import color_msg, create_outfolder
import ROOT as r

in_folder = "."
out_folder = "./plots_sab"

def main():
    
    info_for_plots = [
        {
            "file_name": f"{in_folder}/../efficiencies/histograms/histograms_thr_rsfix6.root",
            "histos_names": "Fwshower_eff_MBX",
            "legends":  "Before Filter",
        },
        {
            "file_name": f"{in_folder}/../efficiencies/histograms/histograms_thr_rsfix6.root",
            "histos_names": "Fwshower_eff_MBX",
            "legends":  "",
        },
        { 
            "file_name": f"{in_folder}/histograms/histograms_zprime_segv2.root",
            "histos_names": "Fwshower_eff_afterfilter_MBX",
            "legends":  "After Filter - SS Method 2",
        },
        { 
            "file_name": f"{in_folder}/histograms/histograms_zprime_segv1.root",
            "histos_names": "Fwshower_eff_afterfilter_MBX",
            "legends":  "After Filter - SS Method 1",
        },
    ]

    rpf.make_plots(
        info_for_plots=info_for_plots,
        output_name="eff_fwshower_afterfilter",
        outfolder=out_folder,
        legend_pos=(0.42, 0.48, 0.54, 0.6),
        titleY="Shower Trigger Efficiency #scale[0.7]{#left[#frac{TP + TN}{TP + FP + FN + TN}#right]}",
        repite_color_each=2,
    )
    # AM efficiency
    info_for_plots = [
        # {
        #     "file_name": f"{in_folder}/../efficiencies/histograms/histograms_thr_rsfix6.root",
        #     "histos_names": "Eff_MBX_AM",
        #     "legends":  "Before Filter",
        # },
        # {
        #     "file_name": f"{in_folder}/../efficiencies/histograms/histograms_thr_rsfix6.root",
        #     "histos_names": "Eff_MBX_AM",
        #     "legends":  "",
        # },
        { 
            "file_name": f"{in_folder}/histograms/histograms_zprime_segv2.root",
            "histos_names": "AMEff_afterfilter_MBX_AM",
            "legends":  "After Filter - SS Method 2",
        },
        { 
            "file_name": f"{in_folder}/histograms/histograms_zprime_segv1.root",
            "histos_names": "AMEff_afterfilter_MBX_AM",
            "legends":  "After Filter - SS Method 1",
        },
    ]
    rpf.make_plots(
        info_for_plots=info_for_plots,
        output_name="eff_am_afterfilter",
        outfolder=out_folder,
        legend_pos=(0.42, 0.48, 0.54, 0.6),
        titleY="DT Local Trigger Efficiency",
        repite_color_each=2,
    )

if __name__ == "__main__":
    create_outfolder(out_folder)
    main()