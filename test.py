from pdf_editor import EditPDF


old_text = "25"
page_num = 1
pdf_path = "/home/ghost/Downloads/AdebayoDavidBamigboyeCV.pdf"
new_text = "26"


edit_pdf = EditPDF(pdf_path=pdf_path)


def test_edit_pdf(edit_pdf, old_text, new_text, page_num):
  try: 
    pdf = edit_pdf.__enter__()
    return pdf
  except Exception as e:
    print(f"An error occurred: {e}")
  
  try:
    text_area = edit_pdf.get_text_area(pdf, old_text, page_num)
    # the get_text area takes a pdf, the page number and then finds the page, then iterates through the text area to find the old_text. it returns the exact dimensions of the text_area, the page number and the text within that area. 
    pdf= edit_pdf.add_white_background(pdf, text_area)
    # add a white background over the dimensions of the text area, find the exact page number and add.
    edited_pdf =  edit_pdf.add_new_text(pdf, new_text)
    # add a new text over what we have stored in the pdf dict.

    save_pdf = edit_pdf.save_pdf(edited_pdf)
    edit_pdf.download_pdf(save_pdf)
    return
  except Exception as e:
    print(f"An error occurred while saving or downloading the PDF: {e}")
    return None  
    # when we edit a file, we give it a signature name, and a path to save in the downloads of the user. then save in that location 