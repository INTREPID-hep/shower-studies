import os
import gc
import importlib
import matplotlib.pyplot as plt
from pandas import DataFrame
from mplhep import style
from copy import deepcopy

from dtpr.base import Event, NTuple
from dtpr.utils.functions import color_msg, save_mpl_canvas
from mpldts.geometry import Station as DT
from mpldts.geometry import AMDTSegments
from mpldts.patches import DTStationPatch, MultiDTSegmentsPatch
from dtpr.base.config import RUN_CONFIG
from matplotlib import colors

cmap_segs = colors.ListedColormap(["k", "r"]) 
cmap_segs.set_under('none')  # Set color for values below the minimum
segs_norm = colors.BoundaryNorm(boundaries=[0, 1, 2], ncolors=2, clip=True)

segs_kwargs = {
    "cmap": cmap_segs,
    "norm": segs_norm,
}

def embed_dtwheel2axes(ev, wheel, ax=None, bounds_kwargs=None, cells_kwargs=None, include_AMtps=False):
    """
    Add the dt patches for a specific wheel for the given event.

    :param ev: The event containing DT data.
    :type ev: Event
    :param wheel: The wheel number to plot.
    :type wheel: int
    :param ax: The axes to plot on. Default is None, which creates a new figure.
    :type ax: matplotlib.axes._subplots.AxesSubplot
    :param bounds_kwargs: Additional keyword arguments for the bounds of the patch.
    :type bounds_kwargs: dict
    :param cells_kwargs: Additional keyword arguments for the cells of the patch.
    :type cells_kwargs: dict
    :return: The axes for the specified wheel.
    :return type:  matplotlib.axes._subplots.AxesSubplot
    """
    if not ax:
        _, ax = plt.subplots(figsize=(8, 6))

    # use RUN_CONFIG to determine which evetn info to use as dt_info
    particle_type, cmap_var = RUN_CONFIG.dt_plots_configs["dt-cell-info"].values()
    infoDts = DataFrame([particle.__dict__ for particle in ev.filter_particles(particle_type, wh=wheel)])

    if infoDts.empty:
        ax.text(
            0.5,
            0.5, 
            f"No digis in wheel {wheel}",
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes
        )
        return ax
    else:
        if any( not col_name in infoDts.columns for col_name in ["sl", "l", "w", cmap_var]):
            raise ValueError(f"Columns 'sl', 'l', 'w', and '{cmap_var}' must be present in {particle_type} data")

        infoDts = infoDts.groupby(["wh", "sc", "st"])

        # add the circle representing the CMS Wheel
        circle = plt.Circle((0, 0), 800, edgecolor='black', facecolor="gray", alpha=0.1, linewidth=0.5)
        ax.add_patch(circle)
        ax.set_aspect("equal")
        ax.set_xlim(-800, 800)
        ax.set_ylim(-800, 800)
        ax.set_xlabel("x [cm]")
        ax.set_ylabel("y [cm]")
        ax.set_title(f"wheel {wheel}")

        _tps_info = []
        for (wh, sc, st), dt_info in infoDts:
            _dt_chamber = DT(wheel=wh, sector=sc, station=st, dt_info=dt_info[["sl", "l", "w", cmap_var]])

            DTStationPatch(
                station=_dt_chamber,
                axes=ax,
                local=False,
                faceview="phi",
                bounds_kwargs=bounds_kwargs,
                cells_kwargs=cells_kwargs,
            )
            if include_AMtps:
                for _tp in ev.filter_particles("tps", wh=wh, sc=sc, st=st):
                    _tps_info.append({
                    "parent": _dt_chamber,  # parent station of the TP
                    "index": _tp.index,
                    "sl": _tp.sl,
                    "angle": -1 * getattr(_tp, "dirLoc_phi"), # CAUTION: angle appears to be bad signed in the ntuple, according to the plots...
                    "position": getattr(_tp, "posLoc_x"),
                })

        if _tps_info:
            color_msg(f"Adding TPs for {wh}/{sc}/{st} with {len(_tps_info)} TPs", "blue")
            _tps_geo = AMDTSegments(segs_info=_tps_info) # geometrically objects that allow to get global coordinates of TPs
            MultiDTSegmentsPatch(
                segments=_tps_geo, axes=ax, faceview="phi", local=False, vmap="quality", segs_kwargs=segs_kwargs
            )
    return ax

def make_dt_plots(ev: Event, name="test_dt_plot", path=".", save=False):
    """
    Create and display the global DT plots for the given event.

    :param ev: The event containing DT data.
    :type ev: Event
    :param name: (str): The name of the plot file. Default is "test_dt_plot".
    :type name: str
    :param path: (str): The directory where the plot file will be saved. Default is ".".
    :type path: str
    :param save: Whether to save the plot to disk. Default is False.
    :type save: bool
    """
    fig, axs = plt.subplots(2, 3, figsize=(25,15), layout="constrained")
    axs = axs.flat
    fig.suptitle(f"Event #{ev.index}")

    bounds_kwargs = deepcopy(RUN_CONFIG.dt_plots_configs["bounds-kwargs"])
    cells_kwargs = deepcopy(RUN_CONFIG.dt_plots_configs["cells-kwargs"])

    cmap_configs = deepcopy(RUN_CONFIG.dt_plots_configs["cmap-configs"])

    cmap = plt.get_cmap(cmap_configs["cmap"]).copy()
    cmap.set_under(cmap_configs["cmap_under"])

    norm_module, norm_name = cmap_configs["norm"].pop("class").rsplit('.', 1)
    module = importlib.import_module(norm_module)
    norm = getattr(module, norm_name)(**cmap_configs["norm"])

    cells_kwargs.update({"cmap": cmap, "norm": norm})

    for iaxs in range(-2, 3):
        _ = embed_dtwheel2axes(ev, iaxs, axs[iaxs + 2], bounds_kwargs=bounds_kwargs, cells_kwargs=cells_kwargs, include_AMtps=True)

    axs[-1].remove()
    fig.tight_layout()
    if save:
        save_mpl_canvas(fig, name, path, dpi=RUN_CONFIG.dt_plots_configs["figure-configs"]["figure.dpi"])
    else:
        plt.show()
    plt.close(fig)
    del fig  # Explicitly delete the figure object
    gc.collect()

def plot_dt_chambers(
        inpath: str,
        outfolder: str,
        tag: str,
        maxfiles: int,
        event_number: int,
        save: bool,
    ):
    """
    Generate DT plots from DTNTuples and save them to the specified output folder.

    Parameters:
    inpath (str): The input directory containing DTNTuples.
    outfolder (str): The output directory where the plots will be saved.
    filter_type (str): The type of filter to apply to events.
    tag (str): A tag to append to the plot filenames.
    maxfiles (int): The maximum number of files to process.
    event_number (int): The event number to plot.
    save (bool): Whether to save the plots to disk.
    """

    # Start of the analysis 
    color_msg(f"Running program to produce DT plots based on DTNTuples", "green")

    # Create the Ntuple object
    ntuple = NTuple(
        inputFolder=inpath,
        maxfiles=maxfiles,
    )

    color_msg(f"Making plots...", color="purple", indentLevel=1)

    ev = ntuple.events[event_number]
    if not ev:
        color_msg(f"Event not pass filter: {ev}", color="red")
        return
    with plt.style.context(getattr(style,RUN_CONFIG.dt_plots_configs["mplhep-style"])):
        plt.rcParams.update(RUN_CONFIG.dt_plots_configs["figure-configs"]) 
        make_dt_plots(ev, name=f"dt_plots{tag}_ev{ev.index}", path=os.path.join(outfolder, "dt_plots"), save=save)

    color_msg(f"Done!", color="green")

if __name__ == "__main__":
    RUN_CONFIG.change_config_file("./run_config.yaml")
    plot_dt_chambers(
        inpath = "../../ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/ZprimeToMuMu_M-6000_PU200/250312_131631/0000/",
        outfolder=".",
        tag="test",
        maxfiles=-1,
        event_number=34991,
        save=False
    )