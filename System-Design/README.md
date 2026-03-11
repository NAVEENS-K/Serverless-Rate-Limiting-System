## System Design

The system implements a **serverless rate limiting architecture** to protect APIs from abuse and excessive traffic. The design focuses on scalability, fault tolerance, and minimal operational overhead.

### Design Goals

* Prevent API abuse
* Track request usage per client
* Automatically reset usage counters
* Scale automatically with traffic
* Maintain low operational cost

### Architecture Pattern

The system follows a **serverless microservice pattern** where each AWS service handles a specific responsibility:

* **API Gateway** acts as the entry point for HTTP requests.
* **AWS Lambda** processes requests and implements rate limiting logic.
* **DynamoDB** stores request counters with expiration (TTL).
* **SNS** handles alerts when limits are exceeded.
* **CloudWatch** provides logging and monitoring.

This design removes the need for traditional servers and allows the system to automatically scale based on incoming traffic.
