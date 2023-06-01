# TEMA 1 ASC David Mihalcenco 331CB

## MARKETPLACE
- Init
    - cons_cart_list : lista cu toti consumatorii
    - producer_list : lista cu toti producatorii
    - lock-uri pentru functii
    - logging

- Register_producer
    - creez o lista pentru producator, si incrementez producer_id

- Pubish
    - verific daca lista producatorului este plina, daca da atunci astept
    daca nu adaug productul in lista lui

- New_cart
    - creez o lista pentru consumator, si incrementez cart_id

- Add_to_cart
    - caut daca produsul dorit exista la toti producatorii, daca l-am gasit
    atunci il sterg din lista producatorului si il adaug in lista consumatorului

- Remove_rom_cart
    - incerc sa sterg productul din cos, daca el exista atunci l-am sters, si 
    il adaug inapoi in lista producatorului

- Place_order
    - intorc lista unui anumit cos, adica ce se afla acolo

- TestMarketplace
    - aici am testat fiecare functie si am facut cate doua cazuri la fiecare,
    atunci cand se poate adauga sau sterge, cand exista sau nu exista, cand
    am creat un cos sau un producator corect, adica cu id_urile corecte.

## PRODUCER
- run
    - creez un producer, si creez produse atat timp cat imi permite adica, 
    cate produse poate sa aiba un producator la un anumit moment de timp,
    daca este full atunci astept, daca nu creez. Daca am putut publica acest
    product atunci sterg din cantitatea de produse, daca nu astept timpul dat

## CONSUMER
- run
    - creez un cos nou, verific de ce tip este operatia daca sa sterg sau sa 
    adaug un element in cos, daca am putut sa fac una din operatii atunci 
    cantitatea produselor se scade, daca nu am putut atunci astept acel timp.