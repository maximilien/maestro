import io, sys, asyncio, subprocess, threading

import streamlit as st
import streamlit.web.cli as st_cli

from streamlit import runtime

import streamlit_mermaid as stmd

from src.workflow import Workflow
from cli.common import Console, parse_yaml, read_file

# TODO: refactor

sys_stdout = sys.stdout

global workflow_instance
global thread

def start_workflow():
    global output
    output = io.StringIO()
    sys.stdout = output
    asyncio.run(workflow_instance.run())

def create_workflow(agents_yaml, workflow_yaml):
    return Workflow(agents_yaml, workflow_yaml[0])

def generate_output():
    global output
    global position
    position = 0
    message = output.getvalue()
    if len(message) > position:
        lines = output.getvalue()[position:].splitlines()
        for line in lines:
            yield f"{line}\n\n"
        position = len(message)

def deploy_agents_workflow_streamlit(agents_file, workflow_file):
    agents_yaml = parse_yaml(agents_file)
    workflow_yaml = parse_yaml(workflow_file)
    workflow = create_workflow(agents_yaml, workflow_yaml)

    # Set page configuration
    st.set_page_config(
        page_title="Maestro Workflow",
        page_icon="🤖",
        layout="centered"
    )
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to Maestro workflow?"}
        ]

    # Page header
    st.image("images/maestro.png", width=200)
    st.title(f"Maestro workflow")
    st.markdown(f"### {workflow_yaml[0]['metadata']['name']}")
    
    with st.popover("agents.yaml"):
        st.markdown("## Formatted agents YAML")
        st.code(read_file(agents_file), language="yaml", line_numbers=True, wrap_lines=False, height=500)

    with st.popover("workflow.yaml"):
        st.markdown("## Formatted workflow YAML")
        st.code(read_file(workflow_file), language="yaml", line_numbers=True, wrap_lines=False, height=500)

    # create workflow
    global output
    global workflow_instance
    try:
        workflow_instance = Workflow(agents_yaml, workflow_yaml[0])
    except Exception as excep:
        raise RuntimeError("Unable to create agents") from excep
    
    # add workflow mermaid diagram to page
    mermaid_diagram = workflow_instance.to_mermaid()
    stmd.st_mermaid(mermaid_diagram)

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(message["role"], avatar="🤖"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar="👤"):
                st.markdown(message["content"])

    # Function to process user input
    async def process_query(query):
        try:
            return await workflow.run()
        except Exception as e:
            return f"An error occurred: {str(e)}"

    # Chat input
    if prompt := st.chat_input(f"{workflow_yaml[0]['spec']['template']['prompt']}"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant", avatar="🔑"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")

            start_workflow()

            responses = ''
            # stream response
            for response in st.write_stream(generate_output):
                message_placeholder.markdown(response)
                responses += f"{response}"
                
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": responses})

if __name__ == '__main__':
    if runtime.exists():
        deploy_agents_workflow_streamlit(sys.argv[1], sys.argv[2])
    else:
        sys.exit(st_cli.main())