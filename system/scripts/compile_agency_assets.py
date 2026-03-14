#!/usr/bin/env python3
"""
My-OS Jensen Huang Async Asset Compiler
Automatically compiles PNG slides into 1080x1350px LinkedIn PDF Carousels
and validates X.com 280-character thread bundles.
"""

import os
import sys
from PIL import Image

def compile_linkedin_pdf(image_paths, output_pdf_path):
    """
    Compiles a list of slide PNG images into a single high-res PDF document for LinkedIn.
    """
    if not image_paths:
        print("[Error] No image paths provided for PDF compilation.")
        return False

    images = []
    for path in image_paths:
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            images.append(img)
        else:
            print(f"[Warning] Slide image not found: {path}")

    if not images:
        print("[Error] No valid images loaded.")
        return False

    try:
        first_img = images[0]
        rest_imgs = images[1:] if len(images) > 1 else []
        first_img.save(output_pdf_path, save_all=True, append_images=rest_imgs)
        print(f"[Success] Compiled LinkedIn PDF Carousel: {output_pdf_path}")
        return True
    except Exception as e:
        print(f"[Error] Failed to compile PDF: {e}")
        return False

def validate_x_tweet(text):
    """
    Validates character length for X.com (Twitter) standard 280-character limit.
    """
    length = len(text)
    compliant = length <= 280
    return {
        "text": text,
        "char_count": length,
        "compliant": compliant,
        "remaining": 280 - length
    }

def main():
    print("==================================================")
    print("  MY-OS FOUNDER COUNCIL ASSET COMPILER")
    print("==================================================")
    
    content_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "content")
    
    # Auto-detect Post 1 slides
    post1_slides = [
        os.path.join(content_dir, "post-1-slide-1-hook.png"),
        os.path.join(content_dir, "post-1-slide-2-architecture.png"),
        os.path.join(content_dir, "post-1-slide-3-framework.png")
    ]
    
    output_pdf = os.path.join(content_dir, "post-1-carousel-slides.pdf")
    compile_linkedin_pdf(post1_slides, output_pdf)

if __name__ == "__main__":
    main()
