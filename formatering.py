def formater_nummer(n, desimaler=0):
    try:
        return f"{n:,.{desimaler}f}".replace(",", " ").replace(".", ",")
    except (TypeError, ValueError):
        return str(n)