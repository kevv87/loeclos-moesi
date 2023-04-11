Para la interfaz vamos a hacerla lo más desacoplada posible

- Cada objeto va a tener un atributo logger, cada vez que pase algo, vamos 
  a usar el metodo log de ese logger.
- Ese metodo log va a ser implementado por las diferentes interfaces
  que vayamos a usar, por el momento solo vamos a usar consola y REST
- Log recibe n argumentos, el primero es la accion, el resto son los
  objetos que están involucrados en la accion

Acciones:
  1. Processor creation
    1. Id procesador
  2. Generated_calc_operation: Define que se generó una operación de calculo
    1. Procesador creador
  3. Generated_write_operation:
    1. Procesador creador
    2. Direccion
    3. Dato
  4. Gererated_read_operation:
    1. Procesador creador
    2. Direccion
  5. Generated_response_operation:
    1. Procesador creador
    2. Direccion
    3. Dato
  6. Cache read:
    1. Procesador dueño
    2. Direccion que está leyendo
  7. Cache Hit:
    1. Procesador dueño
    2. Numero de bloque
    3. Direccion leida
    4. Dato leido
    5. Nuevo estado del bloque
  8. Cache Miss:
    1. Procesador
    2. Direccion
  9. Cache requesting value bus:
    1. Procesador 
    2. Direccion
  10. Cache gives response:
    1. Giving processor
  11. Retrieving from memory
    1. Address
    2. Data
  12. Replacing block:
    1. Procesador
    2. Numero de bloque
    3. Direccion
    4. Dato
    5. Nuevo estado del bloque

  13. Replacing block:
    1. Procesador
    2. Numero de bloque
    3. Direccion
    4. Dato
    5. Nuevo estado del bloque
  14. Updating block:
    1. Procesador
    2. Numero de bloque
    3. Direccion
    4. Dato
    5. Nuevo estado del bloque
  15. Writeback:
    1. Procesador
    2. Direccion
    3. Dato


