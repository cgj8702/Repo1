from pdf2image.pdf2image import convert_from_path
import os


def convert_pdf_to_png(pdf_path, output_folder):
    """
    Converts a PDF file to a series of PNG images.

    Args:
        pdf_path (str): The path to the PDF file.
        output_folder (str): The folder where the PNG images will be saved.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert the PDF to a list of PIL images
    images = convert_from_path(pdf_path)

    # Save each image as a PNG file
    for i, image in enumerate(images):
        image.save(os.path.join(output_folder, f'page_{i+1}.png'), 'PNG')

    print(
        f"Successfully converted {len(images)} pages from {pdf_path} to PNG images in {output_folder}"
    )


if __name__ == '__main__':
    # Replace 'your_scanned_document.pdf' with the path to your PDF file
    pdf_file = "C:\\Users\\carly\\Desktop\\Carly_Johnson_Notary_Public.pdf"
    # Replace 'output_images' with the desired output folder name
    output_directory = "C:\\Users\\carly\\Desktop\\New folder"

    convert_pdf_to_png(pdf_file, output_directory)
