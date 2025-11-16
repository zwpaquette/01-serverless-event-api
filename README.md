# Serverless Event API

A fully serverless REST API built with AWS Lambda, API Gateway v2 (HTTP API), and DynamoDB. This project demonstrates modern serverless architecture patterns using Infrastructure as Code (Terraform).

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │───▶│   AWS Lambda    │───▶│    DynamoDB     │    │   CloudWatch    │
│   (HTTP API)    │    │   (Python 3.12) │    │     Table       │    │   Dashboard     │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Components

- **API Gateway v2 (HTTP API)**: RESTful endpoint with `ANY /{proxy+}` routing
- **AWS Lambda**: Python 3.12 runtime handling GET and POST requests
- **DynamoDB**: NoSQL database with pay-per-request billing
- **IAM Roles**: Least-privilege access policies
- **CloudWatch**: Monitoring dashboard and logging

## 🚀 Features

- **GET Requests**: Retrieve all items from the database
- **POST Requests**: Add new items to the database
- **Error Handling**: Proper HTTP status codes and error messages
- **JSON Validation**: Request body validation
- **Logging**: Structured logging with AWS CloudWatch
- **Monitoring**: Real-time metrics dashboard
- **Infrastructure as Code**: Complete Terraform configuration

## 📋 Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.5.0
- Python 3.12 (for local development)
- An AWS account with necessary permissions

## 🛠️ Installation & Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/zwpaquette/01-serverless-event-api.git
cd 01-serverless-event-api
```

### 2. Configure Variables (Optional)

Edit `terraform/variables.tf` to customize:

```hcl
variable "region" {
  type    = string
  default = "us-east-1"  # Change to your preferred region
}

variable "project_name" {
  type    = string
  default = "serverless-api"  # Change to your project name
}

variable "table_name" {
  type    = string
  default = "serverless-items"  # Change to your table name
}
```

### 3. Deploy Infrastructure

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 4. Get API Endpoint

After deployment, Terraform will output your API endpoint:

```bash
terraform output api_endpoint
```

## 📚 API Usage

### Base URL

Your API will be available at: `https://{api-id}.execute-api.{region}.amazonaws.com`

### Endpoints

#### GET - Retrieve All Items

```bash
curl -X GET https://your-api-endpoint.execute-api.us-east-1.amazonaws.com/
```

**Response:**

```json
[
  {
    "id": "item1",
    "name": "Sample Item",
    "description": "This is a sample item"
  }
]
```

#### POST - Add New Item

```bash
curl -X POST https://your-api-endpoint.execute-api.us-east-1.amazonaws.com/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "item1",
    "name": "Sample Item",
    "description": "This is a sample item"
  }'
```

**Response:**

```json
{
  "message": "Item added",
  "id": "item1"
}
```

### Error Responses

#### 400 - Bad Request

```json
{
  "error": "Invalid JSON"
}
```

```json
{
  "error": "Item must include 'id'"
}
```

#### 405 - Method Not Allowed

```json
{
  "error": "Method not allowed"
}
```

## 📁 Project Structure

```
01-serverless-event-api/
├── lambda/
│   └── app.py                 # Lambda function code
├── terraform/
│   ├── main.tf               # Core infrastructure
│   ├── variables.tf          # Input variables
│   ├── outputs.tf            # Output values
│   ├── versions.tf           # Provider versions
│   ├── iam.tf               # IAM roles and policies
│   └── monitoring.tf        # CloudWatch dashboard
└── README.md
```

## 🔧 Configuration Details

### Lambda Function

- **Runtime**: Python 3.12
- **Handler**: `app.lambda_handler`
- **Environment Variables**:
  - `TABLE_NAME`: DynamoDB table name
- **Permissions**: DynamoDB read/write, CloudWatch logs

### DynamoDB Table

- **Billing Mode**: Pay-per-request
- **Hash Key**: `id` (String)
- **Backup**: Point-in-time recovery available

### API Gateway

- **Type**: HTTP API (v2)
- **Integration**: AWS_PROXY with Lambda
- **Payload Format**: 2.0
- **CORS**: Configurable

## 📊 Monitoring

The project includes a CloudWatch dashboard that tracks:

- Lambda invocations
- Lambda errors
- Duration metrics
- Throttles

Access your dashboard in the AWS Console:
`CloudWatch → Dashboards → {project_name}-dashboard`

## 🧪 Testing

### Local Testing (Optional)

You can test the Lambda function locally:

```python
import json
from lambda.app import lambda_handler

# Test GET request
event = {
    "requestContext": {
        "http": {
            "method": "GET"
        }
    }
}
response = lambda_handler(event, {})
print(json.dumps(response, indent=2))
```

### Integration Testing

Use the provided curl commands above or tools like Postman to test the deployed API.

## 💰 Cost Optimization

This serverless architecture is cost-effective:

- **API Gateway**: Pay per request
- **Lambda**: Pay per invocation and duration
- **DynamoDB**: Pay per request (no idle costs)
- **CloudWatch**: Basic monitoring included in free tier

Estimated cost for moderate usage: **$1-5/month**

## 🔐 Security Features

- **IAM Least Privilege**: Lambda can only access specified DynamoDB table
- **HTTPS Only**: All API requests encrypted in transit
- **AWS Managed Security**: Leverages AWS security controls
- **No Hardcoded Secrets**: Uses environment variables and IAM roles

## 🚨 Troubleshooting

### Common Issues

1. **403 Forbidden**: Check IAM permissions for Lambda execution role
2. **500 Internal Server Error**: Check CloudWatch logs for Lambda errors
3. **Timeout**: Increase Lambda timeout in `main.tf`

### Debugging

Check Lambda logs:

```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/serverless-api"
aws logs tail "/aws/lambda/serverless-api-lambda" --follow
```

## 🧹 Cleanup

To avoid ongoing AWS charges:

```bash
cd terraform
terraform destroy
```

This will remove all resources created by this project.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Additional Resources

- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [API Gateway v2 Documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/latest/developerguide/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

**Built with ❤️ using AWS Serverless Technologies**
