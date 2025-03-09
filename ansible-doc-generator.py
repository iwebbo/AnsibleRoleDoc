#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to generate Markdown/text documentation from a zip file 
containing the structure of an Ansible role.
"""

import os
import sys
import zipfile
import yaml
import argparse
import re
from pathlib import Path


class AnsibleRoleDocGenerator:
    """Documentation generator for Ansible roles."""

    def __init__(self, zip_path, output_format="markdown", output_file=None):
        """
        Initialize the generator.
        
        Args:
            zip_path (str): Path to the Ansible role zip file
            output_format (str): Output format ("markdown" or "text")
            output_file (str): Output file path (optional)
        """
        self.zip_path = zip_path
        self.output_format = output_format.lower()
        self.output_file = output_file
        self.role_name = ""
        self.role_structure = {}
        
        # Check that the output format is valid
        if self.output_format not in ["markdown", "text"]:
            raise ValueError("Output format must be 'markdown' or 'text'")
    
    def extract_role_info(self):
        """Extract role information from the zip file."""
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                # Determine role name (based on first directory)
                if len(file_list) > 0:
                    first_item = file_list[0].split('/')[0]
                    if first_item and first_item != '.':
                        self.role_name = first_item
                
                # Extract role structure
                self.role_structure = self._analyze_structure(file_list)
                
                # Get content of important files
                metadata = self._read_metadata(zip_ref)
                defaults = self._read_defaults(zip_ref)
                tasks = self._read_tasks(zip_ref)
                templates = self._find_templates(file_list)
                handlers = self._read_handlers(zip_ref)
                vars_data = self._read_vars(zip_ref)
                
                return {
                    "name": self.role_name,
                    "structure": self.role_structure,
                    "metadata": metadata,
                    "defaults": defaults,
                    "tasks": tasks,
                    "templates": templates,
                    "handlers": handlers,
                    "vars": vars_data
                }
        except zipfile.BadZipFile:
            raise Exception(f"Error: {self.zip_path} is not a valid zip file")
    
    def _analyze_structure(self, file_list):
        """Analyze the role structure from file paths."""
        structure = {}
        
        for file_path in file_list:
            parts = file_path.split('/')
            # Ignore role name at the beginning of the path
            if len(parts) > 1 and parts[0] == self.role_name:
                parts = parts[1:]
            
            current_level = structure
            for i, part in enumerate(parts):
                if i == len(parts) - 1 and part:  # If it's a file (not an empty directory)
                    if "__files__" not in current_level:
                        current_level["__files__"] = []
                    current_level["__files__"].append(part)
                elif part:  # If it's a directory
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]
        
        return structure
    
    def _read_yaml_file(self, zip_ref, file_path):
        """Read and parse a YAML file in the zip."""
        try:
            if file_path in zip_ref.namelist():
                content = zip_ref.read(file_path).decode('utf-8')
                return yaml.safe_load(content)
        except Exception as e:
            print(f"Warning: Unable to read {file_path}: {str(e)}")
        return None
    
    def _read_metadata(self, zip_ref):
        """Read the meta/main.yml file."""
        meta_path = f"{self.role_name}/meta/main.yml"
        return self._read_yaml_file(zip_ref, meta_path)
    
    def _read_defaults(self, zip_ref):
        """Read the defaults/main.yml file."""
        defaults_path = f"{self.role_name}/defaults/main.yml"
        return self._read_yaml_file(zip_ref, defaults_path)
    
    def _read_tasks(self, zip_ref):
        """Read task files."""
        tasks = {}
        main_tasks_path = f"{self.role_name}/tasks/main.yml"
        tasks["main"] = self._read_yaml_file(zip_ref, main_tasks_path)
        
        # Search for other task files
        for filename in zip_ref.namelist():
            if filename.startswith(f"{self.role_name}/tasks/") and filename != main_tasks_path:
                task_name = os.path.basename(filename)
                tasks[task_name] = self._read_yaml_file(zip_ref, filename)
        
        return tasks
    
    def _find_templates(self, file_list):
        """Identify template files."""
        templates = []
        templates_prefix = f"{self.role_name}/templates/"
        
        for filename in file_list:
            if filename.startswith(templates_prefix) and not filename.endswith('/'):
                template_path = filename[len(templates_prefix):]
                templates.append(template_path)
        
        return templates
    
    def _read_handlers(self, zip_ref):
        """Read the handlers/main.yml file."""
        handlers_path = f"{self.role_name}/handlers/main.yml"
        return self._read_yaml_file(zip_ref, handlers_path)
    
    def _read_vars(self, zip_ref):
        """Read variable files."""
        vars_data = {}
        vars_path = f"{self.role_name}/vars/main.yml"
        vars_data["main"] = self._read_yaml_file(zip_ref, vars_path)
        
        # Search for other variable files
        for filename in zip_ref.namelist():
            if filename.startswith(f"{self.role_name}/vars/") and filename != vars_path:
                var_name = os.path.basename(filename)
                vars_data[var_name] = self._read_yaml_file(zip_ref, filename)
        
        return vars_data
    
    def generate_documentation(self):
        """Generate documentation based on extracted information."""
        role_info = self.extract_role_info()
        
        if self.output_format == "markdown":
            content = self._generate_markdown(role_info)
        else:  # text
            content = self._generate_text(role_info)
        
        if self.output_file:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Documentation generated in {self.output_file}")
        
        return content
    
    def _generate_markdown(self, role_info):
        """Generate documentation in Markdown format."""
        lines = []
        
        # Title and description
        lines.append(f"# Ansible Role: {role_info['name']}")
        lines.append("")
        
        # Description from metadata
        if role_info['metadata'] and 'galaxy_info' in role_info['metadata']:
            galaxy_info = role_info['metadata']['galaxy_info']
            if 'description' in galaxy_info:
                lines.append(f"{galaxy_info['description']}")
                lines.append("")
        
        # Metadata information
        lines.append("## General Information")
        lines.append("")
        
        if role_info['metadata'] and 'galaxy_info' in role_info['metadata']:
            galaxy_info = role_info['metadata']['galaxy_info']
            
            if 'author' in galaxy_info:
                lines.append(f"**Author:** {galaxy_info['author']}")
            
            if 'license' in galaxy_info:
                lines.append(f"**License:** {galaxy_info['license']}")
            
            if 'min_ansible_version' in galaxy_info:
                lines.append(f"**Minimum Ansible Version:** {galaxy_info['min_ansible_version']}")
            
            if 'platforms' in galaxy_info:
                lines.append("")
                lines.append("**Supported Platforms:**")
                for platform in galaxy_info['platforms']:
                    lines.append(f"- {platform.get('name', 'N/A')}")
                    if 'versions' in platform:
                        versions = ", ".join(str(v) for v in platform['versions'])
                        lines.append(f"  - Versions: {versions}")
            
            lines.append("")
        
        # Default variables
        if role_info['defaults']:
            lines.append("## Default Variables")
            lines.append("")
            lines.append("```yaml")
            lines.append(yaml.dump(role_info['defaults'], default_flow_style=False, sort_keys=False))
            lines.append("```")
            lines.append("")
        
        # Variables (vars)
        if role_info['vars'] and any(role_info['vars'].values()):
            lines.append("## Variables")
            lines.append("")
            for var_file, var_content in role_info['vars'].items():
                if var_content:
                    lines.append(f"### {var_file}")
                    lines.append("")
                    lines.append("```yaml")
                    lines.append(yaml.dump(var_content, default_flow_style=False, sort_keys=False))
                    lines.append("```")
                    lines.append("")
        
        # Main tasks
        if role_info['tasks'] and 'main' in role_info['tasks'] and role_info['tasks']['main']:
            lines.append("## Main Tasks")
            lines.append("")
            
            tasks = role_info['tasks']['main']
            for idx, task in enumerate(tasks if isinstance(tasks, list) else []):
                if 'name' in task:
                    lines.append(f"- {task['name']}")
            
            # lines.append("")
            # lines.append("```yaml")
            # lines.append(yaml.dump(tasks, default_flow_style=False, sort_keys=False))
            # lines.append("```")
            lines.append("")
        
        # Other task files
        other_tasks = {k: v for k, v in role_info['tasks'].items() if k != 'main' and v}
        if other_tasks:
            lines.append("## Other Tasks")
            lines.append("")
            
            for task_file, task_content in other_tasks.items():
                lines.append(f"### {task_file}")
                lines.append("")
                lines.append("```yaml")
                lines.append(yaml.dump(task_content, default_flow_style=False, sort_keys=False))
                lines.append("```")
                lines.append("")
        
        # Handlers
        if role_info['handlers']:
            lines.append("## Handlers")
            lines.append("")
            lines.append("```yaml")
            lines.append(yaml.dump(role_info['handlers'], default_flow_style=False, sort_keys=False))
            lines.append("```")
            lines.append("")
        
        # Templates
        if role_info['templates']:
            lines.append("## Templates")
            lines.append("")
            for template in role_info['templates']:
                lines.append(f"- `{template}`")
            lines.append("")
        
        # Role structure
        lines.append("## Role Structure")
        lines.append("")
        lines.append("```")
        structure_text = self._format_structure(role_info['structure'])
        lines.append(structure_text)
        lines.append("```")
        
        # Dependencies
        if role_info['metadata'] and 'dependencies' in role_info['metadata']:
            dependencies = role_info['metadata']['dependencies']
            if dependencies:
                lines.append("")
                lines.append("## Dependencies")
                lines.append("")
                
                for dep in dependencies:
                    if isinstance(dep, str):
                        lines.append(f"- {dep}")
                    elif isinstance(dep, dict) and 'role' in dep:
                        lines.append(f"- {dep['role']}")
                        # Add other details if available
                        for key, value in dep.items():
                            if key != 'role':
                                lines.append(f"  - {key}: {value}")
        
        return "\n".join(lines)
    
    def _generate_text(self, role_info):
        """Generate documentation in text format."""
        lines = []
        
        # Title and description
        lines.append(f"ANSIBLE ROLE: {role_info['name'].upper()}")
        lines.append("=" * (len(role_info['name']) + 14))
        lines.append("")
        
        # Description from metadata
        if role_info['metadata'] and 'galaxy_info' in role_info['metadata']:
            galaxy_info = role_info['metadata']['galaxy_info']
            if 'description' in galaxy_info:
                lines.append(f"{galaxy_info['description']}")
                lines.append("")
        
        # Metadata information
        lines.append("GENERAL INFORMATION")
        lines.append("---------------------")
        lines.append("")
        
        if role_info['metadata'] and 'galaxy_info' in role_info['metadata']:
            galaxy_info = role_info['metadata']['galaxy_info']
            
            if 'author' in galaxy_info:
                lines.append(f"Author: {galaxy_info['author']}")
            
            if 'license' in galaxy_info:
                lines.append(f"License: {galaxy_info['license']}")
            
            if 'min_ansible_version' in galaxy_info:
                lines.append(f"Minimum Ansible Version: {galaxy_info['min_ansible_version']}")
            
            if 'platforms' in galaxy_info:
                lines.append("")
                lines.append("Supported Platforms:")
                for platform in galaxy_info['platforms']:
                    lines.append(f"- {platform.get('name', 'N/A')}")
                    if 'versions' in platform:
                        versions = ", ".join(str(v) for v in platform['versions'])
                        lines.append(f"  - Versions: {versions}")
            
            lines.append("")
        
        # Default variables
        if role_info['defaults']:
            lines.append("DEFAULT VARIABLES")
            lines.append("--------------------")
            lines.append("")
            yaml_content = yaml.dump(role_info['defaults'], default_flow_style=False, sort_keys=False)
            lines.append(yaml_content)
            lines.append("")
        
        # Variables (vars)
        if role_info['vars'] and any(role_info['vars'].values()):
            lines.append("VARIABLES")
            lines.append("---------")
            lines.append("")
            for var_file, var_content in role_info['vars'].items():
                if var_content:
                    lines.append(f"{var_file}:")
                    lines.append("-" * (len(var_file) + 1))
                    lines.append("")
                    yaml_content = yaml.dump(var_content, default_flow_style=False, sort_keys=False)
                    lines.append(yaml_content)
                    lines.append("")
        
        # Main tasks
        if role_info['tasks'] and 'main' in role_info['tasks'] and role_info['tasks']['main']:
            lines.append("MAIN TASKS")
            lines.append("-----------------")
            lines.append("")
            
            tasks = role_info['tasks']['main']
            for idx, task in enumerate(tasks if isinstance(tasks, list) else []):
                if 'name' in task:
                    lines.append(f"- {task['name']}")
            
            lines.append("")
            yaml_content = yaml.dump(tasks, default_flow_style=False, sort_keys=False)
            lines.append(yaml_content)
            lines.append("")
        
        # Other task files
        other_tasks = {k: v for k, v in role_info['tasks'].items() if k != 'main' and v}
        if other_tasks:
            lines.append("OTHER TASKS")
            lines.append("-------------")
            lines.append("")
            
            for task_file, task_content in other_tasks.items():
                lines.append(f"{task_file}:")
                lines.append("-" * (len(task_file) + 1))
                lines.append("")
                yaml_content = yaml.dump(task_content, default_flow_style=False, sort_keys=False)
                lines.append(yaml_content)
                lines.append("")
        
        # Handlers
        if role_info['handlers']:
            lines.append("HANDLERS")
            lines.append("--------")
            lines.append("")
            yaml_content = yaml.dump(role_info['handlers'], default_flow_style=False, sort_keys=False)
            lines.append(yaml_content)
            lines.append("")
        
        # Templates
        if role_info['templates']:
            lines.append("TEMPLATES")
            lines.append("---------")
            lines.append("")
            for template in role_info['templates']:
                lines.append(f"- {template}")
            lines.append("")
        
        # Role structure
        lines.append("STRUCTURE DU RÔLE")
        lines.append("----------------")
        lines.append("")
        structure_text = self._format_structure(role_info['structure'])
        lines.append(structure_text)
        
        # Dependencies
        if role_info['metadata'] and 'dependencies' in role_info['metadata']:
            dependencies = role_info['metadata']['dependencies']
            if dependencies:
                lines.append("")
                lines.append("DEPENDENCIES")
                lines.append("-----------")
                lines.append("")
                
                for dep in dependencies:
                    if isinstance(dep, str):
                        lines.append(f"- {dep}")
                    elif isinstance(dep, dict) and 'role' in dep:
                        lines.append(f"- {dep['role']}")
                        # Ajouter d'autres détails si disponibles
                        for key, value in dep.items():
                            if key != 'role':
                                lines.append(f"  - {key}: {value}")
        
        return "\n".join(lines)
    
    def _format_structure(self, structure, prefix="", is_last=True, indent=""):
        """Format the role structure for display."""
        lines = []
        
        # Process files before directories
        files = structure.pop("__files__", []) if "__files__" in structure else []
        
        # Determine keys (directories) and sort them
        items = list(structure.items())
        
        for i, (key, value) in enumerate(items):
            is_last_dir = (i == len(items) - 1 and not files)
            
            # Add line for directory
            if not prefix:  # First level
                lines.append(f"{key}/")
                new_indent = "    "
            else:
                branch = "└── " if is_last_dir else "├── "
                lines.append(f"{indent}{branch}{key}/")
                new_indent = indent + ("    " if is_last_dir else "│   ")
            
            # Recursively add subdirectories
            if value:
                sub_structure = self._format_structure(value, f"{prefix}/{key}", is_last_dir, new_indent)
                lines.append(sub_structure)
        
        # Add files
        for i, filename in enumerate(sorted(files)):
            is_last_file = (i == len(files) - 1)
            branch = "└── " if is_last_file else "├── "
            
            if not prefix:  # First level
                lines.append(f"{filename}")
            else:
                lines.append(f"{indent}{branch}{filename}")
        
        return "\n".join(lines)

def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(
        description="Generate documentation from a zip file containing an Ansible role."
    )
    parser.add_argument(
        "zip_file", 
        help="Path to the zip file containing the Ansible role"
    )
    parser.add_argument(
        "-f", "--format", 
        choices=["markdown", "text"], 
        default="markdown",
        help="Output format (markdown or text). Default: markdown"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output file. Default: stdout"
    )
    
    args = parser.parse_args()
    
    try:
        generator = AnsibleRoleDocGenerator(
            args.zip_file, 
            output_format=args.format, 
            output_file=args.output
        )
        doc = generator.generate_documentation()
        
        if not args.output:
            print(doc)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
