import diskcache
import pickle
import hashlib
from typing import Callable, Any
from sprompt.security_policy_manager import SecurityPolicyManagerPrimary
import sprompt.prompt_security_engine

# Constants
DEFAULT_CACHE_EXPIRATION = 60 * 60
CACHE_MAX_SIZE = 1024 ** 3
cache = diskcache.Cache('./cache', size_limit=CACHE_MAX_SIZE)

# Keeping the original functions aside
original_create_policy = SecurityPolicyManagerPrimary.create_policy
original_prompt_security_engine_init = sprompt.prompt_security_engine.PromptSecurityEngine.__init__
original_prompt_security_engine_process_prompt = sprompt.prompt_security_engine.PromptSecurityEngine.process_prompt


def hash_string(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()


def hash_object(obj: Any) -> str:
    return hashlib.sha256(pickle.dumps(obj)).hexdigest()


def cached_method_wrapper(original_function: Callable, cache_key: Callable[..., str],
                          expiration: int = DEFAULT_CACHE_EXPIRATION):
    """
    Returns a cached version of the original function.
    In case the parameters were used in the past - uses their cache values.
    Otherwise - run the original function.
    :param original_function: original function to fallback in case it doesn't exist in the cache.
    :param cache_key: a function that takes the function parameters to store a unique state
    :param expiration: how much time to save the cache for
    """
    def wrapper(self, *args, **kwargs):
        key = cache_key(*args, **kwargs)
        if key in cache:
            return cache[key]
        result = original_function(self, *args, **kwargs)
        cache.set(key, result, expire=expiration)
        return result
    return wrapper


class CachedPromptSecurityEngine(sprompt.prompt_security_engine.PromptSecurityEngine):
    expiration = DEFAULT_CACHE_EXPIRATION

    def __init__(self, policy):
        policy_hash = hashlib.sha256(pickle.dumps(policy)).hexdigest()
        # Initializing the policy from the cache.
        if policy_hash in cache:
            self.__dict__.update(pickle.loads(cache[policy_hash]).__dict__)
        else:
            original_prompt_security_engine_init(self, policy)
            cache.set(policy_hash, pickle.dumps(self), expire=self.expiration)

    def process_prompt(self, prompt: str):
        cached_function = cached_method_wrapper(
            cache_key=lambda prompt: f'{hash_string(prompt)}-{hash_object(self.policy)}',
            original_function=original_prompt_security_engine_process_prompt)
        return cached_function(self, prompt)


def monkey_patching_cache():
    SecurityPolicyManagerPrimary.create_policy = cached_method_wrapper(
        cache_key=lambda security_level, additional_rules: hash_string(f'{security_level}-{additional_rules}'),
        original_function=original_create_policy
    )


def optimize(optimize_cpu=False):
    monkey_patching_cache()
    if not optimize_cpu:
        sprompt.prompt_security_engine.PromptSecurityEngine = CachedPromptSecurityEngine


def main():
    optimize(optimize_cpu=False)
    manager = SecurityPolicyManagerPrimary()
    policy = manager.create_policy("high", ["no external links", "strict sanitizations"])
    # Instantiate the prompt security engine with the generated policy.
    engine = sprompt.prompt_security_engine.PromptSecurityEngine(policy)

    # Define a test prompt.
    prompt = "This is a benign prompt with malicious content <script>evil()</script>"

    # Process the prompt using the security engine.
    report = engine.process_prompt(prompt)

    # Display the security report.
    print("Security Report:")
    print(report)


if __name__ == "__main__":
    main()
