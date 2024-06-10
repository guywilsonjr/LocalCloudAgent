KEYWORD=local_cloud_agent
cd /usr/local
rm -rf /usr/local/LocalCloudAgent
git clone --depth 1 https://github.com/guywilsonjr/LocalCloudAgent.git --branch v0.0.0-rc8
mkdir -p /root/.local_cloud_agent
mkdir -p /etc/$KEYWORD
touch /etc/$KEYWORD/config.json
cp /usr/local/LocalCloudAgent/conf/local_cloud_agent.service /etc/systemd/system/

