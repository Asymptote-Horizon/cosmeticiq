from typing import Optional, Dict, Any
import io
from PIL import Image
import re


class OCRService:
    """OCR service for extracting text from product images."""

    def __init__(self):
        self.pytesseract_available = False
        self._check_dependencies()

    def _check_dependencies(self):
        try:
            import pytesseract
            self.pytesseract_available = True
        except ImportError:
            self.pytesseract_available = False

    def extract_text_from_image(self, image_data: bytes) -> Dict[str, Any]:
        try:
            image = Image.open(io.BytesIO(image_data))

            if self.pytesseract_available:
                import pytesseract
                text = pytesseract.image_to_string(image)
            else:
                text = self._basic_image_analysis(image)

            cleaned_text = self._clean_text(text)
            ingredients = self._extract_ingredients(cleaned_text)

            return {
                "success": True,
                "raw_text": text,
                "cleaned_text": cleaned_text,
                "ingredients": ingredients,
                "has_ingredients": bool(ingredients),
                "confidence": 0.8 if self.pytesseract_available else 0.3
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "raw_text": "",
                "cleaned_text": "",
                "ingredients": [],
                "has_ingredients": False,
                "confidence": 0.0
            }

    def _basic_image_analysis(self, image: Image.Image) -> str:
        width, height = image.size
        mode = image.mode
        return f"[Image analysis: {width}x{height}, mode={mode}. OCR not available - please provide ingredients as text.]"

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'[^\w\s,;:\-()./%]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        corrections = {
            '1ngredients': 'Ingredients',
            'ingredients:': 'Ingredients:',
            'INGREDIENTS:': 'Ingredients:',
            'inc': 'INCI',
            'Aqua.': 'Aqua',
        }
        for old, new in corrections.items():
            text = text.replace(old, new)
        return text.strip()

    def _extract_ingredients(self, text: str) -> str:
        patterns = [
            r'Ingredients?[:\s]+(.*?)(?:Directions|Warning|Caution|$)',
            r'INCI[:\s]+(.*?)(?:Directions|Warning|Caution|$)',
            r'Composition[:\s]+(.*?)(?:Directions|Warning|Caution|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        if ',' in text:
            sections = text.split('.')
            longest_section = max(sections, key=lambda s: s.count(','))
            if longest_section.count(',') >= 3:
                return longest_section.strip()
        return text


class BarcodeScanner:
    def scan_barcode(self, image_data: bytes) -> Dict[str, Any]:
        try:
            from pyzbar import pyzbar
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            decoded_objects = pyzbar.decode(image)
            if decoded_objects:
                barcode = decoded_objects[0].data.decode('utf-8')
                return {"success": True, "barcode": barcode, "type": decoded_objects[0].type}
            return {"success": False, "error": "No barcode detected"}
        except ImportError:
            return {"success": False, "error": "Barcode scanning library not available"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def lookup_barcode(self, barcode: str) -> Dict[str, Any]:
        import httpx
        url = f"https://world.openbeautyfacts.org/api/v2/product/{barcode}.json"
        try:
            response = httpx.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                product = data.get("product", {})
                return {
                    "success": True,
                    "name": product.get("product_name", "Unknown"),
                    "brand": product.get("brands", "Unknown"),
                    "ingredients": product.get("ingredients_text", ""),
                    "image": product.get("image_front_url", ""),
                    "categories": product.get("categories", ""),
                }
            return {"success": False, "error": "Product not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}


ocr_service = OCRService()
barcode_scanner = BarcodeScanner()
