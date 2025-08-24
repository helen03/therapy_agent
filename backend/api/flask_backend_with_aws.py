
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File Name: flask_backend_with_aws.py
#
# Script to call from command line to launch application
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend import create_app

# ~~~ Create application ~~~ #
application = create_app()
#
# from backend import db # noqa
# from backend.database.models import User # noqa

