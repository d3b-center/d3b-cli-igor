IGOR
====

IGOR stands for ... actually it does not stands for anything. It just a tool to help developers to get information they need quick!

Installation
============

Recommended Installation
------------------------

We recommend installing using Docker. However, dev-env-tunnel command yet does not work  with Docker install.

~~~sh
git clone git@github.com:d3b-center/d3b-cli-igor.git
cd d3b-cli-igor
docker build . -tag igor:latest
docker run -v $HOME/.aws/credentials:/.aws/credentials -i -p 12200:12200 igor:latest igor
~~~

Installation with pipx
----------------------

Installing IGOR with [`pipx`](https://pypa.github.io/pipx). `pipx` can be installed on MacOS with `brew` and on  Linux and Windows with `pip`. `pipx` is recommended over other methods because it installs the CLI in its own virtual environment and then puts the CLI on your machine's `PATH`. Please follow the instructions for installing `pipx` [here](https://pypa.github.io/pipx/installation/)

After installing `pipx`, to install IGOR, run:

~~~sh
pipx install git+https://github.com/d3b-center/d3b-cli-igor.git@latest-release
~~~

Manual Installation
-------------------

1. Clone repo
2. Execute the following script:

~~~sh
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

Deploy application from current directory. This operation supports modules in d3b-infra organization. This command requires to have Jenkinsfile to be in the same directory.

Options:
 [] mode - Choose between 4 modes : build, plan, apply, destroy. Build mode will do a standard docker build. Plan will create plan of resources that will be created. Deploy mode will execute terraform apply command.

***Usage:***

This example show how to deploy a application into kf-strides account , us-east-1 region and dev environment.

~~~
igor deploy --mode plan --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev --config_file Jenkinsfile
igor deploy --mode apply --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev --config_file Jenkinsfile
igor deploy --mode destroy --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev --config_file Jenkinsfile
~~~

The command also supports wildcards. When using wildcards prefix your config file with .deploy. So for instance config files with names some_config.deploy and other_config.deploy both will be executed.

~~~
igor deploy --mode apply --account_name kf-strides --organization kf-strides --region us-east-1 --environment dev  --mode destroy --config_file *.deploy 
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
  aws-accounts : AWS Accounts Information Notion Page

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

secrets
-------

Igor will retrieve secrets for a specific application.

***Usage***

~~~
igor secrets --app kf-keycloak --environment qa --region us-east-1 --account kf-strides
~~~

generate
--------

Igor will generate a standard template and will replace variables.

***Usage***

~~~
igor generate --project route_53_healthchecks --environment qa --account kf-strides --region us-east-1 --template simple-tf
~~~

In this example, "igor" will generate files based on the "simple-tf" template. It will replace placeholders for account, environment, project, region with values supplied values. Additionally, igor will replace values in templates that found in accounts_info.json file. 
In our case it will look up a bucket for terraform state files. 
You can add more templates here:

~~~
d3b_cli_igor/utils/templates
~~~

Developing Igor
===============

Igor releases are managed by the [d3b-release-maker](https://github.com/d3b-center/d3b-release-maker/). Please follow the instructions there to build releases.
