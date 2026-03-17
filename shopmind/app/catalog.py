"""
Product catalog – 30 realistic e-commerce products across 5 categories.
In a production app this would load from a database or CSV file.
"""

from typing import Any


def load_catalog() -> list[dict[str, Any]]:
    return [
        # ── Electronics ────────────────────────────────────────────────────────
        {
            "id": "elec-001",
            "name": "ProSound X3 Wireless Noise-Cancelling Headphones",
            "brand": "ProSound",
            "category": "electronics",
            "price": 249,
            "rating": 4.7,
            "description": (
                "Premium over-ear headphones with active noise cancellation, "
                "30-hour battery life, and hi-fi sound. Bluetooth 5.3, foldable "
                "design, USB-C fast charging."
            ),
            "tags": ["headphones", "wireless", "noise-cancelling", "audio", "bluetooth"],
        },
        {
            "id": "elec-002",
            "name": "VisionTab Pro 11 Tablet",
            "brand": "VisionTech",
            "category": "electronics",
            "price": 499,
            "rating": 4.5,
            "description": (
                "11-inch OLED tablet with 120Hz refresh rate, octa-core processor, "
                "256 GB storage, 12 MP rear camera, and all-day battery. Perfect for "
                "work and entertainment."
            ),
            "tags": ["tablet", "oled", "portable", "work", "entertainment"],
        },
        {
            "id": "elec-003",
            "name": "SnapShot Z7 Mirrorless Camera",
            "brand": "SnapShot",
            "category": "electronics",
            "price": 899,
            "rating": 4.8,
            "description": (
                "Full-frame mirrorless camera with 45 MP sensor, in-body image "
                "stabilisation, 4K60 video, dual card slots, and weather sealing. "
                "Ideal for professional photographers."
            ),
            "tags": ["camera", "mirrorless", "photography", "professional", "4k"],
        },
        {
            "id": "elec-004",
            "name": "PowerBank Slim 20000",
            "brand": "ChargeFast",
            "category": "electronics",
            "price": 49,
            "rating": 4.4,
            "description": (
                "Ultra-slim 20 000 mAh portable charger with 65 W PD fast charging, "
                "3 output ports, LED indicator, and airline-safe design. Charges a "
                "laptop twice on a single fill."
            ),
            "tags": ["powerbank", "charging", "portable", "travel", "usb-c"],
        },
        {
            "id": "elec-005",
            "name": "SmartHub 8-in-1 USB-C Dock",
            "brand": "ConnectPro",
            "category": "electronics",
            "price": 79,
            "rating": 4.6,
            "description": (
                "8-in-1 USB-C hub with 4K HDMI, 100 W passthrough, SD/MicroSD slots, "
                "3× USB-A 3.0, and Ethernet. Compatible with MacBook, iPad, and "
                "Windows laptops."
            ),
            "tags": ["hub", "usb-c", "hdmi", "dock", "laptop", "accessories"],
        },
        {
            "id": "elec-006",
            "name": "EchoSmart 4 Smart Speaker",
            "brand": "SoundHouse",
            "category": "electronics",
            "price": 129,
            "rating": 4.3,
            "description": (
                "360° room-filling sound, built-in voice assistant, smart home hub, "
                "Zigbee support, and multi-room audio. Streams from Spotify, Apple "
                "Music, and 100+ services."
            ),
            "tags": ["speaker", "smart-home", "voice-assistant", "wifi", "music"],
        },

        # ── Clothing ───────────────────────────────────────────────────────────
        {
            "id": "clth-001",
            "name": "ArcticShield Men's Insulated Jacket",
            "brand": "ArcticShield",
            "category": "clothing",
            "price": 179,
            "rating": 4.6,
            "description": (
                "Lightweight yet ultra-warm men's jacket with 600-fill-power down "
                "insulation, water-resistant shell, and packable design. Available "
                "in S–3XL."
            ),
            "tags": ["jacket", "winter", "men", "insulated", "outdoor"],
        },
        {
            "id": "clth-002",
            "name": "FlexFit Women's Yoga Leggings",
            "brand": "FlexFit",
            "category": "clothing",
            "price": 65,
            "rating": 4.7,
            "description": (
                "High-waist 4-way stretch leggings with moisture-wicking fabric, "
                "hidden pocket, and squat-proof design. Perfect for yoga, gym, or "
                "casual wear."
            ),
            "tags": ["leggings", "yoga", "women", "gym", "activewear"],
        },
        {
            "id": "clth-003",
            "name": "UrbanThreads Oxford Button-Down Shirt",
            "brand": "UrbanThreads",
            "category": "clothing",
            "price": 55,
            "rating": 4.4,
            "description": (
                "Classic slim-fit Oxford shirt in 100% organic cotton. Wrinkle-"
                "resistant, machine-washable, and available in 12 colours. Versatile "
                "for office or casual outings."
            ),
            "tags": ["shirt", "men", "oxford", "formal", "casual", "organic-cotton"],
        },
        {
            "id": "clth-004",
            "name": "TrailBlazer Waterproof Hiking Boots",
            "brand": "TrailBlazer",
            "category": "clothing",
            "price": 149,
            "rating": 4.8,
            "description": (
                "Mid-cut waterproof hiking boots with Gore-Tex membrane, Vibram "
                "outsole, and cushioned midsole. Supports ankle stability on rough "
                "terrain."
            ),
            "tags": ["boots", "hiking", "waterproof", "outdoor", "unisex"],
        },
        {
            "id": "clth-005",
            "name": "SoftCloud Merino Wool Sweater",
            "brand": "SoftCloud",
            "category": "clothing",
            "price": 95,
            "rating": 4.5,
            "description": (
                "100% extra-fine merino wool crew-neck sweater. Temperature-"
                "regulating, odour-resistant, and naturally soft. Great for travel "
                "and all-season layering."
            ),
            "tags": ["sweater", "merino", "wool", "unisex", "travel", "winter"],
        },

        # ── Home & Kitchen ─────────────────────────────────────────────────────
        {
            "id": "home-001",
            "name": "BrewMaster Pro Espresso Machine",
            "brand": "BrewMaster",
            "category": "home",
            "price": 399,
            "rating": 4.7,
            "description": (
                "15-bar pump espresso machine with built-in grinder, milk frother, "
                "digital temperature control, and 2 L water tank. Makes café-quality "
                "espresso, cappuccino, and latte."
            ),
            "tags": ["coffee", "espresso", "kitchen", "appliance", "grinder"],
        },
        {
            "id": "home-002",
            "name": "AirPure HEPA Air Purifier",
            "brand": "AirPure",
            "category": "home",
            "price": 189,
            "rating": 4.6,
            "description": (
                "True HEPA + activated carbon filter removes 99.97% of allergens, "
                "dust, smoke, and pet dander. Covers up to 500 sq ft, whisper-quiet "
                "sleep mode, air quality sensor."
            ),
            "tags": ["air-purifier", "hepa", "allergy", "home", "clean-air"],
        },
        {
            "id": "home-003",
            "name": "ChefKnife Master 8-Piece Set",
            "brand": "KitchenEdge",
            "category": "home",
            "price": 129,
            "rating": 4.8,
            "description": (
                "German high-carbon stainless-steel knife set including chef, bread, "
                "paring, utility, and steak knives with wooden block. Full-tang, "
                "ergonomic handles for precise control."
            ),
            "tags": ["knives", "kitchen", "cooking", "chef", "steel"],
        },
        {
            "id": "home-004",
            "name": "NestWarm Electric Blanket",
            "brand": "NestWarm",
            "category": "home",
            "price": 69,
            "rating": 4.5,
            "description": (
                "Dual-zone heated electric blanket with 10 heat settings, "
                "auto shut-off, machine-washable fleece fabric, and ETL safety "
                "certification. King size."
            ),
            "tags": ["blanket", "heated", "winter", "bedroom", "comfort"],
        },
        {
            "id": "home-005",
            "name": "InstantCook 7-in-1 Pressure Cooker",
            "brand": "InstantCook",
            "category": "home",
            "price": 99,
            "rating": 4.9,
            "description": (
                "7-in-1 multi-cooker: pressure cooker, slow cooker, rice cooker, "
                "steamer, sauté, yogurt maker, and warmer. 6-quart capacity, 13 "
                "one-touch programs."
            ),
            "tags": ["pressure-cooker", "instant-pot", "kitchen", "cooking", "appliance"],
        },
        {
            "id": "home-006",
            "name": "GreenThumb Smart Plant Watering System",
            "brand": "GreenThumb",
            "category": "home",
            "price": 45,
            "rating": 4.3,
            "description": (
                "Automatic drip irrigation kit with soil moisture sensor, smartphone "
                "app control, and 15-day water reservoir. Ideal for indoor plants "
                "when you travel."
            ),
            "tags": ["plants", "garden", "smart-home", "watering", "iot"],
        },

        # ── Sports & Fitness ───────────────────────────────────────────────────
        {
            "id": "sprt-001",
            "name": "ProLift Adjustable Dumbbell Set",
            "brand": "ProLift",
            "category": "sports",
            "price": 299,
            "rating": 4.8,
            "description": (
                "Space-saving adjustable dumbbells that replace 15 pairs. Quick-"
                "change dial system adjusts weight from 5 to 50 lbs (2.3–22.7 kg). "
                "Includes tray and exercise guide."
            ),
            "tags": ["dumbbells", "weights", "gym", "fitness", "home-gym"],
        },
        {
            "id": "sprt-002",
            "name": "SpeedX Pro Running Shoes",
            "brand": "SpeedX",
            "category": "sports",
            "price": 129,
            "rating": 4.6,
            "description": (
                "Carbon-fibre plate running shoes with responsive foam midsole, "
                "breathable mesh upper, and grippy outsole. Engineered for marathon "
                "and daily training."
            ),
            "tags": ["running", "shoes", "marathon", "carbon", "fitness"],
        },
        {
            "id": "sprt-003",
            "name": "PeakPulse GPS Fitness Watch",
            "brand": "PeakPulse",
            "category": "sports",
            "price": 249,
            "rating": 4.7,
            "description": (
                "GPS multi-sport watch with heart rate, SpO2, sleep tracking, 20-day "
                "battery, and 100+ workout modes. Water-resistant to 50 m. Compatible "
                "with Strava and Garmin Connect."
            ),
            "tags": ["watch", "gps", "fitness", "sports", "wearable"],
        },
        {
            "id": "sprt-004",
            "name": "ZenMat Premium Yoga Mat",
            "brand": "ZenMat",
            "category": "sports",
            "price": 79,
            "rating": 4.7,
            "description": (
                "6 mm thick non-slip yoga mat with alignment lines, extra grip "
                "texture, eco-friendly natural rubber base, and carrying strap. "
                "72 × 26 inches."
            ),
            "tags": ["yoga", "mat", "fitness", "non-slip", "eco"],
        },
        {
            "id": "sprt-005",
            "name": "AquaFlex Resistance Bands Set",
            "brand": "AquaFlex",
            "category": "sports",
            "price": 35,
            "rating": 4.5,
            "description": (
                "Set of 5 fabric resistance bands (10–50 lbs) with non-slip design, "
                "carry bag, and exercise guide. Ideal for glutes, legs, and rehab "
                "training."
            ),
            "tags": ["resistance-bands", "gym", "fitness", "workout", "portable"],
        },

        # ── Beauty & Personal Care ─────────────────────────────────────────────
        {
            "id": "bty-001",
            "name": "GlowLab Vitamin C Serum",
            "brand": "GlowLab",
            "category": "beauty",
            "price": 38,
            "rating": 4.6,
            "description": (
                "Brightening 20% Vitamin C + Hyaluronic Acid face serum that fades "
                "dark spots, evens skin tone, and boosts collagen. Cruelty-free, "
                "vegan, dermatologist-tested."
            ),
            "tags": ["serum", "vitamin-c", "skincare", "face", "brightening"],
        },
        {
            "id": "bty-002",
            "name": "LuxeGroom Men's Beard Care Kit",
            "brand": "LuxeGroom",
            "category": "beauty",
            "price": 45,
            "rating": 4.5,
            "description": (
                "Complete beard care kit: balm, oil, wash, wooden comb, and boar "
                "bristle brush. Conditions and shapes beard while reducing itch. "
                "Cedar & sandalwood scent."
            ),
            "tags": ["beard", "grooming", "men", "skincare", "gift-set"],
        },
        {
            "id": "bty-003",
            "name": "AquaWave Ionic Hair Dryer",
            "brand": "AquaWave",
            "category": "beauty",
            "price": 89,
            "rating": 4.7,
            "description": (
                "2200 W ionic hair dryer with 3 heat / 2 speed settings, cool-shot "
                "button, diffuser + concentrator attachments. Reduces frizz by 60% "
                "vs conventional dryers."
            ),
            "tags": ["hair-dryer", "ionic", "hair-care", "beauty", "styling"],
        },
        {
            "id": "bty-004",
            "name": "PureSmile Whitening Electric Toothbrush",
            "brand": "PureSmile",
            "category": "beauty",
            "price": 59,
            "rating": 4.6,
            "description": (
                "Sonic electric toothbrush with 40 000 strokes/min, 5 brushing modes, "
                "2-minute smart timer, UV sanitiser case, and 3-month battery life. "
                "Includes 3 brush heads."
            ),
            "tags": ["toothbrush", "electric", "dental", "whitening", "oral-care"],
        },
        {
            "id": "bty-005",
            "name": "SereneScent Aromatherapy Diffuser",
            "brand": "SereneScent",
            "category": "beauty",
            "price": 39,
            "rating": 4.4,
            "description": (
                "300 ml ultrasonic essential-oil diffuser with 7-colour LED light, "
                "4 timer settings, auto shut-off, and whisper-quiet operation. Covers "
                "up to 250 sq ft."
            ),
            "tags": ["diffuser", "aromatherapy", "wellness", "home", "relaxation"],
        },
        {
            "id": "bty-006",
            "name": "SunShield SPF 50 Tinted Moisturiser",
            "brand": "SunShield",
            "category": "beauty",
            "price": 28,
            "rating": 4.5,
            "description": (
                "Lightweight SPF 50 PA++++ tinted moisturiser with hyaluronic acid "
                "and niacinamide. Provides sheer coverage, sun protection, and hydration "
                "in one step. Suitable for all skin types."
            ),
            "tags": ["sunscreen", "spf", "tinted", "moisturiser", "skincare"],
        },
    ]
