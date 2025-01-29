# Copyright © 2025 IBM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io, sys

from common import *

class CLI:
    def __init__(self, args):
        self.args = args
        if self.args['--verbose']:
            VERBOSE = True

    def command(self):
        if self.args.get('validate') and self.args['validate']:
            return Validate(self.args)
        else:
            raise Exception("Invalid command")

class Command:
    def __init__(self, args, credentials, client):
        self.__init_empty_options(args)
        self.args = args
    
    def println(self, msg):
        self.print(msg + "\n")

    def print(self, msg):
        Console.print(msg)

    def warn(self, msg):
        Console.warn(msg)

    def verbose(self):
        return self.args['--verbose']
    
    def execute(self):
        func = self.dispatch()
        rc = func()
        if rc == None:
            return 0
        else:
            if isinstance(rc, int):
                return rc
            else:
                return 1

    def dispatch(self):
        if self.args['validate']:
            return self.validate
        else:
            raise Exception("Invalid subcommand")
