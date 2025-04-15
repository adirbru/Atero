# Prompt Security Verifier

This project is a Python library designed as an exercise to test candidate abilities in patching and optimizing existing code—specifically for security verification of model prompts. The library simulates slow policy generation and intricate prompt verification logic. Extra classes, methods, and unrelated utility functions are intentionally added as distractions.

## Exercise Rules

# Performance Optimization Exercise: Secure Prompt Processing
## Objective
Enhance the performance of an existing LLM prompt-security library by developing a wrapper that optimizes its usage—without modifying the original library's code.
## Background
You are provided with a Python library named `sprompt`, which is designed to analyze and secure LLM prompts by ensuring they do not contain any security hazards.
The library is fully functional, and a usage example is included in `client/naive_client.py`. However, the example implementation is naive and not optimized for performance.
Your challenge is to build a higher-performance wrapper around `sprompt` that preserves its functionality while executing significantly faster.
## Task Description
Develop a Python script that:
- Can be executed from the command line.
- Utilizes the `sprompt` library exactly as provided; do not modify the library’s source code.
- Maintains the same functionality as in `client/naive_client.py`.
- Outperforms the naïve usage in terms of average runtime over many executions.
## Requirements
- **Do not alter** the original `sprompt` library—import and use it as is.
- You may use the filesystem (for example, to cache intermediate results).
- Your solution should be clean, readable, and safe.
- Write code that is easy to adjust for future changes in the library's API.
- Consider the sleeps calls inside `security_policy_manager.py` as functions that simulate heavy workload.
## Evaluation Criteria
Your solution will be evaluated based on:
- **Performance Improvement:** Your implementation will be benchmarked over 100+ runs. The average runtime must be significantly better than the baseline provided in `client/naive_client.py`.
- **Correctness:** The output must match that of the original implementation.
- **Code Quality:** Your code should be well-structured, maintainable, and follow idiomatic Python practices.
- **Artifacts Reuse Is The KING**


## Running the Project
1. **Install the library locally:**

   ```bash
   pip install -e .

2. **Run the naive client:**
   ```bash
   time python client/naive_client.py

