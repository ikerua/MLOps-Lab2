# MLOps-Lab2
[![CICD](https://github.com/ikerua/MLOps-Lab2/actions/workflows/CICD.yml/badge.svg)](https://github.com/ikerua/MLOps-Lab2/actions/workflows/CICD.yml)
## Overview
MLOps-Lab2 is a Python-based machine learning operations project that demonstrates modern MLOps practices with multiple interfaces for model interaction.  The project showcases containerization, CI/CD automation, and flexible deployment options.

## Features
- **FastAPI REST API**: Web service for model predictions with HTML template support
- **Command-Line Interface**:  CLI tool built with Click for easy command-line interactions
- **Containerization**: Docker support for consistent deployment environments
- **Testing & Quality**: Comprehensive testing with pytest and code quality checks with pylint and black
- **CI/CD Pipeline**: Automated testing and deployment workflows via GitHub Actions

## Project Structure
- `api/` - FastAPI web application for serving predictions
- `cli/` - Command-line interface for model interactions
- `mylib/` - Core prediction logic and utilities
- `templates/` - HTML templates for web interface
- `tests/` - Unit and integration tests
- `dockerfile` - Container configuration

## Technology Stack
- Python 3.13+
- FastAPI & Uvicorn for web services
- Click for CLI
- Gradio for interactive interfaces
- Docker for containerization
- pytest for testing
