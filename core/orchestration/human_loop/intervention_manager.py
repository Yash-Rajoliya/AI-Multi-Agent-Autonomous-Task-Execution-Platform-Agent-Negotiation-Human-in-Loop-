class InterventionManager:
    def intervene(self, workflow):
        workflow["paused"] = True
        return workflow