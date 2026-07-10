#!/usr/bin/env python3
import os
import yaml
from pathlib import Path
from PIL import Image

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "static" / "img"
DATA_FILE = BASE_DIR / "data" / "site_data.yml"

def optimize_images():
    print("--- Optimizando imágenes a formato WebP ---")
    
    # Extensiones de imagen soportadas para conversión
    extensions = {".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"}
    converted_mapping = {}

    # 1. Convertir imágenes en static/img/
    for img_path in IMG_DIR.iterdir():
        if img_path.is_file() and img_path.suffix in extensions:
            webp_name = f"{img_path.stem}.webp"
            webp_path = IMG_DIR / webp_name
            
            try:
                with Image.open(img_path) as img:
                    # Guardamos como WebP con calidad 85 y compresión de alta calidad
                    img.save(webp_path, "WEBP", quality=85, method=6)
                
                original_size = img_path.stat().st_size
                new_size = webp_path.stat().st_size
                reduction = (original_size - new_size) / original_size * 100
                
                print(f"Convertida: {img_path.name} -> {webp_name} ({reduction:.1f}% menor peso)")
                converted_mapping[img_path.name] = webp_name
                
                # Eliminamos la imagen original obsoleta para no dejar basura
                os.remove(img_path)
                
            except Exception as e:
                print(f"Error al convertir {img_path.name}: {e}")

    # 2. Actualizar el archivo site_data.yml
    if not DATA_FILE.exists():
        print(f"Error: No se encontró el archivo de datos {DATA_FILE}")
        return

    print("\n--- Actualizando archivo site_data.yml ---")
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Actualizar imágenes en categorías
        updated_categories = 0
        if "categories" in data:
            for cat in data["categories"]:
                old_img = cat.get("image")
                if old_img in converted_mapping:
                    cat["image"] = converted_mapping[old_img]
                    updated_categories += 1
                elif old_img and old_img.endswith(tuple(extensions)):
                    # Caso por si el archivo ya no existe pero la extensión en YAML es vieja
                    stem, _ = os.path.splitext(old_img)
                    cat["image"] = f"{stem}.webp"
                    updated_categories += 1

        # Actualizar imágenes en carrusel
        updated_slides = 0
        if "carousel_slides" in data:
            for slide in data["carousel_slides"]:
                old_img = slide.get("image")
                if old_img in converted_mapping:
                    slide["image"] = converted_mapping[old_img]
                    updated_slides += 1
                elif old_img and old_img.endswith(tuple(extensions)):
                    stem, _ = os.path.splitext(old_img)
                    slide["image"] = f"{stem}.webp"
                    updated_slides += 1

        # Guardar cambios
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            # Usar default_flow_style=False para un YAML legible
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"Categorías actualizadas en YAML: {updated_categories}")
        print(f"Slides del carrusel actualizados en YAML: {updated_slides}")
        print("¡Optimización de imágenes e integración con YAML finalizada con éxito!")

    except Exception as e:
        print(f"Error al actualizar YAML: {e}")

if __name__ == "__main__":
    optimize_images()
