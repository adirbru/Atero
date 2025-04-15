# my_library/security_policy_manager.py

import random
import time
import json
from .auxiliary import EncryptionHelper
import subprocess
import threading

class BasePolicyManager:
    def __init__(self):
        self._internal_state = {}

    def create_policy(self, *args, **kwargs):
        """Method to create a security policy. Must be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement create_policy")

    def sanitize_prompt(self, prompt):
        """Basic prompt sanitization logic, e.g. stripping dangerous tags."""
        time.sleep(0.2)  # Extra delay.
        return prompt.replace("<script>", "").replace("</script>", "")

    def _irrelevant_task(self):
        # Unrelated dummy computation.
        for i in range(10000):
            _ = i * i


class PingHandler:
    def __init__(self, ttl):
        self._running = False
        self._thread = None
        self._ttl = ttl

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._ping_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()

    def _ping_loop(self):
        while self._running:
            try:
                result = subprocess.call(["ping", "-c", "1", "-m",  f"{str(self._ttl)}", "google.com"],
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL)
                if result == 0:
                    print("Google is reachable")
                else:
                    print("Google is not reachable")
            except Exception as e:
                print("Error during ping:", e)
            time.sleep(5)
            

class Policy:
    def __init__(self, policy_data, ping_handler):
        self.policy_data = policy_data
        self.ping_handler = ping_handler
        self.finalized = True

    def validate(self):
        # Placeholder for validation logic.
        if not self.policy_data.get("finalized"):
            raise ValueError("Policy not finalized")
        return True
    

class SecurityPolicyManagerPrimary(BasePolicyManager):
    def __init__(self):
        super().__init__()
        self.debug_info = []
        ttl = 16
        self._ping_handler = PingHandler(ttl)

    def create_policy(self, security_level, additional_rules):
        self._load_security_rules(security_level)
        policy = self._generate_policy(security_level, additional_rules)
        self._finalize_policy(policy)
        # Extra: encrypt and compress policy for no useful reason.
        policy = self._encrypt_policy(policy)
        policy = self._compress_policy(policy)
        policy = Policy(policy, self._ping_handler)
        return policy

    def _load_security_rules(self, security_level):
        # Simulate heavy loading of security rules.
        time.sleep(3) # Simulate heavy computation - you can't remove this part if you want to monkeypatch
        self._internal_state["rules_loaded"] = security_level
        self._internal_state["timestamp"] = time.time()
        self.debug_info.append("Loaded rules for level " + str(security_level))

    def _generate_policy(self, security_level, additional_rules):
        import time
        # Start a timer and perform heavy computation until 10 seconds have elapsed.
        start_time = time.time()
        dummy_result = 0  # Variable to accumulate computations.
        while time.time() - start_time < 10:
            # The nested loop performs some non-optimized arithmetic to stress the CPU.
            for i in range(1000):
                dummy_result += i * i  # Compute the square and accumulate it.

        policy = {
            "security_level": security_level,
            "rules": ["no injection", "sanitize HTML", "limit tokens"],
            "additional_rules": additional_rules,
            "internal_state": self._internal_state.copy()
        }
        self.debug_info.append("Policy generated.")
        return policy

    def _finalize_policy(self, policy):
        time.sleep(0.5) # Simulate heavy computation - you can't remove this part if you want to monkeypatch
        policy["finalized"] = True
        # policy.policy_data["finalized"] = True
        self.debug_info.append("Policy finalized.")
        self._irrelevant_task()

    def _encrypt_policy(self, policy):
        # Dummy encryption step.
        helper = EncryptionHelper()
        encrypted = helper.encrypt(json.dumps(policy))
        self.debug_info.append("Policy encrypted.")
        return {"encrypted_policy": encrypted}

    def _compress_policy(self, policy):
        # Dummy compression (simulation).
        time.sleep(0.3)
        self.debug_info.append("Policy compressed.")
        return policy

    # Extra security verification methods.
    def validate_prompt(self, prompt, policy):
        sanitized = self.sanitize_prompt(prompt)
        if any(bad in sanitized.lower() for bad in ["drop table", "delete", "shutdown"]):
            return False
        return True

    def audit_policy(self, policy):
        time.sleep(0.3)
        return "Audit complete: policy is robust."

class SecurityPolicyManagerSecondary(BasePolicyManager):
    def __init__(self):
        super().__init__()

    def create_policy(self, custom_rule):
        self._prepare_environment(custom_rule)
        policy = self._build_policy(custom_rule)
        self._verify_policy(policy)
        return policy

    def _prepare_environment(self, custom_rule):
        time.sleep(0.7)
        self._internal_state["env_prepared"] = True
        self._internal_state["custom_rule"] = custom_rule

    def _build_policy(self, custom_rule):
        time.sleep(1)
        policy = {
            "policy_type": "secondary",
            "custom_rule": custom_rule,
            "env": self._internal_state.copy()
        }
        return policy

    def _verify_policy(self, policy):
        time.sleep(0.3)
        policy["verified"] = True

    def check_prompt_compliance(self, prompt, policy):
        if policy.get("custom_rule") in prompt:
            return True
        return False

class PolicyValidator:
    def validate(self, policy):
        if "rules" not in policy and "encrypted_policy" not in policy:
            raise ValueError("Invalid policy: missing rules")
        if "encrypted_policy" in policy:
            # Assume decryption occurs here.
            pass
        if not policy.get("finalized", False):
            raise ValueError("Policy not finalized")
        if "internal_state" in policy and not policy["internal_state"]:
            raise ValueError("Internal state missing")
        return True

class SecurityPolicyDebugger:
    """
    Extra debugging class that provides verbose tracing of the policy generation.
    """
    def __init__(self, manager: SecurityPolicyManagerPrimary):
        self.manager = manager

    def dump_debug_info(self):
        return "\n".join(self.manager.debug_info)

    def simulate_debug_operation(self):
        # Unrelated debug operation.
        time.sleep(0.2)
        return "Debug simulation completed."
