# PyTEA Pi
**PyTEA Pi** es una aplicación interactiva diseñada para facilitar la comunicación de personas con Trastorno del Espectro Autista (TEA). La aplicación utiliza pictogramas acompañados de locuciones, organizados por categorías, para crear una experiencia intuitiva y accesible. Está optimizada para ejecutarse en dispositivos con Raspberry Pi OS.

---

## 🚀 Características
- Interfaz gráfica intuitiva y accesible.
- Pictogramas organizados por categorías como animales, objetos, acciones, entre otras.
- Locuciones asociadas para cada pictograma.
- Compatible con dispositivos Raspberry Pi.
- Código modular y fácilmente extensible.

---

## 📂 Estructura del proyecto
```plaintext
PyTEA_Pi/
├── assets/               # Recursos estáticos como el logo.
├── audio/                # Archivos de audio organizados por categorías.
├── data/                 # Configuración y mapeo de datos.
├── pictograms/           # Pictogramas organizados por categorías.
├── scripts/              # Scripts para despliegue y automatización.
├── src/                  # Código fuente principal de la aplicación.
├── tests/                # Tests automatizados.
├── README.md             # Documentación del proyecto.
├── requirements.txt      # Lista de dependencias del proyecto.
└── main.py               # Archivo principal para ejecutar la aplicación.
```

---

## 🛠️ Instalación
### Requisitos previos
- **Sistema operativo:** Raspberry Pi OS o cualquier distribución basada en Linux.
- **Python:** Versión 3.7 o superior.
- Dependencias especificadas en `requirements.txt`.

### Instrucciones
1. Clona el repositorio:
   ```bash
   git clone git@github.com:jcarloswg264/PyTEA_Pi.git
   cd PyTEA_Pi
   ```
2. Crea un entorno virtual y actívalo:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

---

## 🖼️ Uso
1. Al iniciar la aplicación, se muestra una pantalla con categorías de pictogramas.
2. Selecciona una categoría para visualizar los pictogramas disponibles.
3. Haz clic en un pictograma para reproducir su locución.

---

## ⚖️ Consideraciones legales
### Uso de pictogramas de ARASAAC
Este proyecto utiliza pictogramas proporcionados por **ARASAAC (https://arasaac.org)**, una fuente gratuita de recursos gráficos destinados a personas con necesidades comunicativas específicas.

**Condiciones de uso:**
- **Uso no comercial:** Los pictogramas se emplean exclusivamente para fines educativos, terapéuticos o personales, sin ningún propósito comercial.
- **Reconocimiento de autoría:** ARASAAC y el Gobierno de Aragón son reconocidos como los autores y propietarios de los pictogramas utilizados.
- **No alteración:** Los pictogramas no han sido modificados, salvo autorización expresa.

Para más información sobre las condiciones de uso, visita la página oficial de ARASAAC: [Condiciones de uso de ARASAAC](https://arasaac.org/terms-of-use).

Si deseas utilizar los pictogramas para fines comerciales o necesitas modificar los recursos, es obligatorio obtener autorización expresa de ARASAAC y del Gobierno de Aragón.

---

## 🧩 Contribución
¡Tu ayuda es bienvenida! Si deseas contribuir:
1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad o corrección:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza tus cambios y haz un commit:
   ```bash
   git commit -m "Añadida nueva funcionalidad"
   ```
4. Haz un push a tu rama y abre un pull request.

---

## 📜 Licencia
Este proyecto está licenciado bajo la **[MIT License](LICENSE)**. Sin embargo, esta licencia no aplica a los recursos gráficos (pictogramas) de **ARASAAC**, que están protegidos por sus propios términos de uso.

---

## 🙌 Agradecimientos
- A **ARASAAC** por proporcionar pictogramas y recursos gratuitos que mejoran la comunicación.
- A la comunidad de Python y Kivy por su soporte y documentación.

---
