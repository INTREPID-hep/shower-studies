def cut_on_pt(reader, threshold=1000):

    good_event = True

    for gen in getattr(reader, "gens", []):
        if gen.pt > threshold:
            good_event = False
            break

    return good_event