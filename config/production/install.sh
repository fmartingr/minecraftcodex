
# Updating system
echo "=> Updating system"
pacman -Syu --noconfirm

echo "=> Installing python"
# Install python
pacman -S python2 python2-pip python2-virtualenv --noconfirm

echo "=> Installing Postgresql"
# Install postgresql
pacman -S postgresql --noconfirm
systemd-tmpfiles --create postgresql.conf
mkdir /var/lib/postgres/data
chown -c -R postgres:postgres /var/lib/postgres
su - postgres -c "initdb -D '/var/lib/postgres/data'"
systemctl start postgresql
systemctl enable postgresql

echo "=> Installing nginx"
# Install nginx
pacman -S nginx --noconfirm
systemctl start nginx
systemctl enable nginx

echo "=> Installing git"
# Install git
pacman -S git --noconfirm

echo "=> Installing nodejs and dependencies"
# Install node & dependencies
pacman -S nodejs --noconfirm
npm install -g coffee-script
npm install -g uglify-js
npm install -g less

echo "=> Creating user APP with its requirements"
# Create site user
useradd app
mkdir /home/app
chown app:app /home/app
su - app -c "mkdir conf"
su - app -c "touch ./conf/app_version"
su - app -c "touch .environment"
su - app -c "echo 'source .environment' > .bash_profile"

# Reminders
echo "[REMEMBER!]"
echo " - Create ssh keypair for the server."
