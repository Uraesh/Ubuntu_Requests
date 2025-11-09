import requests
import os
from urllib.parse import urlparse
import hashlib
from pathlib import Path


def get_file_hash(filepath):
    """Calculate MD5 hash of a file to detect duplicates."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def is_duplicate(content, directory):
    """Check if image content already exists in directory."""
    new_hash = hashlib.md5(content).hexdigest()

    for existing_file in Path(directory).glob("*"):
        if existing_file.is_file():
            existing_hash = get_file_hash(existing_file)
            if new_hash == existing_hash:
                return True, existing_file.name
    return False, None


def validate_image_headers(response):
    """Check if the response contains valid image data."""
    content_type = response.headers.get('Content-Type', '')

    # Check if content type indicates an image
    if not content_type.startswith('image/'):
        print(f"⚠ Warning: Content-Type is '{content_type}', not an image type")
        return False

    # Check content length
    content_length = response.headers.get('Content-Length')
    if content_length:
        size_mb = int(content_length) / (1024 * 1024)
        if size_mb > 50:  # Warn if file is larger than 50MB
            print(f"⚠ Warning: Large file size ({size_mb:.2f} MB)")

    return True


def fetch_image(url, directory="Fetched_Images", check_duplicates=True):
    """
    Fetch an image from a URL and save it to the specified directory.

    Args:
        url (str): The URL of the image to fetch
        directory (str): Directory to save the image to
        check_duplicates (bool): Whether to check for duplicate images

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Fetch the image with timeout
        print(f"→ Fetching image from: {url}")
        response = requests.get(url, timeout=10, stream=True)

        # Raise exception for bad status codes (4xx, 5xx)
        response.raise_for_status()

        # Validate headers
        if not validate_image_headers(response):
            proceed = input("Continue anyway? (y/n): ").lower()
            if proceed != 'y':
                return False, "Download cancelled by user"

        # Get the actual content
        content = response.content

        # Check for duplicates if enabled
        if check_duplicates:
            is_dup, existing_filename = is_duplicate(content, directory)
            if is_dup:
                return False, f"Duplicate detected: {existing_filename} already exists"

        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # If no filename in URL, generate one based on content type
        if not filename or '.' not in filename:
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            extension = content_type.split('/')[-1].split(';')[0]
            # Use first 8 chars of hash as filename
            hash_prefix = hashlib.md5(content).hexdigest()[:8]
            filename = f"image_{hash_prefix}.{extension}"

        # Construct full filepath
        filepath = os.path.join(directory, filename)

        # Handle filename conflicts
        counter = 1
        base, ext = os.path.splitext(filepath)
        while os.path.exists(filepath):
            filepath = f"{base}_{counter}{ext}"
            counter += 1

        # Save the image in binary mode
        with open(filepath, 'wb') as f:
            f.write(content)

        # Get file size for display
        file_size = len(content) / 1024  # KB

        return True, f"✓ Successfully fetched: {os.path.basename(filepath)} ({file_size:.2f} KB)\n✓ Image saved to {filepath}"

    except requests.exceptions.Timeout:
        return False, "✗ Connection timeout: Server took too long to respond"
    except requests.exceptions.ConnectionError:
        return False, "✗ Connection error: Could not reach the server"
    except requests.exceptions.HTTPError as e:
        return False, f"✗ HTTP error: {e} (Status code: {e.response.status_code})"
    except requests.exceptions.RequestException as e:
        return False, f"✗ Request error: {e}"
    except OSError as e:
        return False, f"✗ File system error: {e}"
    except Exception as e:
        return False, f"✗ Unexpected error: {e}"


def main():
    """Main function to run the Ubuntu Image Fetcher."""
    print("=" * 60)
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("=" * 60)
    print("\n💡 Ubuntu principle: 'I am because we are'\n")

    # Ask if user wants to download multiple images
    multiple = input("Would you like to download multiple images? (y/n): ").lower()

    if multiple == 'y':
        print("\nEnter image URLs (one per line, empty line to finish):")
        urls = []
        while True:
            url = input(f"URL {len(urls) + 1}: ").strip()
            if not url:
                break
            urls.append(url)

        if not urls:
            print("No URLs provided. Exiting.")
            return

        print(f"\n{'=' * 60}")
        print(f"Fetching {len(urls)} images...")
        print(f"{'=' * 60}\n")

        success_count = 0
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}]")
            success, message = fetch_image(url)
            print(message)
            if success:
                success_count += 1

        print(f"\n{'=' * 60}")
        print(f"Summary: {success_count}/{len(urls)} images downloaded successfully")
        print(f"{'=' * 60}")
    else:
        # Single URL mode
        url = input("\nPlease enter the image URL: ").strip()


            print("No URL provided. Exiting.")
            return

        print()
        success, message = fetch_image(url)
        print(message)

        if success:
            print("\n🌍 Connection strengthened. Community enriched.")


if __name__ == "__main__":
    main()