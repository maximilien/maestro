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

import os, yaml, unittest

from unittest import TestCase

from src.mermaid import Mermaid
from src.workflow import Workflow

def parse_yaml(file_path):
    with open(file_path, "r") as file:
        yaml_data = list(yaml.safe_load_all(file))
    return yaml_data

class TestMermaid(TestCase):
    def setUp(self):        
        self.workflow_yaml = parse_yaml(os.path.join(os.path.dirname(__file__),"../yamls/workflows/simple_workflow.yaml"))[0]
        
    def tearDown(self):
        self.workflow_yaml = None

    def test_markdown_sequenceDiagram(self):
        mermaid = Mermaid(self.workflow_yaml, "sequenceDiagram")
        self.assertTrue(mermaid.to_markdown().startswith("sequenceDiagram"))

        for agent in ['test1', 'test2', 'test3']:
            self.assertTrue(f"participant {agent}" in mermaid.to_markdown())
        
        self.assertTrue(f"test1->>test2: step1" in mermaid.to_markdown())
        self.assertTrue(f"test2->>test3: step2" in mermaid.to_markdown())
        self.assertTrue(f"test3->>test3: step3" in mermaid.to_markdown())

    def test_markdown_flowchartTD(self):
        mermaid = Mermaid(self.workflow_yaml, "flowchart", "TD")
        self.assertTrue(mermaid.to_markdown().startswith("flowchart TD"))

        self.assertTrue(f"test1-- step1 -->test2" in mermaid.to_markdown())
        self.assertTrue(f"test2-- step2 -->test3" in mermaid.to_markdown())
        self.assertTrue(f"test3-- step3 -->test3" in mermaid.to_markdown())

    def test_markdown_flowchartRL(self):
        mermaid = Mermaid(self.workflow_yaml, "flowchart", "RL")
        self.assertTrue(mermaid.to_markdown().startswith("flowchart RL"))

        self.assertTrue(f"test1-- step1 -->test2" in mermaid.to_markdown())
        self.assertTrue(f"test2-- step2 -->test3" in mermaid.to_markdown())
        self.assertTrue(f"test3-- step3 -->test3" in mermaid.to_markdown())

class TestWorkdlow_to_mermaid(TestCase):
    def setUp(self):        
        self.workflow_yaml = parse_yaml(os.path.join(os.path.dirname(__file__),"../yamls/workflows/simple_workflow.yaml"))[0]
        self.workflow = Workflow({}, self.workflow_yaml)
        
    def tearDown(self):
        self.workflow_yaml = None
        self.workflow = None

    def test_markdown_sequenceDiagram(self):
        markdown = self.workflow.to_mermaid("sequenceDiagram")
        self.assertTrue(markdown.startswith("sequenceDiagram"))

        self.assertTrue(f"test1->>test2: step1" in markdown)
        self.assertTrue(f"test2->>test3: step2" in markdown)
        self.assertTrue(f"test3->>test3: step3" in markdown)

    def test_markdown_flowchartTD(self):
        markdown = self.workflow.to_mermaid("flowchart", "TD")
        self.assertTrue(markdown.startswith("flowchart TD"))

        self.assertTrue(f"test1-- step1 -->test2" in markdown)
        self.assertTrue(f"test2-- step2 -->test3" in markdown)
        self.assertTrue(f"test3-- step3 -->test3" in markdown)

    def test_markdown_flowchartRL(self):
        markdown = self.workflow.to_mermaid("flowchart", "RL")
        self.assertTrue(markdown.startswith("flowchart RL"))

        self.assertTrue(f"test1-- step1 -->test2" in markdown)
        self.assertTrue(f"test2-- step2 -->test3" in markdown)
        self.assertTrue(f"test3-- step3 -->test3" in markdown)

if __name__ == '__main__':
    unittest.main()
