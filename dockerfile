FROM debian:bookworm

RUN apt-get update && apt-get upgrade -y

#? create the deploy user
ARG USERNAME=deploy
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

#? set default user
USER $USERNAME

#? zsh setup
#* change default user shell
RUN sudo apt-get install zsh -y && sudo usermod --shell /bin/bash deploy && echo "zsh" >> ~/.bashrc
#* needed for zsh setup
RUN sudo apt-get install git curl micro python3 python-is-python3 python3-pip ripgrep et-tools tig fzf bat exa zoxide cowsay figlet lolcat -y
RUN mkdir -p ~/.config/zsh/ && git clone --depth 1 https://github.com/NADEE-MJ/zsh.git ~/.config/zsh && ln -s ~/.config/zsh/.zshrc ~/.zshrc && ln -s ~/.config/zsh/.p10k.zsh ~/.p10k.zsh
RUN touch ~/.config/zsh/overrides.zsh && printf "alias bat=batcat\n" >> ~/.config/zsh/overrides.zsh

#? poetry and fastapi setup
RUN sudo apt-get install python3-poetry screen -y

#? sveltekit setup
RUN sudo apt-get install npm -y

RUN sudo apt-get autoremove -y

COPY bin/initial-startup.sh ~/initial-startup.sh