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

get-logs 
--------
Get logs for a specific application
--------

***Usage:***
This will print application logs for kf-api-arranger for the past 2 hours (keep in mind it defaults to 2000 lines max)
~~~
 igor get-logs --app kf-api-arranger --environment prd --hours 2 
~~~

restart 
-------
Executes new deployment for a service
-------

***Usage:***

This example with create a new deployment for the ecs service.

~~~
igor restart --app kf-cbioportal --environment qa --account kf-strides
~~~

deploy 
------

Deploy application from current directory. This operation supports "ecs_service_type_1" and "aws_infra_ec2_module" deployments. This command requires to have Jenkinsfile to be in the same directory.

Options:
 [] mode - Choose between 3 modes : build, plan, deploy. Build mode will do a standard docker build. Plan will create plan of resources that will be created. Deploy mode will execute terraform apply command.

***Usage:***

This example show how to deploy a application into kf-strides account , us-east-1 region and dev environment. 

~~~
igor deploy --mode deploy --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev  --mode deploy  --config_file Jenkinsfile
igor deploy --mode deploy --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev  --mode destroy --config_file Jenkinsfile
~~~

The command also supports wildcards. When using wildcards prefix your config file with .deploy. So for instance config files with names some_config.deploy and other_config.deploy both will be executed. 

~~~
igor deploy --mode deploy --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev  --mode destroy --config_file *.deploy 
~~~

check-build 
-----------
(works with Mac only) Opens web page for Jenkins for a particular github repo. You have to be in the directory of that repo in order for this command to work. Also you must pass which instance of Jenkins you want to see (kf-strides, chopd3bPrd).

***Usage:***

~~~
igor check-build --account [kf-strides,chopd3bPrd]
~~~

github-open
-----------
(works with Mac only) Opens web page for github.com for a particular github repo. You have to be in the directory of that repo in order for this command to work. 

***Usage:***

~~~
igor github-open 
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

dev-env-tunnel 
--------------
Open ssh tunnel

***Usage:***

~~~
igor dev-env-tunnel --environment [dev,qa,prd,service]
~~~

onboarding
----------
Install software that required for a specific role

***Usage:***

~~~
igor onboarding --role devops --install_os mac
~~~


get-info
----------
Igor will look for an availble inforamtion about an application. This command will try to gather information about RDS, tasks, deployments etc. and present it in basic view.

***Usage:***

~~~
igor get-info --app kf-keycloak --environment qa --account kf-strides
~~~

