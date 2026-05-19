# Sequence Diagram

User → API → Orchestrator → Queue → Worker → Agent Runtime → Memory → Response

1. User submits task
2. API validates request
3. Orchestrator builds execution graph
4. Tasks dispatched to queue
5. Worker consumes task
6. Agent executes logic
7. Memory accessed
8. Result returned