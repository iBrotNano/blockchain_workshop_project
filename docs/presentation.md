---
marp: true
title: "Python Workshop"
paginate: true
theme: uncover
class: invert
---

#### Die Idee

Ich möchte einen Status einer Softwareveröffentlichung in einer Blockchain speichern um nachvollziehen zu können, welcher Code bzw. welche Dateien von wem, wann veröffentlicht wurde.

---

#### Die Daten, die gespeichert werden sollen

- Name der Software
- Versionsnummer
- Zeitstempel der Veröffentlichung
- Autor, z.B. Name des Unternehmens
- Kontaktinformationen wie E-Mail
- Public Key des Autors
- Commit-Hash
- URL zum Repository
- Merkle-Root der bereitgestellten Dateien

---

#### Warum diese Daten?

Nehmen wir an jemand lädt eine Software aus irgendeiner Quelle (Dateien + Adresse in Datenbank).

Infos können abgerufen werden.

---

Name, Versionsnummer, Zeitstempel, Autor, Kontaktinformationen zum Vergleich mit z.B. dem Impressum der Webseite, von der die Software heruntergeladen wurde.

---

Merkle Root der Dateien == Merkle Root in der DB?

Wenn ja, dann können wir sicher sein, dass die Dateien nicht verändert wurden.

---

Commit Hash + Url zum Repository, zeigt aus welchen Sourcen die Software gebaut wurde. (Deterministische Builds sind oft möglich)

Zusätzlich signierung der Commit durch GPG möglich.

--- 

Author veröffentlicht Public Key.

Public Key zum verifizieren der Signatur, um sicherzustellen, dass die Informationen integer sind und vom Autor stammen.

--- 

#### Chain of Trust

Author >> Commit >> Repository >> Build >> Blockchain

---

#### Key Pair

Author generiert ein Key Pair (Public + Private Key).

Gesichert wird in der Windows Keychain.

`Address`, `CustomAddress`, `SolanaAddress`, `Index`

---

#### Deployment Record

`Project` listet Dateien und beachtet `.gitignore`
`MerkleRoot` erstellt die Merkle Root des Verzeichnisses
`DeploymentRecord` serialisiert die Daten mit `msgpack`, hasht sie und signiert sie mit dem Private Key.
`Client` sendet Record zum Server

---

#### Block

Baut Block in `peer_node._handle_add_deployment_record()`

---

#### Peer Connection

`python .\src\service\main.py`

`python .\src\service\main.py --host 127.0.0.1 --port 5001 --bootstrap 127.0.0.1:5000`

`python .\src\service\main.py --host 127.0.0.1 --port 5002 --bootstrap 127.0.0.1:5000`