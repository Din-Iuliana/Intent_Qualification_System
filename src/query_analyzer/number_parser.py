def parse_number(text: str) -> int:
    text = text.lower().strip()
    text = text.replace("$", "").replace(",", "").replace(" ", "")

    if "billion" in text:
        number_part = text.replace("billion", "")
        return int(float(number_part) * 1_000_000_000)

    if "million" in text:
        number_part = text.replace("million", "")
        return int(float(number_part) * 1_000_000)

    if "thousand" in text:
        number_part = text.replace("thousand", "")
        return int(float(number_part) * 1_000)

    if text.endswith("bn") or text.endswith("b"):
        suffix_len = 2 if text.endswith("bn") else 1
        number_part = text[:-suffix_len]
        return int(float(number_part) * 1_000_000_000)

    if text.endswith("m"):
        return int(float(text[:-1]) * 1_000_000)

    if text.endswith("k"):
        return int(float(text[:-1]) * 1_000)

    return int(float(text))