# CloudRec

Welcome to CloudRec, the innovative open-source solution designed to automatically capture and convert cloud infrastructure configurations created via GUI into Infrastructure as Code (IaC) formats. This tool facilitates the documentation, management, and replication of cloud infrastructures, enhancing operational consistency, traceability, and efficiency.

## Key Features

- Automatic Configuration Capture: CloudRec extracts cloud resource configurations directly from cloud provider APIs, turning GUI actions into reusable code.
- IaC Generation: Converts captured configurations into popular IaC formats, compatible with tools such as IaC, ready for version control and reuse.
- Open Source Flexibility: CloudRec is fully open source, allowing for extensive customization and enhancements based on user needs and community contributions.
- Easy Integration: Designed to seamlessly integrate with existing CI/CD workflows, CloudRec supports automated and scalable infrastructure deployments.

## Getting Started

Follow these instructions to get CloudRec up and running in your local environment.

### Prerequisites

- Python 3.8+
- API access to your cloud provider (AWS, Google Cloud, Azure)

### Installation

Clone the CloudRec repository:

```bash
git clone https://github.com/org-cloudrec/cloudrec.git
cd cloudrec
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Configuration

Edit the config.yaml file to include your API credentials and set the necessary parameters for your cloud environment.

Usage

Run the main script to begin capturing cloud configurations:

```bash
python cloudrec.py
```

Contributing

We welcome contributions from the community! If you have suggestions for improvements or new features, please fork the repository and submit a pull request, or open an issue with the tags "enhancement" or "bug".

License

CloudRec is released under the MIT License. See the LICENSE file for more details.

Support

If you encounter any issues or have questions about using CloudRec, please open an issue on GitHub or contact us at support@cloudrec.io.

Authors

- Thales Gibbon - Founder and Lead Developer - [Thales Gibbon](https://github.com/thalesgibbon)

We are grateful to all the contributors who have participated in this project. Thank you for your contributions!
