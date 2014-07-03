<?php
exit(0);
?>

Web Installation : add these lines to your apache config

	ScriptAlias /CAAS/ "/path/to/CAAS/web/"
	<Directory "/path/to/CAAS/web/">
		Options Indexes FollowSymLinks MultiViews
		AllowOverride None
		Order allow,deny
		allow from all
	</Directory>

Change access rights :
	chmod 644 web
