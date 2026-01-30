from dtpr.utils.functions import color_msg, get_unique_locs
from pandas import DataFrame
from typing import Optional
from dtpr.base import Event, Particle


def build_real_showers(ev: Event, threshold: Optional[int] = None, debug: Optional[bool] = False) -> None:
    """
    Build real showers based on simhit information.
    
    :param ev: The event containing simhits to process
    :type ev: Event
    :param threshold: The threshold for shower building
    :type threshold: Optional[int]
    :param debug: Whether to enable debugging outputs
    :type debug: bool
    :return: None, modifies the event by adding realshowers attribute
    :rtype: None
    """

    ev.realshowers = []
    thr = 8 if threshold is None else threshold

    indexs = get_unique_locs(particles=ev.digis, loc_ids=["wh", "sc", "st", "sl"])

    for wh, sc, st, sl in indexs:

        digis_sdf = DataFrame([digi.__dict__ for digi in ev.filter_particles("digis", wh=wh, sc=sc, st=st, sl=sl)])

        _build_shower = False

        if not digis_sdf.empty:
            digis_sdf = digis_sdf[["l", "w", "parent_pdgId"]].drop_duplicates()
            # conditions...
            # pass the threshold of hits
            pass_thr = len(digis_sdf.drop_duplicates(["l", "w"])) >= thr
            # at least 3 muon hits
            are_muons_hits = len(digis_sdf.loc[digis_sdf["parent_pdgId"].abs() == 13]) >= 3
            # at least 1 electron hit
            are_electron_hits = len(digis_sdf.loc[digis_sdf["parent_pdgId"].abs() == 11]) > 0
            # hits are spread out in the chamber
            spread = digis_sdf["w"].std()**2 > 1

            if pass_thr:
                if debug: color_msg(f'spread: {spread} --> {digis_sdf["w"].std()**2}', "purple", indentLevel=2)
                if are_muons_hits and are_electron_hits and spread:
                    shower_type = 1
                elif are_electron_hits and spread:
                    shower_type = 2
                else:
                    continue
                _build_shower = True

        if _build_shower:
            _index = ev.realshowers[-1].index + 1 if ev.realshowers else 0
            _shower = Particle(index=_index, wh=wh, sc=sc, st=st, name="Shower") 
            _shower.shower_type = shower_type
            _shower.sl = sl
            ev.realshowers.append(_shower)
            if debug:
                color_msg(
                    f'Realshower detected in (wh, sc, st, sl): ({wh}, {sc}, {st}, {sl}) - type: {shower_type}',
                    "green",
                    indentLevel=2,
                )