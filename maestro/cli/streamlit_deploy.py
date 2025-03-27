import io, sys, asyncio, subprocess, threading

import streamlit as st

from streamlit import runtime
from streamlit.web import cli
import streamlit.components.v1 as components

from src.workflow import Workflow
from cli.common import Console, parse_yaml

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
    st.title(f"Maestro workflow: {workflow_yaml[0]['metadata']['name']}")

    # create workflow
    global output
    global workflow_instance
    try:
        workflow_instance = Workflow(agents_yaml, workflow_yaml[0])
    except Exception as excep:
        raise RuntimeError("Unable to create agents") from excep
    
    # add workflow diagram to page
    mermaid_diagram = workflow_instance.to_mermaid()
    html_code = f"""
    <div class="mermaid-container">
    <pre>
    <code class="language-mermaid">
    {mermaid_diagram}
    </code></pre>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

    html_code ="""
    <script>
    var config = {
        startOnLoad:true,
        theme: 'forest',
        flowchart:{
                useMaxWidth:false,
                htmlLabels:true
            }
    };
    mermaid.initialize(config);
    window.mermaid.init(undefined, document.querySelectorAll('.language-mermaid'));
    </script>
    """
    st.markdown(html_code, unsafe_allow_html=True)

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
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(cli.main())