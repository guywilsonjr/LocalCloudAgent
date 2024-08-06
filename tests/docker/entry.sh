echo "Hey, I'm running in a container!" >> /test/echo_command.log
.venv/bin/tox -e py312
systemctl list-unit-files local_cloud_agent.service
shutdown 0
#systemctl restart test_startup.service
# , "-p", "all", "--parallel-live"
