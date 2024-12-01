# Keyword Detector using Coral.AI
## Linux ONLY

Only detecting keywords in file config/labels_gc2.raw

We will need to re-train the model to recognize other keywords or to classify sounds

# Setup
## Python and Pyenv Setup

Install pyenv (if not present)

```pyenv install 3.8.20``` (if not present)

```pyenv virtualenv 3.8.20 coral```

```pyenv local coral```

## Driver Packages to install

install the Google keyring and repo

```echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list```

```curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -```

```sudo apt-get update```

ONLY ONE OF THE FOLLOWING

```sudo apt-get install libedgetpu1-std``` <- for standard performance

```sudo apt-get install libedgetpu1-max``` <- for maximum clock speed

## Python libraries and system packages

```chmod 777 install_requirements.sh```

Then run *install_requirements.sh*

