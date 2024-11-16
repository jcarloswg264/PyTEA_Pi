
# PyTEA Pi
**PyTEA Pi** es una aplicación interactiva diseñada para facilitar la comunicación de personas con Trastorno del Espectro Autista (TEA). La aplicación permite el uso de pictogramas acompañados de locuciones, organizados por categorías, y está optimizada para ejecutarse en dispositivos con Raspberry Pi OS.

---

## 🚀 Características
- Interfaz gráfica intuitiva y accesible.
- Pictogramas organizados por categorías (animales, objetos, acciones, etc.).
- Locuciones asociadas para cada pictograma.
- Compatible con dispositivos Raspberry Pi.
- Código modular y fácilmente extensible.

---

## 📂 Estructura del proyecto
```plaintext
PyTEA_Pi/
├── main.py                  # Archivo principal para ejecutar la aplicación.
├── pictograms/              # Carpeta con los pictogramas organizados por categorías.
├── audio/                   # Carpeta con las locuciones asociadas a los pictogramas.
├── src/                     # Código fuente de la aplicación.
├── data/                    # Configuración y relación pictogramas-locuciones.
├── assets/                  # Iconos, fuentes y otros recursos estáticos.
├── scripts/                 # Scripts de instalación y despliegue.
├── tests/                   # Tests automatizados.
├── requirements.txt         # Lista de dependencias del proyecto.
└── README.md                # Documentación del proyecto.
```

---

## 🛠️ Instalación
### Requisitos previos
- Python 3.7 o superior.
- Raspberry Pi OS o cualquier sistema basado en Linux.
- Dependencias listadas en `requirements.txt`.

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
Este proyecto utiliza pictogramas proporcionados por **ARASAAC (https://arasaac.org)** bajo su licencia de uso. **ARASAAC** es una fuente gratuita de pictogramas y recursos gráficos para personas con necesidades comunicativas específicas. 

Los pictogramas son propiedad de **Gobierno de Aragón (España)** y tienen restricciones en cuanto a su uso comercial. Si planeas distribuir o comercializar este proyecto, consulta previamente los términos de uso detallados en su sitio web: [Licencia de ARASAAC](https://arasaac.org/licencia).

---

## 🧩 Contribución
¡Tu ayuda es bienvenida! Si deseas contribuir, sigue estos pasos:
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
