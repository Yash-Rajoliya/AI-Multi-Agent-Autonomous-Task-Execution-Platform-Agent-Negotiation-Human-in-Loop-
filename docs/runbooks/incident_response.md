
# Incident Response

## Severity Levels

- P0: System down
- P1: Major degradation
- P2: Minor issue

---

## Steps

1. Identify issue
2. Check logs
3. Check metrics
4. Restart service
5. Rollback if needed

---

## Common Issues

### Redis Down
- Restart container
- Check connection

### Worker Crash
- Check logs
- Restart worker

### High Latency
- Check LLM calls
- Enable caching