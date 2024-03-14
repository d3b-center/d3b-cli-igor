# d3b-dff-manifest-validator-lambda

Lambda function that validates a file manifest using the [D3B CLI](https://github.com/d3b-center/d3b-dff-cli). If the file manifest passes validation, it is then loaded to the D3B Datawarehouse.

![lambda flowchar](docs/somatic_annotation_wf.png)


When the validation fails, the validation step logs why each failed line failed validation, but the lambda only returns the line numbers in the error message. The full validation failure reason is present in the logs.

## Testing

Testing file validation should be done using the [D3B CLI](https://github.com/d3b-center/d3b-dff-cli) following the instructions there.

To test the lambda itself, go to the `Test` on the [lambda page](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/d3b-dff-manifest-validator-lambda-dev?tab=testing).

### Example test JSON:
```
{
  "environment": "dev",
  "input": {
    "S3ObjectEvent": {
      "key": "DEV-001/manifest/example_manifest.csv",
      "bucket": "d3b-684194535433-data-transfer-staging-dev-bucket",
      "size": 5,
      "event_time": "2023-11-16T22:52:58.989Z",
      "event_type": "ObjectCreated:Put",
      "etag": "d8e8fca2dc0f896fd7cb4cb0031ba249",
      "version_id": null
    },
    "Rule_Type": "transfer_validation_rules"
  }
}
```