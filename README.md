IGOR
====

IGOR stands for ... actually it does not stands for anything. It just a tool to help developers to get information they need quick!

Installation
============

1. Clone repo
2. Execute the following script:

~~~
 ./setup.sh
~~~


Operations
==========

get-logs - Get logs for a specific application
--------

***Usage:***
This will print application logs for kf-api-arranger for the past 2 hours (keep in mind it defaults to 2000 lines max)
~~~
 igor get-logs --app kf-api-arranger --environment prd --hours 2 
~~~

restart - Executes new deployment for a service
-------

***Usage:***

This example with create a new deployment for the ecs service.

~~~
igor restart --app kf-cbioportal --environment qa --account kf-strides
~~~

deploy 
------

Deploy application from current directory. This operation supports "ecs_service_type_1" and "aws_infra_ec2_module" deployments. This command requires to have Jenkinsfile to be in the same directory.

***Usage:***

This example show how to deploy a application into kf-strides account , us-east-1 region and dev environment. 

~~~
igor deploy --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev  --mode deploy  --config_file Jenkinsfile
igor deploy --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev  --mode destroy --config_file Jenkinsfile
~~~

check_build 
-----------
(works with Mac only) Opens web page for Jenkins for a particular github repo. You have to be in the directory of that repo in order for this command to work. Also you must pass which instance of Jenkins you want to see (kf-strides, chopd3bPrd).

***Usage:***

~~~
igor check_build --account [kf-strides,chopd3bPrd]
~~~

awslogin 
--------
Login to aws using Auth0. 

***Usage:***

~~~
igor awslogin
~~~

shortcuts 
---------
Print out the list of important shortcuts

***Usage:***

Show all shortcuts and open Jenkins server web page
~~~
igor shortcuts --show
  kf-jenkins : Jenkins Server in KidsFirst Strides account
  d3b-jenkins : Jenkins Server in CHOPD3bPRD account
  d3b-auth0 : AWS Auth0 login screen
  devops-notion : DevOps Notion.so Page
  github-d3bcenter : D3b Center Github Account
  github-kidsfirst : KidsFirst Github Account

igor shortcuts --name kf-jenkins 
~~~

dev_env_tunnel 
--------------
Open ssh tunnel

***Usage:***

~~~
igor dev_env_tunnel --environment [dev,qa,prd,service]
~~~

