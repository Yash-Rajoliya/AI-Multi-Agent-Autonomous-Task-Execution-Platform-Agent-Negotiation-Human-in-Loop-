from .checkpointing import CheckpointManager


class RecoveryManager:
    def __init__(self):
        self.checkpoint = CheckpointManager()

    def recover(self):
        return self.checkpoint.load()