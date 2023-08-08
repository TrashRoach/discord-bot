import os


class Config:
    LOG_FORMAT = '%(levelname)-8s [%(asctime)s] %(name)s %(message)s'
    LOG_LEVEL = 'INFO'

    DB_CONFIG = os.getenv(
        'DB_CONFIG',
        'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'.format(
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASS', 'postgres'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'discord_bot'),
        ),
    )

    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    DISCORD_BOT_PREFIX = os.getenv('DISCORD_BOT_PREFIX')


config = Config
