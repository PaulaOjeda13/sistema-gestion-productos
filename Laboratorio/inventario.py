import json

class Producto:
    def __init__(self, nombre, precio, cantidad_en_stock):
        self._nombre = nombre
        self._precio = precio
        self._cantidad_en_stock = cantidad_en_stock

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = valor

    @property
    def cantidad_en_stock(self):
        return self._cantidad_en_stock

    @cantidad_en_stock.setter
    def cantidad_en_stock(self, valor):
        if valor < 0:
            raise ValueError("La cantidad en stock no puede ser negativa.")
        self._cantidad_en_stock = valor

    def __str__(self):
        return f"{self.nombre} - Precio: {self.precio} - Cantidad en stock: {self.cantidad_en_stock}"

    def actualizar_stock(self, cantidad):
        self.cantidad_en_stock += cantidad


class ProductoElectronico(Producto):
    def __init__(self, nombre, precio, cantidad_en_stock, garantia):
        super().__init__(nombre, precio, cantidad_en_stock)
        self._garantia = garantia

    @property
    def garantia(self):
        return self._garantia

    @garantia.setter
    def garantia(self, valor):
        if valor < 0:
            raise ValueError("La garantía no puede ser negativa.")
        self._garantia = valor

    def __str__(self):
        return super().__str__() + f" - Garantía: {self.garantia} años"


class ProductoAlimenticio(Producto):
    def __init__(self, nombre, precio, cantidad_en_stock, fecha_vencimiento):
        super().__init__(nombre, precio, cantidad_en_stock)
        self._fecha_vencimiento = fecha_vencimiento

    @property
    def fecha_vencimiento(self):
        return self._fecha_vencimiento

    @fecha_vencimiento.setter
    def fecha_vencimiento(self, valor):
        if not valor:
            raise ValueError("La fecha de vencimiento no puede estar vacía.")
        self._fecha_vencimiento = valor

    def __str__(self):
        return super().__str__() + f" - Fecha de vencimiento: {self.fecha_vencimiento}"


class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def eliminar_producto(self, nombre):
        self.productos = [p for p in self.productos if p.nombre != nombre]

    def actualizar_producto(self, nombre, cantidad):
        for producto in self.productos:
            if producto.nombre == nombre:
                producto.actualizar_stock(cantidad)

    def listar_productos(self):
        for producto in self.productos:
            print(producto)

    def guardar_datos(self, archivo):
        try:
            with open(archivo, 'w') as f:
                json.dump([p.__dict__ for p in self.productos], f)
        except IOError as e:
            print(f"Error guardando los datos: {e}")

    def cargar_datos(self, archivo):
        try:
            with open(archivo, 'r') as f:
                productos_cargados = json.load(f)
                for p in productos_cargados:
                    if 'garantia' in p:
                        producto = ProductoElectronico(p['_nombre'], p['_precio'], p['_cantidad_en_stock'], p['_garantia'])
                    elif 'fecha_vencimiento' in p:
                        producto = ProductoAlimenticio(p['_nombre'], p['_precio'], p['_cantidad_en_stock'], p['_fecha_vencimiento'])
                    else:
                        producto = Producto(p['_nombre'], p['_precio'], p['_cantidad_en_stock'])
                    self.productos.append(producto)
        except IOError as e:
            print(f"Error cargando los datos: {e}")

if __name__ == "__main__":
    inventario = Inventario()

    producto1 = ProductoElectronico("Laptop", 1200.0, 10, 2)
    producto2 = ProductoAlimenticio("Manzana", 0.5, 100, "2024-09-01")

    inventario.agregar_producto(producto1)
    inventario.agregar_producto(producto2)

    inventario.listar_productos()

    inventario.actualizar_producto("Laptop", 5)
    inventario.eliminar_producto("Manzana")

    inventario.listar_productos()

    inventario.guardar_datos("inventario.json")
    inventario.cargar_datos("inventario.json")
    inventario.listar_productos()
