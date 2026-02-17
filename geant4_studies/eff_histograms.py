import ROOT as r
from functools import partial
from dtpr.utils.functions import get_unique_locs
from utils.genmuon_functions import stations
from efficiencies.shower_histos import tpfptnfn_func, shower_eff_func, shower_eff_numdef

# - shower_tpfptnfn_MB1
# - shower_tpfptnfn_MB2
# - shower_tpfptnfn_MB3
# - shower_tpfptnfn_MB4
# - fwshower_eff_MB1
# - fwshower_eff_MB2
# - fwshower_eff_MB3
# - fwshower_eff_MB4
# - fwshower_eff_MB1_onlytpfp
# - fwshower_eff_MB2_onlytpfp
# - fwshower_eff_MB3_onlytpfp
# - fwshower_eff_MB4_onlytpfp

histos = {}

def get_locs_to_check(reader, station=1, opt=1, by_sl=False):
    loc_ids = ["wh", "sc", "st", "sl"] if by_sl else ["wh", "sc", "st"]
    if opt == 3:
        indexs = get_unique_locs(particles=reader.filter_particles("digis", st=station), loc_ids=loc_ids)
        return indexs

    fwshowers_locs = get_unique_locs(particles=reader.filter_particles("fwshowers", st=station), loc_ids=loc_ids)
    realshowers_locs = get_unique_locs(particles=reader.filter_particles("realshowers", st=station), loc_ids=loc_ids)

    if opt == 1: #every chamber with showers, and traversed by genmuons
        _gm_seg_locs = get_unique_locs(particles=[seg for seg in reader.segs if seg.st==station], loc_ids=["wh", "sc", "st"])
        if by_sl:
            gm_seg_locs = set()
            for wh, sc, st in _gm_seg_locs:
                gm_seg_locs.add((wh, sc, st, 1)) # sl 1
                gm_seg_locs.add((wh, sc, st, 3)) # sl 3
        else:
            gm_seg_locs = _gm_seg_locs
        indexs = fwshowers_locs.union(realshowers_locs).union(gm_seg_locs)

    if opt == 2: #every chamber which any shower
        indexs = fwshowers_locs.union(realshowers_locs)

    return indexs


for st in stations:
    histos.update({ # conf maps
        "shower_tpfptnfn_MB" + str(st): {
        "type": "distribution2d",
        "histo": r.TH2D(f"shower_tpfptnfn_MB{st}", r';Wheel; [TP, FP, TN, FN]', 5, -2.5, 2.5, 4, 0, 4),
        "func": partial(tpfptnfn_func, station=st, locs_getter=get_locs_to_check),
        }, # ----- efficiency
        "fwshower_eff_MB" + str(st):{ 
            "type": "eff",
            "histoDen" : r.TH1D(f"Fwshower_eff_MB{st}_total", r';Wheel; Events', 5, -2.5 , 2.5),
            "histoNum" : r.TH1D(f"Fwshower_eff_MB{st}_num", r';Wheel; Events', 5, -2.5 , 2.5),
            "func"     : partial(shower_eff_func, station=st, locs_getter=get_locs_to_check),
            "numdef"   : partial(shower_eff_numdef, station=st, locs_getter=get_locs_to_check),
        },
        f"fwshower_eff_MB{st}_onlytpfp":{
            "type": "eff",
            "histoDen" : r.TH1D(f"Fwshower_eff_MB{st}_onlytpfp_total", r';Wheel; Events', 5, -2.5 , 2.5),
            "histoNum" : r.TH1D(f"Fwshower_eff_MB{st}_onlytpfp_num", r';Wheel; Events', 5, -2.5 , 2.5),
            "func"     : partial(shower_eff_func, station=st, opt=2, locs_getter=get_locs_to_check),
            "numdef"   : partial(shower_eff_numdef, station=st, opt=2, locs_getter=get_locs_to_check),
        },
    })

histos.update({
    "gen_pt": {
        "type": "distribution",
        "histo": r.TH1D("gen_pt", r';pT [GeV]; Events', 100, 0, 1200),
        "func": lambda reader: [gen.pt for gen in getattr(reader, "gens", [])],
    },
})