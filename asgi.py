import os
from src.server import create_app

# Get environment from variable
config_name = os.getenv("ENVIRONMENT", "local")
debug = os.getenv("DEBUG")

application = create_app(config_name=config_name)

if __name__ == "__main__":
    application.run(debug=debug)
