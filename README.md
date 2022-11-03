# Library

> novu py library



## About

this library helps to interact with the Novu api

Novu is an open-source notification infrastructure, built for engineering teams to help them build rich product notification experiences without constantly reinventing the wheel.


### Available Channel
**Email**
You can specify the content for emails in two ways:

*Visual template builder* - For simple use cases, you can use our visual template editor. The visual template builder has limited control over design but is easier to get-started with.

*Custom Code* - You can use the custom code section to specify custom html for the email.

You can specify custom variables using the {{handlebars}} syntax.

**SMS**
Inside SMS you can specify custom variables using {{handlebars}} syntax.

**In-app**
In the notification center preview, you can type the content of the notification, select the content, and use CMD + B to make the selected text bold.

**Chat**
You can specify custom variables using the {{handlebars}} syntax.

In addition to the integration, any subscriber needs to set credentials to have proper authorization on the channel.
## Getting Started
1.  Install dependencies
```
> pipenv lock --pre --dev && pipenv install --pre --dev
```

2.  Run the project locally

```
cd dev_scripts/docker/
docker-compose up -d
```
you can access to the novu api docs in the url http://localhost:3000/api

the admin panel is available in the url http://localhost:4600/, in this panel we can get the api key
and with it, we can send requests to the api

3.  Run tests

in order to run tests locally you have first to run this script:
```
sh tests/test_environment/start.sh
```
once the script is finished you can run the tests via pytest if you have pycharm IDE or by this command
```
pipenv run coverage run --source=notification_lib -m pytest -v -s --junit-xml=reports/report.xml tests
```
it's possible to delete tests containers with volumes by running this script
```
sh tests/test_environment/stop.sh
```


### Different attributes
#### * Pre-commit
install pre-commit with:
```bash
pre-commit install .
```
check files with:
```bash
pre-commit run --all-files
```
