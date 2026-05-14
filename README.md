[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

Aplikacija predstavlja REST API za stomatološku ordinaciju. Omogućava upravljanje pacijentima i terminima pregleda kroz standardne HTTP metode (GET, POST, PUT, PATCH, DELETE). Sistem je razvijen koristeći FastAPI, SQLModel i SQLite bazu podataka.
Svrha aplikacije je da olakša evidenciju pacijenata (lični i medicinski podaci, alergije, anamneza, status osiguranja) i njihovih termina pregleda u ordinaciji.

## Tim

- **Student A**: Marinela Mitić - resurs: `/patients`
- **Student B**: Iman Osmić - resurs: `/appointments`

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


### Resurs B: `/appointments`

| Metoda | Ruta | Opis |
|--------|------|------|
| GET | `/appointments/` | Lista svih termina pregleda sa query filterima |
| GET | `/appointments/{appointment_id}` | Dohvatanje termina pregleda po ID-u |
| POST | `/appointments/` | Kreiranje novog termina pregleda (status 201) |
| PUT | `/appointments/{appointment_id}` | Potpuna zamjena termina pregleda |
| PATCH | `/appointments/{appointment_id}` | Djelimično ažuriranje termina pregleda |
| DELETE | `/appointments/{appointment_id}` | Brisanje termina pregleda (status 204) |

**Query parametri za GET /appointments/:**

| Parametar | Tip | Opis | Primjer |
|-----------|-----|------|---------|
| `patient_id` | integer | Filter po ID-u pacijenta | `?patient_id=2` |
| `status_filter` | string | Filter po statusu termina | `?status_filter=scheduled` |
| `is_confirmed` | boolean | Filter po potvrdi termina | `?is_confirmed=true` |

Filteri se mogu kombinovati, npr. `?patient_id=2&status_filter=scheduled&is_confirmed=true`.

**Primjer zahtjeva:**
```bash
# Kreiranje novog termina pregleda
curl -X POST "http://localhost:8000/appointments/" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 2,
    "appointment_time": "2026-05-20T10:30:00",
    "procedure_name": "Dental checkup",
    "duration_minutes": 30,
    "price": 50.0,
    "status": "scheduled",
    "is_confirmed": true,
    "notes": "First appointment"
  }'

# Lista termina sa filterom po pacijentu
curl -X GET "http://localhost:8000/appointments/?patient_id=2"

# Lista termina sa filterom po statusu
curl -X GET "http://localhost:8000/appointments/?status_filter=scheduled"

# Dohvatanje termina po ID-u
curl -X GET "http://localhost:8000/appointments/1"

# Djelimično ažuriranje termina
curl -X PATCH "http://localhost:8000/appointments/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# Potpuna zamjena termina
curl -X PUT "http://localhost:8000/appointments/1" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 2,
    "appointment_time": "2026-05-21T12:00:00",
    "procedure_name": "Tooth cleaning",
    "duration_minutes": 45,
    "price": 70.0,
    "status": "scheduled",
    "is_confirmed": true,
    "notes": "Updated appointment"
  }'

# Brisanje termina
curl -X DELETE "http://localhost:8000/appointments/1"
```

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

### Alat: ChatGPT

**Model:** GPT-5.5 Thinking

**Primjer 1:**
- **Prompt:** "Radim svoj dio REST API zadaće za domenu stomatološka ordinacija. Kolegica je implementirala resurs `Patient`, a ja trebam implementirati resurs `Appointment`. Kako da napravim SQLModel model za termin pregleda koji će biti povezan sa pacijentom preko `patient_id`?"
- **Kako je pomoglo:** AI mi je pomogao da pravilno osmislimo strukturu modela `Appointment` i da termin pregleda povežemo sa pacijentom preko stranog ključa `patient_id`. Objašnjeno mi je da `Appointment` i `Patient` ostaju dva odvojena resursa, ali da su logički povezani jer svaki termin pripada jednom pacijentu.
- **Prilagodbe:** Kod sam prilagodila domeni stomatološke ordinacije tako što sam dodala polja `appointment_time`, `procedure_name`, `duration_minutes`, `price`, `status`, `is_confirmed` i `notes`. Također sam dodala šeme `AppointmentCreate` i `AppointmentUpdate`, pri čemu su u `AppointmentUpdate` sva polja opcionalna.

**Primjer 2:**
- **Prompt:** "Imam model `Appointment` i trebam napraviti kompletne CRUD endpoint-e u FastAPI aplikaciji: GET, POST, PUT, PATCH i DELETE. Kako da u `PATCH` endpointu ažuriram samo ona polja koja korisnik pošalje i kako da vratim 404 ako termin ne postoji?"
- **Kako je pomoglo:** AI mi je pomogao da razumijem razliku između `PUT` i `PATCH` zahtjeva. Kod `PUT` se šalju svi podaci i radi se potpuna zamjena resursa, dok se kod `PATCH` šalju samo polja koja se mijenjaju. Objašnjeno mi je i zašto se koristi `exclude_unset=True`, jer se tako izbjegava slučajno prepisivanje polja koja korisnik nije poslao.
- **Prilagodbe:** U `routes_b.py` sam implementirala sve CRUD rute za `/appointments`. Dodala sam provjere za nepostojeći termin i nepostojećeg pacijenta pomoću `HTTPException(status_code=404)`. Također sam dodala query filtere `patient_id`, `status_filter` i `is_confirmed`, te povezala `appointments_router` u `main.py`.

## Napomene

- Aplikacija koristi SQLite bazu podataka (`database.db`) koja se automatski kreira pri prvom pokretanju.
- Svi endpointi koji primaju ID vraćaju **HTTP 404** ako resurs nije pronađen.
- PATCH endpoint koristi `exclude_unset=True` kako bi se ažurirala samo polja koja je korisnik eksplicitno poslao.
- Pretraga po imenu i prezimenu je **case-insensitive** (`ilike` operator) i podržava **parcijalno podudaranje** (npr. `last_name=mit` vraća sve pacijente čije prezime sadrži "mit").


## Provjera zadaće 2 - student A

### Z1

U `PatientCreate` modelu dodana su dva Pydantic validatora:

- **`first_name`** - ne smije biti prazan string. Ako korisnik pošalje prazno ime ili samo razmake, vraća se HTTP 422.
- **`weight_kg`** - ako je polje poslano, mora biti veće od nule. Pošto je weight_kg opcionalno, u validatoru prvo provjeravam da li je vrijednost poslana (if v is not None), a tek onda provjeravam da li je veća od 0.

U POST endpointu /patients/ dodana provjera duplikata po emailu. Ako pacijent sa istim emailom već postoji u bazi, vraća se HTTP 409 Conflict. Email koristim kao jedinstveno polje jer je logično da se ne mogu dva pacijenta voditi pod istom email adresom.

Primjer odgovora kada se pokuša kreirati pacijent sa već postojećim emailom:

```json
{
  "detail": "Pacijent sa emailom 'test@test.com' već postoji"
}
```

### Z2 

Dodan novi GET endpoint koji vraća ukupan broj pacijenata u bazi. Endpoint koristi SQL funkciju `func.count()`.

Ruta /count je definisana prije rute /{patient_id} u kodu, jer bi inače FastAPI pokušao da protumači "count" kao vrijednost parametra patient_id i to bi izazvalo grešku.

Primjer zahtjeva:

```bash
curl -X GET "http://localhost:8000/patients/count"
```

Odgovor:

```json
{
  "ukupno": 5
}
```

### HTTP statusi koji se mogu vratiti

| Situacija | Status |
|-----------|--------|
| Pacijent uspješno kreiran | 201 |
| Pacijent uspješno obrisan | 204 |
| Pacijent sa istim emailom već postoji | 409 |
| Pacijent nije pronađen po ID-u | 404 |
| Validacija nije prošla (prazno ime, težina ≤ 0) | 422 |