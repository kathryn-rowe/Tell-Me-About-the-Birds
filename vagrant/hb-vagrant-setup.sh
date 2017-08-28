#get rid of warnings about updating
#pipe any error messages into dev/null
rm /etc/update-motd.d/90* 2> /dev/null
rm /etc/update-motd.d/91* 2> /dev/null

#set up postgres for vagrant
sudo -u postgres createuser vagrant -s
sudo -u postgres createdb vagrant
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/9.5/main/postgresql.conf
sudo echo "host    all    all    10.0.0.0/16    trust" >> /etc/postgresql/9.5/main/pg_hba.conf
sudo /etc/init.d/postgresql restart

#print success message
echo
echo
echo "***************************************"
echo "HACKBRIGHT VAGRANT SET UP SUCCESSFULLY!"
echo "***************************************"
echo
echo
