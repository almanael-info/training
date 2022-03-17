FROM ubuntu:20.04
ENV TZ="Europe/Paris"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -yy apache2 php libapache2-mod-php tzdata && \
    apt clean && \
    a2enmod rewrite && \
    rm /etc/apache2/sites-enabled/000-default.conf
COPY blog.conf /etc/apache2/sites-enabled/
COPY markdown-blog/ /var/www/
EXPOSE 80
CMD  [ "apachectl", "-D", "FOREGROUND"]
