
# Updating system
pacman -Syu --noconfirm

# Install python
pacman -S python2 python2-pip python2-virtualenv --noconfirm

# Install postgresql
pacman -S postgresql --noconfirm

# Install nginx
pacman -S nginx --noconfirm

# Install git
pacman -S git --noconfirm

# Install node & dependencies
pacman -S nodejs --noconfirm
npm install -g coffee-script
npm install -g uglify-js
npm install -g less

# Create site user
useradd app
mkdir /home/app
chown app:app /home/app
echo "Remember to create ssh keypair for the server."
