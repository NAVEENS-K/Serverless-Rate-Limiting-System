## Why Fixed Window Was Chosen

The **Fixed Window algorithm** was selected for this project due to its simplicity and compatibility with serverless architecture.

Key reasons:

* DynamoDB efficiently stores request counters
* TTL automatically resets the window
* Minimal computation required in Lambda
* Low latency and low cost

Because the goal of this project is to demonstrate **serverless rate limiting architecture**, the Fixed Window method provides a clean and scalable solution.

In large-scale production systems, more advanced algorithms such as **Sliding Window** or **Token Bucket** may be preferred to prevent burst traffic.
