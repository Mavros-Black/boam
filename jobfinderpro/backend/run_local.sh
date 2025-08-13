#!/usr/bin/env bash
set -euo pipefail

export PYTHONUNBUFFERED=1
export ALLOWED_ORIGINS=${ALLOWED_ORIGINS:-http://localhost:5173}
export PORT=${PORT:-8000}

python3 -m pip install -U pip
python3 -m pip install -r /workspace/jobfinderpro/backend/requirements.txt
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --reload