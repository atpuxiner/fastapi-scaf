from typing import Dict, List, Optional


class BaseBiz:

    @staticmethod
    def format_all(rows, fields: List[str]) -> List[Dict[str, Optional[str]]]:
        if not rows:
            return []
        return [dict(zip(fields, row)) for row in rows]

    @staticmethod
    def format_one(row, fields: List[str]) -> Dict[str, Optional[str]]:
        if not row:
            return dict()
        return dict(zip(fields, row))
