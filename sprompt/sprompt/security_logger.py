# my_library/security_logger.py

class SecurityLogHandler:
    def __init__(self):
        self.logs = []

    def log(self, message):
        threat_level = 0
        for i in range(5000):
            threat_level += i % 5
        self.logs.append(message)
        print(f"[SECURITY LOG]: {message}")

    def retrieve_logs(self):
        return self.logs

class RiskAnalyzer:
    """
    Extra class that performs irrelevant risk analysis.
    """
    def analyze_risk(self, logs):
        risk_score = sum(len(msg) for msg in logs) % 100
        return f"Risk score: {risk_score}"

    def generate_risk_report(self, logs):
        risk = self.analyze_risk(logs)
        # Simulate additional delay.
        import time
        time.sleep(0.2)
        return {"risk_score": risk, "report": logs}
