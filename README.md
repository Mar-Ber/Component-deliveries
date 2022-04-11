## Planning component deliveries in a production plant

#### The project is part of the thesis

The aim of the project is to implement an algorithm that approximates the supply problem components in the factory. The resulting application enables simulation of the problem for the created factory model and finding a solution for it.

The factory model can be broken down into many individual components such as workers, machines, transport routes, products, etc. It requires necessity organize the data into certain groups, each of which will refer to a separate one parts of the whole model. Classes allow for this type of implementation. They make it possible grouping data and creating functions that operate on that data. Concept adopted class implementation implies using only attributes, that is, storing a group of data inside an object representing a certain component of the factory. For operating on these external functions will be responsible for the data. For the implementation of the application was defined the following classes:
* Vehicle - class defines a vehicle by assigning average, maximum speed capacity and operating costs,
* Worker - klasa definiuje pracownika poprzez przypisanie mu pojazdu, przechowywanie obecnego oraz całkowitego czasu pracy, kosztu zatrudnienia, aktualnej pojemności pojazdu, przebytego dystansu, list aktualnie oraz łącznie zaopatrywanych indeksów komponentów, listy odwiedzonych komórek produkcyjnych oraz macierzy ilości dostarczonych komponentów,
* Component - klasa definiuje komponent potrzebny do produkcji, poprzez przypisanie mu unikalnego indeksu, typu pojemnika, w którym jest transportowany, pojemności tego pojemnika oraz kosztu jednostkowego,
* Product - klasa definiuje produkt, poprzez przypisanie mu unikalnego indeksu, słownika indeksów komponentów potrzebnych do produkcji wraz z niezbędną liczbą każdego z nich, określenie liczby sztuk produkowanych w ciągu minuty oraz zysku jednostkowego,
* Store - klasa definiuje lokalny magazyn komponentów w gnieździe produkcyjnym, poprzez przypisanie mu unikalnego indeksu, numeru sekcji fabryki, położenia w tej sekcji, maksymalnej liczby przechowywanych pojemników z komponentami, list indeksów zaopatrywanych maszyn oraz produkowanych produktów, a także słownika zawierającego indeksy komponentów oraz odpowiadające im zbiorcze zużycie na minutę dla wszystkich maszyn w gnieździe,
* Factory - klasa definiuje charakterystykę fabryki, przechowując informację o liczbie sekcji, ich długości oraz odległości od siebie, dystansie do magazynu głównego, łącznej liczbie maszyn oraz gniazd produkcyjnych na terenie zakładu, a także słowniki typów pojemników oraz odpowiadających im rozmiarów i pojemności,
* ProductionPlan - klasa definiuje pojedynczy wpis w liście planu produkcyjnego zawierający indeks komponentu, procentowe zużycie na minutę (względem możliwej maksymalnej ilości w magazynie lokalnym), indeks produktu, do którego dany komponent jest potrzebny, indeks maszyny, na której produkt jest tworzony, indeks magazynu lokalnego, do którego należy dostarczyć dany komponent, koszty na minutę produkcji, typ kontenera, w którym komponent jest przechowywany oraz maksymalną liczbę pojemników w danym magazynie lokalnym. Klasa ta służy do zebrania najistotniejszych informacji o produkcji.

The UML diagram of defined classes is as follows:


