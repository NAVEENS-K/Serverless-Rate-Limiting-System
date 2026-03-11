## Deployment Steps

Follow these steps to deploy the Serverless Rate Limiting System using AWS Console.

### 1. Create DynamoDB Table

1. Open **AWS DynamoDB Console**
2. Click **Create Table**

Configuration:

* Table Name: `rate-limit-table`
* Partition Key: `client_id (String)`

Enable:

* **TTL (Time To Live)**

TTL Attribute:

```
ttl
```

This allows DynamoDB to automatically delete expired rate-limit records.

---

### 2. Create Lambda Function

1. Open **AWS Lambda**
2. Click **Create Function**

Configuration:

* Runtime: Python 3.x
* Function Name: `rateLimiterFunction`

Permissions:

Attach IAM role with permissions for:

* DynamoDB access
* CloudWatch logging
* SNS publishing

---

### 3. Connect DynamoDB to Lambda

Inside Lambda:

* Add environment variable

Example:

```
TABLE_NAME = rate-limit-table
```

Lambda will use this table to store request counters.

---

### 4. Create SNS Topic

1. Open **Amazon SNS**
2. Create a topic

Example:

```
rate-limit-alerts
```

Subscribe with:

* Email
* SMS
* HTTP endpoint

This topic will send alerts when limits are exceeded.

---

### 5. Configure API Gateway

1. Open **API Gateway**
2. Create a **REST API**

Create an endpoint:

```
/dashboard
```

Integration type:

```
Lambda Function
```

Select:

```
rateLimiterFunction
```

Deploy the API to a stage:

```
prod
```

---

### 6. Test the API

Example request:

```
GET https://api-id.execute-api.region.amazonaws.com/prod/dashboard
```

Expected responses:

* Request allowed
* Rate limit exceeded
