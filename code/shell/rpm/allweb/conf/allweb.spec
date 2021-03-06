%{!?prefix: %global prefix /opt/allweb}

%define localbin    /usr/local/bin
%define name    allweb
%define _version    1.0.0
%define _release    1001

Name:           %{name}
Version:        %{_version}
Release:        %{_release}.el7
Summary:        all frontend code
Group:          System Environment/Daemons
License:        Commercial
URL:            http://www.datatom.com
Vendor:         Datatom Co.,Ltd.(Build %{git_commit_hash})
Source:         %{name}-%{_version}.tar.gz

BuildRequires:	gcc
Requires:       systemd,chkconfig,firewalld

%description
all frontend code

# ------------ PREP -------------

%prep
# -- unzip the source code
%setup -q

# ------------ BUILD -------------

%build

# ------------ INSTALL -------------

%install
# -- install (just copy file)
make install DESTDIR=%{buildroot}

# ------------ POST -------------

%post
# -- environmental variable
echo '>>> now update /etc/profile ... '
sed '/export FrontEndDir=/'d /etc/profile -i
sudo echo "export FrontEndDir=/opt/allweb/node-express-react" >> /etc/profile
source /etc/profile

# -- symbolic links
echo '>>> create symbolic links for mongodb and node ... '
sudo ln -s /opt/allweb/mongodb-linux-x86_64-rhel70-3.6.4/* %{localbin} -f
sudo ln -s /opt/allweb/node-v8.11.1-linux-x64/bin/* %{localbin} -f

# -- add chkconfig startup service
echo '>>> add chkconfig startup service ... '
chkconfig --add frontend
chkconfig frontend on

# -- open web port for mongodb and node.js
echo '>>> open web port for mongodb and node.js ... '
firewall-cmd --add-port=3000/tcp --permanent
firewall-cmd --add-port=27017/tcp --permanent
firewall-cmd --reload

# -- start frontend service
echo '>>> start frontend service ... '
systemctl start frontend
echo
echo ">>> ------- allweb install success ! ------- <<<"
echo

# ------------ PREUN -------------

%preun
echo '>>> stop frontend service ... '
systemctl stop frontend
systemctl disable frontend
echo '>>> remove frontend service ... '
chkconfig --del frontend

# ------------ POSTUN -------------

%postun
# -- remove files and dirs
echo '>>> remove allweb files ... '
rm /opt/allweb -rf
# -- unset env vir
echo '>>> unset allweb env variable ... '
sed '/export FrontEndDir=/'d /etc/profile -i
sudo rm %{localbin}/mongo* %{localbin}/bsondump %{localbin}/install_compass -f
sudo rm %{localbin}/pm2* %{localbin}/node %{localbin}/npm %{localbin}/npx -f

echo
echo ">>> ------- allweb uninstall success ! ------- <<<"
echo
# ------------ FILES -------------

%files
%attr(755, root, root) %{prefix}/
%attr(755, root, root) /etc/frontend
%attr(755, root, root) /etc/init.d/frontend

# ------------ CHANGELOG -------------

%changelog
