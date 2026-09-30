import os
import boto3
from dotenv import load_dotenv


class Config:
    BASE_URL = ""
    STANDARD_USER = ""
    STANDARD_PASSWORD = ""
    AUTH_STATE_PATH = "state/auth.json"
    ENV_NAME = "qa"

    @staticmethod
    def get_ssm_parameter(param_name: str, region_name: str = "us-east-1") -> str:
        ssm = boto3.client("ssm", region_name=region_name)
        response = ssm.get_parameter(Name=param_name, WithDecryption=True)
        return response["Parameter"]["Value"]

    @classmethod
    def load_environment(cls, env: str = "qa"):
        cls.ENV_NAME = env.lower()

        # 1. First, load local .env.{env} file if present
        env_file = f".env.{cls.ENV_NAME}"
        if os.path.exists(env_file):
            load_dotenv(env_file, override=True)

        # 2. Try fetching from AWS SSM Parameter Store (Cloud CI/CD mode)
        try:
            cls.BASE_URL = cls.get_ssm_parameter(f"/playwright/{cls.ENV_NAME}/BASE_URL")
            cls.STANDARD_USER = cls.get_ssm_parameter(
                f"/playwright/{cls.ENV_NAME}/STANDARD_USER"
            )
            cls.STANDARD_PASSWORD = cls.get_ssm_parameter(
                f"/playwright/{cls.ENV_NAME}/STANDARD_PASSWORD"
            )
        except Exception:
            # 3. Fallback to loaded environment variables or defaults
            cls.BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
            cls.STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
            cls.STANDARD_PASSWORD = os.getenv("STANDARD_PASSWORD", "secret_sauce")
