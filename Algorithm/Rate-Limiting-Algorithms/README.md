## Rate Limiting Algorithms

Rate limiting is a technique used to control the number of requests a client can make to an API within a defined time window. Several algorithms are commonly used in distributed systems.

This project implements the **Fixed Window algorithm**, but other algorithms are also widely used depending on system requirements.

---

### 1. Fixed Window Algorithm

The **Fixed Window** algorithm limits requests within a fixed time interval.

Example:

* Limit: 5 requests
* Window: 1 minute

If a user sends:

```
5 requests within 1 minute → allowed
6th request → blocked
```

At the start of the next minute, the counter resets.

**Advantages**

* Simple implementation
* Low computational overhead
* Easy to implement with databases like DynamoDB

**Disadvantages**

* Allows burst traffic near window boundaries

Example:

```
5 requests at 00:59
5 requests at 01:00
```

Total:

```
10 requests within 2 seconds
```

---

### 2. Sliding Window Algorithm

The **Sliding Window** algorithm provides smoother request distribution by tracking requests over a rolling time window.

Instead of resetting counters at fixed intervals, it continuously evaluates requests over the previous time duration.

Example:

```
Limit: 5 requests per 60 seconds
```

If a request occurs at:

```
12:00:30
```

The system checks requests from:

```
11:59:30 → 12:00:30
```

**Advantages**

* More accurate rate limiting
* Prevents burst traffic

**Disadvantages**

* Higher computational cost
* Requires storing request timestamps

---

### 3. Token Bucket Algorithm

The **Token Bucket** algorithm controls request flow using tokens.

How it works:

1. Tokens are added to a bucket at a fixed rate.
2. Each request consumes one token.
3. If no tokens are available, the request is rejected.

Example:

```
Bucket size = 10
Token refill rate = 1 token/sec
```

If the bucket has tokens:

```
Requests are allowed
```

If empty:

```
Requests are blocked
```

**Advantages**

* Allows controlled burst traffic
* Very efficient

**Disadvantages**

* Slightly more complex implementation

---

### 4. Leaky Bucket Algorithm

The **Leaky Bucket** algorithm processes requests at a constant rate.

Incoming requests are placed into a queue.

Requests "leak" out of the bucket at a fixed rate.

Example:

```
Queue size = 10
Processing rate = 1 request/sec
```

If the queue becomes full:

```
New requests are dropped
```

**Advantages**

* Smooth traffic flow
* Prevents burst spikes

**Disadvantages**

* Can introduce latency due to queueing
