import boto3
from aws_cdk import Environment, Stack
from aws_cdk.aws_ecr import IRepository, Repository
from aws_cdk.aws_ecr_assets import DockerImageAsset, Platform
from constructs import Construct
from cdk_ecr_deployment import ECRDeployment, DockerImageName
import aws_cdk as cdk
from setuptools_scm import get_version, NonNormalizedVersion


VERSION = NonNormalizedVersion(get_version()).base_version


def get_cdk_env() -> Environment:
    client = boto3.client('sts')
    resp = client.get_caller_identity()
    account_id = resp['Account']
    region = boto3.Session().region_name
    return Environment(account=account_id, region=region)


class BuildDeployImage:
    def __init__(self, scope: Construct, cloud_agent_repo: IRepository, platform: Platform) -> None:
        self.scope = scope
        self.platform = platform
        self.image = DockerImageAsset(
            scope,
            f'{platform}-Image',
            directory='.',
            platform=platform,
            cache_disabled=True
        )
        self.versioned_deployment = ECRDeployment(
            scope,
            f'{platform}-VersionedImageDeployment',
            src=DockerImageName(self.image.image_uri),
            dest=DockerImageName(f'{cloud_agent_repo.repository_uri}:{VERSION}')
        )
        self.latest_deployment = ECRDeployment(
            scope,
            f'{platform}-LatestImageDeployment',
            src=DockerImageName(self.image.image_uri),
            dest=DockerImageName(f'{cloud_agent_repo.repository_uri}:latest')
        )


class LocalCloudAgent(Stack):

    def __init__(self, scope: Construct, construct_id: str, env: Environment) -> None:
        super().__init__(scope, construct_id, env=env)
        self.cloud_agent_repo = Repository.from_repository_name(
            self,
            'LocalCloudAgentRepo',
            repository_name='cumulonimbusinfrastructurestackecrb011c8ff-localcloudagent882a885f-uf9f1uyibbfx'
        )

        self.linux64_bdi = BuildDeployImage(self, self.cloud_agent_repo, Platform.LINUX_AMD64)
        self.arm_bdi = BuildDeployImage(self, self.cloud_agent_repo, Platform.LINUX_ARM64)



app = cdk.App()
LocalCloudAgent(app, "LocalCloudAgent", env=get_cdk_env())
app.synth()
