# Script that sets up your web servers for the deployment of web_static
exec { 'update packages':
  command => 'sudo apt-get update > /dev/null',
  path    => ['/usr/bin', '/usr/sbin',],
}

package { 'install nginx':
  ensure   => present,
  provider => 'apt',
}

file { 'create test html file':
  ensure  => file,
  path    => '/data/web_static/releases/test/index.html',
  content => 'Holberton School',
}

file { 'create shared dir':
  ensure => directory,
  path   => '/data/web_static/shared/',
}

file { 'create sym link to source files':
  ensure => link,
  path   => '/data/web_static/current',
  target => '/data/web_static/releases/test/',
  force  => true,
}

file { 'add owner and group id to data dir':
  ensure  => directory,
  path    => '/data/',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

$new_string='\\\\\n\n\tlocation \/hbnb_static {\n\t\t alias /data/web_static/current/;\n\t\t try_files \$uri \$uri/ =404;\n\t}'

exec { 'define route for hbnb_static':
  command => "sudo sed -i \"65i ${new_string}\" /etc/nginx/sites-available/default",
  path    => ['/usr/bin', '/usr/sbin',],
}

exec { 'restart':
  command => 'sudo service nginx start',
  path    => ['/usr/bin', '/usr/sbin',],
}
