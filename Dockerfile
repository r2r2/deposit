###########
# BUILDER #
###########

# pull official base image
FROM python:3.10 as builder

# set work directory
WORKDIR /usr/src/deposit

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# lint
COPY . .

# copy pdm files
COPY ./pyproject.toml .
COPY ./pdm.lock .

#########
# FINAL #
#########

# pull official base image
FROM python:3.10

# create directory for the app user
RUN mkdir -p /home/deposit

# create the app user
RUN addgroup --system -gid 1000 app && adduser --system -uid 1000 -gid 1000 app

# create the appropriate directories
ENV HOME=/home/deposit
ENV APP_HOME=/home/deposit/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -qq -y build-essential libpq-dev
COPY --from=builder /usr/src/deposit/pyproject.toml .
COPY --from=builder /usr/src/deposit/pdm.lock .
RUN python -m pip install -U pdm toml --pre
RUN eval "$(pdm --pep582)"
RUN pdm sync -v

# copy project
COPY . $APP_HOME

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/home/deposit/web/entrypoint.sh"]
