# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/bin/bash
sudo apt-get install -y libasound2 libasound2-dev portaudio19-dev 

sudo apt-get install -y python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev  libfreetype6-dev

pip install -r pips.txt

pip install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp38-cp38-linux_aarch64.whl

pip install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp38-cp38-linux_x86_64.whl

pip install https://github.com/google-coral/pycoral/releases/download/v2.0.0/pycoral-2.0.0-cp38-cp38-linux_aarch64.whl

pip install https://github.com/google-coral/pycoral/releases/download/v2.0.0/pycoral-2.0.0-cp38-cp38-linux_x86_64.whl
