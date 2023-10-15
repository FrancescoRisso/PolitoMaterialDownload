FROM ubuntu:latest

RUN apt update
ARG DEBIAN_FRONTEND=noninteractive
RUN apt -y install cron nano python3 python3-pip software-properties-common tzdata

ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN add-apt-repository -y ppa:mozillateam/ppa
RUN echo '\nPackage: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001\n' | tee /etc/apt/preferences.d/mozilla-firefox
RUN apt install -y firefox
RUN echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox

ENV workdir="PolitoMaterialDownload"

WORKDIR /${workdir}

COPY . /${workdir}/

RUN rm -r ./docker

RUN pip3 install -r requirements.txt

COPY ./docker/docker_run_cron.sh /pmdUtils/start.sh

ARG cronSettings=""
ENV cronSettings=$cronSettings

CMD bash /pmdUtils/start.sh

# FROM ubuntu:latest

# CMD tail -f /dev/null
