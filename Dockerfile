FROM public.ecr.aws/lambda/python:3.14-preview-x86_64 
RUN pip install reportlab 
WORKDIR /var/task
COPY . .
COPY lambda_function.py /var/task/
CMD ["lambda_function.lambda_handler"]
