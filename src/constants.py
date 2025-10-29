LASTFM_API_BASE = "https://ws.audioscrobbler.com/2.0/"

# =======================
# Configurações de cores
# =======================
PASTEL_COLORS_50 = [
    "#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
    "#DEBB9B", "#FAB0E4", "#CFCFCF", "#B9F2F0", "#FFE599",
    "#AEC6CF", "#FF6961", "#77DD77", "#FDFD96", "#CBAACB",
    "#FFB347", "#FFD1DC", "#B2EBF2", "#FFDAC1", "#E0BBE4",
    "#FF9CEE", "#C1F0F6", "#B5EAD7", "#E2F0CB", "#FFB6B9",
    "#D6A4A4", "#E5FFCC", "#FDE2E4", "#B0E0E6", "#FFDAB9",
    "#C6E2FF", "#FFE4E1", "#D8BFD8", "#B0C4DE", "#FFFACD",
    "#E6E6FA", "#FFDEAD", "#F5F5DC", "#FAF0E6", "#F0FFF0",
    "#FFF0F5", "#FFE4B5", "#F0E68C", "#E0FFFF", "#F5DEB3",
    "#FDF5E6", "#E0EEE0", "#FFF8DC", "#F5F5DC", "#F0FFF0"
]

# =======================
# Países e mapeamento topojson (ID → país)
# =======================
COUNTRY_MAP = {
    "Afeganistão": "Afghanistan", "África do Sul": "South Africa", "Albânia": "Albania",
    "Alemanha": "Germany", "Andorra": "Andorra", "Angola": "Angola", "Antígua e Barbuda": "Antigua and Barbuda",
    "Arábia Saudita": "Saudi Arabia", "Argentina": "Argentina", "Armênia": "Armenia",
    "Austrália": "Australia", "Áustria": "Austria", "Azerbaijão": "Azerbaijan",
    "Bahamas": "Bahamas", "Bangladesh": "Bangladesh", "Barbados": "Barbados", "Bélgica": "Belgium",
    "Belize": "Belize", "Benin": "Benin", "Bielorrússia": "Belarus", "Bolívia": "Bolivia",
    "Bósnia e Herzegovina": "Bosnia and Herzegovina", "Botsuana": "Botswana", "Brasil": "Brazil",
    "Brunei": "Brunei", "Bulgária": "Bulgaria", "Burkina Faso": "Burkina Faso", "Burundi": "Burundi",
    "Butão": "Bhutan", "Cabo Verde": "Cape Verde", "Camarões": "Cameroon", "Camboja": "Cambodia",
    "Canadá": "Canada", "Catar": "Qatar", "Cazaquistão": "Kazakhstan", "Chile": "Chile", "China": "China",
    "Colômbia": "Colombia", "Coreia do Norte": "North Korea", "Coreia do Sul": "South Korea",
    "Costa Rica": "Costa Rica", "Croácia": "Croatia", "Cuba": "Cuba", "Dinamarca": "Denmark",
    "Egito": "Egypt", "Espanha": "Spain", "Estados Unidos": "United States", "Estônia": "Estonia",
    "Etiópia": "Ethiopia", "Filipinas": "Philippines", "Finlândia": "Finland", "França": "France",
    "Grécia": "Greece", "Guatemala": "Guatemala", "Holanda": "Netherlands", "Hungria": "Hungary",
    "Índia": "India", "Indonésia": "Indonesia", "Irlanda": "Ireland", "Itália": "Italy",
    "Japão": "Japan", "México": "Mexico", "Moçambique": "Mozambique", "Noruega": "Norway",
    "Nova Zelândia": "New Zealand", "Países Baixos": "Netherlands", "Panamá": "Panama",
    "Paraguai": "Paraguay", "Peru": "Peru", "Polônia": "Poland", "Portugal": "Portugal",
    "Reino Unido": "United Kingdom", "Rússia": "Russia", "Suécia": "Sweden", "Suíça": "Switzerland",
    "Uruguai": "Uruguay", "Venezuela": "Venezuela", "Vietnã": "Vietnam", "Zâmbia": "Zambia",
    "Zimbábue": "Zimbabwe"
}

# IDs do topojson para todos os países
COUNTRY_TO_ID = {
    "Afeganistão": 4, "África do Sul": 710, "Albânia": 8, "Alemanha": 276, "Andorra": 20, "Angola": 24,
    "Antígua e Barbuda": 28, "Arábia Saudita": 682, "Argentina": 32, "Armênia": 51, "Austrália": 36,
    "Áustria": 40, "Azerbaijão": 31, "Bahamas": 44, "Bangladesh": 50, "Barbados": 52, "Bélgica": 56,
    "Belize": 84, "Benin": 204, "Bielorrússia": 112, "Bolívia": 68, "Bósnia e Herzegovina": 70,
    "Botsuana": 72, "Brasil": 76, "Brunei": 96, "Bulgária": 100, "Burkina Faso": 854, "Burundi": 108,
    "Butão": 64, "Cabo Verde": 132, "Camarões": 120, "Camboja": 116, "Canadá": 124, "Catar": 634,
    "Cazaquistão": 398, "Chile": 152, "China": 156, "Colômbia": 170, "Coreia do Norte": 408,
    "Coreia do Sul": 410, "Costa Rica": 188, "Croácia": 191, "Cuba": 192, "Dinamarca": 208, "Egito": 818,
    "Espanha": 724, "Estados Unidos": 840, "Estônia": 233, "Etiópia": 231, "Filipinas": 608,
    "Finlândia": 246, "França": 250, "Grécia": 300, "Guatemala": 320, "Holanda": 528, "Hungria": 348,
    "Índia": 356, "Indonésia": 360, "Irlanda": 372, "Itália": 380, "Japão": 392, "México": 484,
    "Moçambique": 508, "Noruega": 578, "Nova Zelândia": 554, "Países Baixos": 528, "Panamá": 591,
    "Paraguai": 600, "Peru": 604, "Polônia": 616, "Portugal": 620, "Reino Unido": 826, "Rússia": 643,
    "Suécia": 752, "Suíça": 756, "Uruguai": 858, "Venezuela": 862, "Vietnã": 704, "Zâmbia": 894,
    "Zimbábue": 716
}