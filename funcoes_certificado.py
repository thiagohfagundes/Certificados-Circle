#Libs para geração do certificado em PDF
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import qrcode

def gerar_certificado_com_pdf_fundo(
    nome, curso, carga_horaria, data_certificacao, data_emissao, codigo_validacao,
    modelo_pdf_path, output_path
):
    """Gera um certificado PDF com o fundo do modelo fornecido."""
    largura, altura = A4
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # Conteúdo dinâmico com HTML simples
    texto = f"""
    Certificamos que <b>{nome}</b>, foi aprovado(a) no <b>{curso}</b> oferecido pelo Professional Services do Grupo Superlógica, com carga horária total de <b>{carga_horaria}</b> horas, em <b>{data_certificacao}</b>. Esta certificação reconhece o comprometimento do participante com sua capacitação e aprimoramento profissional no setor de gestão imobiliária.
    """

    # Estilo
    styles = getSampleStyleSheet()
    estilo = styles['Normal']
    estilo.fontName = 'Helvetica'
    estilo.fontSize = 16
    estilo.leading = 22

    try:
        paragrafo = Paragraph(texto.strip(), estilo)
        frame = Frame(x1=90, y1=380, width=430, height=180)
        frame.addFromList([paragrafo], can)

    except Exception as e:
        print("Erro ao renderizar o parágrafo:", e)

    # Data e código
    can.setFont("Helvetica", 16)
    can.drawString(90, 330, f"Campinas, {data_emissao}")
    can.setFont("Helvetica", 10)
    can.drawString(90, 300, f"CÓD VALIDAÇÃO: {codigo_validacao}")

    can.save()
    packet.seek(0)

    # Overlay no PDF base
    overlay_pdf = PdfReader(packet)
    background_pdf = PdfReader(modelo_pdf_path)
    output_pdf = PdfWriter()

    background_page = background_pdf.pages[0]
    overlay_page = overlay_pdf.pages[0]
    background_page.merge_page(overlay_page)
    output_pdf.add_page(background_page)

    with open(output_path, "wb") as f:
        output_pdf.write(f)


def gerar_qrcode_para_url(url, caminho_imagem='qrcode.png'): # Usar futuramente
    """Gera um QR Code a partir de uma URL e salva em um arquivo PNG."""
    qr = qrcode.QRCode(
        version=1,
        box_size=4,
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(caminho_imagem)