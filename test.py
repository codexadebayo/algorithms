from pdf_editor import EditPDF


old_text = "My commitment"
pdf_path = "/home/ghost/Downloads/AdebayoDavidBamigboyeCV.pdf"
new_text = "I love"


editor = EditPDF()
editor.set_input_path(pdf_path)
result = editor.process_edit(old_text, new_text, target_page=1)
if result:
    print(f"Success! Modified PDF saved to: {result}")