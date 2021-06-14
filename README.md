IGOR
====

IGOR stands for ... actually it does not stands for anything. It just a tool to help developers to get information they need quick!


Operations
==========

get-logs - Get logs for a specific application

Usage:
-----
This will print application logs for kf-api-arranger for the past 2 hours (keep in mind it defaults to 2000 lines max)
~~~
 igor get-logs --app kf-api-arranger --environment prd --hours 2 
~~~

restart - Executes new deployment for a service

Usage:
------

This example with create a new deployment for the ecs service.

~~~
igor restart --app kf-cbioportal --environment qa --account kf-strides
~~~

deploy - deploy application from current directory. This operation supports "ecs_service_type_1" and "aws_infra_ec2_module" deployments.

Usage:
------

~~~
igor deploy --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev  --mode deploy 
igor deploy --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev  --mode destroy
~~~
