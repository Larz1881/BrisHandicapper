## BrisHandicapper

A Python-based horse racing handicapping tool that leverages Brisnet data to identify top contenders and generate insights optimized for analysis and decision-making.

### Project Overview

This project implements an adapted handicapping process, taking raw Brisnet data files as input and producing structured reports highlighting key race information, contender analysis, and supporting data. The reports are designed to be easily interpreted and used for making informed handicapping decisions.

### Features

*   **Data Ingestion and Processing:** Automatically discovers and processes the latest Brisnet DRF (Data Retrieval Format) files.
*   **Contender Identification:** Filters horses based on performance metrics to isolate top contenders in each race.
*   **Performance Grouping:** Categorizes contenders into groups based on win probability and other factors.
*   **Situational Adjustments:** Refines contender groupings by considering race-specific scenarios and potential biases.
*   **Report Generation:** Creates detailed, JSON-formatted reports summarizing the handicapping analysis.
*   **Extensible Architecture:** Modular design allows for easy addition of new data sources, analytical techniques, and reporting formats.

### Project Structure

```
BrisHandicapper/
├── data/
│   ├── raw/            # Raw, unprocessed Brisnet data files (DRF)
│   └── processed/      # Intermediate and final processed data files
├── logs/               # Log files for pipeline execution
├── reports/            # Generated handicapping reports (JSON format)
├── src/
│   └── bris_handicapper/
│       ├── analysis/   # Modules for core handicapping logic (filtering, grouping, etc.)
│       ├── config/     # Project configuration settings (paths, parameters, etc.)
│       ├── data_processing/ # Scripts for parsing, transforming, and preparing data
│       ├── reporting/  # Module for generating and saving reports
│       ├── handicap.py # Main script to execute the handicapping process
│       └── main.py     # Main script to run the data processing pipeline
├── pyproject.toml      # Project metadata and build configuration
└── README.md           # This file: Project overview, setup, and usage instructions
```

### Setup and Installation

1.  **Prerequisites:**

    *   Python 3.9 or higher

2.  **Create a Virtual Environment:**

    ```bash
    python3 -m venv .venv
    ```

3.  **Activate the Environment:**

    ```bash
    # On macOS/Linux:
    source .venv/bin/activate

    # On Windows (PowerShell):
    .venv\Scripts\activate
    ```

4.  **Install Project Dependencies:**

    ```bash
    pip install -e .
    ```

### Usage

The project provides two main entry points:

1.  **Data Processing Pipeline:**

    This pipeline processes raw Brisnet data and prepares it for handicapping.  The core logic for parsing and transforming data needs to be implemented in the modules within `src/bris_handicapper/data_processing/`.

    ```bash
    bris_handicapper_main
    ```

2.  **Handicapping Process:**

    This process loads the processed data and performs the handicapping analysis, generating reports for each race.

    ```bash
    bris_handicapper_handicap
    ```

### Configuration

Project settings, including file paths and handicapping parameters, can be configured in the `src/bris_handicapper/config/config.py` file.

### Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bug fixes, feature requests, or general feedback.

### License

This project is licensed under the MIT License.