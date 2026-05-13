# Turkish Text Normalizer

The public normalizer API is the `normalize()` function. The old
`TurkishNormalizer` class was removed; use `normalize(text)` with the default
pipeline or pass an explicit `converters=[...]` list for a custom pipeline.

## Features

- Converts numbers to their text representation (123 → yüz yirmi üç)
- Normalizes ordinal numbers (1. → birinci)
- Converts Roman numerals to Arabic numbers
- Converts special symbols (%, $, etc.) to their text representation
- Intelligently handles multiplication symbols in dimensions (3x4 → 3 çarpı 4, 2x5x6x3 → 2 çarpı 5 çarpı 6 çarpı 3)
- Expands unit abbreviations to their full text (cm → santimetre, kg → kilogram)
- Handles Turkish character casing and diacritical marks
- Normalizes time expressions (e.g., "saat 22.00" → "saat yirmi iki")
- Provides a simple function-based API
- Supports processing both single strings and lists of strings
- Allows customization of which normalization steps to apply
- Handles numbers followed by commas in lists and sequences
- Provides apostrophe handling for Turkish suffixes (e.g., "8'i" → "sekizi")

## Usage

### Basic Usage

```python
from trnorm import normalize

# Normalize a single string
text = "Bugün 15. kattaki 3 toplantıya katıldım."
normalized_text = normalize(text)
print(normalized_text)
# Output: "bugün on beşinci kattaki üç toplantıya katıldım."

# Normalize a list of strings
texts = [
    "Saat 14:30'da %25 indirimli ürünler satışa çıkacak.",
    "II. Dünya Savaşı 1939-1945 yılları arasında gerçekleşti."
]
normalized_texts = normalize(texts)
print(normalized_texts)
# Output: [
#   "saat on dört otuzda yüzde yirmi beş indirimli ürünler satışa çıkacak.",
#   "ikinci dünya savaşı bin dokuz yüz otuz dokuz bin dokuz yüz kırk beş yılları arasında gerçekleşti."
# ]
```

### Customizing Normalization Steps

```python
from trnorm import normalize
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.text_utils import turkish_lower

# Only convert numbers to text, then Turkish-lowercase
text = "Âlim insanlar 15 kitap okumuş."
normalized_text = normalize(
    text,
    converters=[convert_numbers_to_words_wrapper, turkish_lower],
)
print(normalized_text)
# Output: "âlim insanlar on beş kitap okumuş."

```

### Handling Dimensions and Multiplication Symbols

```python
from trnorm import normalize

# Handle dimensions with merged multiplication symbols
text = "Odanın boyutları 2x3x4 metre."
normalized_text = normalize(text)
print(normalized_text)
# Output: "odanın boyutları iki çarpı üç çarpı dört metre."

# Handle dimensions with units
text = "Halının boyutu 120x180cm."
normalized_text = normalize(text)
print(normalized_text)
# Output: "halının boyutu yüz yirmi çarpı yüz seksen santimetre."
```

### Handling Unit Abbreviations

```python
from trnorm import normalize

# Convert unit abbreviations to full text
text = "Masanın yüksekliği 75 cm."
normalized_text = normalize(text)
print(normalized_text)
# Output: "masanın yüksekliği yetmiş beş santimetre."

# Multiple units in the same text
text = "Odanın boyutları 5 m x 4 m, yüksekliği 3 m."
normalized_text = normalize(text)
print(normalized_text)
# Output: "odanın boyutları beş metre çarpı dört metre, yüksekliği üç metre."

# Use a custom converter list when you need to omit unit normalization
text = "Sıcaklık 25 °C."
from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.text_utils import turkish_lower
normalized_text = normalize(text, converters=[convert_numbers_to_words_wrapper, turkish_lower])
print(normalized_text)
# Output: "sıcaklık yirmi beş °c."
```

### Handling Time Expressions

```python
from trnorm import normalize

# Normalize time expressions
text = "Saat 22.00'de toplantımız var."
normalized_text = normalize(text)
print(normalized_text)
# Output: "saat yirmi ikide toplantımız var."

# Normalize standalone times
text = "13.30'da görüşeceğiz."
normalized_text = normalize(text)
print(normalized_text)
# Output: "on üç buçukta görüşeceğiz."

# Normalize times with minutes
text = "Saat 10.15'te görüşelim."
normalized_text = normalize(text)
print(normalized_text)
# Output: "saat on on beşte görüşelim."
```

### Handling Number Lists and Sequences

```python
from trnorm import normalize

# Convert numbers in lists
text = "1, 2, 3 sayıları ardışıktır."
normalized_text = normalize(text)
print(normalized_text)
# Output: "bir, iki, üç sayıları ardışıktır."

# Handle numbers in date sequences
text = "Toplantımız 13, 14 ve 15 Mayıs tarihlerinde yapılacak."
normalized_text = normalize(text)
print(normalized_text)
# Output: "toplantımız on üç, on dört ve on beş mayıs tarihlerinde yapılacak."
```

### Apostrophe Handling in Turkish Suffixes

In Turkish, apostrophes are often used to separate suffixes from proper nouns or numbers. The normalizer can remove these apostrophes to create more natural text:

```python
from trnorm import normalize

# Apostrophe handling is part of the default pipeline
text = "8'i almadım"
normalized_text = normalize(text)
print(normalized_text)
# Output: "sekizi almadım"

# More examples
text = "İstanbul'da yaşıyorum"
normalized_text = normalize(text)
print(normalized_text)
# Output: "istanbulda yaşıyorum"
```

## Normalization Order

The normalizer applies the following steps in order:

1. **Time expression normalization**
2. **Alphanumeric normalization**
3. **Ordinal normalization**
4. **Symbol conversion**
5. **Number to text conversion**
6. **Context-aware suffix merge**
7. **Apostrophe removal**
8. **Hat removal**
9. **Dimension preprocessing**
10. **Dimension normalization**
11. **Unit abbreviation expansion**
12. **Turkish lowercasing**
13. **Final hat removal**
14. **Punctuation removal**

## Custom Pipelines

`normalize()` accepts `converters=[...]` for custom behavior. Boolean keyword flags from
the removed `TurkishNormalizer` API are no longer supported.

## Time Normalization

The time normalization feature converts time expressions to their text form before applying number-to-text conversion. This ensures that time expressions are properly normalized and not misinterpreted as decimal numbers.

Examples:

- "saat 22.00" → "saat yirmi iki" (zero minutes are omitted)
- "13.30" → "on üç buçuk" (half hours are converted to "buçuk")
- "9:45" → "dokuz kırk beş"
- "18:00" → "on sekiz" (zero minutes are omitted)

The time normalization handles:

- Times with "saat" prefix (e.g., "saat 22.00", "saat 9:45")
- Standalone times (e.g., "22.00", "9:45")
- Special case for half hours (e.g., "13.30" → "on üç buçuk")
- Omitting zero minutes (e.g., "22.00" → "yirmi iki" instead of "yirmi iki sıfır")
