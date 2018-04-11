FROM python:3.6.5-jessie

MAINTAINER Sebastian Anklamm <sanklamm@gmail.com>

# Install uWSGI
RUN pip install uwsgi

ENV NGINX_VERSION 1.9.11-1~jessie

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
	&& echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base \
	&& rm -rf /var/lib/apt/lists/*
# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log
EXPOSE 80 443
# Finished setting up Nginx

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf
# Copy the modified Nginx conf
COPY nginx.conf /etc/nginx/conf.d/

#python requirements
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt \
	&& rm -rf /requirements.txt

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
&& rm -rf /var/lib/apt/lists/*

RUN apt-get update -y
RUN apt-get install apt-file -y
RUN apt-file update -y
RUN apt-get install vim-nox -y

# Install zsh goodness
RUN apt-get install -y zsh
RUN chsh -s $(which zsh)
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

# Custom Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Get my dotfiles
RUN cd ~ && git clone https://github.com/sanklamm/.dotfiles.git && cp .dotfiles/.vimrc ~

#COPY /webapp /webapp
RUN mkdir /survey_app
VOLUME /survey_app
WORKDIR /survey_app

## copy all files to working dir
COPY . .

CMD ["/usr/bin/supervisord"]
