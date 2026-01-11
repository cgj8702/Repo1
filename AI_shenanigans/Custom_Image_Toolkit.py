import os
import io
from PIL import Image

# ==============================================================================
#                               USER CONFIGURATION
#              (Set value to None if you don't want to use it)
# ==============================================================================

# 1. FOLDERS
INPUT_FOLDER = "."  # Where your files are
OUTPUT_FOLDER = "./processed"  # Where they go

# 2. CONVERT FORMAT
# Options: "PNG", "JPEG", or None (Keep original)
TARGET_FORMAT = "PNG"

# 3. RESIZE DIMENSIONS (Pixels)
# If you set only ONE, the other will scale automatically to keep aspect ratio.
# If you set BOTH, it will force the image to that exact size (might squish).
# Set both to None to skip resizing.
TARGET_WIDTH = 1200
TARGET_HEIGHT = None

# 4. MAX FILE SIZE (Megabytes)
# Set to None to disable compression limit.
# Example: 5.0 (for 5MB), 0.5 (for 500KB)
MAX_SIZE_MB = 2.0

# ==============================================================================
#                  END CONFIGURATION - SCRIPT LOGIC BELOW
# ==============================================================================


def process_images():
    # Create output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    print(f"--- STARTING JOB ---")
    print(f"Format: {TARGET_FORMAT if TARGET_FORMAT else 'Original'}")
    print(
        f"Resize: W={TARGET_WIDTH if TARGET_WIDTH else 'Auto'} / H={TARGET_HEIGHT if TARGET_HEIGHT else 'Auto'}"
    )
    print(f"Max Size: {MAX_SIZE_MB if MAX_SIZE_MB else 'Unlimited'} MB\n")

    files = [
        f
        for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]

    if not files:
        print("No images found in input folder.")
        return

    for filename in files:
        filepath = os.path.join(INPUT_FOLDER, filename)

        try:
            with Image.open(filepath) as img:
                # --- LOGIC 1: FORMAT ---
                # Determine output extension and format
                original_ext = os.path.splitext(filename)[1].lower()

                if TARGET_FORMAT:
                    save_format = TARGET_FORMAT.upper()
                    # Fix common naming mismatch
                    if save_format == "JPG":
                        save_format = "JPEG"
                    new_ext = f".{save_format.lower().replace('jpeg', 'jpg')}"
                else:
                    # Keep original format
                    save_format = "JPEG" if original_ext in [".jpg", ".jpeg"] else "PNG"
                    new_ext = original_ext

                output_filename = f"{os.path.splitext(filename)[0]}{new_ext}"
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)

                # Ensure RGB mode if saving as JPEG (removes transparency to avoid errors)
                if save_format == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # --- LOGIC 2: RESIZE ---
                # Case A: Width AND Height set -> Force exact dimensions
                if TARGET_WIDTH and TARGET_HEIGHT:
                    img = img.resize(
                        (TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS
                    )

                # Case B: Width Only -> Calc Height
                elif TARGET_WIDTH and not TARGET_HEIGHT:
                    aspect = img.height / img.width
                    new_height = int(TARGET_WIDTH * aspect)
                    img = img.resize(
                        (TARGET_WIDTH, new_height), Image.Resampling.LANCZOS
                    )

                # Case C: Height Only -> Calc Width
                elif TARGET_HEIGHT and not TARGET_WIDTH:
                    aspect = img.width / img.height
                    new_width = int(TARGET_HEIGHT * aspect)
                    img = img.resize(
                        (new_width, TARGET_HEIGHT), Image.Resampling.LANCZOS
                    )

                # --- LOGIC 3: SAVE & COMPRESS ---
                # If a size limit is set, run the compression loop
                if MAX_SIZE_MB:
                    target_bytes = MAX_SIZE_MB * 1024 * 1024
                    quality = 95

                    while True:
                        buffer = io.BytesIO()

                        # PNGs use 'quantize' to reduce size, JPEGs use 'quality'
                        if save_format == "PNG":
                            if (
                                quality < 80
                            ):  # Start reducing colors if simple optimization fails
                                img = img.quantize(colors=256)
                            img.save(buffer, format=save_format, optimize=True)
                        else:
                            img.save(
                                buffer,
                                format=save_format,
                                quality=quality,
                                optimize=True,
                            )

                        size = buffer.tell()

                        if size <= target_bytes or quality < 10:
                            with open(output_path, "wb") as f:
                                f.write(buffer.getvalue())
                            print(f"Processed {filename} -> {size/1024/1024:.2f} MB")
                            break

                        # Reduce quality for next attempt
                        quality -= 5

                # If NO size limit, just save normally
                else:
                    img.save(output_path, format=save_format, quality=95)
                    print(f"Processed {filename}")

        except Exception as e:
            print(f"Error on {filename}: {e}")

    print("\nAll Done!")


if __name__ == "__main__":
    process_images()
