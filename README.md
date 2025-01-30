Create a `.env` file with the variables from `settings.py`, for example:

```python
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).parent / ".env"

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")
    db_username: str = Field(alias="DATABASE_USERNAME", default="db_user")
    db_password: Optional[str] = Field(alias="DATABASE_PASSWORD", default=None)
    db_host: str = Field(alias="DATABASE_HOST", default="localhost")
    db_port: int = Field(alias="DATABASE_PORT", default=3306)
    db_name: str = Field(alias="DATABASE_NAME", default="users")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8", env_file=ENV_FILE)
    database: DatabaseSettings = DatabaseSettings()
```
For example, your `.env` file might look like this:

```
DATABASE_USERNAME=my_db_user
DATABASE_PASSWORD=my_db_password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DATABASE_NAME=my_database
```