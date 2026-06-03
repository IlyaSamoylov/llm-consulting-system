from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	"""Класс для хранения конфигурации приложения"""
	model_config = SettingsConfigDict(env_file=".env", env_prefix="")

	APP_NAME: str = "auth-service"
	ENV: str = "local"

	JWT_SECRET: str
	JWT_ALG: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

	AUTH_HOST: str = "0.0.0.0"
	AUTH_PORT: int = 8000

	LOG_LEVEL: str = "INFO"
	AUTH_DEBUG: bool = True

	DB_USER: str
	DB_PASSWORD: str
	DB_HOST: str = "db"
	DB_PORT: int = 5432
	DB_NAME: str = "app_db"

	@property
	def db_url(self) -> str:
		"""Собранный database url"""
		return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
		        f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

settings = Settings()