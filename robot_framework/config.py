"""This module contains configuration constants used across the framework"""

# The number of times the robot retries on an error before terminating.
MAX_RETRY_COUNT = 3

# Whether the robot should be marked as failed if MAX_RETRY_COUNT is reached.
FAIL_ROBOT_ON_TOO_MANY_ERRORS = True

# Error screenshot config
SMTP_SERVER = "smtp.aarhuskommune.local"
SMTP_PORT = 25
SCREENSHOT_SENDER = "robot@friend.dk"

# Constant/Credential names
ERROR_EMAIL = "Error Email"

# Miralix
MIRALIX_SHARED_KEY = "Miralix Shared Key"
MIRALIX_BASE_URL = "https://webrequest-aarhus.miralix.online/mot/12986"
MIRALIX_TIMEOUT = 60

# GetOrganized
GO_API = "https://ad.go.aarhuskommune.dk"
GO_CREDENTIALS = "GetOrganized Login"
GO_TIMEOUT = 60

# Queue specific configs
# ----------------------

# The name of the job queue (if any)
QUEUE_NAME = "Miralix Nedhentning"

# ----------------------
