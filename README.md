# NetCheck

# Add to scheduler
crontab -e
*/15 * * * * /usr/local/bin/netcheck.sh
/etc/init.d/cron restart
