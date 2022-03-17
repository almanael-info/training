FROM ubuntu:20.04

ENV APP_ENV=docker
ENV TZ="Europe/Paris"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -qq
RUN apt install software-properties-common
RUN add-apt-repository ppa:ondrej/php
RUN apt update -qq
RUN apt install -qq -yy tzdata && \
    apt install -qq -yy php8.0-cli php8.0-xml php8.0-mbstring \
                        git unzip wget php8.0-curl php8.0-gd \
                        php8.0-zip php8.0-mysql
RUN wget https://raw.githubusercontent.com/composer/getcomposer.org/76a7060ccb93902cd7576b67264ad91c8a2700e2/web/installer -O - -q | php -- --quiet && \
    mv composer.phar /usr/bin && \
    chmod +x /usr/bin/composer.phar
# prepare dedicated user
RUN useradd -ms /bin/bash basicuser && \
    mkdir /home/basicuser/service && \
    chown basicuser:basicuser /home/basicuser/service
COPY --chown=basicuser:basicuser . /home/basicuser/service

# fetch project dependencies
USER basicuser
WORKDIR /home/basicuser/service
RUN composer.phar update

ENTRYPOINT [ "php", "artisan" ]
CMD [ "serve", "--host=0.0.0.0" ]
