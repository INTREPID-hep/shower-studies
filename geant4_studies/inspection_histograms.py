import ROOT as r
from dtpr.utils.functions import get_unique_locs

# Histograms defined here...
# - SimHit_nHits_per_station
# - SimHit_nHits_per_sl
# - Digi_nDigis_per_station
# - Digi_nDigis_per_sl

# Define the histograms container
histos = {}

histos.update(
    {
        # --- SimHit properties
        "SimHit_nHits_per_station": {
            "type": "distribution",
            "histo": r.TH1D("SimHit_nHits_per_station", r";Number of SimHits per station;", 100, 0, 100),
            "func": lambda reader: [len(reader.filter_particles("simhits", sc=sc, st=st)) for sc, st in get_unique_locs(reader.simhits, loc_ids=["sc", "st"])],
        },
        "SimHit_nHits_per_sl": {
            "type": "distribution",
            "histo": r.TH1D("SimHit_nHits_per_sl", r";Number of SimHits per superlayer;", 100, 0, 100),
            "func": lambda reader: [len(reader.filter_particles("simhits", sc=sc, st=st, sl=sl)) for sc, st, sl in get_unique_locs(reader.simhits, loc_ids=["sc", "st", "sl"])],
        },
        # --- Digi properties
        "Digi_nDigis_per_station": {
            "type": "distribution",
            "histo": r.TH1D("Digi_nDigis_per_station", r";Number of Digis per station;", 100, 0, 100),
            "func": lambda reader: [len(reader.filter_particles("digis", sc=sc, st=st)) for sc, st in get_unique_locs(reader.digis, loc_ids=["sc", "st"])],
        },
        "Digi_nDigis_per_sl": {
            "type": "distribution",
            "histo": r.TH1D("Digi_nDigis_per_sl", r";Number of Digis per superlayer;", 100, 0, 100),
            "func": lambda reader: [len(reader.filter_particles("digis", sc=sc, st=st, sl=sl)) for sc, st, sl in get_unique_locs(reader.digis, loc_ids=["sc", "st", "sl"])],
        },
    }
)