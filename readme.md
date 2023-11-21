# DOCUMENT MANAGEMENT SYSTEM

"Introducing our cutting-edge Document Management System (DMS), a robust solution designed to elevate your document handling experience. Seamlessly integrating OCR (Optical Character Recognition), our DMS ensures lightning-fast search and retrieval capabilities, transforming paper documents into editable and searchable digital files. Experience unparalleled collaboration with real-time co-authoring, comments, and task assignments. With advanced security features, your sensitive data is safeguarded through encryption, access controls, and audit trails. Plus, enjoy peace of mind with version control, allowing you to track, manage, and restore document versions effortlessly. Elevate your document management with efficiency, security, and collaboration at your fingertips."

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [License](#license)

## About

A Document Management System (DMS) is a software solution that helps organizations store, organize, manage, and track electronic documents and digital content. The primary goal of a DMS is to facilitate efficient document management, streamline workflows, and ensure that information is easily accessible and secure.

## Features

- Collaboration
- Version Control
- OCR
- Advanced Search Capabilities

## Getting Started

Since this project is web-based and running in Django, we'll need some external libraries for all the features to run this program.

### Prerequisites

- First, make sure to create and activate a virtual environment:

```bash
python -m venv venv_name  # Create a virtual environment

source venv_name/bin/activate  # Activate the virtual environment (for macOS/Linux)
      
venv_name\Scripts\activate  # Activate the virtual environment (for Windows) 
```

1. Install Proppler

    - For Windows

    ```bash 
    https://github.com/oschwartz10612/poppler-windows/releases/tag/v23.11.0-0

    For Windows, Extract the file in C:/ renaming the folder to 'Proppler'
    ```

    - For Linux

     ```bash 
    https://www.linuxfromscratch.org/blfs/view/svn/general/poppler.html

    https://gist.github.com/Dayjo/618794d4ff37bb82ddfb02c63b450a81

    For Linux, You will have to change the 'Proppler' Location in the project file '../DMS/System/utils.py' in 'extract_text_from_pdf' function.

    ```

2. Download Tesseract.

      ```bash
      https://github.com/tesseract-ocr/tesseract

      For Windows, Extract the file in C:/Program Files/ renaming the folder to 'Tesseract-OCR'

      For Linux, You will have to change the 'Tesseract' Location in the project file '../DMS/System/utils.py' in 'extract_text_from_pdf' function.
      ```

3. Install requirements.

      ```bash 
    pip install -r Requirements.txt
    ```

### Installation

```bash
# Clone the repository
git clone https://github.com/asimbcn/AIP-DMS

# Run server
refer to the -[Prerequisites](#prerequisites) 'Virtual Environment'

# Change into the project directory
cd your-project

# Install dependencies
refer to the -[Prerequisites](#prerequisites) '3. Install requirements'

#run project
For Windows: py manage.py runserver
For Linux: python3 manage.py runserver.

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.