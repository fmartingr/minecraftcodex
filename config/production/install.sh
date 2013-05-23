
# Updating system
echo "=> Updating system"
pacman -Syu --noconfirm

echo "=> Installing python"
pacman -S python2 python2-pip python2-virtualenv --noconfirm

echo "=> Installing Postgresql"
pacman -S postgresql --noconfirm
systemd-tmpfiles --create postgresql.conf
mkdir /var/lib/postgres/data
chown -c -R postgres:postgres /var/lib/postgres
su - postgres -c "initdb -D '/var/lib/postgres/data'"
systemctl start postgresql
systemctl enable postgresql

echo "=> Installing nginx"
pacman -S nginx --noconfirm
systemctl start nginx
systemctl enable nginx

echo "=> Installing git"
pacman -S git --noconfirm

echo "=> Installing supervisor"
pacman -S supervisor --noconfirm
systemctl start supervisord
systemctl enable supervisord

echo "=> Installing nodejs and dependencies"
pacman -S nodejs --noconfirm
npm install -g coffee-script
npm install -g uglify-js
npm install -g less

echo "=> Creating user APP with its requirements"
useradd app
mkdir /home/app
chown app:app /home/app
su - app -c "mkdir conf"
su - app -c "touch ./conf/app_version"
su - app -c "touch .environment"
su - app -c "echo 'source .environment' > .bash_profile"

# Reminders
echo "[REMEMBER!]"
echo " - Create ssh keypair for the app user."
echo " - Configure sudo to let app user execute the maintenance scripts."
echo " - Configure supervisor to include the app configuration."
echo " - Configure nginx to include the app configuration."
