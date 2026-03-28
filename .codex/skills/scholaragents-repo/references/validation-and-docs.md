# Validation and Docs

## Validation

After meaningful changes, prefer running:

```bash
python -m compileall scholaragents examples
python examples/demo.py
```

If you modify models or retrieval, also verify:

- mock mode still works with no credentials
- traces still show provider information
- literature flows remain readable
- artifact export still succeeds

## Documentation Rules

When behavior changes, consider updating:

- `README.md`
- `CHANGELOG.md`
- `outputs/README.md`

Keep docs practical. Prefer:

- what changed
- how to run it
- where to look in the repo

## Repo Presentation

The repository intentionally keeps a small set of generated artifacts in `outputs/` so GitHub viewers can inspect:

- Markdown artifact layout
- JSON artifact structure
- artifact index format
