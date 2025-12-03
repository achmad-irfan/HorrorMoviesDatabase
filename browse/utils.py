import base64
import io
import matplotlib.pyplot as plt

def fig_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')
