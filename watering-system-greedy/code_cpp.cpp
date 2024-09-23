#include <iostream>
#include <bits/stdc++.h>

using namespace std;

#define tiempo first
#define cantidad_max second.first
#define costo second.second
#define primera_llave begin()->first
#define primer_valor begin()->second
#define ultima_llave rbegin()->first
#define ultimo_valor rbegin()->second

typedef long long ll;
typedef pair<ll, ll> par_ll;
typedef pair<ll, par_ll> trio_ll;
typedef vector<trio_ll> vector_trio;
typedef map<ll, ll> mapa_ll;

ll resolver() {
    // Variables de parámetro de consulta.
    ll n, m, c, q;
    cin >> n >> m >> c >> q;

    // Arreglo de datos <tiempo de llegada, cantidad máxima de unidades, costo por unidad>.
    vector_trio datos = vector_trio(n + 1, {0, {0, 0}});

    for (ll i = 0; i < n; i++) 
        cin >> datos[i].tiempo >> datos[i].cantidad_max >> datos[i].costo; // Leer los datos de entrada.

    datos[n++].tiempo = m; // Agregar un dato ficticio al final para simplificar el código.

    sort(datos.begin(), datos.end()); // Ordenar el arreglo por tiempo de llegada.

    // Distribución de unidades disponibles para compra <costo por unidad, unidades disponibles>.
    mapa_ll distribucion = {{0, q}};

    ll costo_total = 0; // Costo final.

    // Para cada llegada.
    for (ll i = 0; i < n; i++) {
        ll tiempo_actual = datos[i].tiempo;
        ll max = datos[i].cantidad_max;
        ll costo_actual = datos[i].costo;

        // Diferencia de tiempo hasta la próxima llegada.
        ll diferencia_tiempo = tiempo_actual - (i ? datos[i - 1].tiempo : 0);

        // Mientras haya unidades disponibles y no hayamos llegado al tiempo actual.
        while (!distribucion.empty() && diferencia_tiempo > 0) {
            try {
                // Cantidad mínima de unidades a comprar para alcanzar el tiempo actual.
                ll comprar = min(distribucion.primer_valor, diferencia_tiempo);

                costo_total += distribucion.primera_llave * comprar; // Sumar el costo de las unidades compradas.

                q -= comprar;   // Actualizar la capacidad utilizada.
                diferencia_tiempo -= comprar; // Reducir la diferencia de tiempo.

                distribucion.primer_valor -= comprar; // Actualizar unidades disponibles.

                // Si se agotan las unidades, eliminar este tipo de unidad de la distribución.
                if (distribucion.primer_valor == 0) distribucion.erase(distribucion.begin());
            } catch (const std::exception& e) {
                cerr << "Error al procesar la compra: " << e.what() << endl;
                return -1; // Manejo de error.
            }
        }

        // Si no hay suficientes unidades para alcanzar el tiempo actual, el problema no tiene solución.
        if (diferencia_tiempo > 0) return -1;

        // Agregar la cantidad máxima de la unidad recién llegada.
        ll agregar = min(c - q, max);
        q += agregar;

        // Mientras haya unidades de este tipo y hay unidades más caras tomadas.
        while (agregar < max && !distribucion.empty() && distribucion.ultima_llave > costo_actual) {
            // Reemplazar unidades más caras por unidades de este tipo.
            if (max - agregar >= distribucion.ultimo_valor) {
                agregar += distribucion.ultimo_valor;
                distribucion.erase(--distribucion.end());
            } else {
                distribucion.ultimo_valor -= max - agregar;
                agregar = max;
            }
        }

        // Actualizar la distribución de unidades disponibles con las unidades tomadas.
        distribucion[costo_actual] += agregar;
    }

    // Retornar el costo total.
    return costo_total;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    ll cantidad_consultas;
    cin >> cantidad_consultas; // Número de consultas.

    // Para cada consulta, imprimir la solución del problema.
    for (ll i = 0; i < cantidad_consultas; i++) 
        cout << resolver() << endl;

    return 0;
}
