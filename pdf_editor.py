import fitz
from typing import Tuple, Optional
import os
from datetime import datetime



# a good attempt but needs more work
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
        self.output_path = None

    def __enter__(self):
        """Context manager entry point"""
        if not self.input_path:
            raise ValueError("Input path must be set before using context manager")
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
        if not self.input_path:
            raise ValueError("Input path not set")
        try:
            self.pdf_document = fitz.open(self.input_path)
        except Exception as e:
            raise Exception(f"Failed to open PDF document: {str(e)}")

    def close_document(self) -> None:
        """Close the PDF document"""
        if self.pdf_document:
            self.pdf_document.close()
            self.pdf_document = None
            self.current_page = None
            self.modified_pages.clear()

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

    def find_text_in_document(self, old_text: str, target_page: int = None) -> list:
        """
        Find all occurrences of text across all pages in the document.
        
        Args:
            old_text (str): Text to search for
            target_page (int, optional): Specific page number to search in. If None, searches all pages.
            
        Returns:
            list: List of tuples containing (page_number, bbox) for each occurrence
        """
        if not self.pdf_document:
            raise Exception("PDF document not opened")
            
        if not old_text or not old_text.strip():
            raise ValueError("Search text cannot be empty")
            
        occurrences = []
        # If target_page is specified, only search that page
        pages_to_search = [target_page - 1] if target_page else range(self.pdf_document.page_count)
        
        print(f"Searching for text: '{old_text}'")
        print(f"Pages to search: {[p+1 for p in pages_to_search]}")
        
        for page_num in pages_to_search:
            if target_page and not self.validate_page_number(target_page):
                raise ValueError(f"Invalid target page number: {target_page}")
                
            page = self.pdf_document.load_page(page_num)
            text_instances = page.get_text("dict")
            
            for block in text_instances.get("blocks", []):
                if block.get("type") == 0:  # Text block
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            span_text = span.get("text", "").strip()
                            if old_text.strip() in span_text:
                                print(f"Found match on page {page_num + 1}: '{span_text}'")
                                occurrences.append((page_num + 1, span["bbox"]))
        
        print(f"Total occurrences found: {len(occurrences)}")
        return occurrences

    def replace_text(self, old_text: str, new_text: str, target_page: int = None) -> bool:
        """
        Replace all occurrences of text in the document.
        
        Args:
            old_text (str): Text to be replaced
            new_text (str): New text to insert
            target_page (int, optional): Specific page number to make changes in. If None, changes all pages.
            
        Returns:
            bool: True if any replacements were made
        """
        if not self.pdf_document:
            raise Exception("PDF document not opened")

        if not new_text or not new_text.strip():
            raise ValueError("Replacement text cannot be empty")

        occurrences = self.find_text_in_document(old_text, target_page)
        if not occurrences:
            print("No text occurrences found to replace")
            return False

        print(f"Replacing {len(occurrences)} occurrences of text")
        for page_num, bbox in occurrences:
            page = self.pdf_document.load_page(page_num - 1)
            
            # Calculate text dimensions for proper positioning
            text_width = fitz.get_text_length(new_text, fontsize=12)
            text_height = 12  # Approximate height for fontsize 12
            
            # Create a larger white background to ensure full coverage
            padding = 4
            extra_width = max(20, text_width * 0.2)  # 20% extra width or minimum 20 points
            
            bg_rect = fitz.Rect(
                bbox[0] - padding,
                bbox[1] - padding,
                bbox[0] + text_width + extra_width + padding,
                bbox[1] + text_height + padding
            )
            
            # Draw white rectangle without border
            page.draw_rect(bg_rect, fill=(1, 1, 1), color=None, overlay=True)
            
            # Insert new text at the original position
            page.insert_text(
                (bbox[0], bbox[1] + text_height),  # Position text at bottom of bbox
                new_text,
                fontsize=12,
                color=(0, 0, 0)
            )
            self.modified_pages.add(page_num)
            print(f"Replaced text on page {page_num}")
        
        return True

    def process_edit(self, old_text: str, new_text: str, target_page: int = None) -> Optional[str]:
        """
        Process the complete edit workflow.
        
        Args:
            old_text (str): Text to be replaced
            new_text (str): New text to insert
            target_page (int, optional): Specific page number to make changes in. If None, changes all pages.
            
        Returns:
            Optional[str]: Path to the saved modified PDF if successful, None otherwise
        """
        if not self.input_path:
            raise ValueError("Input path not set. Use set_input_path() first.")

        try:
            print(f"Processing edit: '{old_text}' -> '{new_text}'")
            if target_page:
                print(f"Target page: {target_page}")
            
            self.open_document()
            if self.replace_text(old_text, new_text, target_page):
                self.output_path = self.generate_output_path()
                print(f"Saving modified PDF to: {self.output_path}")
                self.save_document(self.output_path)
                return self.output_path
            print("No changes were made to the document")
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
        
        try:
            self.pdf_document.save(output_path)
            print(f"Successfully saved PDF to: {output_path}")
        except Exception as e:
            raise Exception(f"Failed to save PDF: {str(e)}")

