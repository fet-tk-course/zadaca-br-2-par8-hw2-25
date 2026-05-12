[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

Aplikacija predstavlja REST API za stomatološku ordinaciju. Omogućava upravljanje pacijentima i terminima pregleda kroz standardne HTTP metode (GET, POST, PUT, PATCH, DELETE). Sistem je razvijen koristeći FastAPI, SQLModel i SQLite bazu podataka.
Svrha aplikacije je da olakša evidenciju pacijenata (lični i medicinski podaci, alergije, anamneza, status osiguranja) i njihovih termina pregleda u ordinaciji.

## Tim

- **Student A**: Marinela Mitić - resurs: `/patients`
- **Student B**: [Ime Prezime] - resurs: `/resursi_b`

## Instalacija i pokretanje

### Preduvjeti

- Python 3.12 ili noviji
- pip

### Koraci

1. Klonirajte repozitorij:
```bash
git clone <url-repozitorija>
cd <naziv-repozitorija>
```

2. Kreirajte virtuelno okruženje:
```bash
python -m venv venv
```

3. Aktivirajte virtuelno okruženje:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalirajte zavisnosti:
```bash
pip install -r requirements.txt
```

5. Pokrenite aplikaciju:
```bash
uvicorn main:app --reload
```

6. Otvorite browser na adresi: `http://localhost:8000/docs`

## API Endpointi

### Resurs A: `/patients`

| Metoda | Ruta | Opis |
|--------|------|------|
| GET | `/patients/` | Lista svih pacijenata (sa query filterima) |
| GET | `/patients/{patient_id}` | Dohvatanje pacijenta po ID-u |
| POST | `/patients/` | Kreiranje novog pacijenta (status 201) |
| PUT | `/patients/{patient_id}` | Potpuna zamjena pacijenta |
| PATCH | `/patients/{patient_id}` | Djelimično ažuriranje pacijenta |
| DELETE | `/patients/{patient_id}` | Brisanje pacijenta (status 204) |

**Query parametri za GET /patients/:**

| Parametar | Tip | Opis | Primjer |
|-----------|-----|------|---------|
| `last_name` | string | Pretraga po prezimenu (case-insensitive, parcijalna) | `?last_name=mit` |
| `first_name` | string | Pretraga po imenu (case-insensitive, parcijalna) | `?first_name=mar` |
| `gender` | string | Filter po spolu (M/F) | `?gender=F` |
| `has_insurance` | boolean | Filter po statusu osiguranja | `?has_insurance=true` |

Filteri se mogu kombinovati, npr. `?last_name=mitic&gender=F&has_insurance=true`.

**Primjer zahtjeva:**
```bash
# Kreiranje novog pacijenta
curl -X POST "http://localhost:8000/patients/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Marinela",
    "last_name": "Mitic",
    "date_of_birth": "1995-06-15",
    "phone": "061123456",
    "gender": "F",
    "email": "marinela@example.com",
    "has_insurance": true,
    "weight_kg": 62.5,
    "allergies": "Penicilin"
  }'

# Lista pacijenata sa filterom
curl -X GET "http://localhost:8000/patients/?last_name=mitic&gender=F"

# Dohvatanje pacijenta po ID-u
curl -X GET "http://localhost:8000/patients/1"

# Djelimično ažuriranje (PATCH)
curl -X PATCH "http://localhost:8000/patients/1" \
  -H "Content-Type: application/json" \
  -d '{"phone": "061999888"}'

# Brisanje pacijenta
curl -X DELETE "http://localhost:8000/patients/1"
```


### Resurs B: `/resursi_b`

[Analogno kao za Resurs A]

## Korištenje AI alata

### Alat: Claude (Anthropic)

**Model:** Claude Sonnet 4.6

**Primjer 1:**
- **Prompt:** "Implementirala sam prvu verziju modela `Patient` i CRUD endpointa. Moj model ima polja tipa `str`, `int` i `bool`. Zadatak traži najmanje pet polja različitih tipova uključujući i `float`. Koje polje tipa `float` bi imalo smisla u kontekstu stomatološke ordinacije?"
- **Kako je pomoglo:** AI mi je dao nekoliko prijedloga za polje tipa float, a ja sam izabrala weight_kg (težinu pacijenta) jer mi je najlogičnije vezana za stomatološku ordinaciju — doziranje lokalne anestezije računa se prema težini pacijenta. Uz to, razgovor me je naveo da preispitam i druge tipove podataka u modelu te sam samostalno odlučila poboljšati validaciju datuma.
- **Prilagodbe:** Dodala sam polje weight_kg u sve tri šeme (`Patient`, `PatientCreate`, `PatientUpdate`) i izmijenila tip `date_of_birth` iz `str` u `date`.

**Primjer 2:**
- **Prompt:** "Implementirala sam filter po prezimenu u GET endpointu, ali primijetila sam da pretraga radi samo kad korisnik unese tačno prezime sa pravilnim velikim slovima. Kako da omogućim pretragu koja ne razlikuje velika i mala slova i koja radi i kada se unese samo dio prezimena?"
- **Kako je pomoglo:** AI mi je objasnio razliku između SQL operatora `like` i `ilike` — `ilike` je verzija koja ignoriše veličinu slova. Pojasnio je i ulogu wildcard znaka `%` koji omogućava parcijalno podudaranje (npr. `%mit%` će uhvatiti i "Mitić" i "Smitović").
- **Prilagodbe:** Na osnovu objašnjenja, zamijenila sam operator u svojoj `read_patients` funkciji i pravilno postavila wildcardove oko vrijednosti iz query parametra. Istu logiku sam zatim primijenila i na novi filter po imenu (`first_name`).

## Napomene

- Aplikacija koristi SQLite bazu podataka (`database.db`) koja se automatski kreira pri prvom pokretanju.
- Svi endpointi koji primaju ID vraćaju **HTTP 404** ako resurs nije pronađen.
- PATCH endpoint koristi `exclude_unset=True` kako bi se ažurirala samo polja koja je korisnik eksplicitno poslao.
- Pretraga po imenu i prezimenu je **case-insensitive** (`ilike` operator) i podržava **parcijalno podudaranje** (npr. `last_name=mit` vraća sve pacijente čije prezime sadrži "mit").
