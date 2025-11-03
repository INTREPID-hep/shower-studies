from dtpr.base import NTuple
from dtpr.base.config import Config
from dtpr.utils.functions import create_outfolder
import matplotlib.pyplot as plt
from mplhep import style
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import os
import argparse

style.use(style.CMS)

# Constants
COLUMNS = ['BX', 'time', 'w', 'l', 'sl', 'st', 'sc', 'wh']
WIRES_PER_STATION = 100
LAYERS_PER_BX = 12
LAYERS_PER_SUPERLAYER = 4
SUPERLAYERS_PER_BX = 3

# Colormap configuration: 0=None, 1=Shower Only, 2=Raw Only, 3=Both
base_cmap = cm.get_cmap('viridis', 4)
colors = list(base_cmap(np.arange(4)))
colors[1] = (1.0, 0.0, 0.0, 1.0)  # Red for shower-only
CMAP = ListedColormap(colors)
CMAP_BOUNDARIES = [-0.5, 0.5, 1.5, 2.5, 3.5]
CMAP_NORM = BoundaryNorm(CMAP_BOUNDARIES, CMAP.N)


def create_digi_map(df_raw, df_shower, bx):
    """
    Create a 2D map of digis for a specific BX.
    
    Args:
        df_raw: DataFrame with raw digis
        df_shower: DataFrame with shower digis
        bx: Bunch crossing number
        
    Returns:
        numpy array of shape (100, 12) with encoded digi information
    """
    digi_map = np.zeros((WIRES_PER_STATION, LAYERS_PER_BX))
    
    # Filter by BX
    df_bx_raw = df_raw[df_raw['BX'] == bx]
    df_bx_shower = df_shower[df_shower['BX'] == bx]
    
    # Mark raw digis (value += 2)
    for _, row in df_bx_raw.iterrows():
        sl, l, w = int(row['sl']), int(row['l']), int(row['w'])
        layer_index = (l - 1) + (sl - 1) * LAYERS_PER_SUPERLAYER
        digi_map[w, layer_index] += 2
    
    # Mark shower digis (value += 1)
    for _, row in df_bx_shower.iterrows():
        sl, l, w = int(row['sl']), int(row['l']), int(row['w'])
        layer_index = (l - 1) + (sl - 1) * LAYERS_PER_SUPERLAYER
        digi_map[w, layer_index] += 1
    
    return digi_map


def add_vertical_separators(ax, nblocks):
    """Add vertical lines to separate BX and superlayer sections."""
    # Separate BX sections
    for i in range(1, nblocks):
        ax.axvline(x=i * LAYERS_PER_BX - 0.5, color='white', 
                   linestyle='--', linewidth=0.6, alpha=0.7)
    
    # Separate superlayer sections within each BX
    for i in range(nblocks):
        for sl in range(1, SUPERLAYERS_PER_BX):
            ax.axvline(x=i * LAYERS_PER_BX + sl * LAYERS_PER_SUPERLAYER - 0.5, 
                      color='white', linestyle=':', linewidth=0.4, alpha=0.6)


def configure_x_axis(ax, station_maps):
    """Configure x-axis with BX labels and superlayer annotations."""
    nblocks = len(station_maps)
    
    # Major ticks: BX numbers at center of each block
    xticks = [i * LAYERS_PER_BX + LAYERS_PER_BX / 2 - 0.5 for i in range(nblocks)]
    xlabels = [str(bx) for bx, _ in station_maps]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    ax.set_xlabel('BX')
    ax.tick_params(axis='x', which='major', pad=10)
    
    # Minor ticks: disable marks, add text annotations for superlayers
    ax.tick_params(axis='x', which='minor', length=0)
    
    for i in range(nblocks):
        for sl in range(SUPERLAYERS_PER_BX):
            x_pos = i * LAYERS_PER_BX + sl * LAYERS_PER_SUPERLAYER + LAYERS_PER_SUPERLAYER / 2 - 0.5
            ax.text(x_pos, -0.01, f'SL{sl + 1}', 
                   ha='center', va='top', fontsize=6,
                   transform=ax.get_xaxis_transform())


def analyze_events_digis(raw_digis, shower_digis, outfilename=None, save=True):
    """
    Analyze and visualize DT digis for a specific station.
    
    Args:
        raw_digis: List of raw digis that exist for the event
        shower_digis: List of digis used inside the shower algorithm to create shower primitives
        outfilename: Base name for output file
        save: Whether to save the plot or display it
    """
    # Convert to DataFrames
    df_raw = pd.DataFrame([digi.__dict__ for digi in raw_digis], columns=COLUMNS)
    df_shower = pd.DataFrame([digi.__dict__ for digi in shower_digis], columns=COLUMNS)

    # Validate data
    if df_raw.empty:
        print("No raw digis data found")
        return
    
    # Extract station identifiers
    wh, sc, st = df_raw['wh'].iloc[0], df_raw['sc'].iloc[0], df_raw['st'].iloc[0]
    
    # Build continuous BX timeline
    bx_values = sorted(df_raw['BX'].unique())
    min_bx, max_bx = min(bx_values), max(bx_values)
    bx_range = range(int(min_bx), int(max_bx) + 1)

    # Create maps for each BX
    station_maps = [(bx, create_digi_map(df_raw, df_shower, bx)) for bx in bx_range]

    # Concatenate maps horizontally
    combined_map = np.hstack([m for _, m in station_maps])

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title(f"Wheel: {wh}, Sector: {sc}, Station: {st}")
    
    # Plot heatmap
    im = ax.imshow(combined_map, aspect='auto', cmap=CMAP, norm=CMAP_NORM, origin='lower')
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(['None', 'Shower Only', 'Raw Only', 'Both'])

    # Configure axes
    configure_x_axis(ax, station_maps)
    add_vertical_separators(ax, len(station_maps))
    
    fig.tight_layout()

    # Save or display
    if save:
        output_path = f"{outfilename}_wh{wh}_sc{sc}_st{st}.svg"
        plt.savefig(output_path)
        print(f"Saved plot to: {output_path}")
    else:
        plt.show()

    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze DT digis for a specific station',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-evn', '--event-number', type=int, required=True, 
                        help='Event number')
    parser.add_argument('-wh', '--wheel', type=int, required=True, 
                        help='Wheel number')
    parser.add_argument('-sc', '--sector', type=int, required=True, 
                        help='Sector number')
    parser.add_argument('-st', '--station', type=int, required=True, 
                        help='Station number')
    parser.add_argument('-o', '--outdir', type=str, 
                        default='./results/obdt_buffer_logic_inspection', 
                        help='Output folder path')
    parser.add_argument('--no-save', action='store_true', 
                        help='Display the plot instead of saving')
    
    args = parser.parse_args()
    
    # Create output folder if saving
    if not args.no_save:
        create_outfolder(args.outdir)
    
    # Configure file paths
    config_dir = os.path.dirname(__file__)
    ntuples_dir = os.path.join(config_dir, "../ntuples")
    
    config_file_digis = os.path.abspath(os.path.join(config_dir, "run_config_digis.yaml"))
    config_file_dts = os.path.abspath(os.path.join(config_dir, "dtntuplev1p2_run_config.yaml"))
    input_file_digis = os.path.abspath(os.path.join(ntuples_dir, "shower_digis.root"))
    input_file_dts = os.path.abspath(os.path.join(ntuples_dir, "last-test.root"))
    
    # Load configurations and ntuples
    dt_config = Config(config_file_dts)
    digis_config = Config(config_file_digis)
    
    ntuple_raw = NTuple(input_file_dts, CONFIG=dt_config)
    ntuple_shower = NTuple(input_file_digis, CONFIG=digis_config)
    
    # Get events
    event_raw = ntuple_raw.events.get_by_number(args.event_number)
    event_shower = ntuple_shower.events.get_by_number(args.event_number)
    
    # Filter digis for the specific station
    filtered_raw_digis = event_raw.filter_particles(
        "digis", wh=args.wheel, sc=args.sector, st=args.station
    )
    filtered_shower_digis = event_shower.filter_particles(
        "digis", wh=args.wheel, sc=args.sector, st=args.station
    )
    
    # Analyze and visualize
    analyze_events_digis(
        filtered_raw_digis,
        filtered_shower_digis,
        outfilename=f"{args.outdir}/event_digis_inspection_event_{event_raw.number}",
        save=not args.no_save
    )


if __name__ == "__main__":
    main()