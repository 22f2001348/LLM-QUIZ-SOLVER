This folder contains simple monitor scripts you can run locally to poll the Hugging Face Space `healthz` endpoint.

Files:
- `monitor.ps1` : PowerShell script that polls `/healthz` repeatedly and prints status.
- `monitor.py` : Python script doing the same. Requires `requests` in the environment.

Example (PowerShell):
```powershell
.\scripts\monitor.ps1 -Url 'https://DS22F2001348-llm-quiz-solver.hf.space/healthz' -Interval 10
```

Example (Python):
```bash
python scripts/monitor.py --url https://DS22F2001348-llm-quiz-solver.hf.space/healthz --interval 10
```
