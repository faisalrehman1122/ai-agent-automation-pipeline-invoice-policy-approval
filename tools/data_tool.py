import pandas as pd
from typing import Dict, Any, Optional

class DataTool:
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None

    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        try:
            self.data = pd.read_csv(file_path)
            return {
                "status": "success",
                "rows": len(self.data),
                "columns": list(self.data.columns),
                "message": f"Successfully loaded {len(self.data)} rows"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def preview(self, n_rows: int = 5) -> Dict[str, Any]:
        if self.data is None:
            return {"status": "error", "message": "No data loaded"}
        
        return {
            "status": "success",
            "preview": self.data.head(n_rows).to_dict('records'),
            "shape": self.data.shape
        }

    def analyze(self) -> Dict[str, Any]:
        if self.data is None:
            return {"status": "error", "message": "No data loaded"}
        
        analysis = {
            "status": "success",
            "missing_values": {},
            "statistics": {},
            "top_categories": {}
        }

        for col in self.data.columns:
            missing_count = self.data[col].isna().sum()
            missing_pct = (missing_count / len(self.data)) * 100
            analysis["missing_values"][col] = {
                "count": int(missing_count),
                "percentage": round(missing_pct, 2)
            }

            if self.data[col].dtype in ['int64', 'float64']:
                analysis["statistics"][col] = {
                    "mean": float(self.data[col].mean()) if not self.data[col].isna().all() else None,
                    "min": float(self.data[col].min()) if not self.data[col].isna().all() else None,
                    "max": float(self.data[col].max()) if not self.data[col].isna().all() else None
                }
            else:
                top_values = self.data[col].value_counts().head(5).to_dict()
                analysis["top_categories"][col] = {
                    k: int(v) for k, v in top_values.items()
                }

        return analysis
