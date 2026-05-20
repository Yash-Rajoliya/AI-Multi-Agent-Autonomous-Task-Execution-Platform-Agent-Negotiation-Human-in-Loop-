# Incident Response Runbook

Operational guide for diagnosing and resolving platform incidents.

---

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| P0 | Critical outage | Entire platform unavailable |
| P1 | Major degradation | Core workflows failing |
| P2 | Minor issue | Partial feature degradation |

---

## Incident Response Workflow

1. Identify and classify the issue
2. Check service health status
3. Review application logs
4. Review metrics and traces
5. Isolate impacted services
6. Restart or scale affected services
7. Roll back recent deployments if required
8. Validate system recovery
9. Document root cause and resolution

---

## Core Diagnostic Commands

### Check Containers

```bash
docker ps