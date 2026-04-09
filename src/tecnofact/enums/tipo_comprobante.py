from enum import Enum


class TipoComprobante(Enum):
    INGRESO = "I"
    EGRESO = "E"
    TRASLADO = "T"
    NOMINA = "N"
    PAGO = "P"

    def label(self) -> str:
        labels = {
            TipoComprobante.INGRESO: "Ingreso",
            TipoComprobante.EGRESO: "Egreso",
            TipoComprobante.TRASLADO: "Traslado",
            TipoComprobante.NOMINA: "Nómina",
            TipoComprobante.PAGO: "Pago"
        }
        return labels[self]
