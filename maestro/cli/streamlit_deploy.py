import io, sys, asyncio

import streamlit as st

from streamlit import runtime
from streamlit.web import cli

from src.workflow import Workflow
from cli.common import Console, parse_yaml

global output, position

def create_workflow(agents_yaml, workflow_yaml):
    return Workflow(agents_yaml, workflow_yaml[0])

def deploy_agents_workflow_streamlit(agents_file, workflow_file):
    output = io.StringIO()
    position = 0
    sys.stdout = output

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
    st.title(f"Maestro workflow: {workflow_yaml[0]['metadata']['name']}")
    st.markdown(f"{workflow_yaml[0]['spec']['template']['prompt']}")

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
            
            # Process the query
            response = asyncio.run(process_query(prompt))

            message = output.getvalue()
            if len(message) > position:
                lines = output.getvalue()[position:].splitlines()
                for line in lines:
                    message_placeholder.markdown(f"{line}")
                position = len(message)

            # Update the placeholder with the response
            message_placeholder.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response}) 

if __name__ == '__main__':
    if runtime.exists():
        deploy_agents_workflow_streamlit(sys.argv[1], sys.argv[2])
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(cli.main())