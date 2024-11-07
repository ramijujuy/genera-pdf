# con pip instalamos paquetes para pdf y front
import streamlit as st
from fpdf import FPDF

# heredamos la clase y modificamos segunr requieramos


class PDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font('Arial', 'B', 12)
            self.cell(self.document_title, w=0, h=10,
                      border=0, ln=1, aling='C')

    def footer(self):
        self.set_y(-15)
        self.set_font(family='Arial', style='I', size=8)
        self.cell(
            w=0, h=10, txt=f'Pagina {self.page_no()}', border=0, ln=0, aling='C')

    def chapter_title(self, title, font='Arial', size=12):
        self.set_font(font, size, style='B')
        self.cell(title, w=0, h=10, border=0, ln=1, aling='L')
        self.ln(10)

    def chapter_body(self, body, font='Arial', size=12):
        self.set_font(font, size, style='')
        self.multi_cell(body, w=0, h=10)
        self.ln(10)

# Funcion para crear pdf obteniendo datos y por cada capitulo y le damos salida como archivo pdf


def create_pdf(filename, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)

    if image_path:
        pdf.image(image_path, x=10, y=25, w=pdf.w - 20)
        pdf.ln(120)

    for chapter in chapters:
        title, body, font, size = chapter
        pdf.chapter_title(title, font, size)
        pdf.chapter_body(body, font, size)

    pdf.output(filename)


def main():
    st.title("Generador de PDF con Python")
    st.header("Configuracion del Documento")
    document_title = st.text_input("Titulo del Documento", "Ingrese Titulo")
    author = st.text_input("Nombre del Autor", "ingrese el nombre...")
    uploaded_image = st.file_uploader(
        "Sube una imagen para el documento", type=["jpg", "pgn"])

    st.header("Capitulos del Documento")
    chapters = []
    chapters_cantidad = st.number_input(
        "Numero de Capitulos..", min_value=1, max_value=10)

    for i in range(chapters_cantidad):
        st.subheader(f"Capitulo {i + 1}")
        title = st.text_input(
            f"Ingrese el Titulo del Capitulo {i + 1}", f"Capitulo {i + 1} nombre...")
        body = st.text_area(f"Cuerpo del capitulo",
                            f"Texto del capitulo {i + 1}")
        font = st.selectbox(f"Fuentes del Capitulo {i + 1}", [
                            'Arial', 'Coureier', 'Times'])
        size = st.slider(f"Tamaño de la fuente {i+1}", 8, 24, 12)
        chapters.append((title, body, font, size))

    if st.button("Generar PDF"):
        image_path = uploaded_image.name if uploaded_image else None
        if image_path:
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
        create_pdf(document_title, author, chapters,
                   image_path, filename="textoenpdf.pdf", )

        with open("textoenpdf.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(
            label="Descargar PDF",
            data=PDFbyte,
            file_name="textoenpdf.pdf",
            mime='apllication/pctet-stream'
        )

        st.success("PDF Generado con Exito")


if __name__ == "__main__":
    main()
