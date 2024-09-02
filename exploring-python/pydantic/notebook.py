import os
import nbformat as nbf

# Define the path where your Markdown files are located
md_files_path = './'  # Adjust this path if your files are in a different directory

# List of Markdown files to be converted
md_files = [
    "1_1_what_is_pydantic.md",
    "1_2_why_use_pydantic.md",
    "1_3_installation_and_setup.md",
    "1_4_basic_concepts_data_validation_and_settings_management.md",
    "2_1_creating_basic_models.md",
    "2_2_field_types_and_annotations.md",
    "2_3_default_values.md",
    "2_4_field_constraints.md",
    "2_5_custom_field_types.md",
    "2_6_nested_models.md",
    "2_7_model_inheritance.md",
    "2_8_python_type_hinting_and_pydantic.md",
    "3_1_basic_validation.md",
    "3_2_custom_validators.md",
    "3_3_pre_and_post_processing_hooks.md",
    "3_4_root_validators.md",
    "3_5_field_level_validation.md",
    "3_6_handling_validation_errors.md"
]

# Directory to save the notebooks
output_dir = 'notebooks'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to split the content into markdown and code cells
def split_content_to_cells(md_content):
    lines = md_content.splitlines()
    cells = []
    in_code_block = False
    code_block = []
    markdown_block = []
    current_code_type = "python"

    for line in lines:
        if line.strip().startswith("```"):  # Detect start or end of a code block
            if in_code_block:
                # End of code block
                if current_code_type == "python":
                    cells.append(nbf.v4.new_code_cell("\n".join(code_block)))
                else:
                    cells.append(nbf.v4.new_code_cell("\n".join(code_block), metadata={"kernelspec": {"name": "bash"}}))
                code_block = []
            else:
                # End of markdown block
                if markdown_block:
                    cells.append(nbf.v4.new_markdown_cell("\n".join(markdown_block)))
                    markdown_block = []
                current_code_type = line.strip()[3:]  # Get the language type
            in_code_block = not in_code_block
        elif in_code_block:
            code_block.append(line)
        else:
            markdown_block.append(line)

    # Add any remaining content as a markdown cell
    if markdown_block:
        cells.append(nbf.v4.new_markdown_cell("\n".join(markdown_block)))

    return cells

# Loop through each Markdown file and convert it to a Jupyter Notebook
for md_file in md_files:
    # Define the output notebook filename
    notebook_filename = os.path.join(output_dir, os.path.splitext(md_file)[0] + '.ipynb')
    
    # Read the content of the markdown file
    with open(os.path.join(md_files_path, md_file), 'r') as f:
        md_content = f.read()

    # Create a new Jupyter notebook
    nb = nbf.v4.new_notebook()

    # Split content into notebook cells
    nb.cells = split_content_to_cells(md_content)

    # Check if the first line of content is an H1 header
    if not nb.cells[0]['source'].startswith("# "):
        # Add a dynamic title cell only if the first line is not an H1 header
        title_cell = nbf.v4.new_markdown_cell(f"# {os.path.splitext(md_file)[0].replace('_', ' ').title()}")
        nb.cells.insert(0, title_cell)

    # Save the notebook
    with open(notebook_filename, 'w') as f:
        nbf.write(nb, f)

    print(f"Notebook created successfully: {notebook_filename}")

print(f"All notebooks have been created and saved in the '{output_dir}' directory.")
