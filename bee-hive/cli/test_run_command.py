#!/usr/bin/env python3

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

from unittest import TestCase

from cli import CLI

class RunCommand(TestCase):
    def setUp(self):
        self.args = {
                        '--dry-run': True,
                        '--help': False,
                        '--verbose': False,
                        '--version': False,
                        'AGENTS_FILE': '../test/yamls/agents/simple_agent.yaml',
                        'SCHEMA_FILE': None,
                        'WORKFLOW_FILE': '../test/yamls/workflows/simple_workflow.yaml',
                        'YAML_FILE': None,
                        'deploy': False,
                        'run': True,
                        'validate': False
                    }
        self.command = CLI(self.args).command()
    
    def tearDown(self):
        self.args = {}
        self.command = None
        
    def test_run__dry_run(self):        
        self.assertTrue(self.command.name() == 'run')
        self.assertTrue(self.command.execute() == 0)
        
if __name__ == '__main__':
    unittest.main()