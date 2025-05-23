> [!WARNING]
> [PRE-Alpha] Please reach out if you want to get involved in the discussions. All feedback is welcomed

# Maestro

A multi-agent platform with the vision to facilitate deployment and running of AI agents.

In this initial version you are going to find some examples showing how to run a group of agents, that you can build using the current and more mature TypeScript [Bee AI Agent framework](https://github.com/i-am-bee/bee-agent-framework), or experiment with the new [Python version](../framework/bee-py).

## Local environment Setup

* Create a Python3.11 virtual environment
* Run a local instance of the [BeeAI Platform](https://github.com/i-am-bee/bee-stack)
  * [Helpful tips](./demos/README.md) on setting up the stack

* Install dependencies: Use the `setup_maestro.sh` script in order to install required libraries using poetry. Run `source ./tools/setup_maestro.sh` in order to install the dependencies and activate a virtual environment. Only need to install the dependencies once, in the future directly activate the venv.

* Configure environmental variables: `cp example.env .env`

## Usage

There are two steps to running a workflow: defining some agents and creating a workflow to run those agents.

> Note: to run Maestro, you will need to [configure your local environment](#local-environment)

### Agent Definition

* You can define your Agent in a declarative way using a YAML file, where you can use the current BeeAI Agent implementation. With that, you can configure your agent or agents. For example, create an `agents.yaml` file containing the following:

```yaml
apiVersion: maestro/v1alpha1
kind: Agent
metadata:
  name: current-affairs
  labels:
    app: mas-example
spec:
  model: meta-llama/llama-3-1-70b-instruct
  description: Get the current weather
  tools:
    - code_interpreter
    - weather
  instructions: Get the current temperature for the location provided by the user. Return results in Fahrenheit.

---
apiVersion: maestro/v1alpha1
kind: Agent
metadata:
  name: hot-or-not
  labels:
    app: mas-example
spec:
  model: meta-llama/llama-3-1-70b-instruct
  description: Is the current temperature hotter than usual?
  tools:
    - code_interpreter
    - weather
  instructions: The user will give you a temperature in Fahrenheit and a location. Use the OpenMateo weather tool to find the average monthly temperature for the location. Answer if the temperature provided by the user is hotter or colder than the average found by the tool.
```

* After defining agents in YAML, create them using Maestro:

```bash
maestro create agents.yaml
```

### Running a Workflow

We use conditional workflows in Maestro, which handle sequential logic by default.

* Define a workflow in YAML listing the agents you wish to run. For example, create a `workflow.yaml` file containing the following:

```yaml
apiVersion: maestro/v1alpha1
kind: Workflow
metadata:
  name: maestro-deployment
  labels:
    app: mas-example
spec:
  template:
    metadata:
      labels:
        app: mas-example
    agents:
      - current-affairs
      - hot-or-not
    prompt: New York City
    steps:
      - name: current-affairs
        agent: current-affairs
      - name: hot-or-not
        agent: hot-or-not
```

* Before running, validate the agent and workflow structure:

```bash
maestro validate agent_schema.json agent.yaml
```

```bash
maestro validate workflow_schema.json workflow.yaml
```

* Execute the workflow:

```bash
maestro run workflow.yaml
```

* Deploy the workflow locally via streamlit:

```bash
maestro deploy agent.yaml workflow.yaml
```

or if you want to change the prompt via CLI:

```bash
maestro deploy agent.yaml workflow.yaml --prompt
```

or

```bash
maestro deploy agent.yaml workflow.yaml --dry-run # to use mock agents for quick testing
```

This will start the workflow in a [`streamlit`]() server and you can access it from your browser: http://localhost:8501/?embed=true

After running, use the `maestro clean` command to shut down the instance.

## Mermaid Support

Maestro supports the creation of visual diagrams of how the workflow will execute. In a given demo,  one can run the following command to visualize:

```bash
maestro mermaid workflow.yaml
```

Additionally, to auto update all maestro readme demos with mermaid (after changes are made in the workflow file), you can use `./tools/update_readme.sh`

### Run workflow in streamlit (default deploy)

* Required Export Tags
  * `export CONTAINER_CMD=podman`
* Deployment
  * `maestro deploy agents.yaml workflow.yaml --streamlit`
* Meta-Agent Specific deployment
  * `maestro meta-agents text_file.txt`
  * the text file contains the prompt you want to run

### Run workflow in local environment with container runtime (e.g. podman) or kubernetes cluster

* Prepare required environments, running from `~/maestro/` top level:
  * Run a local instance of the [BeeAI Platform](https://github.com/i-am-bee/bee-stack)
  * for Kubernetes, [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/), [`kind`](https://kind.sigs.k8s.io/) are required

* Required Export Tags
  * `export IMAGE_PUSH_CMD='kind load docker-image docker.io/library/maestro:latest'`
  * `export IMAGE_TAG_CMD='docker tag localhost/maestro:latest docker.io/library/maestro:latest'`
  * `export CONTAINER_CMD=podman`

* Running command:
  * `kind create cluster --config maestro/tests/integration/deploys/kind-config.yaml`
  * To delete the cluster: `kind delete cluster`

* Deployment:
  * `maestro deploy agents.yaml workflow.yaml --docker BEE_API_KEY=sk-proj-testkey BEE_API=http://<local-ip>:4000`

* Helpful Debugging tools:
  * Find out where your BEE_API is:
    * `ifconfig | grep 'inet'`
  * Restarting containers:
    * `podman ps | grep maestro` -> `podman stop <container_id>` -> `podman rm <container_id>`
  * Finding where the UI is hosted:
    * `podman ps | grep maestro`
    * by default, should be deployed at `127.0.0.1:5000`

### Running agents with the OpenAI Agents API

This allows the execution of Agents on OpenAI, or compatible endpoints (including Ollama), and supports the use of local and remote MCP tools. See [README_openai.md](docs/README_openai.md)

# Contributing
* Learn about [contributing](./demos/CONTRIBUTING.md)
