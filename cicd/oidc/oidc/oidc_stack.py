from aws_cdk import (
    Stack,
    aws_iam as iam,
)
from constructs import Construct


class OidcStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str,
        secondary_region: str,
        gitlab_project_path: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.domain_name = domain_name
        self.secondary_region = secondary_region
        self.gitlab_project_path = gitlab_project_path

        # 1. OIDC Provider for GitLab
        oidc_provider = iam.OpenIdConnectProvider(
            self,
            "GitLabOIDCProvider",
            url="https://gitlab.com",
            client_ids=["https://gitlab.com"],
            thumbprints=[
                "A031C46782E6E6C662C2C87C76DA9AA62CCABD8E"
            ],  # GitLab's thumbprint
        )

        # # 2. IAM Role for GitLab CI/CD
        role = iam.Role(
            self,
            "GitLabOIDCRole",
            assumed_by=iam.WebIdentityPrincipal(
                oidc_provider.open_id_connect_provider_arn,
                conditions={
                    "StringLike": {
                        "gitlab.com:sub": f"project_path:{self.gitlab_project_path}:ref_type:branch:*"
                    },
                    "StringEquals": {"gitlab.com:aud": "https://gitlab.com"},
                },
            ),
            role_name="GitLab-OIDC-CDK-ROLE",
        )

        # 3. Attach policies for CDK deploy
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AdministratorAccess"
            )  # for full deploy access
        )
