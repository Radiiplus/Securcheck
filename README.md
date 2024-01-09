
# Securcheck Documentation

Securcheck is a versatile Python script designed for web and endpoint security checking.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Securcheck is a security assessment script designed to check the security of web servers and endpoints. It can perform various checks, including web page analysis, endpoint testing, and more.

## Features

- Web Checker: Checks web pages for status codes, headers, and sensitive keywords.
- Endpoint Checker: Concurrently tests multiple endpoints for status codes and headers.
- Tampering: Tamper input fields in web forms to test for security vulnerabilities.

## Installation

1. Clone the repository:

   ```
  git clone https://github.com/Radiiplus/Securcheck.git
  cd Securcheck
  ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line:

```
python start.py <base_url> --web-output <web_output_file> --endpoint-output <endpoint_output_file> --concurrency  <concurrency_level> --timeout <timeout_seconds>
```

Replace `<base_url>`, `<web_output_file>`, `<endpoint_output_file>`, `<concurrency_level>`, and `<timeout_seconds>` with your specific values.

## Configuration

- **Web Checker Configuration:**
  - Customize headers in the `files/headers.txt` file.
  - Specify tampered inputs in the `files/inputs.txt` file.
  - Set paths to check in the `files/sp.txt` file.
  - Define sensitive keywords in the `files/keywords.txt` file.

- **Endpoint Checker Configuration:**
  - Add endpoints to check in the `files/Endpoints.txt` file.

## Troubleshooting

- If you encounter issues, please check the logs in the `main_script.log` file for detailed error messages.

## Contributing

Contributions are welcome! Feel free to open issues, propose new features, or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
```

Feel free to use and modify it as needed!