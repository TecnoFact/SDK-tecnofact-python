from decimal import Decimal
from tecnofact import Config, Environment
from tecnofact.models import (
    Emisor,
    Receptor,
    Concepto,
    ImpuestosConcepto,
    Traslado,
    Cfdi4Request,
    Impuestos,
    TrasladoGlobal
)
from tecnofact.http import HttpClient


def main():
    config = Config(
        api_key="TU_API_KEY",
        api_secret="TU_API_SECRET",
        environment=Environment.SANDBOX,
        timeout=30
    )

    print(f"Configuración creada:")
    print(f"  Entorno: {config.get_environment().label()}")
    print(f"  URL Base: {config.get_base_url()}")
    print(f"  Timeout: {config.get_timeout()} segundos\n")

    emisor = Emisor(
        rfc="XAXX010101000",
        nombre="EMPRESA EMISORA SA DE CV",
        regimen_fiscal="601",
        cp="06300"
    )

    receptor = Receptor(
        rfc="XAXX010101001",
        nombre="CLIENTE RECEPTOR",
        uso_cfdi="G03",
        domicilio_fiscal_receptor="06300",
        regimen_fiscal_receptor="612"
    )

    concepto = Concepto(
        clave_prod_serv="01010101",
        cantidad=Decimal("1"),
        clave_unidad="E48",
        descripcion="Servicio de desarrollo de software",
        valor_unitario=Decimal("10000.00"),
        importe=Decimal("10000.00"),
        objeto_imp="02",
        impuestos=ImpuestosConcepto(
            traslados=[
                Traslado(
                    base=Decimal("10000.00"),
                    impuesto="002",
                    tipo_factor="Tasa",
                    tasa_o_cuota=Decimal("0.160000"),
                    importe=Decimal("1600.00")
                )
            ]
        )
    )

    cfdi_request = Cfdi4Request(
        emisor=emisor,
        receptor=receptor,
        conceptos=[concepto],
        tipo_comprobante="I",
        forma_pago="01",
        metodo_pago="PUE",
        moneda="MXN",
        subtotal=Decimal("10000.00"),
        total=Decimal("11600.00"),
        lugar_expedicion="06300",
        impuestos=Impuestos(
            total_impuestos_trasladados=Decimal("1600.00"),
            traslados=[
                TrasladoGlobal(
                    impuesto="002",
                    tipo_factor="Tasa",
                    tasa_o_cuota=Decimal("0.160000"),
                    importe=Decimal("1600.00")
                )
            ]
        )
    )

    print("CFDI Request creado:")
    print(f"  Emisor: {emisor.get_nombre()}")
    print(f"  Receptor: {receptor.get_nombre()}")
    print(f"  Subtotal: ${cfdi_request.subtotal}")
    print(f"  Total: ${cfdi_request.total}")
    print(f"\nDatos completos:")
    print(cfdi_request.to_dict())


if __name__ == "__main__":
    main()
