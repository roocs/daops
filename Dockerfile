##=================================================================================
##
##    EXAMPLE USAGE
##    
##    $ docker build -t daops .
##    $ mkdir ~/container-outputs
##    $ docker run -it \
##                 --mount type=bind,source=$HOME/container-outputs,target=/outputs \
##                 daops
##
##    # id=cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga
##    # path=/root/.mini-esgf-data/test_data/badc/cmip5/data/$(echo $id | tr / .)
##    # ncdump -h $path/*.nc | grep UNLIMITED
##    	time = UNLIMITED ; // (1140 currently)
##    # rm /outputs/*.nc
##    # daops subset --output-dir /outputs --time=2010-1-1/2015-1-1 $id
##    # ncdump -h /outputs/*.nc | grep UNLIMITED
##    	time = UNLIMITED ; // (60 currently)
##    # exit
##
##    $ ls ~/container-outputs/
##    zostoga_mon_inmcm4_rcp45_r1i1p1_20100116-20141216.nc
##
##=================================================================================

FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

ENV BASH_ENV=~/.bashrc                       \
    MAMBA_ROOT_PREFIX=/srv/conda             \
    PATH=$PATH:/srv/conda/envs/daops/bin


# ==== Install apt-packages and micromamba ====

RUN apt-get update                                                                                                           && \
    apt-get install -y ca-certificates ttf-dejavu file wget bash bzip2 git                                                   && \
    wget -qO- https://micromamba.snakepit.net/api/micromamba/linux-64/latest | tar -xvj bin/micromamba --strip-components=1  && \
    ./micromamba shell init -s bash -p ~/micromamba                                                                          && \
    apt-get clean autoremove --yes                                                                                           && \
    cp ./micromamba /usr/bin                                                                                                 && \
    rm -fr /srv/conda/pkgs


# ==== Set up conda environment from yml file ====

ARG tmp_env=/tmp/environment.yml
ADD environment.yml $tmp_env
RUN micromamba create -f $tmp_env    && \
    rm -fr $tmp_env /srv/conda/pkgs


# ==== Clone the data repo ====

ARG data_dir=/root/.mini-esgf-data
ARG data_repo_url=https://github.com/roocs/mini-esgf-data
ARG data_repo_branch=master
RUN git clone $data_repo_url $data_dir  && \
    cd $data_dir                        && \
    git checkout $data_repo_branch      && \
    rm -fr .git


# ==== Set up the roocs.ini file with paths pointing to the data repo ====
# ==== and ensure that ROOCS_CONFIG environment variable points to it ====

ARG config_file=/root/roocs.ini
ARG config_tmpl=/tmp/roocs.ini.tmpl
COPY roocs.ini.tmpl $config_tmpl
RUN sed "s,DATA_DIR,$data_dir,g" $config_tmpl > $config_file  && \
    rm $config_tmpl                                           && \
    echo "export ROOCS_CONFIG=$config_file" >> /root/.bashrc


# ==== Install the daops app ====

ARG tmp_install_dir=/tmp/daops-install
RUN mkdir $tmp_install_dir
COPY . $tmp_install_dir
RUN    cd $tmp_install_dir                                 && \
       /srv/conda/envs/daops/bin/python setup.py install   && \
       rm -fr $tmp_install_dir                             && \
       echo "export USE_PYGEOS=0" >> /root/.bashrc

# ==== Create a directory that we can bind-mount ====
RUN mkdir /outputs


# ==== Some tidying up (NB further apt-install not possible after this) ====

RUN rm -fr /var/lib/{apt,dpkg,cache,log}
