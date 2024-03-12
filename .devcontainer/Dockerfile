FROM ros:iron-ros-base

ARG USERNAME=rosdev
ARG UID=1000
ARG GID=$UID

# Install some dependencies packages
RUN apt update -q \
    && apt upgrade -q -y \
    && apt install -y --no-install-recommends \
    software-properties-common \
    python3-pip \
    xauth \
    && apt clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create and switch to user
RUN groupadd -g $GID $USERNAME \
    && useradd -lm -u $UID -g $USERNAME -s /bin/bash $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# RUN apt-get update -q \
#     && apt-get upgrade -q -y \
#     apt-get install -y --no-install-recommends libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev

RUN apt-get update  -q
RUN apt-get install -y --no-install-recommends  libportaudiocpp0
RUN apt-get install -y --no-install-recommends  libasound2-dev
RUN apt-get install -y --no-install-recommends  libportaudio2
RUN apt-get install -y --no-install-recommends  libasound-dev
RUN apt-get install -y --no-install-recommends  portaudio19-dev
RUN apt-get install -y --no-install-recommends  alsa-utils pulseaudio 
USER $USERNAME

# Create workspace so that user own this directory
RUN mkdir -p /home/$USERNAME/ros2_ws/src
WORKDIR /home/$USERNAME/ros2_ws

# Copy configuration files
RUN echo 'source /opt/ros/'$ROS_DISTRO'/setup.bash' >> /home/$USERNAME/.bashrc \
    && echo 'source /home/'$USERNAME'/ros2_ws/install/setup.bash' >> /home/$USERNAME/.bashrc


RUN pip install pyaudio
RUN pip install requests
RUN pip install SpeechRecognition
RUN pip install soundfile
RUN pip install TTS
RUN pip install torch
RUN pip install sounddevice
RUN  pip install git+https://github.com/openai/whisper.git 
WORKDIR /home/$USERNAME/ros2_ws/src/ros_ws/
RUN  colcon build
RUN . install/setup.bash
RUN  colcon build
RUN pip3 install -U pip
RUN pip3 install rasa
RUN python3 -m spacy download en_core_web_md
RUN python3 -c "import whisper; whisper.load_model('base')"
RUN python3 -c "from TTS.api import TTS; TTS(model_name='tts_models/en/ljspeech/tacotron2-DDC_ph', progress_bar=True)"

# Setup entrypoint
WORKDIR /home/$USERNAME/ros2_ws
COPY ./ros_entrypoint.sh /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
