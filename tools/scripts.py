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

#!/usr/bin/env python3

import sys, subprocess
import re

def lint():
    try:
        subprocess.run(["black", "."], check=True)
        subprocess.run(["ruff", "check", "."], check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)

def commit():
    if len(sys.argv) < 2:
        print('Usage: uv run commit "<commit message>"')
        sys.exit(1)

    commit_msg = sys.argv[1]
    if not re.match(r'^(feat|fix|docs|style|refactor|test|chore)(\([a-z-]+\))?: .+', commit_msg):
        print('Error: Commit message must follow the conventional commits format:')
        print('<type>(<scope>): <subject>')
        print('\nTypes: feat, fix, docs, style, refactor, test, chore')
        sys.exit(1)

    print("📦 Adding files...")
    subprocess.run(["git", "add", "--all"], check=True)

    print("📝 Committing changes...")
    subprocess.run(["git", "commit", "-s", "-m", commit_msg], check=True)

    print("Successfully committed changes")

if __name__ == '__main__':
    commit()
