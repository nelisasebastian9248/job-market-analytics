## dbt Project

This folder contains the dbt transformation layer for Job Market Analytics.

Key model groups:

- `models/staging`
  - Source-backed cleanup models for job postings and GitHub repositories
- `models/intermediate`
  - Skill extraction logic from job descriptions
- `models/marts`
  - Final dashboard-ready tables for skill demand, salary benchmarks, and GitHub momentum

Useful commands:

```powershell
.\run_dbt.ps1 debug
.\run_dbt.ps1 seed --select skills
.\run_dbt.ps1 run
.\run_dbt.ps1 test
```
