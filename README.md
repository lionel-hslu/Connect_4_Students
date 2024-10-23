# Raspi Connect 4
Student Project from **Python Advanced**, HS24

## Administratives
- Projekt als Semesterleistung (40%)
- 2er-Teams
- Spielvarianten:
  - Lokal auf dem PC
  - Auf dem Raspberry Pi sowie im Terminal
  - Über das Netzwerk via REST-API und Flask-Webserver
  - Implementierung eines Bots (Wettbewerb am Ende des Semesters)
- Video 4-5 Minuten zum Projekt:
  - Aufbau
  - Schwierigkeiten / Highlights etc.
  - Demo

## Game Architecture
Das **Connect 4 Game** kann auf 4 verschiedene Arten gespielt werden:
- Lokal (2 Player) auf `CLI`
- Lokal (2 Player) auf `SenseHat`
- Remote (2x 1 Player) auf `CLI`
- Remote (2x 1 Player) auf `SenseHat`

![rough_draft](./imgs/class_diagramm.png)

Diese verschiedenen Spielvarianten unterscheiden sich hauptsächlich durch **unterschiedliche `Player` Klassen**, die alle bestimmte **abstrakte Methoden** auf unterschiedliche Weise implementieren. Die wichtigsten abstrakten Methoden sind:
- `make_move`: Ermöglicht es dem Benutzer, eine Spalte auszuwählen, in die eine Münze fallen gelassen wird
- `visualize`: Visualisiert den aktuellen Board-Zustand für den Benutzer
- `register_in_game`: Registriert den Player in einem bestimmten Game
- `get_game_status`: Ruft den aktuellen Status des Games ab

<div style="text-align: center;">
<img src="./imgs/legend.png" alt="legend" width="250"/>
</div>

## Classes
Das komplette Game enthält die folgenden Klassen:

- `Connect4`: Enthält die **Game Logic**
  - Details unter [Game](#connect4---game)
- `Server`: Stellt Methoden aus `Connect4` für Remote-Player zur Verfügung
  - Details unter [Server](#server)
- `Player`: Abstrakte Klasse (beschreibt, was ein Player können muss)
  - `Player_Local`: Player, der Methoden aus einem lokal verfügbaren `Connect4`-Objekt verwendet.
    - `Player_Raspi_Local`: Lokaler Player auf einem Raspberry Pi (verwendet das `SenseHat`)
    - Details unter [Local Player](#local-player)
  - `Player_Remote`: Player, der **REST-API-Endpunkte** verwendet, um über den `Server` mit `Connect4` zu interagieren
    - `Player_Raspi_Remote`: Remote Player auf einem Raspberry Pi (verwendet das `SenseHat`)
    - Details unter [Remote Player](#remote-player)

- `Coordinator_Local`: Koordiniert **2 lokale Player** (auf demselben Gerät)
  - Details unter [Local Interactions](#local-interactions)
- `Coordinator_Remote`: Koordiniert **1 lokalen Player** (auf demselben Gerät) mit **1 Remote Player** (auf einem anderen Gerät) durch Kommunikation mit dem ``Server``.
  - Details unter [Remote Interaction](#remote-interaction)

### Connect4 - Game
Diese Klasse enthält die grundlegende Game Logic.
Sie definiert den **Game State** (`get_game_state()`):
- **was** ein **erlaubter Zug** ist
- **wann** ein Player **gewinnt** (`winner`)
- **wessen** **Zug** es ist (`active_player`)
- **welcher** **Zug** gerade stattfindet (`turn_number`)

Außerdem kann sie den aktuellen **Board-Zustand** zurückgeben (`get_board()`). Sie gibt dann ein `8x7 numpy array` zurück, das enthält:
  - `'X'` für einen Player
  - `'O'` für den anderen Player
  - `''` für die leeren Felder

### Server
Der ``Connect4_Server`` - Server bietet **vier API-Endpunkte** an und stellt die Hauptmethoden (beschrieben unter [Game](#connect4---game) aus der `Connect4`-Klasse) zur Verfügung.

Diese werden in einer **Swagger-Dokumentation** beschrieben, die unter [http://127.0.0.1:5000/swagger/connect4/](http://127.0.0.1:5000/swagger/connect4/) zugänglich ist, sobald der **Server läuft**.

![swagger_api](./imgs/swagger_api.PNG)

### Remote Player
Die Remote-Player verwenden die **laufenden API-Endpunkte**, um Informationen an die ``Connect4``-Klasse zu senden und von dieser zu empfangen.

### Local Player
Die lokalen Player verwenden eine verfügbare **Instanz** der **gleichen `Connect4`-Klasse**, um Informationen zu demselben Game zu senden und zu empfangen.

### Local Interactions
Wenn lokal gespielt wird (2 Player auf demselben Gerät), erfolgt die Interaktion zwischen den Klassen wie folgt:

<div style="text-align: center;">
<img src="./imgs/local_interaction.png" alt="local_interaction" width="450"/>
</div>

**Hinweis**: Die ``Player`` können entweder über das `CLI` oder das `SenseHat` (auf dem Raspberry Pi) gesteuert werden.

### Remote Interactions
Wenn remote gespielt wird (2 Player auf 2 Geräten), erfolgt die Interaktion zwischen den Klassen wie folgt:

<div style="text-align: center;">
<img src="./imgs/remote_interaction.png" alt="remote_interaction" width="450"/>
</div>

**Hinweis**: Auch hier können die ``Player`` entweder über das `CLI` oder das `SenseHat` (auf dem Raspberry Pi) gesteuert werden.

## Play the Game

Stelle sicher, dass du die [Requirements](#requirements) erfüllst.
Versuche dann, ein [lokales](#local-game) oder [remote](#remote-game) Game zu starten:

### Local Game

1. Starte `local_coordinator.py` in einem **Terminal**
   - Erstellt **2 lokale Player**
     - Entweder ``CLI`` oder `SenseHat`-Player (Standard ist `CLI`)

### Remote Game
1. Starte `server.py` in einem **ersten Terminal**
   - Notiere die `IP-Adresse` des `Servers`
2. Starte `remote_coordinator.py` in einem **zweiten Terminal**
    - Gib die `IP-Adresse` des `Servers` als Ziel an
    - Spiele als **Player 1** im `CLI` oder auf dem `SenseHat` (Standard ist `CLI`)
3. Starte `remote_coordinator.py` in einem **dritten Terminal**
   - Gib die `IP-Adresse` des `Servers` als Ziel an
   - Spiele als **Player 2** im `CLI` oder auf dem `SenseHat` (Standard ist `CLI`)

## Requirements
Um alle Anforderungen für das Game zu erfüllen, gehe wie folgt vor:
1. Erstelle eine neue `conda`- oder `venv`-**Umgebung** und **aktiviere** sie.
2. Wechsle mit `cd` in diesen Ordner des Spieles (wo das `setup.py` File ist)
3. Führe den folgenden Befehl aus:

```bash
pip install .
```


Dies **installiert alle Abhängigkeiten**, die in der `setup.py` aufgelistet sind.

4. Spiele das Game in einer der [verfügbaren Versionen](#game-architecture).

# Raspberry Pi
Der Raspberry Pi benötigt eine schnelle **Korrektur**, um das Verschieben, Ändern usw. von Dateien zu ermöglichen.

1. Wechsle in den Ordner ``home/pi``

2. **Ändere die Berechtigungen** des `student`-Ordners (und aller ``Unterordner``) mit:

```bash
sudo chmod -R 777 student
```