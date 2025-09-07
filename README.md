# Albumy

*Capture and share every wonderful moment.*

> Example application for *[Python Web Development with Flask](https://helloflask.com/en/book/1)* (《[Flask Web 开发实战](https://helloflask.com/book/1)》).

Demo: http://albumy.helloflask.com

![Screenshot](https://helloflask.com/screenshots/albumy.png)

## Installation

clone:
```
$ git clone https://github.com/greyli/albumy.git
$ cd albumy
```
create & activate virtual env then install dependency:

with venv/virtualenv + pip:
```
$ python -m venv env  # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ pip install -r requirements.txt
```
or with Pipenv:
```
$ pipenv install --dev
$ pipenv shell
```

## ML Features Setup

This version includes ML-powered features using Google Cloud Vision API:
- **Auto-generated alt text** for accessibility
- **Object detection** for enhanced search

### Setting up Google Cloud Vision API:
1. Create a Google Cloud project and enable the Vision API
2. **Enable billing** for your project (required by Google):
   - Visit the billing page for your project
   - Add a payment method (new accounts get $300 free credits)
   - Vision API pricing: First 1,000 units/month are free
3. Create a service account and download the credentials JSON file
4. Save the credentials file as `google-credentials.json` in the project root

Note: The credentials file is already in .gitignore for security.
Without billing enabled, the app will still work but ML features will show placeholder text.

### Updating existing photos with ML features:
If you have existing photos without ML features, run:
```
$ python generate_thumbnails.py
```

generate fake data then run:
```
$ flask forge
$ flask run
* Running on http://127.0.0.1:5000/
```
Test account:
* email: `admin@helloflask.com`
* password: `helloflask`

## ML Features Usage

### Alternative Text
- Upload any image and the system automatically generates descriptive alt text
- Alt text is visible in HTML source and used by screen readers
- Improves accessibility and SEO

### Object-based Search
- Search for images by objects detected in them
- Example: Search for "dog", "car", "tree" to find relevant images
- Works alongside traditional description-based search

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
