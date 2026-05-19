# Scaling Strategy

## Horizontal Scaling
- API: stateless → scale via load balancer
- Workers: scale based on queue size

## Queue Scaling
- Redis cluster / Kafka (future)

## Memory Scaling
- Vector DB sharding
- Hybrid retrieval

## Bottlenecks
- LLM latency
- Vector search

## Mitigation
- Caching
- Async execution
- Batch processing