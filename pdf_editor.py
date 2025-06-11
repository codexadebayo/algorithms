import fitz
from typing import Tuple, Optional
import os
from datetime import datetime

class EditPDF:
    def __init__(self, input_path: str = None):
        """
        Initialize the PDF editor.
        
        Args:
            input_path (str, optional): Path to the input PDF file. If None, will be set later.
        """
        self.input_path = input_path
        self.pdf_document = None
        self.current_page = None
        self.modified_pages = set()

    def __enter__(self):
        """Context manager entry point"""
        self.open_document()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        self.close_document()

    def set_input_path(self, input_path: str) -> None:
        """
        Set the input PDF path.
        
        Args:
            input_path (str): Path to the input PDF file
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"PDF file not found: {input_path}")
        self.input_path = input_path

    def generate_output_path(self) -> str:
        """
        Generate a unique output path for the modified PDF.
        
        Returns:

            str: Path for the output PDF file
        """
        if not self.input_path:
            raise ValueError("Input path not set")
        
        directory = os.path.dirname(self.input_path)
        filename = os.path.basename(self.input_path)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(directory, f"{name}_modified_{timestamp}{ext}")

    def open_document(self) -> None:
        """Open the PDF document"""
        try:
            self.pdf_document = fitz.open(self.input_path)
        except Exception as e:
            raise Exception(f"Failed to open PDF document: {str(e)}")

    def close_document(self) -> None:
        """Close the PDF document"""
        if self.pdf_document:
            self.pdf_document.close()
            self.pdf_document = None

    def get_page_count(self) -> int:
        """
        Get the total number of pages in the PDF document.
        
        Returns:
            int: Total number of pages in the document
            
        Raises:
            Exception: If PDF document is not opened
        """
        if not self.pdf_document:
            raise Exception("PDF document not opened")
        return self.pdf_document.page_count

    def validate_page_number(self, page_number: int) -> bool:
        """
        Validate if the page number is within valid range.
        
        Args:
            page_number (int): Page number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not self.pdf_document:
            raise Exception("PDF document not opened")
        return 1 <= page_number <= self.pdf_document.page_count

    def load_page(self, page_number: int) -> None:
        """
        Load a specific page from the PDF.
        
        Args:
            page_number (int): Page number to load
        """
        if not self.validate_page_number(page_number):
            raise ValueError(f"Invalid page number: {page_number}")
        self.current_page = self.pdf_document.load_page(page_number - 1)

    def find_text_location(self, target_text: str) -> Optional[Tuple[float, float, float, float]]:
        """
        Find the location of specific text on the current page.
        
        Args:
            target_text (str): Text to search for
            
        Returns:
            Optional[Tuple[float, float, float, float]]: Bounding box coordinates if found, None otherwise
        """
        if not self.current_page:
            raise Exception("No page loaded")

        text_instances = self.current_page.get_text("dict")
        for text in text_instances:
            if text["type"] == "text" and text["text"].strip() == target_text.strip():
                return text["bbox"]
        return None

    def find_text_in_document(self, target_text: str) -> list:
        """
        Find all occurrences of text across all pages in the document.
        
        Args:
            target_text (str): Text to search for
            
        Returns:
            list: List of tuples containing (page_number, bbox) for each occurrence
        """
        if not self.pdf_document:
            raise Exception("PDF document not opened")
            
        occurrences = []
        for page_num in range(self.pdf_document.page_count):
            page = self.pdf_document.load_page(page_num)
            text_instances = page.get_text("dict")
            for text in text_instances:
                if text["type"] == "text" and target_text.strip() in text["text"].strip():
                    occurrences.append((page_num + 1, text["bbox"]))
        return occurrences

    def replace_text(self, old_text: str, new_text: str) -> bool:
        """
        Replace all occurrences of text in the document.
        
        Args:
            old_text (str): Text to be replaced
            new_text (str): New text to insert
            
        Returns:
            bool: True if any replacements were made
        """
        if not self.pdf_document:
            raise Exception("PDF document not opened")

        occurrences = self.find_text_in_document(old_text)
        if not occurrences:
            return False

        for page_num, bbox in occurrences:
            page = self.pdf_document.load_page(page_num - 1)
            # Draw white rectangle to cover old text
            page.draw_rect(bbox, fill=(1, 1, 1), overlay=True)
            
            # Insert new text
            page.insert_textbox(
                bbox,
                new_text,
                fontname="Arial",
                fontsize=12,
                align=fitz.TEXT_ALIGN_LEFT,
                color=(0, 0, 0)
            )
            self.modified_pages.add(page_num)
        
        return True

    def process_edit(self, old_text: str, new_text: str) -> str:
        """
        Process the complete edit workflow.
        
        Args:
            old_text (str): Text to be replaced
            new_text (str): New text to insert
            
        Returns:
            str: Path to the saved modified PDF
        """
        try:
            self.open_document()
            if self.replace_text(old_text, new_text):
                output_path = self.generate_output_path()
                self.save_document(output_path)
                return output_path
            return None
        except Exception as e:
            print(f"Error processing PDF edit: {str(e)}")
            return None
        finally:
            self.close_document()

    def save_document(self, output_path: str) -> None:
        """
        Save the modified PDF document.
        
        Args:
            output_path (str): Path where to save the modified PDF
        """
        if not self.pdf_document:
            raise Exception("PDF document not opened")
        self.pdf_document.save(output_path)

