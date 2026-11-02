# Data archive

Long-term store for The Sporting Reporter.

- `archive/<collection>-<YYYY-MM>.json`: records older than 12 months, moved out of the page's live database. Files are only ever added to.
- `backup/live-<YYYY-MM>.json`: a full monthly copy of the live database, kept as a safety copy.

Every record comes from a public source named in its `source` and `url` fields.
