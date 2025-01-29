# Liligo-T-TWR Bluetooth Dateiübertragung

Dieses Projekt ermöglicht die drahtlose Übertragung von Dateien über Bluetooth mit dem Liligo-T-TWR.

## Installation und Einrichtung

### 1️⃣ Liligo-T-TWR mit PlatformIO flashen

Um den Liligo-T-TWR zu programmieren, folgen Sie diesen Schritten:

1. Installieren Sie [Visual Studio Code](https://code.visualstudio.com/) und [Python](https://www.python.org/).
2. Suchen Sie nach dem `PlatformIO`-Plugin in den Visual Studio Code-Erweiterungen und installieren Sie es.
3. Starten Sie `Visual Studio Code` nach der Installation neu.
4. Öffnen Sie den Projektordner:
   - Klicken Sie auf **Datei** → **Ordner öffnen** und wählen Sie das `T-TWR`-Verzeichnis aus.
5. Öffnen Sie die Datei `platformio.ini` und aktivieren Sie die gewünschte Konfiguration:
   - Kommentieren Sie nicht benötigte Zeilen aus, sodass nur **eine Konfiguration aktiv** bleibt.
6. Klicken Sie auf das (✔) Symbol unten links, um den Code zu kompilieren.
7. Verbinden Sie das Liligo-T-TWR-Board über USB mit dem Computer.
8. Klicken Sie auf das (→) Symbol, um die Firmware hochzuladen.
9. Öffnen Sie den seriellen Monitor mit dem (Plug-Symbol), um die Ausgabe zu beobachten.

### 2️⃣ Projekt starten

1. Nach dem Flashen starten Sie den Liligo-T-TWR.
2. Führen Sie das Skript `receiver.py` aus:
   - Dieses Skript empfängt eingehende Datenpakete.
   - **Achtung:** Vergessen Sie nicht, das SDR-Modul einzustecken!
3. Zum Senden einer Datei starten Sie das Skript `Bluetoothfunk.py`:
   - **Wichtig:** Bluetooth am Laptop aktivieren!
   - Falls Sie eine eigene Datei senden möchten, ersetzen Sie `output2.wav` durch Ihre Datei und benennen Sie sie entsprechend um.

Nach diesen Schritten sollte die Dateiübertragung über Bluetooth mit dem Liligo-T-TWR funktionieren.
