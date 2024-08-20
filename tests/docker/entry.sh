echo "BEGIN entry.sh"

#IDK DO OPPOSITE
if $DEBUG ; then
  echo "Running entry.sh tests"
else
  echo "Running entry.sh tests in debug mode sleeeping for 200 seconds"
  echo "Found DEBUG=${DEBUG}"
  sleep 400

fi
.venv/bin/tox -e py312
systemctl list-unit-files local_cloud_agent.service
shutdown 0
#systemctl restart test_startup.service
# , "-p", "all", "--parallel-live"
