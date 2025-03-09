![ansible-doc-generator-diagram](https://github.com/user-attachments/assets/91ce4354-12a8-4b4c-ac04-aa737cda8f6b)# AnsibleRoleDoc
 Creation of documentation Roles Ansible

## 📌 Technologies 

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white) ![Ansible](https://img.shields.io/badge/Ansible-3776AB?style=for-the-badge&logo=Ansible&logoColor=white) ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=Linux&logoColor=black) 

## 📌 Prerequisites

python >=3.8, ansible-roles

## 📌 Diagram
![Uploading ans<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">
  <!-- Background -->
  <rect width="800" height="500" fill="#f8f9fa" rx="10" ry="10" />
  
  <!-- Title -->
  <text x="400" y="40" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="#333">Ansible Role Documentation Generator</text>
  
  <!-- Flow diagram -->
  
  <!-- Input -->
  <rect x="50" y="100" width="120" height="60" rx="5" ry="5" fill="#eef" stroke="#99c" stroke-width="2" />
  <text x="110" y="135" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">Ansible Role ZIP</text>
  
  <!-- Process Blocks -->
  <rect x="280" y="100" width="240" height="300" rx="8" ry="8" fill="#f5f5ff" stroke="#aaa" stroke-width="2" />
  <text x="400" y="130" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#333">Documentation Generator</text>
  
  <!-- Sub-processes -->
  <rect x="300" y="150" width="200" height="40" rx="5" ry="5" fill="#e1e1ff" stroke="#99c" stroke-width="1" />
  <text x="400" y="175" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Extract Role Structure</text>
  
  <rect x="300" y="205" width="200" height="40" rx="5" ry="5" fill="#e1e1ff" stroke="#99c" stroke-width="1" />
  <text x="400" y="230" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Read Metadata</text>
  
  <rect x="300" y="260" width="200" height="40" rx="5" ry="5" fill="#e1e1ff" stroke="#99c" stroke-width="1" />
  <text x="400" y="285" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Parse Tasks & Variables</text>
  
  <rect x="300" y="315" width="200" height="40" rx="5" ry="5" fill="#e1e1ff" stroke="#99c" stroke-width="1" />
  <text x="400" y="340" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#333">Format Documentation</text>
  
  <!-- Output -->
  <rect x="630" y="100" width="120" height="60" rx="5" ry="5" fill="#efe" stroke="#9c9" stroke-width="2" />
  <text x="690" y="135" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">Markdown Docs</text>
  
  <rect x="630" y="200" width="120" height="60" rx="5" ry="5" fill="#efe" stroke="#9c9" stroke-width="2" />
  <text x="690" y="235" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#333">Text Docs</text>
  
  <!-- Arrows -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
    </marker>
  </defs>
  
  <!-- Input to Process -->
  <line x1="170" y1="130" x2="280" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />
  
  <!-- Process to Outputs -->
  <line x1="520" y1="130" x2="630" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />
  <line x1="520" y1="230" x2="630" y2="230" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />
  <path d="M 520 180 C 560 180, 560 230, 560 230" stroke="#666" stroke-width="2" fill="none" />
  
  <!-- Role Structure Visualization -->
  <g transform="translate(120, 320)">
    <rect x="0" y="0" width="140" height="140" rx="5" ry="5" fill="#f5f5f5" stroke="#aaa" stroke-width="1" />
    <text x="70" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#333">Role Structure</text>
    
    <!-- Directory tree -->
    <text x="10" y="40" font-family="monospace" font-size="11" fill="#333">role_name/</text>
    <text x="20" y="55" font-family="monospace" font-size="11" fill="#333">├── defaults/</text>
    <text x="30" y="70" font-family="monospace" font-size="11" fill="#333">│   └── main.yml</text>
    <text x="20" y="85" font-family="monospace" font-size="11" fill="#333">├── tasks/</text>
    <text x="30" y="100" font-family="monospace" font-size="11" fill="#333">│   └── main.yml</text>
    <text x="20" y="115" font-family="monospace" font-size="11" fill="#333">├── templates/</text>
    <text x="20" y="130" font-family="monospace" font-size="11" fill="#333">└── meta/</text>
  </g>
  
  <!-- Documentation format visualization -->
  <g transform="translate(580, 320)">
    <rect x="0" y="0" width="180" height="140" rx="5" ry="5" fill="#f5f5f5" stroke="#aaa" stroke-width="1" />
    <text x="90" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#333">Documentation Content</text>
    
    <text x="10" y="40" font-family="Arial, sans-serif" font-size="11" fill="#333">• Title & Description</text>
    <text x="10" y="60" font-family="Arial, sans-serif" font-size="11" fill="#333">• General Information</text>
    <text x="10" y="80" font-family="Arial, sans-serif" font-size="11" fill="#333">• Default Variables</text>
    <text x="10" y="100" font-family="Arial, sans-serif" font-size="11" fill="#333">• Tasks</text>
    <text x="10" y="120" font-family="Arial, sans-serif" font-size="11" fill="#333">• Role Structure</text>
    <text x="10" y="140" font-family="Arial, sans-serif" font-size="11" fill="#333">• Dependencies</text>
  </g>
  
  <!-- Footer -->
  <text x="400" y="485" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#666">Python-based tool to generate documentation from Ansible role structure</text>
</svg>ible-doc-generator-diagram.svg…]()
