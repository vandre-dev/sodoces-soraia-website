# 🍰 Sódoces Web Catalog

> An institutional website and digital catalog built with love for my mother's confectionery business.

## 📖 About the Project
This project holds a very special meaning to me. It is the digital storefront for **Sódoces**, an artisanal bakery business run by my mother, Soraia. For as long as I can remember, the aroma of fresh cakes and handcrafted sweets has been the essence of our home. 

As I journey into software development, I decided to bridge my studies in technology with her life's work. Inspired by major bakery chains like *Sodiê Doces*, this project aims to deliver a clean, professional, and welcoming digital experience for her customers. Simultaneously, it serves as a practical, evolving portfolio piece documenting my progression as a developer.

## 🚀 Current State: v1.0 (MVP)
This initial version focuses on establishing a solid foundation using core programming concepts. Since a full API is not yet in place, the project uses a creative hybrid approach:
* **Python Data Logic:** The catalog (prices, descriptions, categories) is managed entirely through Python data structures (Dictionaries and Lists). 
* **HTML Generator:** A Python script acts as a mock backend, automatically generating formatted HTML snippets from the catalog data to be injected into the website.
* **Semantic UI:** The frontend features a clean HTML5 structure styled with a custom CSS palette carefully extracted from the brand's official logo.

## 🛠️ Tech Stack
* **Python 3** (Data structuring, logic, and HTML generation)
* **HTML5** (Semantic structure)
* **CSS3** (Styling, color variables, and layout)

## 📂 Repository Structure
```text
sodoces-soraia-website/
├── backend/
│   └── gerador_catalogo.py      # Python script to manage menu data and generate HTML
├── frontend/
│   ├── index.html               # Main landing page and catalog UI
│   └── Logo-Definitiva.jpeg     # Brand visual asset
└── README.md