## Monitoring

The system integrates AWS monitoring services to track performance and detect issues.

### CloudWatch Logs

AWS Lambda automatically sends logs to CloudWatch.

Logs include:

* Incoming request information
* DynamoDB operations
* Rate limit violations
* Execution errors

Example log:

```
Client: 192.168.1.10
Request Count: 3
Remaining: 2
```

---

### CloudWatch Metrics

Metrics help monitor system performance.

Important metrics:

| Metric             | Purpose                             |
| ------------------ | ----------------------------------- |
| API Request Count  | Total number of requests            |
| Lambda Invocations | Lambda execution frequency          |
| Lambda Errors      | Detect system failures              |
| Throttled Requests | Requests blocked due to rate limits |

---

### SNS Alerts

When the request limit is exceeded, the system can trigger alerts using SNS.

Alerts can be delivered via:

* Email
* SMS
* Webhooks

Example notification:

```
Rate limit exceeded for client: 192.168.1.10
```

---

### Monitoring Benefits

Observability helps:

* Detect abuse patterns
* Monitor system performance
* Debug issues quickly
* Maintain reliability
