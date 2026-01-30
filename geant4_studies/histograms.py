import ROOT as r
from dtpr.utils.functions import get_unique_locs

# Histograms defined here...
# - Muon_pt_no_showered
# - Muon_pt_showered
# - Muon_nSecondaries_no_showered
# - Muon_nSecondaries_showered
# - Muon_radEnergy_no_showered
# - Muon_radEnergy_showered
# - Muon_radEnergy_vs_pt_no_showered
# - Muon_radEnergy_vs_pt_showered
# - Muon_nSecondaries_vs_pt_no_showered
# - Muon_nSecondaries_vs_pt_showered
# - SimHit_nHits_no_showered
# - SimHit_nHits_showered
# - SimHit_nHits_per_station_no_showered
# - SimHit_nHits_per_station_showered
# - SimHit_nHits_per_sl_no_showered
# - SimHit_nHits_per_sl_showered
# - SimHit_time_no_showered
# - SimHit_time_showered
# - SimHit_energyDeposit_no_showered
# - SimHit_energyDeposit_showered
# - SimHit_trackLength_no_showered
# - SimHit_trackLength_showered
# - Digi_nDigis_no_showered
# - Digi_nDigis_showered
# - Digi_tdc_no_showered
# - Digi_tdc_showered
# - Digi_BX_no_showered
# - Digi_BX_showered
# - Digi_nDigis_per_station_no_showered
# - Digi_nDigis_per_station_showered
# - Digi_nDigis_per_sl_no_showered
# - Digi_nDigis_per_sl_showered
# - muonshowered_vs_pt


# Define the histograms container
histos = {}

for showered_state in ["no_showered", "showered"]:
    showered_cond = (lambda reader: len(reader.realshowers) > 0) if showered_state == "showered" else (lambda reader: len(reader.realshowers) == 0)
    histos.update(
        {
            f"Muon_pt_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"Muon_pt_{showered_state}", r";muon p_T (GeV);", 200, 0, 2000),
                "func": lambda reader, showered_cond=showered_cond: reader.gens[0].pt if showered_cond(reader) else None,
            },
            f"Muon_nSecondaries_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"Muon_nSecondaries_{showered_state}", r";Number of secondaries;", 50, 0, 50),
                "func": lambda reader, showered_cond=showered_cond: reader.gens[0].n_secondaries if showered_cond(reader) else None,
            },
            f"Muon_radEnergy_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"Muon_radEnergy_{showered_state}", r";Muon radiative energy (GeV);", 100, 0, 100),
                "func": lambda reader, showered_cond=showered_cond: reader.gens[0].rad_energy if showered_cond(reader) else None,
            },
            f"Muon_radEnergy_vs_pt_{showered_state}": {
                "type": "distribution2d",
                "histo": r.TH2D(f"Muon_radEnergy_vs_pt_{showered_state}", r";muon p_T (GeV);Muon radiative energy (GeV);", 200, 0, 2000, 100, 0, 100),
                "func": lambda reader, showered_cond=showered_cond: [(reader.gens[0].pt, reader.gens[0].rad_energy)] if showered_cond(reader) else [],
            },
            f"Muon_nSecondaries_vs_pt_{showered_state}": {
                "type": "distribution2d",
                "histo": r.TH2D(f"Muon_nSecondaries_vs_pt_{showered_state}", r";muon p_T (GeV);Number of secondaries;", 200, 0, 2000, 50, 0, 50),
                "func": lambda reader, showered_cond=showered_cond: [(reader.gens[0].pt, reader.gens[0].n_secondaries)] if showered_cond(reader) else [],
            },
            f"SimHit_nHits_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"SimHit_nHits_{showered_state}", r";Number of SimHits;", 100, 0, 100),
                "func": lambda reader, showered_cond=showered_cond: len(reader.simhits) if showered_cond(reader) else None,
            },
            # --- Inspection histograms per station/superlayer
            f"SimHit_nHits_per_station_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"SimHit_nHits_per_station_{showered_state}", r";Number of SimHits per station;", 100, 0, 100),
                "func": lambda reader, showered_cond=showered_cond: [len(reader.filter_particles("simhits", sc=sc, st=st)) for sc, st in get_unique_locs(reader.simhits, loc_ids=["sc", "st"])] if showered_cond(reader) else [],
            },
            f"SimHit_nHits_per_sl_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"SimHit_nHits_per_sl_{showered_state}", r";Number of SimHits per superlayer;", 100, 0, 100),
                "func": lambda reader, showered_cond=showered_cond: [len(reader.filter_particles("simhits", sc=sc, st=st, sl=sl)) for sc, st, sl in get_unique_locs(reader.simhits, loc_ids=["sc", "st", "sl"])] if showered_cond(reader) else [],
            },
            f"SimHit_time_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"SimHit_time_{showered_state}", r";SimHit time (ns);", 100, 0, 1000),
                "func": lambda reader, showered_cond=showered_cond: [hit.time for hit in reader.simhits] if showered_cond(reader) else [],
            },
            f"SimHit_energyDeposit_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"SimHit_energyDeposit_{showered_state}", r";SimHit energy deposit (keV);", 100, 0, 10),
                "func": lambda reader, showered_cond=showered_cond: [hit.edep for hit in reader.simhits] if showered_cond(reader) else [],
            },
            f"SimHit_trackLength_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"SimHit_trackLength_{showered_state}", r";SimHit track length (cm);", 100, 0, 100),
                "func": lambda reader, showered_cond=showered_cond: [hit.track_length / 10 for hit in reader.simhits] if showered_cond(reader) else [],
            },
        # digis histos
        # --- Digi properties
            f"Digi_nDigis_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"Digi_nDigis_{showered_state}", r";Number of Digis;", 100, 0, 100),
                "func": lambda reader, showered_cond=showered_cond: len(reader.digis) if showered_cond(reader) else None,
            },
            f"Digi_nDigis_per_station_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"Digi_nDigis_per_station_{showered_state}", r";Number of Digis per station;", 100, 0, 100),
                "func": lambda reader, showered_cond=showered_cond: [len(reader.filter_particles("digis", sc=sc, st=st)) for sc, st in get_unique_locs(reader.digis, loc_ids=["sc", "st"])] if showered_cond(reader) else [],
            },
            f"Digi_nDigis_per_sl_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"Digi_nDigis_per_sl_{showered_state}", r";Number of Digis per superlayer;", 100, 0, 100),
                "func": lambda reader, showered_cond=showered_cond: [len(reader.filter_particles("digis", sc=sc, st=st, sl=sl)) for sc, st, sl in get_unique_locs(reader.digis, loc_ids=["sc", "st", "sl"])] if showered_cond(reader) else [],
            },
            f"Digi_tdc_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"Digi_tdc_{showered_state}", r";Digi TDC;", 1000, 0, 1000),
                "func": lambda reader, showered_cond=showered_cond: [digi.time for digi in reader.digis] if showered_cond(reader) else [],
            },
            f"Digi_BX_{showered_state}": {
                "type": "distribution",
                "histo": r.TH1D(f"Digi_BX_{showered_state}", r";Digi BX;", 50, 0, 50),
                "func": lambda reader, showered_cond=showered_cond: [digi.BX for digi in reader.digis] if showered_cond(reader) else [],
            },
    }
)

# histos.update(
#     {
#         "muonrad_vs_pt": {
#             "type": "eff",
#             "histoDen": r.TH1D("muonrad_vs_pt_total", r';Pt (GeV);', 200, 0, 2000),
#             "histoNum": r.TH1D("muonrad_vs_pt_num", r';Pt (GeV);', 200, 0, 2000),
#             "func": lambda reader: [gm.pt for gm in reader.gens],
#             "numdef": lambda reader: [any([digi.parent_pdgId != 13 for digi in reader.digis]) for gm in reader.gens],
#         },
#     }
# )

histos.update(
    {
        "muonshowered_vs_pt": {
            "type": "eff",
            "histoDen": r.TH1D("muonshowered_vs_pt_total", r';Pt (GeV);', 200, 0, 2000),
            "histoNum": r.TH1D("muonshowered_vs_pt_num", r';Pt (GeV);', 200, 0, 2000),
            "func": lambda reader: [gm.pt for gm in reader.gens],
            "numdef": lambda reader: [len(reader.realshowers) > 0 for gm in reader.gens],
        },
    }
)