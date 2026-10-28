class QueueWaitTracker:
    def __init__(self):
        self.entered_at = {}
        self.last_seen = {}
    def update(self, track_id, inside_queue, video_seconds):
        if inside_queue and track_id not in self.entered_at:
            self.entered_at[track_id] = video_seconds
        if inside_queue:
            self.last_seen[track_id] = video_seconds
            return max(0.0, video_seconds - self.entered_at.get(track_id, video_seconds))
        if track_id in self.entered_at:
            duration = max(0.0, self.last_seen.get(track_id, video_seconds) - self.entered_at[track_id])
            self.entered_at.pop(track_id, None)
            self.last_seen.pop(track_id, None)
            return duration
        return 0.0
    def average_active_wait(self, ids, video_seconds):
        vals = [max(0.0, video_seconds - self.entered_at[i]) for i in ids if i in self.entered_at]
        return sum(vals) / len(vals) if vals else 0.0
