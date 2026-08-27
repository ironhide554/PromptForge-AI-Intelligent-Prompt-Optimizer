from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "PromptForge AI - Optimized Prompt", align="C", ln=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(prompt_text: str) -> bytes:
    """Generates a PDF byte string from the prompt text."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)
    
    # Using multi_cell for wrapping text
    # Encode and decode to handle special characters slightly better
    safe_text = prompt_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, txt=safe_text)
    
    # Return as bytes
    return pdf.output(dest='S')
