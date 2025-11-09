# Ubuntu Image Fetcher

> *"I am because we are"* - Ubuntu Philosophy

A Python-based image fetcher that embodies the Ubuntu philosophy of community and sharing. This tool respectfully connects to the global internet community, fetches shared image resources, and organizes them for appreciation.

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Examples](#examples)
- [Security Features](#security-features)

## ✨ Features

### Core Functionality
- 🖼️ Download images from any URL
- 📁 Automatic directory creation and management
- 🔄 Support for single or bulk image downloads
- 💾 Smart filename extraction and generation
- ⚠️ Comprehensive error handling

### Advanced Features
- 🔍 **Duplicate Detection**: Uses MD5 hashing to prevent downloading identical images
- 🛡️ **Security Validation**: Checks Content-Type and file size before downloading
- 📊 **Progress Tracking**: Real-time feedback during bulk downloads
- 🔐 **Safe Downloads**: Timeout protection and content validation
- 📈 **File Management**: Automatic filename conflict resolution

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Ubuntu_Requests.git
cd Ubuntu_Requests
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests
```

## 💻 Usage

### Basic Usage
Run the script:
```bash
python ubuntu_image_fetcher.py
```

### Single Image Download
```
Welcome to the Ubuntu Image Fetcher
A tool for mindfully collecting images from the web
============================================================

💡 Ubuntu principle: 'I am because we are'

Would you like to download multiple images? (y/n): n

Please enter the image URL: https://picsum.photos/800/600

→ Fetching image from: https://picsum.photos/800/600
✓ Successfully fetched: image_a3f2b8c1.jpeg (127.45 KB)
✓ Image saved to Fetched_Images/image_a3f2b8c1.jpeg

🌍 Connection strengthened. Community enriched.
```

### Multiple Images Download
```
Would you like to download multiple images? (y/n): y

Enter image URLs (one per line, empty line to finish):
URL 1: https://picsum.photos/800/600
URL 2: https://picsum.photos/1024/768
URL 3: 

============================================================
Fetching 2 images...
============================================================

[1/2]
→ Fetching image from: https://picsum.photos/800/600
✓ Successfully fetched: image_a3f2b8c1.jpeg (127.45 KB)
✓ Image saved to Fetched_Images/image_a3f2b8c1.jpeg

[2/2]
→ Fetching image from: https://picsum.photos/1024/768
✓ Successfully fetched: image_f7e9d2a4.jpeg (215.32 KB)
✓ Image saved to Fetched_Images/image_f7e9d2a4.jpeg

============================================================
Summary: 2/2 images downloaded successfully
============================================================
```

## 📸 Examples

### Test URLs
You can test the application with these public image APIs:

```python
# Random images from Lorem Picsum
https://picsum.photos/800/600
https://picsum.photos/1920/1080

# Test images from httpbin
https://httpbin.org/image/jpeg
https://httpbin.org/image/png
https://httpbin.org/image/webp
```

### Error Handling Examples

**Invalid URL:**
```
✗ Connection error: Could not reach the server
```

**Non-image content:**
```
⚠ Warning: Content-Type is 'text/html', not an image type
Continue anyway? (y/n): n
Download cancelled by user
```

**Duplicate image:**
```
✗ Duplicate detected: image_a3f2b8c1.jpeg already exists
```

## 🔒 Security Features

### Built-in Protections
1. **Timeout Protection**: 10-second timeout prevents hanging connections
2. **Content Type Validation**: Verifies response is actually an image
3. **File Size Warnings**: Alerts for files larger than 50MB
4. **No Code Execution**: Downloaded content is never executed
5. **Stream Mode**: Large files don't overwhelm memory

### Best Practices Implemented
- ✅ Input validation
- ✅ Exception handling for all network operations
- ✅ User confirmation for suspicious content
- ✅ Secure file operations
- ✅ No arbitrary code execution

### Warning Signs to Watch For
- Content-Type mismatch (not an image)
- Unusually large file sizes
- Connection timeouts
- HTTP error codes (404, 403, 500, etc.)

## 📁 Project Structure

```
Ubuntu_Requests/
├── main.py    # Main application script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                 # Git ignore rules
└── Fetched_Images/            # Downloaded images directory (auto-created)
    └── (downloaded images)
```

## 🛠️ Technical Details

### Function Breakdown

#### `fetch_image(url, directory, check_duplicates)`
Main function for downloading images.
- Validates HTTP headers
- Checks for duplicates
- Handles filename conflicts
- Returns success status and message

#### `is_duplicate(content, directory)`
Compares MD5 hash of new content against existing files.
- Returns tuple: (is_duplicate: bool, existing_filename: str)

#### `validate_image_headers(response)`
Checks HTTP response headers for safety.
- Validates Content-Type
- Warns about large files
- Returns boolean indicating validity

#### `get_file_hash(filepath)`
Calculates MD5 hash for duplicate detection.
- Reads file in chunks for memory efficiency