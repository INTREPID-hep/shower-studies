"""" Plotting script """
from dtpr.utils.functions import color_msg
from utils.root_plot_functions import *


def main():    
    # --- Files to be used --- #
    folder = "results"
    color_msg("Plotting fwShower efficiency for G4 data", color="blue")

    info_for_plots = [
        { 
            "file_name": f"{folder}/histograms/histograms_g4_eff.root",
            "histos_names": "Fwshower_eff_MBX",
            "legends": f"Before",
        },
        {
            "file_name": f"{folder}/histograms/histograms_g4_eff_full.root",
            "histos_names": "Fwshower_eff_MBX",
            "legends": f"After",
        }
    ]

    make_plots(
        info_for_plots=info_for_plots,
        output_name = "eff_fwshower_g4",
        outfolder=folder+"/plots",
        legend_pos=(0.2, 0.38, 0.34, 0.5),
        titleY="Shower Trigger Efficiency #scale[0.7]{#left[#frac{TP +TN}{TP + FP + FN + TN}#right]}",
    )

    color_msg("Done!", color="green")


if __name__ == "__main__":
    main()
