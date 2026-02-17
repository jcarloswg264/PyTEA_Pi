<div align="center">
    <img src="assets/logo_banner.png" alt="PyTEA Pi Banner" width="600">
</div>

# PyTEA Pi

**PyTEA Pi** es una aplicación de Comunicación Aumentativa y Alternativa (CAA) pensada para facilitar la expresión de personas con Trastorno del Espectro Autista (TEA) o Trastorno Específico del Lenguaje (TEL).

Permite construir frases mediante pictogramas organizados por categorías y reproducirlas con locución automática.

---

## ✨ ¿Qué hace la aplicación?

- Muestra pictogramas organizados por categorías.
- Permite seleccionar varios pictogramas para formar una frase.
- Visualiza la frase completa en pantalla.
- Reproduce automáticamente el audio correspondiente a cada pictograma en orden.
- Ofrece feedback visual durante la reproducción.

La aplicación está pensada para ser sencilla, visual e intuitiva, especialmente en entornos educativos y terapéuticos.

---

## 🖥️ Funcionamiento básico

1. Al iniciar la aplicación se muestran las categorías disponibles.
2. Al seleccionar una categoría se muestran sus pictogramas.
3. Cada pictograma seleccionado se añade a la barra inferior.
4. Al pulsar **Play**, la frase se muestra en pantalla y se reproduce automáticamente.
5. El botón **Inicio** permite volver al menú principal.

---

## 🧩 Estructura del proyecto
PyTEA_Pi/
├── assets/ # Recursos gráficos (logos, iconos)
├── audio/ # Audios organizados por categorías
├── pictograms/ # Pictogramas organizados por categorías
├── scripts/ # Scripts auxiliares
├── src/ # Código fuente principal
├── main.py # Punto de entrada de la aplicación
├── requirements.txt
└── README.md

El código está organizado de forma modular para facilitar su mantenimiento y evolución.

---

## 🛠️ Instalación

### Requisitos

- Linux (incluido Raspberry Pi OS)
- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

### Instalación

```bash
git clone git@github.com:jcarloswg264/PyTEA_Pi.git
cd PyTEA_Pi

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt
python main.py
```

---

## 📜 Licencia
Este proyecto está licenciado bajo la **[Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**.

### Resumen de la licencia:
1. **Atribución**: Se debe dar crédito al autor original (**Jose Carlos Wittmann**) en cualquier uso o distribución del software.
2. **No Comercial**: No se permite el uso con fines comerciales sin autorización previa.
3. **Compartir Igual**: Si realizas modificaciones o derivados del software, estos deben ser compartidos bajo los mismos términos.

El texto completo de la licencia está disponible en el archivo [LICENSE](LICENSE).

---

## ⚖️ Consideraciones legales sobre los pictogramas de ARASAAC

Este proyecto utiliza pictogramas proporcionados por **ARASAAC (https://arasaac.org)**, una fuente gratuita de recursos gráficos destinados a personas con necesidades comunicativas específicas.

<div align="center">
    <img src="assets/logo_ARASAAC.png" alt="Logo ARASAAC" width="300">
</div>

### Condiciones de uso de los pictogramas:
- **Uso no comercial**: Los pictogramas se emplean exclusivamente para fines educativos, terapéuticos o personales. **No se permite su uso con fines comerciales** sin autorización expresa de ARASAAC.
- **Reconocimiento de autoría**: ARASAAC y el Gobierno de Aragón deben ser reconocidos como los autores de los pictogramas en cualquier uso o distribución.
- **No alteración**: Los pictogramas no pueden ser modificados sin autorización expresa.

Si deseas utilizar los pictogramas para fines comerciales o necesitas modificar los recursos, es obligatorio obtener autorización expresa de **ARASAAC** y del **Gobierno de Aragón**.

Puedes consultar las condiciones completas en la página oficial de ARASAAC: [Condiciones de uso de ARASAAC](https://arasaac.org/terms-of-use).

---

## 🙌 Agradecimientos
- A **ARASAAC** por proporcionar pictogramas y recursos gratuitos que mejoran la comunicación.
- A la comunidad de Python y Kivy por su soporte y documentación.

---
