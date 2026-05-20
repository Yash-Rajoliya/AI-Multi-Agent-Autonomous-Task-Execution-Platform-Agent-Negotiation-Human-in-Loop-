from prometheus_client import Counter, Histogram


class Metrics:
    request_count = Counter("requests_total", "Total Requests")
    latency = Histogram("request_latency_seconds", "Request latency")

    @staticmethod
    def track_request():
        Metrics.request_count.inc()

    @staticmethod
    def track_latency(value: float):
        Metrics.latency.observe(value)