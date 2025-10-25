# _cite/oa_image.py
import os, re, io, yaml, time
import requests
from urllib.parse import urlparse
from unidecode import unidecode
from PIL import Image
try:
    import fitz  # PyMuPDF
except ImportError:
    raise SystemExit("Please pip install pymupdf")

CIT_PATH = "_data/citations.yaml"
OUT_DIR = "images/papers"

os.makedirs(OUT_DIR, exist_ok=True)

def slugify(s):
    s = unidecode(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80]

def find_pdf_url(item):
    # 1) prefer direct url if endswith .pdf
    url = item.get("URL") or item.get("url")
    if url and url.lower().endswith(".pdf"):
        return url
    # 2) try DOI -> doi.org
    doi = item.get("DOI") or item.get("doi")
    if doi:
        return f"https://doi.org/{doi}"
    # 3) fallback: nothing
    return None

def resolve_pdf(url, timeout=15):
    # Follow redirects; if final URL is a PDF or content-type is pdf, return bytes
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent":"Mozilla/5.0"})
        ct = r.headers.get("Content-Type","").lower()
        if r.status_code == 200 and ("pdf" in ct or urlparse(r.url).path.lower().endswith(".pdf")):
            return r.content
    except Exception:
        return None
    return None

def extract_first_image(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        return None
    for page in doc:
        images = page.get_images(full=True)
        for xref in [img[0] for img in images]:
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 4:
                    pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                else:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                    pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                # 过滤太小的图
                if pil.width < 400 or pil.height < 300:
                    continue
                return pil
            except Exception:
                continue
    return None

def main():
    if not os.path.exists(CIT_PATH):
        print("No citations.yaml yet; skip.")
        return
    data = yaml.safe_load(open(CIT_PATH, "r", encoding="utf-8"))
    changed = False
    for i, item in enumerate(data):
        title = item.get("title") or item.get("Title") or "paper"
        if item.get("image"):
            continue
        url = find_pdf_url(item)
        if not url:
            continue
        print("Trying:", title)
        pdf = resolve_pdf(url)
        if not pdf:
            continue
        img = extract_first_image(pdf)
        if not img:
            continue
        slug = slugify(title)
        out_path = os.path.join(OUT_DIR, f"{slug}.jpg")
        # 压缩成 jpg
        img_rgb = img.convert("RGB")
        img_rgb.save(out_path, "JPEG", quality=85, optimize=True)
        item["image"] = "/" + out_path.replace("\\","/")
        changed = True
        # 节流，避免触发风控
        time.sleep(1.0)

    if changed:
        with open(CIT_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
        print("Updated images in", CIT_PATH)
    else:
        print("No images added.")

if __name__ == "__main__":
    main()
