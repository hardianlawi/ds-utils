sudo apt update && sudo apt install -y git g++ make zsh rake wget redis-server libspatialindex-dev

# Change bash to zsh
sudo sed s/required/sufficient/g -i /etc/pam.d/chsh
chsh -s $(which zsh)

# Install oh my zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install spaceship theme
git clone https://github.com/denysdovhan/spaceship-prompt.git "$ZSH_CUSTOM/themes/spaceship-prompt"
ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme"
sed -i 's/ZSH_THEME="robbyrussel"/ZSH_THEME="spaceship"/g' .zshrc

# Install janus vim
curl -L https://bit.ly/janus-bootstrap | bash

# Install docker
curl https://get.docker.com | bash

# Install anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
bash Anaconda3-2019.10-Linux-x86_64.sh
rm Anaconda3-2019.10-Linux-x86_64.sh

# Move `conda init` to `.zshrc`
cat .bashrc | grep -Pzo "\n# >>> conda initialize >>>((.|\n)*)# <<< conda initialize <<<" | tee -a .zshrc

# Remove conda (base) environment status from terminal
conda config --set changeps1 False

# Install zsh autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Install autojump
git clone git://github.com/wting/autojump.git
cd autojump && ./install.py && cd && rm -rf autojump

# Replace plugins
sed -i 's/plugins=(git)/plugins=(autojump git history z zsh-autosuggestions kubectl)/g' .zshrc

# Add LC_ALL and LANG
printf "\nexport LC_ALL=C.UTF-8" >> .zshrc
printf "\nexport LANG=C.UTF-8" >> .zshrc

source .zshrc