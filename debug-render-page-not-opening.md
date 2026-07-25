# [OPEN] Render Page Not Opening

## Session
- Session ID: `render-page-not-opening`
- Date: 2026-07-25
- Symptom: deployed web page does not open

## Hypotheses
1. Render start command is incorrect or not using the expected port binding.
2. A required runtime dependency is missing from `requirements.txt`.
3. Render is reading a different startup configuration than expected.
4. Streamlit is starting in a way that fails Render health checks.
5. Deployment failure is caused by a Render environment/configuration issue.

## Evidence Log
- Session started.
- Confirmed deployment config files:
  - `Procfile` starts `streamlit run app.py --server.port $PORT`
  - `.streamlit/config.toml` binds `address = "0.0.0.0"`
- Local emulation with `PORT=8501` successfully started Streamlit and served on `http://localhost:8501`.
- Found import/runtime mismatch: `app.py` imports `langchain_text_splitters`, but `requirements.txt` did not include `langchain-text-splitters`.

## Interim Conclusion
- Rejected: bad local Streamlit port binding / broken start command.
- Leading cause: missing dependency in `requirements.txt` causing Render startup/import failure.

## Fix Applied
- Added `langchain-text-splitters` to `requirements.txt`.
- Made Render startup command fully explicit in `Procfile` and `render.yaml`:
  - `--server.address 0.0.0.0`
  - `--server.port $PORT`
  - `--server.headless true`

## Post-Fix Verification
- Local emulation with the explicit startup command successfully served the app on `http://localhost:8501`.

## Secondary Issue Found (ChromaDB on Render)
- The app uses ChromaDB, which requires SQLite > 3.35.0. Render's default environment uses an older version of SQLite.
- This causes a crash during deployment: `RuntimeError: Your system has an unsupported version of sqlite3. Chroma requires sqlite3 >= 3.35.0.`

## Final Fix Applied
- Added `pysqlite3-binary` to `requirements.txt`.
- Added the sqlite3 override block to the top of `app.py`, `main.py`, and `create_database.py` (before any other imports).
- This resolves the ChromaDB sqlite3 version requirement on Render. The web page should now open successfully after the next deployment.
