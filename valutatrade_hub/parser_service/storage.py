import json
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List


class RatesStorage:
    def __init__(self, rates_path: str, history_path: str):
        self.rates_path = Path(rates_path)
        self.history_path = Path(history_path)

        self.rates_path.parent.mkdir(parents=True, exist_ok=True)
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.rates_path.exists():
            self._atomic_write(self.rates_path, {
                "pairs": {},
                "last_refresh": None,
            })

        if not self.history_path.exists():
            self._atomic_write(self.history_path, [])

    def _atomic_write(self, path: Path, data) -> None:
        tmp_path = path.with_suffix(path.suffix + ".tmp")

        with tmp_path.open("w", encoding="utf-8") as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)

        if path.exists():
            path.unlink()

        tmp_path.replace(path)



    def write_snapshot(self, pairs: Dict[str, Dict[str, object]]) -> None:
        snapshot = {
            "pairs": pairs,
            "last_refresh": datetime.now(timezone.utc).isoformat()
        }
        self._atomic_write(self.rates_path, snapshot)

    def append_history(self, records: List[Dict[str, object]]) -> None:
        if not records:
            return

        with self.history_path.open("r", encoding="utf-8") as f:
            history = json.load(f)

        history.extend(records)
        self._atomic_write(self.history_path, history)
