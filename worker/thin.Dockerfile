FROM tensorflow/tensorflow:latest-py3
RUN pip install --no-cache-dir \
    Flask \
    waitress
ENV APP_DIR /app
WORKDIR ${APP_DIR}
COPY worker/*.py ${APP_DIR}/
EXPOSE 5002
ENTRYPOINT ["python", "./algorithm.py"]
