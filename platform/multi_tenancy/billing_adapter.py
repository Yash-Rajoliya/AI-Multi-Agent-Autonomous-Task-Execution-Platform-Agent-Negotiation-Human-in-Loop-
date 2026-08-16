class BillingAdapter:
    def charge(self, tenant_id: str, amount: float):
        # Integrate with Stripe/Razorpay in real system
        print(f"[Billing] Charging {tenant_id}: ${amount}")

    def get_usage_cost(self, usage: int) -> float:
        return usage * 0.01  # simple pricing