# Contributing to SkimTerms.ai

Thank you for your interest in contributing to **SkimTerms.ai**! We welcome contributions from developers of all skill levels to help make legal contracts simpler, more transparent, and 100% private for everyone.

---

## 📜 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Message Conventions](#commit-message-conventions)

---

## 🤝 Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## 🛠 How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the [GitHub Issues](https://github.com/krishanth-g/SkimTerms.ai/issues) to ensure the issue hasn't already been reported.

When reporting a bug, please use the **Bug Report** issue template and include:
- A clear and descriptive title.
- Steps to reproduce the problem.
- Expected vs. actual behavior.
- Operating system, Python version, browser, and Ollama model details.
- Console error logs or terminal output.

### Suggesting Enhancements

Feature requests are tracked as [GitHub Issues](https://github.com/krishanth-g/SkimTerms.ai/issues). Use the **Feature Request** issue template to outline:
- The problem your suggestion solves.
- A clear description of the feature or workflow change.
- Any alternative solutions considered.

---

## 🚀 Pull Requests

1. **Fork the Repository**: Create your own copy of the repository.
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/amazing-new-feature
   ```
3. **Make & Test Changes**: Ensure local tests pass and no breaking changes are introduced.
4. **Commit Your Changes**: Follow standard commit message guidelines (e.g., `feat: add PDF batch parsing support`).
5. **Push to Your Fork**:
   ```bash
   git push origin feature/amazing-new-feature
   ```
6. **Submit a Pull Request**: Open a PR against the `main` branch with a thorough description of your changes.

---

## 💻 Development Setup

1. Clone your fork locally.
2. Follow the setup instructions in the [README.md](README.md#installation--setup-guide) to install dependencies.
3. Make sure local Ollama instance is running with `phi3` or `llama3`.

---

## 📐 Coding Standards

- **Python**: Follow PEP 8 style guidelines.
- **Frontend**: Maintain clean HTML5 semantic markup, modular JavaScript, and dark/light mode compatibility.
- **Privacy**: Maintain zero third-party cloud data transmission. All RAG processing MUST run locally.

---

## ✉️ Contact

For major architectural questions or inquiries:
- **Developer**: Krishanth G
- **LinkedIn**: [krishanth-g](https://www.linkedin.com/in/krishanth-g)
