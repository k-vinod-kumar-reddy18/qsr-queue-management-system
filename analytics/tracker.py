def get_track_id(box, index):
    # Ultralytics track() normally supplies persistent IDs. Fallback IDs are frame-local and must not be
    # treated as persistent across frames.
    try:
        value = box.id
        if value is not None:
            return int(value.item())
    except Exception:
        pass
    return 1000000 + index
