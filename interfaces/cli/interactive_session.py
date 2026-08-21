import asyncio
from .commands import Commands


class InteractiveSession:
    def __init__(self):
        self.commands = Commands()

    async def start(self):
        print("AI Platform CLI (type 'exit' to quit)")

        while True:
            cmd = input("> ")

            if cmd == "exit":
                break

            elif cmd.startswith("create_task"):
                await self.commands.create_task({"task": cmd})

            elif cmd == "list_agents":
                await self.commands.list_agents()

            elif cmd.startswith("run_workflow"):
                await self.commands.run_workflow({"workflow": cmd})

            else:
                print("Unknown command")