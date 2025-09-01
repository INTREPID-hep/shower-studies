"""" Plotting script """
from dtpr.utils.functions import color_msg
from utils.root_plot_functions import *


def main():    
    # --- Files to be used --- #
    folder = "."
    color_msg("Plotting fwShower efficiency", color="blue")


    thresholds = [6, 8, 12, 16]
    info_for_plots = [
        { 
            "file_name": f"{folder}/histograms/histograms_onlytpfp_thr_{thr}.root",
            "histos_names": "Fwshower_eff_MBX_onlytpfp",
            "legends": f" Threshold - {thr}",
        }
        for thr in thresholds
    ]

    make_plots(
        info_for_plots=info_for_plots,
        output_name = "eff_fwshower_onytpfp",
        outfolder=folder+"/plots",
        legend_pos=(0.2, 0.58, 0.34, 0.7),
        titleY="Shower Trigger Efficiency #scale[0.7]{#left[#frac{TP}{TP + FP + FN}#right]}",
        # aditional_notes=[("(TP + TN) / (TP + TN + FP + FN)", (.44, .38, .5, .47), 0.03)]
    )

    color_msg("Done!", color="green")


if __name__ == "__main__":
    main()
