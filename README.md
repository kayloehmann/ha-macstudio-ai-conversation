# MacStudio AI Conversation — Home-Assistant-Integration

Conversation-Agent für Home Assistant, der die lokalen OpenClaw-Agenten auf
**`macstudio-ai`** über eine abgesicherte, OpenAI-kompatible Bridge anspricht.
Natives Tool-Calling erlaubt echte HA-Steuerung über die Assist-API.

Die Integration trennt normale Sprachdialoge vom privaten Dokumentzugriff.
Paperless ist nur im angemeldeten Text-Assist und auf ausdrücklich freigegebenen
Satelliten verfügbar.

## Voraussetzung

Die MacStudio-AI-Bridge läuft im privaten Netz. Die lokale Basis-URL ist
`http://10.107.0.186:19790/v1`; der getrennte Bridge-Schlüssel ist erforderlich.

## Installation

**Via HACS (Custom Repository):** HACS → ⋮ → *Custom repositories* → URL dieses
Repos, Kategorie *Integration* → installieren → HA neu starten.

**Manuell:** `custom_components/macstudio_ai/` nach `/config/custom_components/`
kopieren, HA neu starten.

## Einrichtung

*Einstellungen → Geräte & Dienste → Integration hinzufügen → „MacStudio AI Conversation"*

1. **Basis-URL** bestätigen und den Bridge-Schlüssel eintragen.
2. Unter *Konfigurieren*: **Instruktionen** (System-Prompt) anpassen,
   **Control Home Assistant** auf *Assist* stellen (Steuerung), Modell/Tokens
   nach Bedarf.
3. *Einstellungen → Sprachassistenten*: Pipeline auf diesen Agenten zeigen lassen.

4. Nur private Satelliten für Paperless freigeben.

## Agenten

`openclaw/macstudio-ai` beantwortet Haussteuerungs- und Wissensfragen.
`openclaw/macstudio-ai-private` besitzt zusätzlich rein lesenden Paperless-Zugriff.
Die Integration wählt den privaten Agenten nur anhand der konfigurierten
Gerätefreigabe oder eines angemeldeten Text-Assist-Dialogs.

Jede HA-Konversation erhält eine getrennte OpenClaw-Sitzung. Geräte- und
Gesprächskennung werden nicht an externe Dienste weitergegeben.
