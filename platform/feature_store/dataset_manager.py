from typing import Dict, List, Any


class DatasetManager:
    def __init__(self):
        self.datasets: Dict[str, Dict[str, List[Any]]] = {}

    def _get_key(self, tenant_id: str, name: str) -> str:
        return f"{tenant_id}:{name}"

    def create_dataset(self, tenant_id: str, name: str):
        if tenant_id not in self.datasets:
            self.datasets[tenant_id] = {}
        if name not in self.datasets[tenant_id]:
            self.datasets[tenant_id][name] = []

    def add_data(self, tenant_id: str, name: str, record: Any):
        if tenant_id not in self.datasets or name not in self.datasets[tenant_id]:
            raise ValueError(f"Dataset '{name}' not found for tenant '{tenant_id}'")
        self.datasets[tenant_id][name].append(record)

    def get_dataset(self, tenant_id: str, name: str) -> List[Any]:
        return self.datasets.get(tenant_id, {}).get(name, [])