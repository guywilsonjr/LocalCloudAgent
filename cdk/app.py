import boto3
from aws_cdk import Environment, Stack
from aws_cdk.aws_ecr import Repository
from aws_cdk.aws_ecr_assets import DockerImageAsset
from constructs import Construct
from cdk_ecr_deployment import ECRDeployment, DockerImageName
import aws_cdk as cdk


with open('VERSION') as f:
    VERSION = f.read().strip()


def get_cdk_env() -> Environment:
    client = boto3.client('sts')
    resp = client.get_caller_identity()
    account_id = resp['Account']
    region = boto3.Session().region_name
    return Environment(account=account_id, region=region)


class LocalCloudAgent(Stack):

    def __init__(self, scope: Construct, construct_id: str, env: Environment) -> None:
        super().__init__(scope, construct_id, env=env)
        self.cloud_agent_repo = Repository.from_repository_name(
            self,
            'LocalCloudAgentRepo',
            repository_name='cumulonimbusinfrastructurestackecrb011c8ff-localcloudagent882a885f-uf9f1uyibbfx'
        )
        self.image = DockerImageAsset(
            self,
            'Image',
            directory='.',
        )
        self.versioned_deployment = ECRDeployment(
            self,
            'VersionedImageDeployment',
            src=DockerImageName(self.image.image_uri),
            dest=DockerImageName(f'{self.cloud_agent_repo.repository_uri}:{VERSION}')
        )
        self.latest_deployment = ECRDeployment(
            self,
            'LatestImageDeployment',
            src=DockerImageName(self.image.image_uri),
            dest=DockerImageName(f'{self.cloud_agent_repo.repository_uri}:latest')
        )


app = cdk.App()
LocalCloudAgent(app, "LocalCloudAgent", env=get_cdk_env())
app.synth()
