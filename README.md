# uniscan

An AI-powered site, that helps interpret human test results to into ordinary language

## Features

- 📊 Interpreting biological tests (PDF or Photo)
- 📈 Chat with AI doctor

## Tech Stack

- Backend: Flask + Python
- AI: Google Gemini 2.0

## Setup

1. Clone the repository
    ```bash
    git clone https://github.com/lordwateroff/uniscan
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.1* If you're on a Windows system
    You can run requirements_installer.bat to install dependencies instead of installing it manually
3. Edit `index.html`:
    ```bash
    const API_KEY = 'enter your api key'; // Replace with your actual API key
    ```
4. Edit `app.py`:
    ```python
    genai.configure(api_key="enter your gemini api key"); // Replace with your actual API key
    ```
5. Run the server:
    ```bash
    python app.py
    ```

## Contributing

- Fork this repository.
- Create a feature branch.
- Add or update tests.
- Submit a pull request.

## Contributing Issues

If you encounter any issues or have suggestions for improvements, please check the [Issues](https://github.com/lordwateroff/uniscan/issues) section of the repository. You can contribute by:

- Reporting bugs
- Requesting features
- Discussing potential improvements

## Contacts

If you have any questions, you can contact me at mail:

```bash
kernel@wateroff.xyz
```

## License

📃 [MIT LICENSE](LICENSE)
