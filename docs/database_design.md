# Database design
New application-owned tables: `qsr_users`, `qsr_video_sources`, `qsr_processing_runs`, `qsr_queue_measurements`, `qsr_queue_events`, `qsr_alerts`, and `qsr_settings`.

All are additive and use a `qsr_` prefix. Existing unrelated tables are not modified. Back up the database and review migrations before production rollout.
