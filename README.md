# Photo-Slider

## Installation
To install the Photo-Slider project, you need to have [PDM](https://pdm.fming.dev/) installed on your system. PDM is a modern Python package and dependency manager.

### Prerequisites

- Python 3.12 is required as specified in the `pyproject.toml`.
- Ensure you have PDM installed. If not, you can install it via pip:

  ```bash
  curl -sSL https://pdm-project.org/install-pdm.py | python3 -
  ```

### Installation Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd Photo-Slider
   ```

2. Install the dependencies using PDM:

   ```bash
   pdm install
   ```

This will install all the dependencies specified in the `pyproject.toml` and `pdm.lock` files.


## Design
This will be built of 2 components:
1. WebApp - is in charge of displaying the photos in a photo slide format
2. Backend - The backend is in charge of retrieving the photos from google drive and supplying them to the webap

Features:
1. 
