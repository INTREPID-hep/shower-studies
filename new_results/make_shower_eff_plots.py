"""" Plotting script """
from dtpr.utils.functions import color_msg
from utils.root_plot_functions import *


def main():    
    # --- Files to be used --- #
    folder = "."
    color_msg("Plotting fwShower efficiency", color="blue")

    tags = ["", "_simhitsfilter", "_simhitsfilter_diffThrs", "_simhitsfilter_diffThrs_nn"]#, "_simhitsfilter_diffThrs_nn_covercell"]
    labels = ["Nothing", "SimHits filter", "SimHits filter + diff. thresholds", "SimHits filter + diff. thresholds + NN filter"]#, "SimHits filter + diff. thresholds + NN filter + cover cell"]
    info_for_plots = [
        { 
            "file_name": f"{folder}/histograms/histograms{tag}.root",
            "histos_names": "Fwshower_eff_MBX",
            "legends": f" {label} "
        } for tag, label in zip(tags, labels)
    ]

    make_plots(
        info_for_plots=info_for_plots,
        output_name = "eff_fwshower_3",
        outfolder=folder+"/plots",
        legend_pos=(0.3, 0.58, 0.44, 0.7),
        titleY="Shower Trigger Efficiency #scale[0.7]{#left[#frac{TP + TN}{TP + FP + FN + TN}#right]}",
    )

    color_msg("Done!", color="green")


if __name__ == "__main__":
    main()
