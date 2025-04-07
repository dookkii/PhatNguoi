# Tra cứu phạt nguội // PhatNguoiAPI
A tool for looking up and tracking delayed fines.

## See it in action
Check it out live at [phatnguoi.tunaa.io.vn](https://phatnguoi.tunaa.io.vn)!

## Features
The system offers:
- **Search Delayed Fines**: Quickly find fines using license plate numbers.
- **Track Updates** (*coming soon*): Get notified about the status of your fines.
- **User-Friendly Interface**: Designed for simplicity and ease of use.
- **Mobile Compatibility**: Fully responsive for a seamless experience on any device.
- **Secure Access**: Your data is always protected. (maybe, idk)
- **API Integration**: Provides API support for developers.

## Used Packages
- **requests**, **ssl**, **beautifulsoup4**: Handle the post and scrape data process.
- **flask**, **flask-restful**: Website interface, webserver and APIs.
- **pillow**: Read image data (for Captcha thingy).
- **pyterserract**: Image-to-text services (for solving Captcha). *This is our default OCR engine, you could also implement a new Image-to-text function with your favorite OCR engine. For more information, read the instructions below!*

## Installation Instructions
1. Clone this repository.
```bash
git clone https://github.com/dookkii/PhatNguoi.git
cd PhatNguoi
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
  - On **Windows**:
    ```bash
    .venv\Scripts\activate
    ```
  - On **Linux**:
    ```bash
    . .venv/bin/activate
    ```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Install **pyteserract**: (If you are not using the default, implemented **pyteserract** OCR engine, then you should follow that OCR installation and read 6 to implement the I2T function)

- Installing via pip:
  ```bash
  pip install pytesseract
  ```
  - Check the [pytesseract](https://pypi.python.org/pypi/pytesseract) package page for more information.

- Install [Google Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (additional info how to install the engine on Linux, Mac OSX and Windows). You must be able to invoke the tesseract command as tesseract. If this isn’t the case, for example because tesseract isn’t in your PATH, you will have to change the “tesseract_cmd” variable `pytesseract.pytesseract.tesseract_cmd`.
  - Under Debian/Ubuntu you can use the package **tesseract-ocr**.
  - For Mac OS users. please install homebrew package **tesseract**.

6. Implement Image-to-text function with custom OCR engine:
- Go to `handlers/image_to_text.py`, create a new function with any name, input is a PIL-image, and it returns a string:
  ```py
  def image_to_string_easy_ocr(image):
    ...
  ```
- Then change the `image_to_string` variable into your function (your **\*function**, which is without the brackets):
  ```py
  image_to_string = image_to_string_easy_ocr
  ```

7. Change the settings in ```settings.py``` to match your needs (these settings will only be used in development environment).

## Deployment Instructions
- To deploy the app, you can use `gunicorn` or any WSGI servers you want to. Follow their steps and integrate it with `nginx` to make the server online.
- We have already provided the `wsgi.py` file, you can take advantage of it.
- This section will be extended and more details in the future for easier navigation.