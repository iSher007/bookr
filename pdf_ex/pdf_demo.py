from weasyprint import CSS, HTML


def generate_pdf(url, pdf_file):
    print("Generating PDF...")
    css = CSS(string='body{ font-size: 8px; }')
    HTML(url).write_pdf(pdf_file, stylesheets=[css])


if __name__ == '__main__':
    url = 'http://www.npr.org/'
    pdf_file = 'demo_page.pdf'
    generate_pdf(url, pdf_file)
