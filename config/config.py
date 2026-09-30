import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    ENV_NAME = "QA_ENVIRONMENT"
    BASE_URL = ""
    STANDARD_USER = ""
    LOCKED_USER = ""
    STANDARD_PASSWORD = ""
    AUTH_STATE_PATH = "state/auth.json"

    @classmethod
    def load_environment(cls, env_name: str = "qa"):
        target_env = env_name.lower()
        root_dir = Path(__file__).parent.parent
        env_file_path = root_dir / f".env.{target_env}"

        if not env_file_path.exists():
            env_file_path = root_dir / ".env"

        load_dotenv(dotenv_path=env_file_path, override=True)

        cls.ENV_NAME = os.getenv("ENV_NAME", target_env.upper())
        cls.BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
        cls.STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
        cls.LOCKED_USER = os.getenv("LOCKED_USER", "locked_out_user")
        cls.STANDARD_PASSWORD = os.getenv("STANDARD_PASSWORD", "secret_sauce")
        cls.AUTH_STATE_PATH = os.getenv("AUTH_STATE_PATH", "state/auth.json")