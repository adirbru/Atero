# client/naive_client.py

from solution_client import optimize
optimize(optimize_cpu=False)

from sprompt.security_policy_manager import SecurityPolicyManagerPrimary
from sprompt.prompt_security_engine import PromptSecurityEngine


def main():
    # Instantiate the security policy manager.
    # This will use the library's naive (slow) approach to generate the security policy.
    print("Generating security policy naively without caching...")
    manager = SecurityPolicyManagerPrimary()
    policy = manager.create_policy("high", ["no external links", "strict sanitization"])
    # Instantiate the prompt security engine with the generated policy.
    engine = PromptSecurityEngine(policy)
    
    # Define a test prompt.
    prompt = "This is a benign prompt with malicious content <script>evil()</script>"
    
    # Process the prompt using the security engine.
    report = engine.process_prompt(prompt)
    
    # Display the security report.
    print("Security Report:")
    print(report)

if __name__ == "__main__":
    main()
