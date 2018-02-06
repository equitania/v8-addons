## Modul eq_stock_account_compatibility

#### 06.02.2018
#### Version 1.0.5
##### CHG/FIX
- Ticket 5247: Odoo Standard Bug => durch die in der Action definierte Domain war nur die Gruppierung sichtbar, jedoch nach dem kompletten Aufklappen, waren keine Einträge mehr zu sehen.

#### 30.11.2016
#### Version 1.0.4
##### CHG
- SQl Statement aus dem Standard übernommen (Ticket 5048). Anpassung Anzeige nur von aktivierten Lager.

#### 15.12.2016
#### Version 1.0.3
##### CHG
- Sprachdatei ersetzt, Beschreibung ergänzt

#### 14.12.2016
#### Version 1.0.2
##### ADD
- Sprachdatei angelegt damit keine Warnings mehr in der Konsole angezeigt werden

#### 17.12.2015
#### Version 1.0.0
##### Veröffentlichung
- Kompatibilitätsmodul für das equitania und stock_account Modul, wodurch die Berechnung des Lagerwertes (Durchschnitt) funktioniert.
- Aktuelle Bestandsbewertung des Lagers überarbeitet, sodass nicht stock.moves für die id genutzt werden, sondern die stock.quants. Somit fehlen keine Einträge, wenn in einem stock.move unterscheidliche stock.quants hinterlegt sind.