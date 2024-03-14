FROM public.ecr.aws/lambda/python:3.9
LABEL maintainer=""
LABEL description=""

ENV REPO_NAME d3b-dff-cli

RUN yum install -y git && yum clean all

COPY src/requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip3 install -r requirements.txt  --no-cache-dir

COPY src/app.py ${LAMBDA_TASK_ROOT}

RUN git clone https://github.com/d3b-center/${REPO_NAME}.git

WORKDIR ${LAMBDA_TASK_ROOT}/${REPO_NAME}

RUN pip install --no-cache-dir .

WORKDIR ${LAMBDA_TASK_ROOT}

RUN yum remove -y git

CMD ["app.handler"]
