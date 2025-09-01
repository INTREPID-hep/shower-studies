from dtpr.utils.functions import color_msg
import utils.root_plot_functions as rpf

def main():
    # --- Files to be used --- #
    in_folder = "."

    color_msg("Plotting rates", color="blue")

    # ------------------------------ all bx plot ------------------------------ #
    info_for_plots_allbx = [
        {
            "file_name": f"{in_folder}/../rates/histograms/histograms_sbxfix_thr6.root",
            "histos_names": ["Rate_allBX_MBX_FwShower", "Rate_goodBX_MBX_FwShower"],
            "legends":  ["Before Filter all BX", "Before Filter good BX"],
        },
        { 
            "file_name": f"{in_folder}/histograms/histograms_minbias_segv2.root",
            "histos_names": ["FWshower_Rate_afterfilter_allBX_MBX_FWShower", "FWshower_Rate_afterfilter_goodBX_MBX_FWShower"],
            "legends":  ["After Filter all BX - SS Method 2", "After Filter good BX - SS Method 2"],
        },
        {
            "file_name": f"{in_folder}/histograms/histograms_minbias_segv1.root",
            "histos_names": ["FWshower_Rate_afterfilter_allBX_MBX_FWShower", "FWshower_Rate_afterfilter_goodBX_MBX_FWShower"],
            "legends":  ["After Filter all BX - SS Method 1", "After Filter good BX - SS Method 1"],
        },
    ]

    rpf.make_plots(
        info_for_plots=info_for_plots_allbx,
        type="histo",
        titleY="Showers Rate (Hz)",
        output_name = "showerrate_afterfilter",
        outfolder=in_folder + "/plots_sab", 
        logy=True,
        scaling= (1/1929240) * 2760 * 11246, #(1/1565520) * 2760 * 11246,
        repite_color_each=2,
        legend_pos=(0.14, 0.42, 0.30, 0.56),
        maxY=1e8,
    )

if __name__ == "__main__":
    main()