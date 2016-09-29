from fabric.api import env, run
import datetime
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

class RemoteCommand():
    def __init__(self, host, command):
        self.remote_user = settings.REMOTE_USER
        self.remote_host = host
        self.remote_key  = settings.REMOTE_KEY
        self.command = command
        self.log_dir = settings.LOG_DIR

    def execute(self):

        env.user         = self.remote_user
        env.host_string  = self.remote_host
        env.key_filename = self.remote_key

        try:
            run_command = run(self.command)
            self.log_file = self.log_dir + self.remote_host + '.' + str(datetime.datetime.now().strftime('%Y%m%d.%H%M%S')) + '.txt'
            with open(self.log_file, 'wb') as file:
                for line in run_command.splitlines():
                    # logger.debug(line)
                    file.write(line)
                    file.write('\n')
            file.close()
        except Exception, e:
            raise Exception('ERROR: ', str(e))

        return self.log_file