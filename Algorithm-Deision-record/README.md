## Architecture Decision Record (ADR)

### Decision

Use a **serverless architecture** with AWS managed services to implement API rate limiting.

### Context

Traditional rate limiting systems require dedicated servers, caching layers, and infrastructure management. The goal of this project was to create a scalable and cost-efficient system without maintaining servers.

### Alternatives Considered

1. Redis-based rate limiting using EC2
2. Nginx rate limiting
3. API Gateway built-in throttling

### Decision Outcome

The chosen architecture uses:

* API Gateway
* AWS Lambda
* DynamoDB
* SNS
* CloudWatch

This approach provides:

* Automatic scaling
* Minimal operational overhead
* Cost efficiency
* High availability

### Trade-offs

**Pros**

* Fully serverless
* Highly scalable
* Simple deployment

**Cons**

* Slight latency compared to in-memory solutions like Redis
* DynamoDB read/write cost at extremely high scale

Despite these trade-offs, the architecture provides an excellent balance between **simplicity, scalability, and cost efficiency**.
