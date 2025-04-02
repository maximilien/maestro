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

import os, unittest

from unittest import TestCase

from src.agents.agent_factory import AgentFramework, AgentFactory, EMOJIS

class TestAgentFramework(TestCase):    
    def test_frameworks(self):        
        self.assertTrue(AgentFramework.BEEAI is not None)
        self.assertTrue(AgentFramework.CREWAI is not None)
        self.assertTrue(AgentFramework.MOCK is not None)
        self.assertTrue(AgentFramework.REMOTE is not None)

    def test_EMOJIS(self):
        self.assertTrue(EMOJIS['beeai'] == '🐝')
        self.assertTrue(EMOJIS['crewai'] == '👥')
        self.assertTrue(EMOJIS['mock'] == '🤖')
        self.assertTrue(EMOJIS['remote'] == '💸')

class TestAgentFactory(TestCase):    
    def test_create_agents(self):
        pass

    def test_get_factory(self):
        pass

if __name__ == '__main__':
    unittest.main()