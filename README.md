# Finger Scan Web Application 👋

![Header Image](./7d1p.gif)

Finger Scan is a web application developed using Django backend, centered around image processing. This project originated as a freelance endeavor and addresses the intriguing domain of fingerprint analysis. The primary objective of this application is to capture raw fingerprint images from a mobile camera, process them, and make them visually interpretable even to the human eye. The processed images are then optimized for further analysis by DMIT (Dermatoglyphics Multiple Intelligence Test) professionals. 🕵️‍♂️

## Table of Contents

- [Introduction](#finger-scan-web-application)
- [Features](#features)
- [Core Functionality](#core-functionality)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features 🌟

- Capture raw fingerprint images using a mobile camera 📷.
- Transmit captured images to the backend for processing 🚀.
- Provide admin functionality to download processed images as a zip archive ⬇️.
- Enable analysis and prediction by DMIT professionals 🔍.
- Optimize images to make fingerprints visually discernible to the human eye 👁️.

## Core Functionality 🔑

The Finger Scan application is built around the following core process:

1. **Image Capture:** The application allows users to capture raw fingerprint images using a mobile camera 📸.
2. **Backend Processing:** Captured images are sent to the backend for further processing 🖥️.
3. **Human-Visible Processing:** The application employs image processing techniques to make the fingerprints visible to the human eye 👁️.
4. **Admin Functionality:** Admin users have the ability to download processed images in a zip archive 📥.
5. **DMIT Analysis:** Processed images are suitable for analysis by Dermatoglyphics experts 🧪.
6. **Optimization:** Images are optimized to enhance visibility of fingerprints, aiding analysis 🔍.

## Technologies Used 🛠️

The project utilizes the following technologies:

- **Backend Framework:** Django 🐍
- **Image Processing:** OpenCv, matplotlib 🖼️
- **Database:** SQLite (for development), PostgreSQL (for production) 🗄️
- **Frontend:** HTML, CSS, JavaScript (minimal) 🌐
- **Version Control:** Git, GitHub 📜

## Getting Started 🚀

To run the Finger Scan web application locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/finger-scan.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure database settings in `settings.py`.
4. Perform database migrations: `python manage.py migrate`
5. Launch the development server: `python manage.py runserver`
6. Access the application in your browser at `http://127.0.0.1:8000/`

## Usage 🧑‍💻

1. Capture fingerprint images using the mobile camera 📸.
2. Upload captured images to the Finger Scan application 🚀.
3. Admin users can download processed images for analysis ⬇️.
4. DMIT professionals can analyze and predict based on the processed images 🔍.

## Contributing 🤝

Contributions are welcome! If you'd like to contribute to this project, feel free to submit pull requests or open issues in the repository.

## License 📝

This project is licensed under the [MIT License](LICENSE).

---

Thank you for your interest in the Finger Scan project. If you have any questions or suggestions, please feel free to contact us. 📬
